# -*- coding: utf-8 -*-

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import ConversationHandler
from telegram.ext import RegexHandler

import message_reply_functions
import config
import logging

from conversation_states import *

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level = logging.INFO)

    updater = Updater(token=config.token)

    conversation = ConversationHandler(
        entry_points = [
                CommandHandler('start', message_reply_functions.start),
                MessageHandler(Filters.all, message_reply_functions.error_start)
            ],

        states = {
            BASE: [
                CommandHandler("get_access", message_reply_functions.get_access, pass_args=True),
                RegexHandler('^(Посмотреть свои результаты)$', message_reply_functions.get_contest_id),
                RegexHandler('^(Отправить задачу)$', message_reply_functions.get_problem_id_for_send),
                RegexHandler('^(Проверить задачу)$', message_reply_functions.get_problem_id_for_check),
            ],

            GETTING_SEND_PROB: [
                CommandHandler("get_access", message_reply_functions.get_access, pass_args=True),
                RegexHandler('^(На главную)$', message_reply_functions.return_to_base),
                MessageHandler(Filters.text, message_reply_functions.handle_send_prob, pass_user_data=True),
                MessageHandler(~ Filters.text, message_reply_functions.invalid_problem_id_type_send),
            ],

            SENDING: [
                CommandHandler("get_access", message_reply_functions.get_access, pass_args=True),
                RegexHandler('^(Это все)$', message_reply_functions.return_to_problem_id),
                MessageHandler(Filters.text, message_reply_functions.handle_save_text, pass_user_data=True),
                MessageHandler(Filters.photo, message_reply_functions.handle_save_photo, pass_user_data=True),
                MessageHandler(Filters.document, message_reply_functions.handle_save_doc, pass_user_data=True),
                MessageHandler(~(Filters.text | Filters.photo | Filters.document), message_reply_functions.invalid_problem_data),
            ],

            GETTING_CHECK_PROB: [
                CommandHandler("get_access", message_reply_functions.get_access, pass_args=True),
                RegexHandler('^(На главную)$', message_reply_functions.return_to_base),
                MessageHandler(Filters.text, message_reply_functions.handle_check_prob, pass_user_data=True),
                MessageHandler(~ Filters.text, message_reply_functions.invalid_problem_id_type_check),
            ],

            CHECKING: [
                CommandHandler("get_access", message_reply_functions.get_access, pass_args=True),
                RegexHandler('^(Оставить без оценки)$', message_reply_functions.return_to_gc, pass_user_data=True),
                MessageHandler(Filters.text, message_reply_functions.save_mark, pass_user_data=True),
                MessageHandler(~ Filters.text, message_reply_functions.invalid_mark_type),
            ],

            GETTING_CONTEST_ID: [
                CommandHandler("get_access", message_reply_functions.get_access, pass_args=True),
                RegexHandler('^(На главную)$', message_reply_functions.return_to_base),
                MessageHandler(Filters.text, message_reply_functions.handle_contest_id),
                MessageHandler(~ Filters.text, message_reply_functions.invalid_contest_id_type),
            ],
       },
       fallbacks = [],
    )

    disp = updater.dispatcher

    disp.add_handler(conversation)

    updater.start_polling()

if __name__ == "__main__":
    main()