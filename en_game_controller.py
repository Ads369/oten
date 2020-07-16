#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from typing import TextIO

import en_request
import parser_game_engine as pge
import re
import json
import time
from telegram.ext.dispatcher import run_async
from contextlib import closing
from bs4 import BeautifulSoup
from lxml import html, etree

# import for debug and test
import preset_for_test as dbt

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class en_game_controller(object):
    """
    Class organize handling game control
    """

    def __init__(self,
                 domain=None,
                 game_id=None,
                 game_url=None,
                 stats_url=None):
        self.domain = domain
        self.game_id = game_id
        self.current_level = 0
        self.spread = False
        self.is_game = False
        self.json_data = None
        self.game_url = game_url
        self.stats_url = stats_url
        self.en_session = en_request.en_session()
        self.error_logs = []

    def get_error_logs(self):
        """
        Return all errors which happened to web-parsing
        :return: String
        """
        result_req = self.en_session.get_error_logs()
        result = '\n'.join(self.error_logs)
        self.error_logs.clear()
        return result_req + result

    @run_async
    def revive_the_demon(self, bot, chat_id):
        """ Start Demon witch will get page"""
        logger.info('Demon Start')
        bot.send_message(chat_id=chat_id, text='Demon Start')

        # While game in active
        while self.is_game is True:
            time.sleep(2)  # wait 2 sec

            # Get page
            do_get_json = self.get_json()

            # if get_page is success
            if do_get_json is not None:
                pass
            else:
                # if network error
                bot.send_message(chat_id=chat_id, text=self.get_error_logs())
        logger.info('Demon Stop')
        bot.send_message(chat_id=chat_id, text='Demon Stop')

    def fill_url(self, url_str):
        """
        This method get DOMAIN(domain) and Game-ID(gid) from URL
        Args:
            url_str - str
        Result:
            True - if all is good
            None - if have problem
        """

        match = re.search(r'([\w\d]*.en.cx).*(gid=[\d]*)', url_str)
        try:
            self.domain = match.groups()[0].split('.')[0]
            self.game_id = match.groups()[1][4:]
            self.game_url = 'http://{0}.en.cx/gameengines/encounter/play/{1}'.format(self.domain, self.game_id)
            self.stats_url = 'http://{0}.en.cx/GameStat.aspx?gid={1}'.format(self.domain, self.game_id)
            return True
        except AttributeError:
            self.error_logs.append('Произошла ошибка при генерации URL')
            return None

    def generate_json_url(self, level=0):
        """
        This method generate url for json
        Args:
            level - int
        Result:
            string - url
        """

        if level == 0:
            return_url = self.game_url + '?json=1'
        else:
            return_url = self.game_url + '?level={0}&json=1'.format(level)

        return return_url

    def get_json(self, level=None, back=None):
        """
        :return:
        """
        # Headler for shortcut functions
        if level is None:
            level = self.current_level

        try:
            json_data = self.en_session.get_json_page(self.generate_json_url(level))
        except:
            self.error_logs.append('Ошибка в получениии JSON data')
            return None

        if json_data is not None:
            # Return json for shortcut functions
            if back is None:
                self.json_data = json_data
                return True
            else:
                return json_data
        else:
            self.error_logs.append('Не получилось сгенерировать ссылку')
            return None

    def fill_user(self, str_in):
        """
        This method get DOMAIN(domain) and Game-ID(gid) from URL
        Args:
            str_in - str
        Result:
            True - if all is good
            None - if have problem
        """

        args = str_in.split(' ')
        if len(args) == 2:
            login = args[0]
            password = args[1]
            self.en_session.set_parameters(login=login, password=password)
            return True
        else:
            self.error_logs.append('Произошла ошибка при заполнении Логина и Пароля')
            return None

    def change_spread_mode(self):
        """ Method for change EN-Mode game Line or Spread """
        if self.spread:
            self.spread = False
            return 'Установлен режим "Линейка"'
        else:
            self.spread = True
            return 'Установлен режим "Штурм"'

    def change_game_status(self):
        """ Method for change EN-Mode game Line or Spread """
        if self.is_game:
            self.is_game = False
        else:
            self.is_game = True
        return self.is_game  # 'Режим игры установлен в значение {0}'.format(self.is_game)

    def change_current_level(self, level_number):
        """ Change current level for Spread mode"""
        if len(level_number) > 0:
            self.current_level = level_number
            return 'Перешли на уровень {0}'.format(self.current_level)
        else:
            return 'Укажи уровень'

    def get_short_information(self):
        """ Get short and beautiful info about level"""
        if self.json_data is not None:
            result = pge.get_short_information_msg(self.json_data)
            return result
        else:
            return 'Инофрмация отсутсвтует'

    def get_level(self):
        """
        :return:
        """
        if self.game_url is not None:

            # Get JSON data -- current lvl include in get_json()
            do_get_json = self.get_json()

            # Check did get JSON or Not
            if do_get_json:
                # Generate msg for TG
                array_msgs = pge.get_level_task(self.json_data)

                if array_msgs is not None:
                    return array_msgs
                else:
                    self.error_logs.append('Неудачная попытка геренации сообщения для ТГ')
                    return None
            else:
                self.error_logs.append('Неудачная попытка получить JSON')
                return None
        else:
            self.error_logs.append('Не введен URL')
            return None

    def get_bonus_list(self):
        return pge.get_bonus_list(self.json_data)

    def get_sector_list(self):
        return pge.get_sector_list(self.json_data)

    def generate_kml_file(self):
        """ Generate kml file for gps coords for every level"""
        levels_sum = len(self.json_data['Levels'])

        placemark_str = ''
        for i in range(levels_sum):
            data = self.get_json(level=i, back=True)
            info = pge.get_short_information_msg(data)
            cords = pge.get_level_gps(data)
            for cord in cords:
                xy = cord.split()
                placemark_str += '<Placemark>\n' \
                                 '<description>{3}</description>\n' \
                                 '<name>Уровень {0}</name>\n' \
                                 '<Point>\n' \
                                 '<coordinates>{2},{1},0.0 </coordinates>\n' \
                                 '</Point>\n' \
                                 '</Placemark>\n'.format(i+1, xy[0], xy[1], info)

        kml_str = '''<kml>
                       <Document>
                          {0}
                       </Document>
                    </kml>'''.format(placemark_str)

        f = open("My Map.kml", "w", encoding="utf-8")
        f.write(kml_str)
        f.close()
        f = open("My Map.kml", "rb")
        return f

    def get_location(self):
        """
        :return:
        """
        array_msgs = pge.get_level_gps(self.json_data)
        return array_msgs

    def send_answer(self, answer_in):
        # Check there is answer in history
        is_old_answer = pge.is_old_answer(self.json_data, answer_in)

        # Post answer request
        request_answer = self.en_session.post_answer(url=self.game_url,
                                                     answer=answer_in,
                                                     level_id=self.json_data['Level']['LevelId'],
                                                     level_number=self.json_data['Level']['Number'])
        if request_answer:
            self.get_json()
            is_correct = pge.check_answer(self.json_data, answer_in, is_old_answer)
            return is_correct
        else:
            return None


def main():
    pass


if __name__ == '__main__':
    main()
