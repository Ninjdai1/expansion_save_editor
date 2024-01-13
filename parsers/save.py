import struct
from . import utils
from games import offsets_dict, gamedata_dict
import re
from . import readRomHeader, parseRom
from operator import xor
import io
import os

# More complete information on how the save data is structured can be found at:
# https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_(Generation_III)

def getSaveInfo(data):
    save = {
        "sections": [ {} for _ in range(14) ],
        "slot": None
    }

    for i in range(0, 14):
        section = {
            "i": i * 4096 # The byte position of the current section. Each section is 4Kb, so 4096 bytes long
        }
        section["rawData"] = data[section["i"]:section["i"]+4096] # The raw data of the section, for further use
        section["footer"] = section["rawData"][4084:]
        # The section's data is up to 3968 bytes long (see table below). The end 12 bytes of the section are occupied by footer data.
        # There are 116 bytes of padding between the section's data and its footer
        # Footer includes Section ID (2 bytes), Checksum (2 bytes), Signature (4 bytes), Save index (4 bytes)
        #print(section["footer"])

        section["id"] = struct.unpack('<H', section["footer"][0:2])[0]
        section["index"] = struct.unpack('<I', section["footer"][4:8])[0]
        #print(section["id"], section["index"])

        ds = 0

        if section["id"] == 0:
            ds = struct.unpack('<HBBB', section["rawData"][14:19])
            dt = (ds[0] * 3600) + (ds[1] * 60) + ds[2]
            save["index"] = section["index"]
            save["playtime"] = dt

        save["sections"][section["id"]] = section

    # We return the save's index and the playtime on it
    return save

def getCurrentSave(save_a: dict, save_b: dict):
    save = None
    # We check for the save's index and pick whichever is the greatest
    if save_a["index"] < save_b["index"]:
        save = save_b
        save["slot"] = "B"
    elif save_a["index"] > save_b["index"]:
        save = save_a
        save["slot"] = "A"
    else:
        # If both saves have the same index, we pick the most recent one
        if save_a["playtime"] < save_b["playtime"]:
            save = save_b
            save["slot"] = "B"
        else:
            save = save_a
            save["slot"] = "A"
    return save


