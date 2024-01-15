import struct
from ... import utils
from ..constants import type_table


abilities_struct_size = 13 + 4 + 1 + 1
abilities_struct_padding = 9
def readAbilities(rom, header):
    abilities_offset = header['abilities']
    abilities_count = header['abilitiesCount']
    abilityNameLength = 12 + 1
    abilities_dict = {}

    for i in range(abilities_count):
        ability_bytes = rom[abilities_offset + (abilities_struct_size+abilities_struct_padding)*i : abilities_offset + (abilities_struct_size+abilities_struct_padding)*(i+1)]
        ability = parseAbility(ability_bytes, abilityNameLength, i)
        abilities_dict[i] = ability
    return abilities_dict

def parseAbility(byteAbility, abilityNameLength, index):
    name = utils.readstring(byteAbility[0:abilityNameLength])
    return {
        'id': index,
        'name': name
    }


item_struct_size = 38
item_struct_padding = 6
def readItems(rom, header):
    items_offset = header['items']
    items_count = 846
    itemNameLength = 13
    items_dict = {}

    for i in range(items_count):
        item_bytes = rom[items_offset + (item_struct_size+item_struct_padding)*i : items_offset + (item_struct_size+item_struct_padding)*(i+1)]
        item = parseItem(item_bytes, itemNameLength, i)
        items_dict[i] = item
    return items_dict

def parseItem(byteItem, itemNameLength, index):
    price = struct.unpack("<I", byteItem[0:4])[0]
    name = utils.readstring(byteItem[19:19+itemNameLength])
    return {
        'id': index,
        'price': price,
        'name': name,
    }

def readMoves(rom, header):
    move_names_offset = header['moveNames']
    moves_count = header['movesCount']
    moveNames = []
    moveNameLength = 12 + 1

    for i in range(moves_count):
        move_name_bytes = rom[move_names_offset + moveNameLength*i : move_names_offset + moveNameLength*(i+1)]
        move_name = utils.readstring(move_name_bytes)
        moveNames.append(move_name)
    return moveNames

species_struct_size = 160
def readSpecies(rom, header):
    species_offset = header['speciesInfo']
    species_count = header['numSpecies']
    pokemonNameLength = header['pokemonNameLength1']
    species_dict = {}

    for i in range(species_count):
        species_bytes = rom[species_offset + species_struct_size*i : species_offset + species_struct_size*(i+1)]
        species = parseSpecies(species_bytes, pokemonNameLength, i)
        species_dict[species['id']] = species

        #print(f"{species['name']} ({species['natDexNum']}) is a {species['category']} Pokémon\n"
        #    + f"    Its types are: {species['types']}\n"
        #    + f"    It has {species['stats']['hp']} HP, {species['stats']['attack']} Attack, {species['stats']['defense']} Def, {species['stats']['speed']} Speed, {species['stats']['spattack']} SpAtk, {species['stats']['spdefense']} SpDef\n"
        #    + f"    Its abilities are {species['abilities']}\n")
    return species_dict


def parseSpecies(byteSpecies, pokemonNameLength, index):
    stats = struct.unpack('< B B B B B B  ', byteSpecies[0:6])
    typesNumbers = struct.unpack('< B B ', byteSpecies[6:8])
    if typesNumbers[0] == typesNumbers[1]:
        types = (type_table[typesNumbers[0]])
    else:
        types = (type_table[typesNumbers[0]], type_table[typesNumbers[1]])
    abilities = struct.unpack('< H H H ', byteSpecies[24:30])
    category = utils.readstring(byteSpecies[31 : 31 + 13])
    name = utils.readstring(byteSpecies[44 : 44 + pokemonNameLength+1])
    genderRatio = struct.unpack('< B', byteSpecies[18:19])

    natDexNum = struct.unpack('<H', byteSpecies[56 : 58])[0]

    return {
        'id': index,
        'name': name,
        'natDexNum': natDexNum,
        'stats': {
            'hp':       stats[0],
            'attack':   stats[1],
            'defense':  stats[2],
            'speed':    stats[3],
            'spattack': stats[4],
            'spdefense':stats[5]
        },
        'types': types,
        'abilities': abilities,
        'category': category,
        'genderRatio': genderRatio,
    }
