#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import logging
import json
import time
from contextlib import closing
from bs4 import BeautifulSoup
from lxml import html, etree

# import for debug and test
import preset_for_test as dbt

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class en_session(object):
    """
    Class for handling requests from site
    """

    def __init__(self,
                 domain=None,
                 game_id=None,
                 url_game=None,
                 url_statistic=None,
                 login=None,
                 password=None):
        # self.domain = domain
        # self.game_id = game_id
        # self.url_game = url_game
        # self.url_statistic = url_statistic
        # self.page = None
        self.login = login
        self.password = password
        self.relogin = True
        self.relogin_limiter = 3
        self.error_logs = []

        self.session = requests.session()
        self.session.headers.update({
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
            'User-Agent': 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
            'Connection': 'keep-alive'})

    def set_parameters(self,
                       login=None,
                       password=None,
                       game_id=None,
                       url_game=None,
                       url_statistic=None,
                       relogin=None):
        """ Set variable for web-parsing """

        if login is not None:
            self.login = login
        if password is not None:
            self.password = password
        # if game_id is not None:
        #    self.game_id = game_id
        # if url_game is not None:
        #     self.url_game = url_game
        # if url_statistic is not None:
        #     self.url_statistic = url_statistic
        if relogin is not None:
            self.relogin = relogin

    def get_error_logs(self):
        """
        Return all errors which happened to web-parsing
        :return: String
        """
        result = '\n'.join(self.error_logs)
        self.error_logs.clear()
        return result

    def _request_wrapper(self, resp=None):
        """
        Wraps Requests request for handling known exceptions

        :returns
        soup - if all is good
        None - if have error
        """

        if resp is not None:
            if 200 <= resp.status_code <= 299:
                # parser = html.HTMLParser(encoding='utf-8')
                # page = html.fromstring(resp.content, parser=parser)
                page = BeautifulSoup(resp.text, 'lxml')
                return page
            else:
                self.error_logs.append('Не удалось страницу code:{0}'.format(resp.status_code))
                return None

    def get_web_page(self,
                     url,
                     relogin_limiter=None):
        """
        Main function for get web page. Have trying to relogin.

        :arg
        Url - url page which need get
        relogin_limiter - int: Counter limit to relogin

        :returns
        soup - if all is good
        None - if have error
        """

        # Check counter of relogin - protection against recursion
        if relogin_limiter is None:
            relogin_limiter = self.relogin_limiter

        # Userdate for login
        userdata = {
            'socialAssign': 0,
            'Login': self.login,
            'Password': self.password,
            'EnButton1': 'Вход',
            'ddlNetwork': 1
        }

        # Web Request
        resp = self.session.get(url, data=userdata)
        # print('{0} - {1} {2}'.format(resp.status_code, resp.url, resp.history))

        # If LogOUT and try recursive RE logIN
        if len(resp.history) == 1 and relogin_limiter > 0:
            relogin_limiter -= 1
            page = self.get_web_page(resp.url, relogin_limiter)
            return page

        # If excess of relogin_limiter
        elif relogin_limiter == 0:
            self.error_logs.append('Не удалось перелогениться')
            return None

        # If all is good
        else:
            page = self._request_wrapper(resp)
            return page

    def get_json_page(self, url):
        """ Get json page"""
        page = self.get_web_page(url)

        if page is not None:
            # self.page = self.get_web_page(url)
            json_page = json.loads(page.text)
            # self.json_data = json_page
            return json_page
        else:
            self.error_logs.append('get_json_page: Пришла пустая страница')
            return None

    def get_html_page(self, url):
        """ Загатовка для статистики пока выводит просто текст """
        page = self.get_web_page(url)
        print('get_html_page')
        # print(page)

        if page is not None:
            # self.page = self.get_web_page(url)
            text_page = page.text
            print(text_page)

    def post_answer(self, url=None, answer='', level_id=None, level_number=None, bonus_mode=False):
        """
        Input:
            bonus_mode: False - Level Answer
                        True - Bonus Answer
        """

        if url is None:
            url = self.url

        #last_data = self.page.xpath('//input[@type="hidden"]/@value')
        if bonus_mode:
            userdata = {
                'LevelId': level_id,
                'LevelNumber': level_number,
                'BonusAction.Answer': answer
            }
        else:
            userdata = {
                'LevelId': level_id,
                'LevelNumber': level_number,
                'LevelAction.Answer': answer
            }

        resp = self.session.post(url, data=userdata)
        result = self._request_wrapper(resp)
        if result:
            return True
        else:
            self.error_logs.append('post_answer: отправка прошла не успешна (code:{0})'.format(resp.status_code))
            return None




if __name__ == '__main__':
    # unit_test_relogin()
    en_ses = en_session()
    en_ses.error_logs = ['123', '234']
    print(en_ses.error_logs)
    print(en_ses.get_error_logs())
    print(en_ses.error_logs)
    """ 
    
    en_ses.set_parameters(dbt.domain, dbt.login, dbt.password)
    en_ses.get_json_page(dbt.page_game)
    en_ses.get_html_page(dbt.page_stat)
    en_ses.get_json_page(dbt.page_game)
    """
