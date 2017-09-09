import text_constants
import keyboard_markups
import utility
import config
from conversation_states import *


def error_start(bot, update):
    update.message.reply_text(text_constants.error_start_r, reply_markup=keyboard_markups.get_base_markup(update.message.chat_id))
    return BASE


def start(bot, update):
    update.message.reply_text(text_constants.start_r, reply_markup=keyboard_markups.get_base_markup(update.message.chat_id))
    return BASE


def get_problem_id_for_send(bot, update):
    if utility.is_now_contest():
        update.message.reply_text(text_constants.need_send_prob_r, reply_markup=keyboard_markups.get_problems_markup())
        return GETTING_SEND_PROB
    else:
        update.message.reply_text(text_constants.no_contest_r, rely_markup=keyboard_markups.get_base_markup(update.message.chat_id))
        return BASE


def return_to_base(bot, update):
    update.message.reply_text(text_constants.back_r, reply_markup=keyboard_markups.get_base_markup(update.message.chat_id))
    return BASE


def invalid_problem_id_type_send(bot, update):
    update.message.reply_text(text_constants.invalid_type_send_r, reply_markup=keyboard_markups.get_problems_markup())
    return GETTING_SEND_PROB


def handle_send_prob(bot, update, user_data):
    problem_ids = utility.get_all_problem_ids()
    id = update.message.text
    if id in problem_ids:
        user_data["current_problem"] = update.message.text
        update.message.reply_text(text_constants.got_num_send_r, reply_markup=keyboard_markups.markup_send)
        return SENDING
    else:
        update.message.reply_text(text_constants.no_such_problem_r, reply_markup=keyboard_markups.get_problems_markup())
        return GETTING_SEND_PROB


def return_to_problem_id(bot, update):
    update.message.reply_text(text_constants.got_problem_data_r)
    update.message.reply_text(text_constants.waiting_for_next_problem, reply_markup=keyboard_markups.get_problems_markup())
    return GETTING_SEND_PROB


def handle_save_text(bot, update, user_data):
    update.message.reply_text(text_constants.got_text_r, reply_markup=keyboard_markups.markup_send)
    utility.save_text(bot, update, user_data)
    return SENDING


def handle_save_photo(bot, update, user_data):
    update.message.reply_text(text_constants.got_img_r, reply_markup=keyboard_markups.markup_send)
    utility.save_photo(bot, update, user_data)
    return SENDING


def handle_save_doc(bot, update, user_data):
    update.message.reply_text(text_constants.got_doc_r, reply_markup=keyboard_markups.markup_send)
    utility.save_doc(bot, update, user_data)
    return SENDING


def invalid_problem_data(bot, update):
    update.message.reply_text(text_constants.invalid_type_send_r, reply_markup=keyboard_markups.markup_send)
    return SENDING

'''
From now on there will only be functions handling the checking process
'''

def get_problem_id_for_check(bot, update):
    if utility.get_permit_for_check(update.message.chat_id):
        update.message.reply_text(text_constants.need_check_prob_r, reply_markup=keyboard_markups.get_problems_markup())
        return GETTING_CHECK_PROB
    else:
        update.message.reply_text(text_constants.authorization_failed, rely_markup=keyboard_markups.get_base_markup(update.message.chat_id))
        return BASE


def handle_check_prob(bot, update, user_data):
    problem_ids = utility.get_all_problem_ids()
    id = update.message.text
    if id in problem_ids:
        user_data["current_problem"] = update.message.text
        try:
            solution = utility.get_solution(update, user_data)
        except BaseException as e:

            if e.args[0] == "noone":
                update.message.reply_text(text_constants.no_solutions_yet)
            elif e.args[0] == "you":
                update.message.reply_text(text_constants.only_your_solution)
            elif e.args[0] == "already":
                update.message.reply_text(text_constants.already_checked_all)
            return GETTING_CHECK_PROB
        update.message.reply_text(text_constants.got_num_check_r)
        user_data["solution_author"] = solution[0]
        utility.send_solution(update, solution[1]["content"])
        utility.increase_counter(user_data["current_problem"], solution[0])
        update.message.reply_text(text_constants.mark_warning, reply_markup=keyboard_markups.markup_check)
        return CHECKING
    else:
        update.message.reply_text(text_constants.no_such_problem_r, reply_markup=keyboard_markups.get_problems_markup())
        return GETTING_CHECK_PROB


def invalid_problem_id_type_check(bot, update):
    update.message.reply_text(text_constants.invalid_type_check_r, reply_markup=keyboard_markups.get_problems_markup())
    return GETTING_CHECK_PROB


def save_mark(bot, update, user_data):
    try:
        mark = int(update.message.text)
    except ValueError:
        update.message.reply_text(text_constants.invalid_mark_type_err)
        return CHECKING
    if not (100 >= mark >= 0):
        update.message.reply_text(text_constants.invalid_mark_type_err)
        return CHECKING

    utility.save_mark(mark, user_data, update.message.chat_id)
    update.message.reply_text(text_constants.got_mark, reply_markup=keyboard_markups.get_problems_markup())

    return GETTING_CHECK_PROB


def return_to_gc(bot, update, user_data):
    utility.decrease_counter(user_data["current_problem"], user_data["solution_author"])
    user_data.clear()
    update.message.reply_text(text_constants.back_c_r, reply_markup=keyboard_markups.get_problems_markup())
    return GETTING_CHECK_PROB

def invalid_mark_type(bot, update):
    update.message.reply_text(text_constants.invalid_mark_type_err)

def get_contest_id(bot, update):
    update.message.reply_text(text_constants.need_contest_id, reply_markup=keyboard_markups.get_contests_markup())
    return GETTING_CONTEST_ID

def handle_contest_id(bot, update):
    try:
        contest_id = int(update.message.text)
    except ValueError:
        update.message.reply_text(text_constants.invalid_mark_type_err)
        return GETTING_CONTEST_ID
    if contest_id <= 0 or contest_id > int(config.contest_id):
        update.message.reply_text(text_constants.no_such_contest)
        return GETTING_CONTEST_ID

    utility.send_mark(str(contest_id), update)
    return BASE


def invalid_contest_id_type(bot, update):
    update.message.reply_text(text_constants.invalid_contest_type)


def get_access(bot, update, args):
    if len(args) == 1:
        key = args[0]
        if key == config.secret_key:
            utility.add_auditor(update.message.chat_id)
            update.message.reply_text(text_constants.access_success)