import struct

# Rom header parsing credit goes to
# CebolaBros64 ( https://gist.github.com/CebolaBros64/c7eb2a3f48df5d4a8488ab75a7d0f9c9 )

def readRomHeader(rom):
    HEADER_FMT = "< 4s 156s 12s 4s 2s c c c 7x c c 2x"
    PADDING_1 = f"{256 - struct.calcsize(HEADER_FMT)}s"
    GF_HEADER_FMT = "4s 4s 32s \
            4s 4s 4s 4s 4s 4s 4s \
            4s 4s 4s \
            4s 4s 4s 4s 4s \
            4s 4s 4s \
            4s c c c c \
            c c c c c c c c c c c c c \
            4s 4s \
            4s 4s 4s 4s 4s 4s 4s 4s 4s 4s \
            4s \
            4s 4s 4s \
            4s 4s 4s 4s \
            4s 4s 4s \
            c c c c c \
            3s 4s 4s 4s 4s 4s 4s \
            "
    PADDING_2 = f"{516 - struct.calcsize(HEADER_FMT + PADDING_1 + GF_HEADER_FMT)}s"
    RHH_HEADER_FMT = f"6s \
            c c c c \
            4s 4s 4s 4s\
            "

    HEADERS = HEADER_FMT + PADDING_1 + GF_HEADER_FMT + PADDING_2 + RHH_HEADER_FMT

    header_size = struct.calcsize(HEADERS)
    header = rom[:header_size]

    unpacked_header = struct.Struct(HEADERS).unpack(header)


    header_dict = {
        # ROM HEADER
        'ROM Entry Point':          unpacked_header[0], # 4 bytes
        'Nintendo Logo':            unpacked_header[1], # 156 bytes
        'Game Title':               unpacked_header[2], # 12 bytes
        'Game Code':                unpacked_header[3], # 4 bytes
        'Maker Code':               unpacked_header[4], # 2 bytes
        'Fixed value':              unpacked_header[5], # 1 byte
        'Main unit code':           unpacked_header[6], # 1 byte
        'Device type':              unpacked_header[7], # 1 byte
                                                    # 7 bytes reserved area
        'Software version':         unpacked_header[8], # 1 byte
        'Complement check':         unpacked_header[9], # 1 byte
                                                    # 2 bytes reserved area
        #'PADDING_1':            unpacked_header[10],

        # GF ROM HEADER
        # Fields marked with * should be filled with 0 or NULL if using expansion (doesn't affect their offset)
        'Game version':             unpacked_header[11], # 4 bytes
        'Game language':            unpacked_header[12], # 4 bytes
        'Game name':                unpacked_header[13], # 32 bytes

        # 'monFrontPics':             unpacked_header[14], # 4 bytes  *
        # 'monBackPics':              unpacked_header[15], # 4 bytes  *
        # 'monNormalPalettes':        unpacked_header[16], # 4 bytes  *
        # 'monShinyPalettes':         unpacked_header[17], # 4 bytes  *
        # 'monIcons':                 unpacked_header[18], # 4 byte   *
        # 'monIconPaletteIds':        unpacked_header[19], # 4 byte   *
        'monIconPalettes':          unpacked_header[20], # 4 bytes

        # 'monSpeciesNames':          unpacked_header[21], # 4 bytes  *
        'moveNames':                unpacked_header[22], # 4 bytes
        'decorations':              unpacked_header[23], # 4 bytes

        'flagsOffset':              unpacked_header[24], # 4 bytes
        'varsOffset':               unpacked_header[25], # 4 bytes
        'pokedexOffset':            unpacked_header[26], # 4 bytes
        'seen1Offset':              unpacked_header[27], # 4 bytes
        'seen2Offset':              unpacked_header[28], # 4 bytes

        'pokedexVar':               unpacked_header[29], # 4 bytes
        'pokedexFlag':              unpacked_header[30], # 4 bytes
        'mysteryEventFlag':         unpacked_header[31], # 4 bytes

        'pokedexCount':             unpacked_header[32], # 4 bytes
        'playerNameLength':         unpacked_header[33], # 1 byte
        'trainerNameLength':        unpacked_header[34], # 1 byte
        'pokemonNameLength1':       unpacked_header[35], # 1 byte
        'pokemonNameLength2':       unpacked_header[36], # 1 byte

        #'unknown fields 5-17':      unpacked_header[37:49], # 1 byte each
        'saveBlock2Size':           unpacked_header[50], # 4 bytes
        'saveBlock1Size':           unpacked_header[51], # 4 bytes

        'partyCountOffset':         unpacked_header[52], # 4 bytes
        'partyOffset':              unpacked_header[53], # 4 bytes
        'warpFlagsOffset':          unpacked_header[54], # 4 bytes
        'trainerIdOffset':          unpacked_header[55], # 4 bytes
        'playerNameOffset':         unpacked_header[56], # 4 bytes
        'playerGenderOffset':       unpacked_header[57], # 4 bytes
        'frontierStatusOffset':     unpacked_header[58], # 4 bytes
        'frontierStatusOffset2':    unpacked_header[59], # 4 bytes
        'externalEventFlagsOffset': unpacked_header[60], # 4 bytes
        'externalEventDataOffset':  unpacked_header[61], # 4 bytes

        'unk16':                    unpacked_header[62], # 4 bytes

        'speciesInfo':              unpacked_header[63], # 4 bytes
        # 'abilityNames':             unpacked_header[64], # 4 bytes *
        # 'abilityDescriptions':      unpacked_header[65], # 4 bytes *

        'items':                    unpacked_header[66], # 4 bytes
        'moves':                    unpacked_header[67], # 4 bytes
        'ballGfx':                  unpacked_header[68], # 4 bytes
        'ballPalettes':             unpacked_header[69], # 4 bytes

        'moves':                    unpacked_header[70], # 4 bytes
        'ballGfx':                  unpacked_header[71], # 4 bytes
        'ballPalettes':             unpacked_header[72], # 4 bytes

        'bagCountItems':            unpacked_header[73], # 1 byte
        'bagCountKeyItems':         unpacked_header[74], # 1 byte
        'bagCountPokeballs':        unpacked_header[75], # 1 byte
        'bagCountTMHMs':            unpacked_header[76], # 1 byte
        'bagCountBerries':          unpacked_header[77], # 1 byte

        'pcItemsCount':             unpacked_header[78], # 3 bytes
        'pcItemsOffset':            unpacked_header[79], # 4 bytes
        'giftRibbonsOffset':        unpacked_header[80], # 4 bytes
        'enigmaBerryOffset':        unpacked_header[81], # 4 bytes
        'enigmaBerrySize':          unpacked_header[82], # 4 bytes
        'moveDescriptions':         unpacked_header[83], # 4 bytes
        'unk20':                    unpacked_header[84], # 4 bytes

        #'PADDING_1':                unpacked_header[85],

        'rhh_magic':                unpacked_header[86], # 6 bytes, should be "RHHEXP"

        'expansionVersionMajor':    unpacked_header[87], # 1 byte
        'expansionVersionMinor':    unpacked_header[88], # 1 byte
        'expansionVersionPatch':    unpacked_header[89], # 1 byte
        'expansionVersionFlags':    unpacked_header[90], # 1 byte

        'movesCount':               unpacked_header[91],
        'numSpecies':               unpacked_header[92],
        'abilitiesCount':           unpacked_header[93],
        'abilities':                unpacked_header[94],
    }
    return header_dict

