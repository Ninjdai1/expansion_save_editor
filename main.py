from parsers import parseSave
import export

data = parseSave('./pokeemerald.sav', "expansion")

print(f"Player: {data}")

export.teamToCompetitive(data['team'])
