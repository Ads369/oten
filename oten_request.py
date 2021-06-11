#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
from bs4 import BeautifulSoup
from lxml import html, etree
import json
from aiogram import types as aitype
import aiohttp
import asyncio
import cProfile

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
log = logging.getLogger(__name__)


def save_bs_to_file(soup=None, file_path=None):
    """
    Just save BS Soup to file
    :param soup: (BS object) Page of WebSite
    :param file_path: (str) File path
    :return: pass
    """
    if file_path is None:
        file_path = 'materials/temp.html'
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(str(soup.prettify()))
    pass


def get_bs_from_file(file_path=None):
    """
    Get BS page from file
    :param file_path: {str} - File path
    :return: soup {BeautifulSoup} - page for heading
    """
    with open(file_path, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
    return soup


def get_json_from_file(file_path=None):
    """
    Get JSON from file
    :param file_path:
    :return: json data
    """
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


class EnSession(object):
    """
    Class for handling requests from site
    """

    def __init__(self):
        self.session = requests.session()
        self.resp = None
        self.info = ''

        self._domain = None
        self._login = None
        self._password = None

        # self.url = None
        # self.page = None

        self.session.headers.update({
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
            'User-Agent': 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
            'Connection': 'keep-alive'})

    def set_domain(self, domain=None):
        self._domain = domain

    def set_login(self, login=None):
        self._login = login

    def set_password(self, password=None):
        self._password = password

    def set_setting(self, domain=None, login=None, password=None):
        if domain is not None:
            self._domain = domain
        if login is not None:
            self._login = login
        if password is not None:
            self._password = password

    def _request_wrapper(self, resp=None):
        """Wraps Requests for handling known exceptions."""
        if resp is not None:
            if 'login.aspx' in resp.url:
                log.info('Need to log in {}'.format(resp.url))
                return False
            elif 200 <= resp.status_code <= 299:
                # self.resp = resp
                return resp
            else:
                log.info('Failed to load the page')
                return False
        else:
            return False

    def get(self, url=None):
        """
        Main function for GET 
        :param url: (str) Url for request
        :return: (resp) The response from the request
        """
        resp = self.session.get(url)
        resp.encoding = 'utf-8'
        return self._request_wrapper(resp)

    def post(self, url=None, data=None):
        """
        Main function for POST request
        :param data: (dict) (optional) of data for post request
        :param url: (str) Url for request
        :return: (resp) The response from the request
        """
        resp = self.session.post(url=url, data=data)
        return self._request_wrapper(resp)

    def get_json(self, url=None):
        """
        This function focus to get json from Encounter
        :param url:
        :return: Json structure
        """
        resp = self.get(url)
        if resp:
            self.resp = resp
            try:
                result_json = json.loads(self.resp.text)
            except ValueError:
                result_json = {}
        else:
            result_json = {}
        return result_json

    def get_json_resp(self, url=None):
        """
        This function focus to get json from Encounter
        :param url:
        :return: Json structure
        """
        try:
            result_json = json.loads(self.resp.text)
        except ValueError as value_error:
            result_json = {}
        except AttributeError as attribute_error:
            result_json = {}
        return result_json

    def get_html_resp(self):
        parser = html.HTMLParser(encoding='utf-8')
        page = html.fromstring(self.resp.content, parser=parser)
        return page

    def resp_to_file(self, file_path=None):
        """
        JUST Save the resulting page to file
        :param file_path: (str) File path
        :return: None
        """
        if file_path is None:
            file_path = 'materials/temp.html'
        with open(file_path, 'w') as file:
            file.write(self.resp.text)
        pass

    def get_page_to_file(self, url='http://72.en.cx', file_path=None):
        """
        Send request and Save the resulting page to file
        :param url: (str) Link
        :param file_path: (str) File path for save page
        :return: pass
        """
        resp = self.get(url)
        with open(file_path, 'w') as file:
            file.write(resp.text)
        pass

    def get_json_to_file(self, url, file_path=None):
        """
        Send request and Save the resulting page to file
        :param url: (str) Link
        :param file_path: (str) File path for save page
        :return: pass
        """
        data = self.get_json(url)
        with open(file_path, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True, ensure_ascii=False)

    def get_bs(self, url='http://72.en.cx'):
        """
        Get BS page from the url
        :param url: (str) Url for request
        :return: (BS object) Soup
        """
        resp = self.get(url)
        soup = BeautifulSoup(resp.content, "html.parser")
        return soup

    def check_login(self, domain='72'):
        url = 'http://{0}.en.cx/UserDetails.aspx'.format(domain)
        resp = self.session.get(url)
        if resp.url == url:
            return True
        else:
            return False

    def login_en(self, domain=None, login=None, password=None):
        """
        Method login on encounter website
        """
        if domain is None:
            domain = self._domain
        else:
            self._domain = domain

        if login is None:
            login = self._login
        else:
            self._login = login

        if password is None:
            password = self._password
        else:
            self._password = password

        if domain is None or login is None or password is None:
            msg = 'login_en -> Bad args for login'
            log.error(msg)
            self.info = msg
            return False
        else:
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
                msg = 'login_en -> LogIN'
                log.info(msg)
                self.info = msg
                return True
            else:
                msg = 'login_en -> LogOUT'
                log.info(msg)
                self.info = msg
                # log.info(resp.url)
                return False

    def send_answer(self, url, data):
        """
        This function focus to get json from Encounter
        :param url:
        :return: Json structure
        """
        resp = self.post(url, data)
        if resp:
            self.resp = resp
            try:
                result_json = json.loads(self.resp.text)
            except ValueError:
                result_json = {}
        else:
            result_json = {}
        return result_json

def main():
    en_ws = EnSession()
    # en_ws.set_login = 'forcabarca'
    # en_ws.set_password = 'otwinteam1'
    en_ws.login_en(domain='demo', login='forcabarca', password='otwinteam1')
    page = en_ws.get_json(url='http://demo.en.cx/gameengines/encounter/play/31224/?json=1')
    print(page)


if __name__ == '__main__':
    main()
