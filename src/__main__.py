import os
import time

import requests
import pandas as pd

from local_module import gui

obj = gui.select_event()
URL: str = "https://api.pjsekai.moe/api/user/%7Buser_id%7D/event/{event_id}/ranking?targetRank={rank}&lowerLimit=99"
EVENT_ID : int = obj["id"]
DT = obj["start"]
OUTPUT_DIR: str = f"./border/{DT:%Y}"
OUTPUT_PATH: str = f"{OUTPUT_DIR}/border_{EVENT_ID:05}.tsv"

os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(r"C:\Users\kmyas\Desktop\stock\prsk\border\plotter_of_top1000_event_points\db\team.txt", mode="r", encoding="utf-8") as f:
    txt = f.read()
    team_dict: dict = {id_: name for id_, name in [row.split("\t") for row in txt.splitlines()]}


def main():
    for n in range(obj["limit"]):
        rank : int = 1 + (100 * n)
        url: str = URL.format(event_id=EVENT_ID, rank=rank)
        r = requests.get(url)
        time.sleep(0.5)
        json_dict: dict = r.json()
        table: list = []
        for ranking in json_dict["rankings"]:
            team_num: str = str(ranking["userCheerfulCarnival"].get("cheerfulCarnivalTeamId"))
            table.append({
                "rank": ranking["rank"],
                "score": ranking["score"],
                "user_id": ranking["userId"],
                "name": ranking["name"],
                "twitter_id": ranking["userProfile"].get("twitterId"),
                "cheerful_team": team_dict.get(team_num),
            })
        df = pd.DataFrame(table)
        if not os.path.exists(OUTPUT_PATH):
            with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                print("rank", "score", "user_id", "name", "twitter_id", "cheerful_team", sep="\t", file=f)
        with open(OUTPUT_PATH, "a", encoding="utf-8") as f:
            for record in df.values.tolist():
                print(*record, sep="\t", file=f)


if __name__ == "__main__":
    main()
