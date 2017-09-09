import config
import sqlite3
import datetime
import json
import keyboard_markups


def is_now_contest():
    return config.is_now_contest


def get_all_problem_ids():
    return config.problem_ids


def save_text(bot, update, user_data):
    with open("solutions.json") as solutions_file:
        solutions = json.load(solutions_file)
    if solutions[user_data["current_problem"]].get(str(update.message.chat_id)) == None:
        solutions[user_data["current_problem"]][str(update.message.chat_id)] = {"times_checked": 0, "content": []}
    solutions[user_data["current_problem"]][str(update.message.chat_id)]["content"].append([update.message.text, "text"])
    with open("solutions.json", "w") as solutions_file:
        json.dump(solutions, solutions_file, indent=4)



def save_photo(bot, update, user_data):
    with open("solutions.json") as solutions_file:
        solutions = json.load(solutions_file)
    if solutions[user_data["current_problem"]].get(str(update.message.chat_id)) == None:
        solutions[user_data["current_problem"]][str(update.message.chat_id)] = {"times_checked": 0, "content": []}
    solutions[user_data["current_problem"]][str(update.message.chat_id)]["content"].append([update.message.photo[-1].file_id, "photo"])
    with open("solutions.json", "w") as solutions_file:
        json.dump(solutions, solutions_file, indent=4)


def save_doc(bot, update, user_data):
    with open("solutions.json") as solutions_file:
        solutions = json.load(solutions_file)
    if solutions[user_data["current_problem"]].get(str(update.message.chat_id)) == None:
        solutions[user_data["current_problem"]][str(update.message.chat_id)] = {"times_checked": 0, "content": []}
    solutions[user_data["current_problem"]][str(update.message.chat_id)]["content"].append([update.message.document.file_id, "doc"])
    with open("solutions.json", "w") as solutions_file:
        json.dump(solutions, solutions_file, indent=4)


def send_solution(update, content):
    for instance in content:
        if instance[1] == "text":
            update.message.reply_text(instance[0])
        elif instance[1] == "doc":
            update.message.reply_document(instance[0])
        elif instance[1] == "photo":
            update.message.reply_photo(instance[0])


def increase_counter(problem_id, user):
    with open("solutions.json") as solutions_file:
        solutions = json.load(solutions_file)
    solutions[problem_id][user]["times_checked"] += 1
    with open("solutions.json", "w") as solutions_file:
        json.dump(solutions, solutions_file, indent=4)


def decrease_counter(problem_id, user):
    with open("solutions.json") as solutions_file:
        solutions = json.load(solutions_file)
    solutions[problem_id][user]["times_checked"] -= 1
    with open("solutions.json", "w") as solutions_file:
        json.dump(solutions, solutions_file, indent=4)


def get_solution(update, user_data):


    def already_checked(auditor, author, problem_id):
        with open("marks.json", "r") as marks_file:
            all_marks = json.load(marks_file)
        if all_marks.get(config.contest_id) == None:
            return False
        if all_marks[config.contest_id].get(author) == None:
            return False
        if all_marks[config.contest_id][author].get(problem_id) == None:
            return False
        marks = all_marks[config.contest_id][author][problem_id]
        for mark in marks:
            if mark[1] == auditor:
                return True
        return False


    with open("solutions.json") as solutions_file:
        all_solutions = json.load(solutions_file)
    solutions = all_solutions[user_data["current_problem"]]

    solution_items_raw = list(solutions.items())
    solution_items_with_repeats = []
    solution_items = []

    if len(solution_items_raw) == 0:
        raise BaseException("noone")

    for solution in solution_items_raw:
        if solution[0] != str(update.message.chat_id):
            solution_items_with_repeats.append(solution)

    if len(solution_items_with_repeats) == 0:
        raise BaseException("you")

    for solution in solution_items_with_repeats:
        if not already_checked(update.message.chat_id, solution[0], user_data["current_problem"]):
            solution_items.append(solution)

    if len(solution_items) == 0:
        raise BaseException("already")

    current_solution = solution_items[0]
    minimum_times_checked = solution_items[0][1]["times_checked"]

    for solution in solution_items:
        if solution[1]["times_checked"] < minimum_times_checked:
            current_solution = solution
            minimum_times_checked = solution[1]["times_checked"]

    return current_solution

def save_mark(mark, data, author):
    with open("marks.json") as marks_file:
        marks = json.load(marks_file)
    if marks.get(config.contest_id) == None:
        marks[config.contest_id] = {}
    if marks[config.contest_id].get(data["solution_author"]) == None:
        marks[config.contest_id][data["solution_author"]] = {}
    if marks[config.contest_id][data["solution_author"]].get(data["current_problem"]) == None:
        marks[config.contest_id][data["solution_author"]][data["current_problem"]] = []

    marks[config.contest_id][data["solution_author"]][data["current_problem"]].append([mark, author])

    with open("marks.json", "w") as marks_file:
        json.dump(marks, marks_file, indent=4)


def send_mark(contest_id, update):
    author = update.message.chat_id
    with open("marks.json") as marks_file:
        all_marks = json.load(marks_file)
    marks = all_marks[contest_id][str(author)]
    result = ""
    for mark_raw in list(list(marks.items())):
        mark_with_author = mark_raw[1]
        mark = []
        for item in mark_with_author:
            mark.append(str(item[0]))
        if len(mark_with_author) == 0:
            result += "Задача {0}: Нет оценок\n".format(mark_raw[0])
        else:
            result += "Задача {0}: {1}\n".format(mark_raw[0], ', '.join(mark))
    update.message.reply_text(result, reply_markup=keyboard_markups.get_base_markup(update.message.chat_id))


def get_permit_for_check(chat_id):
    with open("permitted.txt") as permitted_file:
        permitted = permitted_file.readlines()

    chat_id = str(chat_id)
    if chat_id in permitted or not config.is_now_contest:
        return True
    else:
        return False


def add_auditor(chat_id):
    chat_id = str(chat_id)
    with open("permitted.txt") as permitted_file:
        permitted = permitted_file.readlines()
    permitted.append(chat_id)
    with open("permitted.txt", "w") as permitted_file:
        permitted_file.write('\n'.join(permitted))