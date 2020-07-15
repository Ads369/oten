#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import parser_game_engine
import config
import logging
import en_game_controller

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

ENGC = en_game_controller.en_game_controller()
access_admin_list = 64798180
access_chat_list = {64798180, 228485598, }
game_chat = 64798180
global_bot = None


def decor_log(method):
    """Just log it"""
    def logging_f(*args, **kwargs):
        # args:<telegram.update.Update object>, <telegram.ext.callbackcontext.CallbackContext>
        logger.info('IN: ChatID:%d UserID:%d User:"%s" Message:"%s"' %(
                    args[0].message.chat_id,
                    args[0].message.from_user.id,
                    args[0].message.from_user.username,
                    args[0].message.text))
        return method(*args, **kwargs)
    return logging_f


def access_user(method):
    """ Check user access"""
    def logging_access_f(*args, **kwargs):
        # args: <telegram.update.Update object>, <telegram.ext.callbackcontext.CallbackContext>
        if args[0].message.from_user.id == access_admin_list:
            return method(*args, **kwargs)
        else:
            # args[1].bot.send_message(args[0].message.chat_id, text="Deny access")
            args[0].message.reply_text("Deny access")
    return logging_access_f


def access_chat(method):
    """ Check chat access"""
    def logging_access_f(*args, **kwargs):
        if args[0].message.chat_id in access_chat_list:
            return method(*args, **kwargs)
        else:
            # args[1].bot.send_message(args[0].message.chat_id, text="Deny access")
            args[0].message.reply_text("Deny access")
    return logging_access_f

@decor_log
@access_user
def status(update, context):
    update.message.reply_text('ChatId:{0}\nUserId:{1}\n\nChatList:{2}\nUserList{3}\nGameChat:{4}'.format(
                                    update.effective_chat.id,
                                    update.message.from_user.id,
                                    access_chat_list,
                                    access_admin_list,
                                    game_chat))


@decor_log
@access_user
def accept_chat(update, context):
    global game_chat
    access_chat_list.add(update.message.chat_id)
    game_chat = update.message.chat_id
    update.message.reply_text('ChatId:{0}\nUserId:{1}\n\nChatList:{2}\nUserList:{3}\nGameChat:{4}'.format(
                                    update.message.chat_id,
                                    update.message.from_user.id,
                                    access_chat_list,
                                    access_admin_list,
                                    game_chat))


def take_arguments(str_in):
    end_cmd = str_in.find(' ')
    if end_cmd > 0:
        result = str_in[end_cmd:].strip()
        return result
    else:
        return ''


@access_chat
def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(config.HELP_new)

@decor_log
@access_user
def enter_url(update, context):
    """Send a message when the command /url is issued."""
    # Высчитываю текст сообщения
    msg_in = take_arguments(update.message.text)

    # Вызов метода
    result = ENGC.fill_url(msg_in)

    # Обработчки ошибок
    if result is not None:
        update.message.reply_text('Url принят!')
    else:
        update.message.reply_text(ENGC.get_error_logs())

@decor_log
@access_user
def enter_login(update, context):
    """Send a message when the command /login is issued."""
    # Высчитываю текст сообщения
    msg_in = take_arguments(update.message.text)

    # Вызов метода
    result = ENGC.fill_user(msg_in)

    # Обработчки ошибок
    if result is not None:
        update.message.reply_text('User принят!')
    else:
        update.message.reply_text(ENGC.get_error_logs())


@decor_log
@access_chat
def get_level(update, context):
    """Send a message when the command /lvl is issued."""
    # Высчитываю текст сообщения
    msg_in = take_arguments(update.message.text)

    # Вызов метода
    result = ENGC.get_level()

    # Обработчки ошибок
    if result is not None:
        for i in range(len(result)):
            if i == 0:
                update.message.reply_text(result[i], parse_mode="Markdown", disable_web_page_preview=True)
            else:
                update.message.reply_text(result[i])
    else:
        update.message.reply_text(ENGC.get_error_logs())


@decor_log
@access_chat
def get_gps(update, context):
    # Try get GPS location
    loactions = ENGC.get_location()
    if loactions is not None:
        for each in loactions:
            xy = each.split()
            loc = Location(xy[0], xy[1])
            update.message.reply_location(latitude=xy[0], longitude=xy[1])

@decor_log
@access_chat
def check_answer(update, context):
    """Send a code when the command /a is issued."""
    # Высчитываю текст сообщения
    msg_in = take_arguments(update.message.text)

    # Вызов метода
    result = ENGC.send_answer(msg_in)

    if result is not None:
        update.message.reply_text(result, parse_mode="Markdown")
    else:
        update.message.reply_text(ENGC.get_error_logs())

@decor_log
def code(update, context):
    """Send a code when the command . is issued."""
    msg_in = update.message.text
    if msg_in.startswith('.'):
        result = ENGC.send_answer(update.message.text[1:])
        if result is not None:
            update.message.reply_text(result, parse_mode='markdown')
        else:
            update.message.reply_text(ENGC.get_error_logs())



@decor_log
@access_chat
def change_level(update, context):
    """Change current level for EN"""
    msg_in = take_arguments(update.message.text)
    result = ENGC.change_current_level(msg_in)
    update.message.reply_text(result)


@decor_log
@access_chat
def change_line_mode(update, context):
    """Change mode Speared or Line"""
    msg_in = take_arguments(update.message.text)
    result = ENGC.change_spread_mode()
    update.message.reply_text(result)


@decor_log
@access_chat
def get_short_info(update, context):
    """Change mode Speared or Line"""
    result = ENGC.get_short_information()
    update.message.reply_text(result)

@access_chat
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)



def send_msg_to_gamechat(msg=''):
    global_bot.bot.send_message(chat_id=game_chat, text=msg)





def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    global global_bot
    updater = Updater(config.TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("url", enter_url))
    dp.add_handler(CommandHandler("login", enter_login))
    dp.add_handler(CommandHandler("task", get_level))
    dp.add_handler(CommandHandler("gps", get_gps))
    dp.add_handler(CommandHandler("a", check_answer))
    dp.add_handler(CommandHandler("set_lvl", change_level))
    dp.add_handler(CommandHandler("change_mode", change_line_mode))
    dp.add_handler(CommandHandler("info", get_short_info))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("accept", accept_chat))

    #dp.add_handler(CommandHandler("startgame", ))
    #dp.add_handler(CommandHandler("stopgame", ))
    # dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, code))


    # Start the Bot
    updater.start_polling()
    global_bot = dp.bot

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
