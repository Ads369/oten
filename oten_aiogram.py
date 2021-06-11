"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
import oten_logger
import os
import time
import oten_core
import asyncio
from aiogram import Bot, Dispatcher, executor, types, utils

# Configure logging
log_file = 'oten.log'
log = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=os.getenv('TG_TOKEN'))
dp = Dispatcher(bot)
oten = oten_core.Oten()
user_id_required = [64798180]
# chat_id_required = [64798180]
chat_id_required = [64798180,  # Me
                    -347136758,  # Test Bot chat
                    -587436992]  # Бонд поле


# EN Block


@dp.message_handler(commands=['access'],
                    user_id=user_id_required)
async def add_chat_required(message: types.Message):
    global chat_id_required
    chat_id_required.append(int(message.chat.id))
    # chat_id_required = message.chat.id
    await message.answer('Game chat added')


@dp.message_handler(commands=['url'],
                    user_id=user_id_required)
async def set_url(message: types.Message):
    msg_in = ''.join(message.text.split(' ')[1:])
    await oten.args_from_url(msg_in, message)


@dp.message_handler(commands=['user'],
                    user_id=user_id_required)
async def set_login(message: types.Message):
    msg_in = ''.join(message.text.split(' ')[1:])
    await oten.set_login(msg_in, message)


@dp.message_handler(commands=['password'],
                    user_id=user_id_required)
async def set_password(message: types.Message):
    msg_in = ''.join(message.text.split(' ')[1:])
    await oten.set_password(msg_in, message)


@dp.message_handler(commands=['defuser'],
                    user_id=user_id_required)
async def set_default_user(message: types.Message):
    await oten.args_from_url('', message)
    await oten.set_login(os.getenv('EN_LOGIN_DEMO'), message)
    await oten.set_password(os.getenv('EN_PASSWORD_DEMO'), message)


@dp.message_handler(commands=['en_login'],
                    user_id=user_id_required)
async def en_login(message: types.Message):
    await message.bot.send_chat_action(message.chat.id, 'typing')
    await oten.en_login(message)


@dp.message_handler(commands=['en_start'],
                    user_id=user_id_required)
async def en_demon_start(message: types.Message):
    await oten.start_en(message=message)


@dp.message_handler(commands=['en_stop'],
                    user_id=user_id_required)
async def en_demon_start(message: types.Message):
    oten.is_in_game = False


async def remind(message: types.Message, seconds=0, text=''):
    await asyncio.sleep(seconds)
    await message.bot.send_message(chat_id=message.chat.id, text=time.strftime("%H:%M:%S", time.localtime()))


@dp.message_handler(commands=['level', 'lvl', 'лвл'],
                    chat_id=chat_id_required)
async def get_level(message: types.Message):
    msg_in = ''.join(message.text.split(' ')[1:])
    await oten.level(level_number=msg_in, message=message)


@dp.message_handler(commands=['info'],
                    chat_id=chat_id_required)
async def get_info(message: types.Message):
    await oten.get_level_info(message=message)


@dp.message_handler(commands=['task'],
                    chat_id=chat_id_required)
async def get_task(message: types.Message):
    await oten.get_task(message=message)


@dp.message_handler(commands=['hint'],
                    chat_id=chat_id_required)
async def get_hint(message: types.Message):
    await oten.get_hints(message=message)


@dp.message_handler(commands=['bonus'],
                    chat_id=chat_id_required)
async def get_bonuses(message: types.Message):
    await oten.get_bonuses(message=message)


@dp.message_handler(commands=['sector'],
                    chat_id=chat_id_required)
async def get_sectors(message: types.Message):
    await oten.get_sector(message=message)


@dp.message_handler(commands=['time'],
                    chat_id=chat_id_required)
async def get_sectors(message: types.Message):
    await oten.calculate_time(message=message)


@dp.message_handler(commands=['gps'],
                    chat_id=chat_id_required)
async def get_sectors(message: types.Message):
    await oten.find_gps(message=message)


@dp.message_handler(commands=['json'],
                    chat_id=chat_id_required)
