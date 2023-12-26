import struct
import utils
from offsets import offsets_dict

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
        print(section["footer"])

        section["id"] = struct.unpack('<H', section["footer"][0:2])[0]
        section["index"] = struct.unpack('<I', section["footer"][4:8])[0]
        print(section["id"], section["index"])

        ds = 0

        if section["id"] == 0:
            ds = struct.unpack('<HBBB', section["rawData"][14:19])
            dt = (ds[0] * 3600) + (ds[1] * 60) + ds[2]
            save["index"] = section["index"]
            save["playtime"] = dt

        save["sections"][section["id"]] = section

    # We return the save's index and the playtime on it
    return save

def getCurrentSave(save_a, save_b):
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
def process(savedata):
    player = {
        "name": None,
        "team": [],
        "boxes": [],
    }

    player["name"] = utils.readstring(savedata["sections"][0]["rawData"][0:7]).strip()


    return player

def parse(path: str, game_version: str):
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

    processed_data = process(save)

    print(f"Player: {processed_data}")

    return processed_data
