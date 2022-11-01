import requests


def write(*data, mode="a", sep="\t"):
    with open("./db/team.txt", mode=mode, encoding="utf-8") as f:
        print(*data, sep="\t", file=f)

url = "https://api.pjsek.ai/database/master/cheerfulCarnivalTeams?$limit=1000&$skip=0&"
r = requests.get(url)
teams = r.json()["data"]
for n, team in enumerate(teams):
    write(
        team["id"], team["teamName"],
        mode="a" if  n else "w"
    )
