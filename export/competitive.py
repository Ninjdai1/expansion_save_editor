import os

def teamToCompetitive(team: dict):

    competitiveFilePath = 'CompetitiveTeam.txt'

    if os.path.exists(competitiveFilePath):
        os.remove(competitiveFilePath)

    with open(competitiveFilePath, 'w') as f:
        for i in range (0, len(team)):
            if str.lower(team[i]['nickname']) == str.lower(team[i]['species']):
                f.write(team[i]['nickname'] + " ")
            else:
                f.write(team[i]['nickname'] + " (" + team[i]['species'] + ") " )
            f.write(team[i]['Gender'] + ' ')
            if team[i]['item'] != 'NONE':
                f.write('@ ' + team[i]['item'])
            f.write("\n")
            f.write("Ability: " + str(team[i]['Ability']) + "\n")
            f.write("Level: " + str(team[i]['Level']) + "\n")
            f.write("EVs: " + str(team[i]['EvHp']) + " HP / " + str(team[i]['EvAtk']) + " Atk / " + str(team[i]['EvDef']) + " Def / ")
            f.write(str(team[i]['EvSpA']) + " SpA / " + str(team[i]['EvSpD']) + " SpD / " + str(team[i]['EvSpe']) + " Spe\n")
            f.write(team[i]['Nature'] + " Nature\n")
            f.write("IVs: " + str(team[i]['Ivs']['hp']) + " HP / " + str(team[i]['Ivs']['attack']) + " Atk / " + str(team[i]['Ivs']['defence']) + " Def / ")
            f.write(str(team[i]['Ivs']['spatk']) + " SpA / " + str(team[i]['Ivs']['spdef']) + " SpD / " + str(team[i]['Ivs']['speed']) + " Spe\n")
            for move in team[i]['moves']:
                f.write("- " + move + "\n")
            f.write("\n")

        f.close()