async def get_json(message: types.Message):
    msg_in = ''.join(message.text.split(' ')[1:])
    file = oten.get_level_json(msg_in)
    if file:
        await message.bot.send_document(chat_id=message.chat.id, document=file)
    else:
        await message.answer("I can't spend file")


@dp.message_handler(commands=['html'],
                    chat_id=chat_id_required)
async def get_html(message: types.Message):
    msg_in = ''.join(message.text.split(' ')[1:])
    await bot.send_chat_action(chat_id=message.chat.id, action='upload_document')
    file = oten.get_level_html(msg_in)
    if file:
        await message.bot.send_document(chat_id=message.chat.id, document=file)
    else:
        await message.answer("I can't spend file")


@dp.message_handler(commands=['test'],
                    chat_id=chat_id_required)
async def test(message: types.Message):
    str_in = "\u003chr\u003e\u003cblockquote\u003e Текст цитаты \u003c/blockquote\u003e\u003chr\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\u003cspan id=\"LevelsScenarioRepeater_ctl00_LevelTasksRepeater_ctl00_lblLevelTask\" class=\"white\"\u003eПостройте из того, что есть в Пакете №22 (в «Наборе разведчика»)\r\u003cbr/\u003e\r\u003cbr/\u003e- то, что нарисовано на схеме в задании:\r\u003cbr/\u003e\u003ca href=\"http://dekormyhome.ru/wp-content/uploads/2019/07/46e19f43fdcfe8ea9f5522f021e5ab0b.jpg\"\u003e\u003cimg src=\"http://dekormyhome.ru/wp-content/uploads/2019/07/46e19f43fdcfe8ea9f5522f021e5ab0b.jpg\" border=\"0\"\u003e\u003c/a\u003e\r\u003cbr/\u003e\r\u003cbr/\u003eПодойдите к агентам в координатах \r\u003cbr/\u003e\u003cfont color=\"gold\"\u003eN58°33\u0027 38.3\" \r\u003cbr/\u003eE59°13\u0027 54.3\"\u003c/font\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\u003cp style=\u0027text-align: justify\u0027\u003e\u003cspan style=\u0027color: #FF9933\u0027\u003e\u003cb\u003eНазвание\u003c/b\u003e\u003c/span\u003e\r\u003cbr/\u003e\u003cvideo width=\u0027640\u0027 height=\u0027360\u0027 src=\"https://youtu.be/L_LUpnjgPso\" controls autobuffer\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\u003cp\u003eЕсли видео не воспроизводится, скачайте его по ссылке: \u003ca href=\"https://youtu.be/L_LUpnjgPso\"\u003eDownload\u003c/a\u003e (РАЗМЕР Mb)\u003c/p\u003e \u003c/video\u003e\u003c/p\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\u003ciframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/JTjTyU_DC4k\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen\u003e\u003c/iframe\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\u003caudio controls\u003e\u003csource src=\u0027http://d2.endata.cx/data/games/31242/%D0%95%D0%93%D0%9E%D0%A032%D0%A8%D0%98%D0%9F32-32Dior.mp3\u0027 type=\u0027audio/mp3\u0027\u003e\r\u003cbr/\u003eТег audio не поддерживается вашим браузером. \u003ca href=\u0027http://d2.endata.cx/data/games/31242/%D0%95%D0%93%D0%9E%D0%A032%D0%A8%D0%98%D0%9F32-32Dior.mp3\u0027\u003eСкачайте музыку\u003c/a\u003e\u003c/audio\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\u003ca href=\"geo:53.000000, 23.000000;\"\u003e53.000000 23.000000\u003c/a\u003e\r\u003cbr/\u003e\r\u003cbr/\u003eПоразите цель трижды. Получите код у агента. Подсказок не будет.\r\u003cbr/\u003e\r\u003cbr/\u003e\u003cb\u003eФормат ответа:\u003c/b\u003e Код. \r\u003cbr/\u003e\r\u003cbr/\u003e\u003cb\u003eВнимание опасность:\u003c/b\u003e Беречь глаза. Осторожно переходите дорогу.\r\u003cbr/\u003e\r\u003cbr/\u003e\u003cb\u003eАгент:\u003c/b\u003e Рядом с вами.\r\u003cbr/\u003e\r\u003cbr/\u003e\u003cb\u003eПримечания:\u003c/b\u003e \r\u003cbr/\u003eНичего не выбрасывать, все нужно далее!\u003c/span\u003e"
    await oten.text_handler(str_in, message)