def getSpecies(rom: str):
    pass
"""
Documentation from GBATEK
    https://problemkaputt.de/gbatek-gba-cartridge-header.htm

Header Overview
    Address Bytes Expl.
    000h    4     ROM Entry Point  (32bit ARM branch opcode, eg. "B rom_start")
    004h    156   Nintendo Logo    (compressed bitmap, required!)
    0A0h    12    Game Title       (uppercase ascii, max 12 characters)
    0ACh    4     Game Code        (uppercase ascii, 4 characters)
    0B0h    2     Maker Code       (uppercase ascii, 2 characters)
    0B2h    1     Fixed value      (must be 96h, required!)
    0B3h    1     Main unit code   (00h for current GBA models)
    0B4h    1     Device type      (usually 00h) (bit7=DACS/debug related)
    0B5h    7     Reserved Area    (should be zero filled)
    0BCh    1     Software version (usually 00h)
    0BDh    1     Complement check (header checksum, required!)
    0BEh    2     Reserved Area    (should be zero filled)
"""
"""
Below is the struct of GFRomHeader :
struct GFRomHeader
{
    u32 version;
    u32 language;
    u8 gameName[32];
    const struct CompressedSpriteSheet * monFrontPics;
    const struct CompressedSpriteSheet * monBackPics;
    const struct CompressedSpritePalette * monNormalPalettes;
    const struct CompressedSpritePalette * monShinyPalettes;
    const u8 *const * monIcons;
    const u8 *monIconPaletteIds;
    const struct SpritePalette * monIconPalettes;
    const u8 (* monSpeciesNames)[];
    const u8 (* moveNames)[];
    const struct Decoration * decorations;
    u32 flagsOffset;
    u32 varsOffset;
    u32 pokedexOffset;
    u32 seen1Offset;
    u32 seen2Offset;
    u32 pokedexVar;
    u32 pokedexFlag;
    u32 mysteryEventFlag;
    u32 pokedexCount;
    u8 playerNameLength;
    u8 trainerNameLength;
    u8 pokemonNameLength1;
    u8 pokemonNameLength2;
    u8 unk5;
    u8 unk6;
    u8 unk7;
    u8 unk8;
    u8 unk9;
    u8 unk10;
    u8 unk11;
    u8 unk12;
    u8 unk13;
    u8 unk14;
    u8 unk15;
    u8 unk16;
    u8 unk17;
    u32 saveBlock2Size;
    u32 saveBlock1Size;
    u32 partyCountOffset;
    u32 partyOffset;
    u32 warpFlagsOffset;
    u32 trainerIdOffset;
    u32 playerNameOffset;
    u32 playerGenderOffset;
    u32 frontierStatusOffset;
    u32 frontierStatusOffset2;
    u32 externalEventFlagsOffset;
    u32 externalEventDataOffset;
    u32 unk18;
    const struct SpeciesInfo * speciesInfo;
    const u8 (* abilityNames)[];
    const u8 *const * abilityDescriptions;
    const struct Item * items;
    const struct BattleMove * moves;
    const struct CompressedSpriteSheet * ballGfx;
    const struct CompressedSpritePalette * ballPalettes;
    u32 gcnLinkFlagsOffset;
    u32 gameClearFlag;
    u32 ribbonFlag;
    u8 bagCountItems;
    u8 bagCountKeyItems;
    u8 bagCountPokeballs;
    u8 bagCountTMHMs;
    u8 bagCountBerries;
    u8 pcItemsCount;
    u32 pcItemsOffset;
    u32 giftRibbonsOffset;
    u32 enigmaBerryOffset;
    u32 enigmaBerrySize;
    const u8 *moveDescriptions;
    u32 unk20;
};
"""
