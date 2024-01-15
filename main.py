from parsers import parseSave, parseRom
import export

rom = parseRom('./pokeemerald.gba')
data = parseSave('./pokeemerald.sav', "expansion", rom)

print(f"Player: {data}")

export.teamToCompetitive(data['team'])
