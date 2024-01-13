from parsers import parseSave
import export

data = parseSave('./pokeemerald.sav', "emerald")

print(f"Player: {data}")

export.teamToCompetitive(data['team'])
