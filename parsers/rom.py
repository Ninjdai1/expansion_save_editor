from . import readRomHeader
import struct

def parseRom(path: str):
    with open(path, 'rb') as f:
        rom = f.read()

        headerInfo = readRomHeader(rom)
        for k in headerInfo.keys():
            print(f"{k}: \"{headerInfo[k]}\"")

        expansionVersion = getExpansionVersion(headerInfo)
        if not expansionVersion >= minimum_expansion_version:
            raise ValueError(f"Your rom is using expansion version {expansionVersion}, which is older than minimum supported version {minimum_expansion_version}")

        # readSpecies(rom, headerInfo['speciesInfo'])

minimum_expansion_version = "1.7.1"
def getExpansionVersion(header):
    return f"{header['expansionVersionMajor']}.{header['expansionVersionMinor']}.{header['expansionVersionPatch']}"

def readSpecies(rom, species_offset):
    SPECIES_FMT = "c c c c c c "

    for species in struct.iter_unpack(SPECIES_FMT, rom[species_offset:species_offset + struct.calcsize(SPECIES_FMT):]):
        print(species)
