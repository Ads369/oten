#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import requests
import logging
import json
import time
from contextlib import closing
from bs4 import BeautifulSoup
from lxml import html, etree

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class Session(object):
    """
    Class for handling requests from site
    """

    def __init__(self, domain=None, game_id=None, url_game=None, url_statistic=None, login=None, password=None):
        self.domain = domain
        self.game_id = game_id
        self.url_game = url_game
        self.url_statistic = url_statistic
        self.page = None
        self.login = login
        self.password = password
        self.relogin = True

        self.session = requests.session()
        self.session.headers.update({
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
            'User-Agent': 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
            'Connection': 'keep-alive'})

    def set_parameters(self,
                       domain=None,
                       login=None,
                       password=None,
                       game_id=None,
                       url_game=None,
                       url_statistic=None,
                       relogin=None):

        if domain is not None:
            self.domain = domain
        if login is not None:
            self.login = login
        if password is not None:
            self.password = password
        if game_id is not None:
            self.game_id = game_id
        if url_game is not None:
            self.url_game = url_game
        if url_statistic is not None:
            self.url_statistic = url_statistic
        if relogin is not None:
            self.relogin = relogin

    def get_page_json(self, url):
        result = self.get_page(url)
        if result:
            return self.page
        else:
            return result

    def get_page(self, url=None):
        """-"""
        if url is None:

        try:
            with closing(self.session.get(url)) as resp:
                if 200 <= resp.status_code <= 299:
                    parser = html.HTMLParser(encoding='utf-8')
                    page = html.fromstring(resp.content, parser=parser)
                    return page
                else:
                    return None

        except RequestException as e:
            log_error('Error during requests to {0} : {1}'.format(url, str(e)))
            return None

        resp = self.session.get(url)
        if self._request_wrapper(resp):
            return True
        else:
            if self.try_relogin():
                resp = self.session.get(url)
                if self._request_wrapper(resp) is True:
                    return True
                else:
                    False

    def _request_wrapper(self, url):
        """Wraps Requests request for handling known exceptions"""

        try:
            resp = self.session.get(url)

        if resp is not None:
            if 200 <= resp.status_code <= 299:
                parser = html.HTMLParser(encoding='utf-8')
                page = html.fromstring(resp.content, parser=parser)
                self.page = page
                return True
            else:
                logger.info('Не удалось загрузить страницу Status:{0}'.format(resp.status_cod))
                return resp.status_cod

    def try_relogin(self):
        for i in range(10):
            if self.login_en():
                return True
        return False

    def _check_correct_page(self, resp):
        """
        Validation LogOUT

        Input: Domain (else take from self)
        Output: True - If still Log IN
                False - if Log OUT
        """

        soup = BeautifulSoup(resp.text, 'lxml')
        find_error = soup.find("div", {"class": "error"})
        if find_error:
            logger.info('Error: {}'.format(find_error.text))
            return False
        else:
            return True

    def login_en(self, domain=None, login=None, password=None):
        """
        Method login on encounter website
        """
        if domain is None:
            domain = self.domain
        if login is None:
            login = self.login
        if password is None:
            password = self.password

            url = 'http://{0}.en.cx/Login.aspx?return=%%2f'.format(domain)
            userdata = {
                'socialAssign': 0,
                'Login': login,
                'Password': password,
                'EnButton1': 'Вход',
                'ddlNetwork': 1
            }

            resp = self.session.get(url)
            resp = self.session.post(url, data=userdata)

            # Check LogIN
            # Данный код основывается на том что при авторизации
            # у нас будет переадресация на главную старницу
            if resp.history:
                logger.info("LogIN")
                return True
            else:
                logger.info("LogOUT")
                return False
        else:
            logger.info('Bad args for login')
            return None


def main():
    """-"""
    en_session = Session()
    en_session.set_parameters('demo', 'pofiggg', 'A4346253657')
    en_session.login_en()

    for i in range(10):
        result = en_session.get_page(url='http://demo.en.cx/gameengines/encounter/play/30415?json=1')
        todos = json.loads(en_session.page.text)
        print(todos)
        time.sleep(10)

    # parser = html.HTMLParser(encoding='utf-8')
    # page = html.parse('page/storm/Сеть городских игр Encounter.html', parser=parser)
    # print(en_session.check_shtorm(page=page))
    # print(en_session.get_raw_page(page=page,correct_lvl=False))


if __name__ == '__main__':
    main()
