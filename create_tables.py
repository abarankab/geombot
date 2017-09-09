import sqlite3, json

print("Введи название контеста:")
data = {}
contest_name = input()
data["contest_name"] = contest_name
print("Введи количество задач:")
problems_quant = int(input())
print("Введи названия задач, каждую в новой строке:")
problem_ids = []
for i in range(problems_quant):
    problem_ids.append(input())
data["problem_ids"] = problem_ids

with open("solutions.json", "w") as solutions_file:
    problems = {}
    for problem in problem_ids:
        problems[problem] = {}
    json.dump(problems, solutions_file)

with open("config.json", "w") as config_file:
    json.dump(data, config_file, indent=4)

with open("contest_id.txt", "r") as contest_id_file:
    contest_id = int(contest_id_file.readline()) + 1

with open("contest_id.txt", "w") as contest_id_file:
    contest_id_file.write(str(contest_id))