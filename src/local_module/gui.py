import PySimpleGUI as sg

from . import events


sg.theme("Dark Brown 1")


event_dict: dict = events.get_event_list()
event_name_list = list(event_dict.keys())

layout: list = [
    [sg.Text("取得するイベントを選択してください")],
    [sg.Listbox(event_name_list, size=(48, 16), key="event_name")],
    [sg.Text("取得する順位の下限を入力してください")],
    [sg.Input(100, key="rank")],
    [sg.Text("")],
    [sg.Button("Ok"), sg.Button("Cancel")],
]


def select_event() -> dict:
    window = sg.Window("EVENT_BORDER", layout=layout)
    try:
        while True:
            event, values = window.read()
            if event in (None, "Cancel"):
                break
            elif event == "Ok":
                name: str = values["event_name"][0]
                limit: int = int(values["rank"]) // 100
                return {
                    "id": event_dict[name]["id"],
                    "limit": limit,
                    "start": event_dict[name]["start"],
                }
    finally:
        window.close()


if __name__ == "__main__":
    print(select_event())
