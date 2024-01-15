from .versions import versions_parsers
from . import utils

def parseRom(path: str):
    with open(path, 'rb') as f:
        rom = f.read()

        expansionVersion = utils.getExpansionVersion(rom)
        expansionVersion = "1.8.0" # TEMPORARY DEV OVERRIDE
        if not expansionVersion >= minimum_expansion_version:
            raise ValueError(f"Your rom is using expansion version {expansionVersion}, which is older than minimum supported version {minimum_expansion_version}")

        header_info = versions_parsers[expansionVersion].readRomHeader(rom)
        # for k in header_info.keys():
        #    print(f"{k}: \"{header_info[k]}\"")

        species = versions_parsers[expansionVersion].readSpecies(rom, header_info)
        moves = versions_parsers[expansionVersion].readMoves(rom, header_info)
        items = versions_parsers[expansionVersion].readItems(rom, header_info)
        abilities = versions_parsers[expansionVersion].readAbilities(rom, header_info)

        return {
            'expansionVersion': expansionVersion,
            'header': header_info,
            'species': species,
            'movesNames': moves,
            'items': items,
            'abilities': abilities,
        }

minimum_expansion_version = "1.7.1"
