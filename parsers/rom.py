from . import readRomHeader
from . import utils
import struct

def parseRom(path: str):
    with open(path, 'rb') as f:
        rom = f.read()

        headerInfo = readRomHeader(rom)
        #for k in headerInfo.keys():
        #    print(f"{k}: \"{headerInfo[k]}\"")

        expansionVersion = getExpansionVersion(headerInfo)
        if not expansionVersion >= minimum_expansion_version:
            raise ValueError(f"Your rom is using expansion version {expansionVersion}, which is older than minimum supported version {minimum_expansion_version}")

        readSpecies(rom, headerInfo)

minimum_expansion_version = "1.7.1"
def getExpansionVersion(header):
    return f"{header['expansionVersionMajor']}.{header['expansionVersionMinor']}.{header['expansionVersionPatch']}"

species_struct_size = 160
def readSpecies(rom, header):
    species_offset = 11514832 # Hardcoded until I get the offsets right
    species_count = 1523# header['numSpecies']
    pokemonNameLength = header['pokemonNameLength1']
    print(pokemonNameLength)

    for i in range(species_count):
        speciesBytes = rom[species_offset +species_struct_size*i : species_offset + species_struct_size*(i+1)]
        species = parseSpecies(speciesBytes, pokemonNameLength)

        print(f"{species['name']} ({species['natDexNum']}) is a {species['category']} Pokémon\n"
            + f"    Its types are: {species['types']}\n"
            + f"    It has {species['stats']['hp']} HP, {species['stats']['attack']} Attack, {species['stats']['defense']} Def, {species['stats']['speed']} Speed, {species['stats']['spattack']} SpAtk, {species['stats']['spdefense']} SpDef\n"
            + f"    Its abilities are {species['abilities']}\n")

def parseSpecies(byteSpecies, pokemonNameLength):
    stats = struct.unpack('b b b b b b ', byteSpecies[0:6])
    typesNumbers = struct.unpack('b b ', byteSpecies[6:8])
    if typesNumbers[0] == typesNumbers[1]:
        types = (type_table[typesNumbers[0]])
    else:
        types = (type_table[typesNumbers[0]], type_table[typesNumbers[1]])
    abilities = struct.unpack('h h h ', byteSpecies[24:30])
    category = utils.readstring(byteSpecies[31 : 31 + 13])
    name = utils.readstring(byteSpecies[44 : 44 + pokemonNameLength+1])

    natDexNum = struct.unpack('h ', byteSpecies[56 : 58])[0]

    return {
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
        'category': category
    }

type_table = [
    'NORMAL',   #0
    'FIGHTING', #1
    'FLYING',   #2
    'POISON',   #3
    'GROUND',   #4
    'ROCK',     #5
    'BUG',      #6
    'GHOST',    #7
    'STEEL',    #8
    'MYSTERY',  #9
    'FIRE',     #10
    'WATER',    #11
    'GRASS',    #12
    'ELECTRIC', #13
    'PSYCHIC',  #14
    'ICE',      #15
    'DRAGON',   #16
    'DARK',     #17
    'FAIRY',    #18
]

