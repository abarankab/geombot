# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup
from telegram import KeyboardButton
import config
import utility
import json


def get_base_markup(chat_id):
    if utility.get_permit_for_check(str(chat_id)):
        return markup_base_unlocked
    else:
        return markup_base_locked


def get_problems_markup():
    keyboard = to_base_keyboard
    for item in config.problem_ids:
        to_base_keyboard.append(list(item))
    return ReplyKeyboardMarkup(keyboard)


def get_contests_markup():
    keyboard = to_base_keyboard

    with open("marks.json") as contests_file:
        contests = json.load(contests_file)

    contest_list_raw = list(contests.items())


    for raw_contest in contest_list_raw:
        keyboard.append(list(raw_contest[0]))

    return ReplyKeyboardMarkup(keyboard)




base_keyboard_unlocked = [[KeyboardButton("Отправить задачу")], [KeyboardButton("Проверить задачу")], [KeyboardButton("Посмотреть свои результаты")]]
base_keyboard_locked = [[KeyboardButton("Отправить задачу")], [KeyboardButton("Посмотреть свои результаты")]]
send_keyboard = [[KeyboardButton("Это все")]]
mark_keyboard = [[KeyboardButton("Подтвердить результат")], [KeyboardButton("Назад")]]
check_keyboard = [[KeyboardButton("Оставить без оценки")]]
to_base_keyboard = [[KeyboardButton("На главную")]]

markup_base_unlocked = ReplyKeyboardMarkup(base_keyboard_unlocked)
markup_base_locked = ReplyKeyboardMarkup(base_keyboard_locked)
markup_send = ReplyKeyboardMarkup(send_keyboard)
markup_check = ReplyKeyboardMarkup(check_keyboard)
markup_to_base = ReplyKeyboardMarkup(to_base_keyboard)