import datetime

import requests
import pandas as pd

URL: str = "https://api.pjsek.ai/database/master/events?$limit=1024"


def _epoc2dt(epoc: int):
    return datetime.datetime.fromtimestamp(epoc / 1000)


def get_event_list() -> dict:
    event_db_dict: dict = requests.get(URL).json()["data"]
    df = pd.DataFrame(event_db_dict)
    df["start"] = df.startAt.map(_epoc2dt)
    fdf = df[["id", "name", "start"]].sort_values("id", ascending=False)
    event_dict: dict = {}
    for eid, name, start in fdf.values.tolist():
        event_dict[name] = {"id": eid, "start": start}
    return event_dict


if __name__ == "__main__":
    print(get_event_list())
