from . import readRomHeader

def parseRom(path: str):
    with open(path, 'rb') as f:
        rom = f.read()

        headerInfo = readRomHeader(rom)
        for k in headerInfo.keys():
            print(f"{k}: \"{headerInfo[k]}\"")
