import json

with open("config.json") as config_file:
    data = json.load(config_file)

token = "448061851:AAHubT0cG5iojyVOLHomV3wO2Wc43QPA-zA"
secret_key = "7s9XjMPhPq"
is_now_contest = True
problem_ids = data["problem_ids"]
contest_name = data["contest_name"]

with open("contest_id.txt", "r") as contest_id_file:
    contest_id = contest_id_file.readline()