@dp.message_handler(commands=['testgps'],
                    chat_id=chat_id_required)
async def test(message: types.Message):
    await message.bot.send_location(message.chat.id, latitude=57.154526, longitude=65.503772)


@dp.message_handler(commands=['testbot'],
                    chat_id=chat_id_required)
async def test(message: types.Message):
    await oten.testbot(message)
    # await message.bot.send_location(message.chat.id, latitude=57.154526, longitude=65.503772)


@dp.message_handler(commands=['testmsg'],
                    chat_id=chat_id_required)
async def test(message: types.Message):
    msgs = oten.handler_task(' ')
    for msg in msgs:
        await message.answer(**msg)


@dp.message_handler(commands=['status'],
                    chat_id=chat_id_required)
async def test(message: types.Message):
    msg = '{} {}'.format(oten.is_in_game, oten.last_update)
    await message.answer(msg)



@dp.message_handler(commands=['log'],
                    user_id=user_id_required,
                    chat_id=chat_id_required)
async def send_log(message: types.Message):
    file = open(log_file, 'rb')
    await message.bot.send_document(chat_id=message.chat.id,
                                    document=file,
                                    reply_to_message_id=message.message_id)


# En end block


@dp.message_handler(commands=['help'],
                    user_id=user_id_required)
async def send_welcome(message: types.Message):
    msg = "/access\n" \
          "/user\n" \
          "/password\n" \
          "/def_user\n" \
          "/en_start\n" \
          "/en_stop\n" \
          "/en_login\n" \
          "/status\n" \
          "/log\n" \
          "/htm\n" \
          "/json\n" \
          "/chatid\n" \
          "/chats\n" \
          "/set_com\n"
    await message.reply(msg)


@dp.message_handler(commands=['chatid'])
async def send_info(message: types.Message):
    msg_txt = 'ChatId:{}\nUserId:{}\n'.format(
        message.chat.id,
        message.from_user.id)
    await message.answer(msg_txt)


# Example typing status
@dp.message_handler(commands=['type'])
async def send_info(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    time.sleep(5)
    await message.answer('msg_txt')


@dp.message_handler(commands=['chats'],
                    user_id=user_id_required)
async def show_required_chats(message: types.Message):
    await message.answer('User:{}\nChats:{}'.format(user_id_required, chat_id_required))
    for id in chat_id_required:
        await message.answer('ID="{}", Type={}'.format(id, type(id)))


@dp.message_handler(commands=['set_com'],
                    user_id=user_id_required)
async def set_com(message: types.Message):
    commands = [types.BotCommand(command="/lvl", description="Загрузить уровень"),
                types.BotCommand(command="/info", description="Загрузить статистику по уровню"),
                types.BotCommand(command="/task", description="Загрузить задание"),
                types.BotCommand(command="/hint", description="Загрузить подсказки"),
                types.BotCommand(command="/bonus", description="Загрузить бонусы"),
                types.BotCommand(command="/sector", description="Загрузить сектора"),
                # types.BotCommand(command="/.", description="отправить ответ"),
                ]
    await message.bot.set_my_commands(commands)
    await message.answer("Команды настроены.")


# @dp.message_handler(regexp='(^cat[s]?$|puss)')
# async def cats(message: types.Message):
#     with open('data/cat.jpg', 'rb') as photo:
#         await message.reply_photo(photo, caption='Cats are here 😺')


# @dp.message_handler()
# async def echo(message: types.Message):
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)
#     # await message.answer(message.text)
#     await message.answer(message.chat.id)


@dp.message_handler(regexp=r'[\.\/]',
                    chat_id=chat_id_required)
async def answer(message: types.Message):
    await oten.send_answer(message)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