"""
struct SpeciesInfo /*0x8C*/
{
 /* 0x00 */ u8 baseHP;
 /* 0x01 */ u8 baseAttack;
 /* 0x02 */ u8 baseDefense;
 /* 0x03 */ u8 baseSpeed;
 /* 0x04 */ u8 baseSpAttack;
 /* 0x05 */ u8 baseSpDefense;

 /* 0x06 */ u8 types[2];

 /* 0x08 */ u8 catchRate;

 /* 0x09 */ u8 padding1;

 /* 0x0A */ u16 expYield; // expYield was changed from u8 to u16 for the new Exp System.

 /* 0x0C */ u16 evYield_HP:2;
            u16 evYield_Attack:2;
            u16 evYield_Defense:2;
            u16 evYield_Speed:2;
 /* 0x0D */ u16 evYield_SpAttack:2;
            u16 evYield_SpDefense:2;
            u16 padding2:4;

 /* 0x0E */ u16 itemCommon;
 /* 0x10 */ u16 itemRare;

 /* 0x12 */ u8 genderRatio;
 /* 0x13 */ u8 eggCycles;
 /* 0x14 */ u8 friendship;
 /* 0x15 */ u8 growthRate;
 /* 0x16 */ u8 eggGroups[2];

 /* 0x18 */ u16 abilities[NUM_ABILITY_SLOTS]; // 3 abilities, no longer u8 because we have over 255 abilities now.

 /* 0x1E */ u8 safariZoneFleeRate;

            // Pokédex data
 /* 0x1F */ u8 categoryName[13];
 /* 0x1F */ u8 speciesName[POKEMON_NAME_LENGTH + 1];
 /* 0x2C */ u16 cryId;
 /* 0x2E */ u16 natDexNum;
 /* 0x30 */ u16 height; //in decimeters
 /* 0x32 */ u16 weight; //in hectograms
 /* 0x34 */ u16 pokemonScale;
 /* 0x36 */ u16 pokemonOffset;
 /* 0x38 */ u16 trainerScale;
 /* 0x3A */ u16 trainerOffset;
 /* 0x3C */ const u8 *description;
 /* 0x40 */ u8 bodyColor : 7;
            // Graphical Data
            u8 noFlip : 1;
 /* 0x41 */ u8 frontAnimDelay;
 /* 0x42 */ u8 frontAnimId;
 /* 0x43 */ u8 backAnimId;
 /* 0x44 */ const union AnimCmd *const *frontAnimFrames;
 /* 0x48 */ const u32 *frontPic;
 /* 0x4C */ const u32 *frontPicFemale;
 /* 0x50 */ const u32 *backPic;
 /* 0x54 */ const u32 *backPicFemale;
 /* 0x58 */ const u32 *palette;
 /* 0x5C */ const u32 *paletteFemale;
 /* 0x60 */ const u32 *shinyPalette;
 /* 0x64 */ const u32 *shinyPaletteFemale;
 /* 0x68 */ const u8 *iconSprite;
 /* 0x6C */ const u8 *iconSpriteFemale;
#if P_FOOTPRINTS
 /* 0x70 */ const u8 *footprint;
#endif
            // All Pokémon pics are 64x64, but this data table defines where in this 64x64 frame the sprite's non-transparent pixels actually are.
 /* 0x74 */ u8 frontPicSize; // The dimensions of this drawn pixel area.
 /* 0x74 */ u8 frontPicSizeFemale; // The dimensions of this drawn pixel area.
 /* 0x75 */ u8 frontPicYOffset; // The number of pixels between the drawn pixel area and the bottom edge.
 /* 0x76 */ u8 backPicSize; // The dimensions of this drawn pixel area.
 /* 0x76 */ u8 backPicSizeFemale; // The dimensions of this drawn pixel area.
 /* 0x77 */ u8 backPicYOffset; // The number of pixels between the drawn pixel area and the bottom edge.
 /* 0x78 */ u8 iconPalIndex:3;
            u8 iconPalIndexFemale:3;
            u8 padding3:2;
 /* 0x79 */ u8 enemyMonElevation; // This determines how much higher above the usual position the enemy Pokémon is during battle. Species that float or fly have nonzero values.
            // Flags
 /* 0x7A */ u32 isLegendary:1;
            u32 isMythical:1;
            u32 isUltraBeast:1;
            u32 isParadoxForm:1;
            u32 isMegaEvolution:1;
            u32 isPrimalReversion:1;
            u32 isUltraBurst:1;
            u32 isGigantamax:1;
            u32 isAlolanForm:1;
            u32 isGalarianForm:1;
            u32 isHisuianForm:1;
            u32 isPaldeanForm:1;
            u32 cannotBeTraded:1;
            u32 allPerfectIVs:1;
            u32 dexForceRequired:1; // This species will be taken into account for Pokédex ratings even if they have the "isMythical" flag set.
            u32 padding4:17;
            // Move Data
 /* 0x80 */ const struct LevelUpMove *levelUpLearnset;
 /* 0x84 */ const u16 *teachableLearnset;
 /* 0x88 */ const struct Evolution *evolutions;
 /* 0x84 */ const u16 *formSpeciesIdTable;
 /* 0x84 */ const struct FormChange *formChangeTable;
};

"""
