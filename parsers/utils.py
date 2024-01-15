import struct


def byteArrayFromFile(path: str):
    with open(path, "rb") as file:
        data = bytearray(file.read())
    return data

def readstring(text):
    chars = "0123456789!?.-         ,  ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    ret = ""
    for i in text:
        c = int(i) - 161
        if c<0 or c>len(chars):
            ret = ret + " "
        else:
            ret = ret + chars[c]
    return ret.strip()

def getExpansionVersion(rom):
    expansionVersionBytes = struct.unpack("<b b b", rom[522:525])
    expansionVersionMajor = expansionVersionBytes[0]# 522
    expansionVersionMinor = expansionVersionBytes[1] # 523
    expansionVersionPatch = expansionVersionBytes[2] # 524
    return f"{expansionVersionMajor}.{expansionVersionMinor}.{expansionVersionPatch}"
