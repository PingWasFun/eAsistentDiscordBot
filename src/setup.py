import json
import os

from util import get_data_dir_path


credentials_file_location = get_data_dir_path("credentials.json")
settings_file_location = get_data_dir_path("settings.json")

if not os.path.exists(credentials_file_location):
    with open(credentials_file_location, "w") as credentials_file:
        credentials_data = {"BOT_TOKEN": "INSERT BOT TOKEN"}
        credentials_file.write(json.dumps(credentials_data, indent=4))
        exit("Generating credentials.json. Please insert bot token.")

with open(credentials_file_location, "r") as credentials_file:
    credentials_data = json.load(credentials_file)
    TOKEN = credentials_data["BOT_TOKEN"]
    if TOKEN == "INSERT BOT TOKEN":
        exit("Insert bot token in credentials.json")

if not os.path.exists(settings_file_location):
    with open(settings_file_location, "w") as settings_file:
        settings_data = {
            "SCHOOL_ID": "INSERT SCHOOL ID",
            "CLASS_ID": "INSERT CLASS ID",
            "SCHEDULE_CHANNEL_ID": "INSERT SCHEDULE_CHANNEL_ID",
        }
        settings_file.write(json.dumps(settings_data, indent=4))
        exit("Generating settings.json. Please insert the required data.")

with open(settings_file_location, "r") as settings_file:
    settings_data = json.load(settings_file)
    SCHOOL_ID = settings_data["SCHOOL_ID"]
    CLASS_ID = settings_data["CLASS_ID"]
    SCHEDULE_CHANNEL_ID = settings_data["SCHEDULE_CHANNEL_ID"]
