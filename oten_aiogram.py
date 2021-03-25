"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
import os
import time

from aiogram import Bot, Dispatcher, executor, types

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=os.getenv('TG_TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['status', 'info'])
async def send_info(message: types.Message):
    msg_txt = 'ChatId:{}\nUserId:{}\n'.format(
                                    message.chat.id,
                                    message.from_user.id)
    await message.answer(msg_txt)


@dp.message_handler(commands=['test'])
async def send_info(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action='typing')
    time.sleep(5)
    await message.answer('msg_txt')


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cat.jpg', 'rb') as photo:
        await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)