# Here is the data stored in each section according to bulbapedia:
# ID 	Size 	Contents
# 0 	3884 	Trainer info
# 1 	3968 	Team / items
# 2 	3968 	Game State
# 3 	3968 	Misc Data
# 4 	3848 	Rival info
# 5 	3968 	PC buffer A
# 6 	3968 	PC buffer B
# 7 	3968 	PC buffer C
# 8 	3968 	PC buffer D
# 9 	3968 	PC buffer E
# 10 	3968 	PC buffer F
# 11 	3968 	PC buffer G
# 12 	3968 	PC buffer H
# 13 	2000 	PC buffer I
def process(savedata: dict, game_version: str, rom: dict):
    save = {
        "name": None,
        "gender": None,
        "team": [],
        "boxes": [],
    }
    offsets = offsets_dict[game_version]
    gamedata = gamedata_dict[game_version]

    sections = savedata["sections"]
    # Section 0 data
    save["name"] = utils.readstring(sections[0]["rawData"][0:7]).strip()
    save["trainer_id"] = int(struct.unpack('<I', sections[0]["rawData"][offsets["trainer_id"][0]:offsets["trainer_id"][1]])[0])
    save["security_key"] = int(struct.unpack('<I', sections[0]["rawData"][offsets["security_key"][0]:offsets["security_key"][1]])[0])
    if("gender" in offsets):
        gender_id = sections[0]["rawData"][offsets["gender"]]
        save["gender"] = gamedata["genders"][gender_id]




    # Section 1 data
    natures = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile", "Relaxed", "Impish", "Lax", "Timid", "Hasty", "Serious", "Jolly", "Naive", "Modest", "Mild", "Quiet", "Bashful", "Rash", "Calm", "Gentle", "Sassy", "Careful", "Quirky"]

    #When a pokemons data is saved, it's encrypted in one of 24 orders. We need to run a modulo against this list to get the order we need to interpret bytes.
    #Sources:https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_data_substructures_(Generation_III), https://github.com/ads04r/Gen3Save/blob/master/pokemondata/Gen3Pokemon.py
    orders = ['GAEM', 'GAME', 'GEAM', 'GEMA', 'GMAE', 'GMEA', 'AGEM', 'AGME', 'AEGM', 'AEMG', 'AMGE', 'AMEG', 'EGAM', 'EGMA', 'EAGM', 'EAMG', 'EMGA', 'EMAG', 'MGAE', 'MGEA', 'MAGE', 'MAEG', 'MEGA', 'MEAG']

    save["team_count"] = int(struct.unpack('<I', sections[1]["rawData"][offsets["team_count"][0]:offsets["team_count"][1]])[0])
    for i in range (0, save["team_count"]):

        pokemon = {}

        personality = int(struct.unpack('<I', sections[1]["rawData"][offsets["team_offset"]+((i*100)):offsets["team_offset"]+(4+(i*100))])[0])
        orderstring = orders[personality % 24]
        decryptionkey = personality ^ save["trainer_id"]

        pokemon["nickname"] = utils.readstring(sections[1]["rawData"][offsets["team_offset"]+(8+(i*100)):offsets["team_offset"]+(18+(i*100))]).strip()


        pokemon["checksum"] = int(struct.unpack('<I', sections[1]["rawData"][offsets["team_offset"]+(28 + (i*100)):offsets["team_offset"]+(32+(i*100))])[0])
        pokemon["Level"] = int(struct.unpack('<B', sections[1]["rawData"][offsets["team_offset"]+(84 + (i*100)):offsets["team_offset"]+(85+(i*100))])[0])

        substructSections = {}
        for j in range (0, 4):
            #Calculation below:
            #(i * 100) gets current pokemon, 32 is the offset for the 48 bit encrypted block. Blocks are encrypted in 12 byte chuncks, hence 12 * j
            sectionData = (sections[1]["rawData"][offsets["team_offset"]+(32+(i*100)+(j*12)):offsets["team_offset"]+(32+(i*100)+(j+1)*12)])
            decryptedValue = decryptSubstruct(sectionData, decryptionkey)
            substructSections[orderstring[j]] = decryptedValue
        #print(substructSections[orderstring[j]])

        species = rom['species'][int(struct.unpack('<H', substructSections['G'][0:2])[0])]
        pokemon['species'] = species['name'].upper()
        print(pokemon['species'].upper())

        pokemon['exp'] = int(struct.unpack('<I', substructSections['G'][4:8])[0])
        heldItemId = int(struct.unpack('<H', substructSections['G'][2:4])[0])
        pokemon['item'] = rom['items'][heldItemId]['name']

        moves = []
        for i in range(4):
            moveId = int(struct.unpack('<H', substructSections['A'][i*2:i*2+2])[0])
            moves.append(rom['movesNames'][moveId])
        pokemon['moves'] = moves

        pokemon['EvHp'] = int(struct.unpack('<B', substructSections['E'][0:1])[0])
        pokemon['EvAtk'] = int(struct.unpack('<B', substructSections['E'][1:2])[0])
        pokemon['EvDef'] = int(struct.unpack('<B', substructSections['E'][2:3])[0])
        pokemon['EvSpe'] = int(struct.unpack('<B', substructSections['E'][3:4])[0])
        pokemon['EvSpA'] = int(struct.unpack('<B', substructSections['E'][4:5])[0])
        pokemon['EvSpD'] = int(struct.unpack('<B', substructSections['E'][5:6])[0])

        pokemon['Nature'] = natures[personality % 25]

        ''''
        pokemon['HP'] = int(struct.unpack('<H', sections[1]["rawData"][offsets["team_offset"]+(88 + (i*100)):offsets["team_offset"]+(90 + (i*100))])[0])
        pokemon['Atk'] = int(struct.unpack('<H', sections[1]["rawData"][offsets["team_offset"]+(90 + (i*100)):offsets["team_offset"]+(92 + (i*100))])[0])
        pokemon['Def'] = int(struct.unpack('<H', sections[1]["rawData"][offsets["team_offset"]+(92 + (i*100)):offsets["team_offset"]+(94 + (i*100))])[0])
        pokemon['Spe'] = int(struct.unpack('<H', sections[1]["rawData"][offsets["team_offset"]+(94 + (i*100)):offsets["team_offset"]+(96 + (i*100))])[0])
        pokemon['SpA'] = int(struct.unpack('<H', sections[1]["rawData"][offsets["team_offset"]+(96 + (i*100)):offsets["team_offset"]+(98 + (i*100))])[0])
        pokemon['SpD'] = int(struct.unpack('<H', sections[1]["rawData"][offsets["team_offset"]+(98 + (i*100)):offsets["team_offset"]+(100 + (i*100))])[0])
        '''

        pokemon['Ivs'] = getivs(int(struct.unpack('<I', substructSections['M'][4:8])[0]))

        abilitiesIds = species['abilities']
        abilityId = abilitiesIds[pokemon['Ivs']['AbilityFlag']]
        pokemon['Ability'] = rom['abilities'][abilityId]['name']
        # Only need to translate Abilities from int to strings and we're pretty much done here

        genderRatio = species['genderRatio']
        genderInteger = int(struct.unpack('<B', sections[1]["rawData"][offsets["team_offset"]+(0+(i*100)):offsets["team_offset"]+(1+(i*100))])[0])

        if len(str(genderRatio)) < 2:
            pokemon['Gender'] = ""
        elif genderInteger > (224 * 0.01 * float(genderRatio[0])):
            pokemon['Gender'] = "(M)"
        else:
            pokemon['Gender'] = "(F)"

        save['team'].append(pokemon)

    # Section 2 Data

    teamToShowdown(save['team'])

    return save

