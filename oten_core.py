#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging
import datetime

import mistletoe
from deepdiff import DeepDiff
import oten_pydantic
import oten_request
import oten_utilits

from bs4 import BeautifulSoup
from mistletoe import markdown
from html2text import HTML2Text
from markdownify import markdownify as md

import asyncio
from aiogram import types as aitype
import sys

log = logging.getLogger(__name__)


def format_message(text, parse_mode='markdown', disable_web_page_preview=False):
    msg = {'text': text,
           'parse_mode': parse_mode,
           'disable_web_page_preview': disable_web_page_preview
           }
    return msg


def html2txt(str_in):
    # Convert html to Markdown text
    parser = HTML2Text()
    parser.ignore_anchors = True
    parser.body_width = 0
    markdown_txt = parser.handle(str_in)

    # Fix multi NEWLINE
    markdown_txt = re.sub(r'(\s+\n){3,}', '\n\n', markdown_txt)

    return markdown_txt


class Oten():
    """
    This class provides parsing and handling encounter
    """

    def __init__(self, url_game=None):
        """-"""
        self.domain = None
        self.gid = None

        self.en_conn = oten_request.EnSession()
        self.en_engine = oten_pydantic.EngineEN(**oten_pydantic.empty_data)
        self.last_update = 0

        self.is_in_game = False
        self.current_level = 0
        self.storm = None

        # self.st_monitor_bonus = 0

    def get_en_engine(self, json_in=None):
        """
        Parse JSON and make structure of EngineEN (pydantic)
        :param json_in:
        :return: pass
        """
        if json_in is None:
            json_in = oten_pydantic.empty_data

        self.en_engine = oten_pydantic.EngineEN(**json_in)
        return self.en_engine

    async def chek_login(self):
        # Check is login now?
        if self.en_conn.check_login(self.domain):
            return True
        else:
            # If not try to reconnect
            return self.en_conn.login_en()

    async def args_from_url(self, url_str, message: aitype.Message):
        """
        This metod get DOMAIN(domain) and Game-ID(gid) from URL
        Args:
            url_str - str
        Result:
            tuple(domain,gid)
        """
        match = re.search(r'([\w\d]*).en.cx.*gid=([\d]*)', url_str)
        try:
            self.domain = match.groups()[0]
            self.en_conn.set_domain(self.domain)  # Bad code need refactoring
            self.gid = match.groups()[1]
            await message.answer('Url: +')
        except AttributeError as ae:
            await message.answer('Url: invalid link')
        except BaseException as e:
            await message.answer('Url: ERROR: {}'.format(e))

    async def set_login(self, login, message: aitype.Message):
        self.en_conn.set_login(login)
        await message.answer('Login: +')

    async def set_password(self, password, message: aitype.Message):
        self.en_conn.set_password(password)
        await message.answer('Password: +')

    async def en_login(self, message: aitype.Message):
        if self.en_conn.login_en(self.domain):
            await message.answer('Login is successful')
        else:
            await message.answer('Login failed: {}'.format(self.en_conn.info))

    async def start_en(self, message: aitype.Message):
        """
        Main DEMON
        :param message:
        :return:
        """
        await self.en_login(message)

        # Generate URL
        url = self.generation_url(self.current_level)

        if url:
            # Check login and if not to Try reconnect
            is_login = self.chek_login()
            if is_login:
                # If all is well then the game has started
                self.is_in_game = True
            else:
                self.is_in_game = False
        else:
            self.is_in_game = False

        # Report it
        if self.is_in_game:
            await message.answer('EN-Demon is alive')
        else:
            await message.answer("EN-Demon died")

        # Main Game Loop
        while self.is_in_game:
            await asyncio.sleep(2)
            await self.update_en(message)
            self.last_update = datetime.datetime.now()
        await message.answer('EN-Demon died')

    async def stop_en(self, message: aitype.Message):
        self.is_in_game = False
        message.answer('+')

    async def update_en(self, message: aitype.Message):
        url = self.generation_url(self.current_level)

        if url:
            json = self.en_conn.get_json(url)
            # log.info('Load LVL')

        if json:
            # log.info('load JSON')
            ene_old = self.en_engine
            ene_new = self.en_engine
            ene_new = self.get_en_engine(json)
            await asyncio.sleep(0.1)

            # Check is it real game
            if (ene_new.game_id != 0) and (ene_new != ene_old):

                if ene_new is None:
                    log.info('update_en ene_new is None')
                if ene_old is None:
                    log.info('update_en ene_old is None')

                if ene_new.event != 0:
                    if ene_new.event == 5:
                        await message.answer('Игра еще не началась')
                    elif ene_new.event == 6:
                        await message.answer('Игра закончена')
                    elif ene_new.event == 9:
                        await message.answer('Администратор игры всё ещё не допустил вас к игре')

                # New level
                elif (ene_old.level is None and ene_new.level is not None) \
                        or (ene_new.level.number != ene_old.level.number) \
                        or (ene_new.level.tasks != ene_old.level.tasks):
                    await message.answer('#АП!')
                    await self.get_level_info(message=message)
                    await self.get_task(message=message)

                # Sector
                try:
                    if (ene_new.level.sectors != ene_old.level.sectors) \
                            and (ene_new.level.number == ene_old.level.number):
                        await message.bot.send_message(message.chat.id, '📩 Изменились сектора')
                        # await self.get_sector(message=message)
                except AttributeError as ae:
                    log.info('update_en: (status) {}'.format(ae))

                # Hint
                try:
                    if (ene_new.level.helps != ene_old.level.helps) \
                            and (ene_new.level.number == ene_old.level.number):
                        await message.bot.send_message(message.chat.id, '📩 Изменились подсказки')
                        # await self.get_hints(message=message)
                except AttributeError as ae:
                    log.info('update_en: (helps) {}'.format(ae))

                # Message
                try:
                    if ene_new.level.messages != ene_old.level.messages:
                        await message.answer(
                            '📩 Изменились сообщения от автора:\n{}'.format(ene_new.level.messages)
                        )
                except AttributeError as ae:
                    log.info('update_en: (messages) {}'.format(ae))

                try:
                    if ene_new.level.bonuses != ene_old.level.bonuses:
                        await message.bot.send_message(message.chat.id, '📩 Изменились бонусы')
                        # await self.get_bonuses(message=message)
                except AttributeError as ae:
                    log.info('update_en: (bonuses) {}'.format(ae))

                # Update new ene
                self.en_engine = ene_new
        else:
            # Try relogin and if failed send message
            if not await self.chek_login():
                await message.bot.send_message(message.chat.id, 'Не получилось загрузить уровень')

    async def text_handler(self, str_in, message: aitype.Message):
        """
        This function accept input html code,
        parse all attachments from it,
        and convert to markdown text
        :param message:
        :param str_in: html code
        :return: list of construction:
        """
        markdown_txt = html2txt(str_in)

        # Handler images in MarkDown (remove '!' before link)
        # Handler nested URL
        nested_url = re.findall(r'(\[(!?\[([^\[\]\(\)]*?)\]\((.*?)\))\]\((.*?)\))', markdown_txt)
        for item in nested_url:
            full_item = item[0]
            sub_item = item[1]
            text_sub_item = item[2]
            link_sub_item = item[3].strip()
            file_name_sub_item = link_sub_item[link_sub_item.rfind('/') + 1:]
            link_item = item[4].strip()
            file_name_item = link_item[link_item.rfind('/') + 1:]

            if link_item == link_sub_item:
                if text_sub_item == '':
                    new_item = '[{}]({}) '.format(file_name_sub_item, link_item)
                    markdown_txt = markdown_txt.replace(full_item, new_item)
                else:
                    new_item = '[{}]({}) '.format(text_sub_item, link_item)
                    markdown_txt = markdown_txt.replace(full_item, new_item)
            else:
                if text_sub_item == '':
                    new_item = '(🔗 [{}]({})->[{}]({}) )'.format(file_name_sub_item,
                                                                 link_sub_item,
                                                                 file_name_item,
                                                                 link_item)
                    markdown_txt = markdown_txt.replace(full_item, new_item)
                else:
                    new_item = '(🔗 [{}]({})->[{}]({}) )'.format(text_sub_item,
                                                                 link_sub_item,
                                                                 file_name_item,
                                                                 link_item)
                    markdown_txt = markdown_txt.replace(full_item, new_item)

        # Handler URL
        urls = re.findall(r'(!?\[([^\[\]\(\)]*?)\]\((.*?)\))', markdown_txt)
        for url in urls:
            full_item = url[0]
            link_item = url[2].strip()
            if url[1] == '':
                text_item = link_item[link_item.rfind('/') + 1:]
            else:
                text_item = url[1]

            new_item = '[{}]({})'.format(text_item, link_item)
            markdown_txt = markdown_txt.replace(full_item, new_item)

        # msgs_list.append(format_message(markdown_txt, disable_web_page_preview=True, parse_mode=''))
        try:
            await message.bot.send_message(chat_id=message.chat.id,
                                           text=markdown_txt,
                                           parse_mode='markdown',
                                           disable_web_page_preview=True)
        except BaseException as e:
            await message.bot.send_message(chat_id=message.chat.id,
                                           text=markdown_txt,
                                           disable_web_page_preview=True)

        # Find all some link
        attachments_list = re.findall(r'src=\"(http.*?)\"|href=\"(http.*?)\"', str_in)

        # unique attachment
        attachments_set = set()
        for attachment in attachments_list:
            attachments_set.update(attachment)

        for attachment in attachments_set:
            attach_url = attachment.strip()
            attach_name = attach_url[attach_url.rfind('/') + 1:]
            attach_msg = '[{}]({})'.format(attach_name, attach_url)
            try:
                await message.bot.send_message(chat_id=message.chat.id,
                                               text=attach_msg,
                                               parse_mode='markdown')
            except BaseException as e:
                await message.bot.send_message(chat_id=message.chat.id,
                                               text=attach_url)

    async def get_level_info(self, ene=None, message: aitype.Message = None):
        """
        Get main info about Level
        :param ene:
        :param message:
        :return:
        """
        if ene is None:
            ene = self.en_engine

        # Check is levle is not Null
        if ene.level:

            if ene.level.has_answer_block_rule:
                answer_block = '⚠️ Answer block 👤:{} 📤:{} ⏱:{}\n'.format(
                    ene.level.block_target_id,
                    ene.level.attemts_number,
                    datetime.timedelta(seconds=ene.level.attemts_period)
                )
            else:
                answer_block = ''

            if ene.level.helps:
                hint_summary = ''
                for hint in ene.level.helps:
                    if hint.remain_seconds == 0:
                        hint_summary += 'Подсказка {} - доступна\n'.format(str(hint.number))
                    else:
                        hint_summary += \
                            'Подсказка {} - через {}\n'.format(
                                str(hint.number),
                                datetime.timedelta(seconds=hint.remain_seconds)
                            )
            else:
                hint_summary = ''

            args = {
                'lvl_num': ene.level.number,
                'lvl_cnt': len(ene.levels),
                'lvl_name': ene.level.name,
                'timeout': str(datetime.timedelta(seconds=ene.level.timeout_seconds_remain)),
                'answer_block': answer_block,
                'sectors_count': len(ene.level.sectors),
                'required_sectors_count': ene.level.required_sectors_count,
                'passed_sectors_count': ene.level.passed_sectors_count,
                'left_sectors_count': ene.level.sectors_left_to_close,
                'hint_counts': len(ene.level.helps),
                'bonus_count': len(ene.level.bonuses),
                'left_bonus_count': len(list([x for x in ene.level.bonuses if not x.is_answered])),
                'passed_bonus_count': len(list([x for x in ene.level.bonuses if x.is_answered])),
                'hint_summary': hint_summary
            }

            text = 'Уровень *{lvl_num}* из {lvl_cnt}: {lvl_name}\n' \
                   '⏳:{timeout}\n{answer_block}' \
                   '------------------------------\n' \
                   '🔑:{sectors_count} | ✅:{passed_sectors_count} | ☑️:{left_sectors_count}\n' \
                   '🎁:{bonus_count} | ✅:{passed_bonus_count} | ☑️:{left_bonus_count}\n' \
                   '------------------------------\n' \
                   '{hint_summary}'.format(**args)

            await message.bot.send_message(chat_id=message.chat.id,
                                           text=text,
                                           parse_mode='markdown')
        else:
            await message.answer('Need load level')

    async def get_task(self, ene=None, message=aitype.Message()):
        """
        Get task messages from ENEngine
        :param message:
        :type ene: ENEngine object
        :return: str: msg for TG with MarkDown format
        """
        if ene is None:
            ene = self.en_engine

        try:
            if ene.level.tasks:
                for task in ene.level.tasks:
                    await message.bot.send_message(chat_id=message.chat.id,
                                                   text='Задание')
                    await self.text_handler(task.task_text_formatted, message)
            # !!! think what will do if there are not hints
            return False
        except AttributeError as ae:
            await message.bot.send_message(chat_id=message.chat.id,
                                           text="Get_task: Can't find hints")

    async def get_hints(self, ene=None, message=aitype.Message):
        """
        Get hints messages from ENEngine
        :param message:
        :type ene: ENEngine object
        :return: str: msg for TG with MarkDown format
        """
        if ene is None:
            ene = self.en_engine

        try:
            if ene.level.helps:
                for hint in ene.level.helps:
                    await message.bot.send_message(chat_id=message.chat.id,
                                                   text='*Подсказка {}:*'.format(hint.number),
                                                   parse_mode='markdown')
                    await self.text_handler(hint.help_text, message)
            else:
                await message.bot.send_message(chat_id=message.chat.id,
                                               text='Подсказок нет')
        except AttributeError as ae:
            await message.bot.send_message(chat_id=message.chat.id,
                                           text="GET_hint: Can't find hints")

    async def get_bonuses(self, ene=None, message=aitype.Message):
        """
        Get hints messages from ENEngine
        :param current_bonus:
        :param message:
        :type ene: ENEngine object
        :return: str: msg for TG with MarkDown format
        """
        if ene is None:
            ene = self.en_engine

        try:
            current_bonus = int(''.join(message.text.split(' ')[1:]))
        except BaseException:
            current_bonus = -1

        # try get current bonus
        if current_bonus > 0:
            bonus = [x for x in ene.level.bonuses if x.number == current_bonus]
            try:
                await self.text_handler(bonus[0].task, message)
            except BaseException as e:
                await message.answer("Can't get bonus №{}".format(current_bonus))
                log.info('get_bonuses: try get current bonus {}'.format(e))

        else:
            try:
                bonus_msg = ''

                if ene.level.bonuses:
                    for bonus in ene.level.bonuses:
                        # IF bonus is available
                        # Answered bonus
                        if bonus.is_answered:
                            bonus_msg += '✅ Бонус {}: {}(+{})\n'.format(
                                bonus.number,
                                bonus.name,
                                datetime.timedelta(seconds=bonus.award_time))

                        # Expired bonus
                        elif bonus.expired:
                            bonus_msg += '❌ Бонус {}: {}\n'.format(
                               bonus.number,
                               'не выполнен (время выполнения истекло)')

                        # Bonus is inactive yet
                        elif bonus.seconds_to_start > 0:
                            bonus_msg += '🕑 Бонус {}: Будет доступен через {}\n'.format(
                               bonus.number,
                               bonus.name,
                               str(datetime.timedelta(seconds=bonus.seconds_to_start)))

                        # Just bonus is not answered
                        else:
                            bonus_msg += '🔘 Бонус {}: {}\n'.format(
                               bonus.number,
                               bonus.name)

                        # if need sped full info
                        if current_bonus == 0:
                            await message.answer(bonus_msg)
                            bonus_msg = ''
                            try:
                                await self.text_handler(bonus.task, message)
                            except BaseException as e:
                                log.info('get_bonuses: try load all bonus {}'.format(e))

                    # If need short info
                    await message.answer(bonus_msg)

                else:
                    await message.bot.send_message(chat_id=message.chat.id,
                                                   text='Бонусов нет')
            except AttributeError as ae:
                await message.bot.send_message(chat_id=message.chat.id,
                                               text="GET_bonus: Can't find hints")

    async def get_sector(self, ene=None, message=aitype.Message):
        if ene is None:
            ene = self.en_engine

        msg = ''
        try:
            if ene.level.sectors:
                msg += '🔑:{} | ✅:{} | ☑️:{}\nОстались: '.format(
                    len(ene.level.sectors),
                    ene.level.passed_sectors_count,
                    ene.level.required_sectors_count
                )
                for sector in ene.level.sectors:
                    if sector.is_answered is False:
                        if sector.name is not None or sector.name != '':
                            msg += sector.name + ', '
                        else:
                            msg += str(sector.sector_id) + ', '
                await message.bot.send_message(chat_id=message.chat.id,
                                               text=msg)
            else:
                await message.bot.send_message(chat_id=message.chat.id,
                                               text='Секторов нет')
        except AttributeError as ae:
            await message.bot.send_message(chat_id=message.chat.id,
                                           text="GET_sectors: Can't find json")

    async def level(self, level_number=None, message=aitype.Message):
        """
        Function setting curent level, gettid and format final message for TG
        :param message:
        :param level_number:
        :return: str: msg for TG with MarkDown format
        """
        if level_number != '':
            self.current_level = level_number

        url = self.generation_url(self.current_level)
        if url:
            json = self.en_conn.get_json(url)
        else:
            json = None

        if json:
            ene = self.get_en_engine(json)
            await self.get_level_info(ene=ene, message=message)
            await self.get_task(ene=ene, message=message)
            await self.get_hints(ene=ene, message=message)
        else:
            await message.bot.send_message(chat_id=message.chat.id,
                                           text="Level: Can't load json")

    async def calculate_time(self, message=aitype.Message):
        ene = self.en_engine
        ts = ene.level.start_time
        await message.reply(ts)

    async def find_gps(self, message=aitype.Message):
        full_txt = ''
        ene = self.en_engine

        try:
            full_txt += html2txt(ene.level.tasks[0].task_text_formatted) + '\n'
        except BaseException as e:
            log.info('find_gps: (task) {}'.format(e))

        try:
            bonuses = list([x for x in ene.level.bonuses])
            for bonus in bonuses:
                full_txt += html2txt(bonus.task) + '\n'
                full_txt += html2txt(bonus.help) + '\n'
        except BaseException as e:
            log.info('find_gps: (bonuses) {}'.format(e))

        await oten_utilits.text2gps(full_txt, message)







    def get_level_html(self, level_number=None):
        if level_number is None:
            level_number = self.current_level

        url = self.generation_url(self.current_level, json=False)
        file_path = 'materials/' + url[url.rfind('/'):] + '.html'
        # self.get_page(url=url, type_page='html', file_path=file_path)
        self.en_conn.get_page_to_file(url=url, file_path=file_path)
        try:
            file_b = open(file_path, 'rb')
            return file_b
        except:
            return False

    def get_level_json(self, level_number=None):
        file_path = 'materials/level=' + str(self.current_level) + '.json'
        self.en_conn.resp_to_file(file_path=file_path)
        try:
            file_b = open(file_path, 'rb')
            return file_b
        except:
            return False

    def generation_url(self, level=None, json=True):
        """
        Generate URL for request
        Example link = http://demo.en.cx/gameengines/encounter/play/31228/?level=1&json=1
        :param json:
        :param level:
        :return:
        """
        if self.domain is None or self.gid is None:
            log.error('Domain or GID is None')
            return False
        else:
            if level is None or level == 0:
                url = 'http://{0}.en.cx/gameengines/encounter/play/{1}/'.format(self.domain, self.gid)
                if json:
                    url += '?json=1'
            else:
                url = 'http://{0}.en.cx/gameengines/encounter/play/{1}/?level={2}'.format(
                    self.domain, self.gid, level)
                if json:
                    url += '&json=1'
            return url

    async def send_answer(self, message=aitype.Message):
        ene = self.en_engine

        # Prepare Code and Prefix
        code_match = re.match(r'([\.\/]{1,2})[\s]?(.*)', message.text)

        try:
            code = code_match.group(2)
            pre = code_match.group(1)
        except AttributeError:
            code = ''
            pre = '.'
        answer_msg = ''

        data = {'LevelId': ene.level.level_id,
                'LevelNumber': ene.level.number,
                # 'LevelAction.Answer': code.group(2)
                # 'BonusAction.Answer': code.group(2)
                }

        # Check if bot in the game
        if ene.game_id != 0:

            # Chek has this code been sent
            level_answers = list([x for x in ene.level.mixed_actions if x.answer == code])
            if level_answers:
                answer_msg += '🔁'

            # IF this new code
            # If there is block Answer
            if ene.level.has_answer_block_rule:
                if len(pre) > 1:
                    data['LevelAction.Answer'] = code
                else:
                    data['BonusAction.Answer'] = code

            # If there is not block Answer
            else:
                # Configure data and send it
                data['LevelAction.Answer'] = code

            # IF has not block and want to spend code
            if ene.level.block_duration > 0 and len(pre) > 1:
                await message.answer(
                    '⛔️ Ввод заблокирован, осталось {}'.format(
                        datetime.timedelta(seconds=ene.level.block_duration)))
            else:
                await self.wrapper_send_answer(data=data,
                                               code=code,
                                               answer_msg=answer_msg,
                                               message=message)

        else:
            await message.answer("Answer: Game is stop!")

    async def wrapper_send_answer(self, data, code, answer_msg='', message=aitype.Message):

        url = self.generation_url(self.current_level)
        json = self.en_conn.send_answer(url, data)

        # if POST request is successful
        if json:
            try:
                ene_new = self.get_en_engine(json)
                # print(ene_new)
                # Check answer is Correct:
                answer_list = list([x for x in ene_new.level.mixed_actions if x.answer == code])

                if answer_list[0].is_correct:
                    answer_msg += '✅ {}:\n'.format(code)

                    for bonus in ene_new.level.bonuses:
                        try:
                            if bonus.answer.answer == code:
                                answer_msg += '🎁 {}:{}\n'.format(bonus.number, bonus.name)
                        except BaseException:
                            pass

                    for sector in ene_new.level.sectors:
                        try:
                            if sector.answer.answer == code:
                                answer_msg += '🔑 {}:{}\n'.format(sector.order, sector.name)
                        except BaseException:
                            pass

                    await message.reply(answer_msg)

                else:
                    await message.reply('❌ {}'.format(code))

            except BaseException as e:
                await message.answer("Answer: spend but can't parse ene")
                log.info('Answer: (ene) {}'.format(e))
        else:
            await message.answer("Answer: can't spend answer - json")
            log.info('Answer: (json) {}'.format(e))


def main():
    pass


if __name__ == '__main__':
    main()
