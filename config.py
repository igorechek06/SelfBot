from json import dump, load
from os import environ, path


def save_settigns():
    with open("data/settings.json", "w") as file:
        dump(settings, file)


session_name = environ["sessionName"]
api_id = environ["apiId"]
api_hash = environ["apiHash"]

if path.exists("data/settings.json"):
    with open("data/settings.json", "r") as file:
        settings = load(file)
else:
    settings = {}
    save_settigns()

settings["backup"] = settings.get("backup", [])
save_settigns()