def parseSave(path: str, game_version: str):
    if not game_version in offsets_dict:
        print(f"This version ({game_version}) is not supported ! If you are this version's developer, please define its offsets in offsets.py")
        return
    else:
        offsets = offsets_dict[game_version]
    data = utils.byteArrayFromFile(path)
    # There are two save files in gen III
    # The first one goes from 0 to 57344 (not included), the second from 57344 to 114688 (not included).
    save_a = getSaveInfo(data[offsets["save_a"][0]:offsets["save_a"][1]])
    save_b = getSaveInfo(data[offsets["save_b"][0]:offsets["save_b"][1]])

    save = getCurrentSave(save_a, save_b)

    #print(save)
    print(f"The current save slot is {save['slot']}")

    rom = parseRom("pokeemerald.gba")
    processed_data = process(save, game_version, rom)

    print(f"Player: {processed_data}")


    return processed_data

def getivs(value):

    iv = {}
    bitstring = str(str(bin(value)[2:])[::-1] + '00000000000000000000000000000000')[0:32]
    iv['hp'] = int(bitstring[0:5], 2)
    iv['attack'] = int(bitstring[5:10], 2)
    iv['defence'] = int(bitstring[10:15], 2)
    iv['speed'] = int(bitstring[15:20], 2)
    iv['spatk'] = int(bitstring[20:25], 2)
    iv['spdef'] = int(bitstring[25:30], 2)
    iv['AbilityFlag'] = int(bitstring[30:31], 2)
    return iv

def decryptSubstruct(data, key):
    if len(data) != 12:
        return []
    a = xor(struct.unpack('<I', data[0:4])[0], key)
    b = xor(struct.unpack('<I', data[4:8])[0], key)
    c = xor(struct.unpack('<I', data[8:12])[0], key)
    return struct.pack('<III', a, b, c)

def teamToShowdown(team: dict):

    showdownFilePath = 'ShowdownTeam.txt'

    if os.path.exists(showdownFilePath):
        os.remove(showdownFilePath)

    with open(showdownFilePath, 'w') as f:
        for i in range (0, len(team)):
            if str.lower(team[i]['nickname']) == str.lower(team[i]['species']):
                f.write(team[i]['nickname'] + " ")
            else:
                f.write(team[i]['nickname'] + " (" + team[i]['species'] + ") " )
            f.write(team[i]['Gender'] + ' ')
            if team[i]['item'] != 'NONE':
                f.write('@ ' + team[i]['item'])
            f.write("\n")
            f.write("Ability: " + str(team[i]['Ability']) + "\n")
            f.write("Level: " + str(team[i]['Level']) + "\n")
            f.write("EVs: " + str(team[i]['EvHp']) + " HP / " + str(team[i]['EvAtk']) + " Atk / " + str(team[i]['EvDef']) + " Def / ")
            f.write(str(team[i]['EvSpA']) + " SpA / " + str(team[i]['EvSpD']) + " SpD / " + str(team[i]['EvSpe']) + " Spe\n")
            f.write(team[i]['Nature'] + " Nature\n")
            f.write("IVs: " + str(team[i]['Ivs']['hp']) + " HP / " + str(team[i]['Ivs']['attack']) + " Atk / " + str(team[i]['Ivs']['defence']) + " Def / ")
            f.write(str(team[i]['Ivs']['spatk']) + " SpA / " + str(team[i]['Ivs']['spdef']) + " SpD / " + str(team[i]['Ivs']['speed']) + " Spe\n")
            for move in team[i]['moves']:
                f.write("- " + move + "\n")
            f.write("\n")

        f.close()
