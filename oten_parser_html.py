#!/usr/bin/env python
# -*- coding: utf-8 -*-

import html2text
from html2text import HTML2Text
from bs4 import BeautifulSoup as bs
from markdownify import markdownify as md
import re
import asyncio


def text_handler(str_in):
    """
    This function accept input html code,
    parse all attachments from it,
    and convert to markdown text
    :param message:
    :param str_in: html code
    :return: list of construction:
    """


    # Convert html to Markdown text
    parser = HTML2Text()
    parser.ignore_anchors = True
    parser.body_width = 0
    markdown_txt = parser.handle(str_in)

    # Fix multi NEWLINE
    markdown_txt = re.sub(r'(\s+\n){3,}', '\n\n', markdown_txt)

    # Find all some link
    attachments_list = re.findall(r'src=\"(http.*?)\"|href=\"(http.*?)\"', str_in)
    attachments_set = set()
    for attachment in attachments_list:
        attachments_set.update(attachment)
    print(attachments_set)

    gps = re.findall("""([SNsn][\s]*)?((?:[\+-]?[0-9]*[\.,][0-9]+)|(?:[\+-]?[0-9]+))(?:(?:[^ms'′"″,\.\dNEWnew]?)|(?:[^ms'′"″,\.\dNEWnew]+((?:[\+-]?[0-9]*[\.,][0-9]+)|(?:[\+-]?[0-9]+))(?:(?:[^ds°"″,\.\dNEWnew]?)|(?:[^ds°"″,\.\dNEWnew]+((?:[\+-]?[0-9]*[\.,][0-9]+)|(?:[\+-]?[0-9]+))[^dm°'′,\.\dNEWnew]*))))([SNsn]?)[^\dSNsnEWew]+([EWew][\s]*)?((?:[\+-]?[0-9]*[\.,][0-9]+)|(?:[\+-]?[0-9]+))(?:(?:[^ms'′"″,\.\dNEWnew]?)|(?:[^ms'′"″,\.\dNEWnew]+((?:[\+-]?[0-9]*[\.,][0-9]+)|(?:[\+-]?[0-9]+))(?:(?:[^ds°"″,\.\dNEWnew]?)|(?:[^ds°"″,\.\dNEWnew]+((?:[\+-]?[0-9]*[\.,][0-9]+)|(?:[\+-]?[0-9]+))[^dm°'′,\.\dNEWnew]*))))([EWew]?)\s*?"""
                     , markdown_txt)
    print(gps)


    # <(\w*)[^<]*?src.*?>

    # Handler images in MarkDown (remove '!' before link)
    # Handler nested URL
    nested_url = re.findall(r'(\[(!?\[([^\[\]\(\)]*?)\]\((.*?)\))\]\((.*?)\))', markdown_txt)
    print(nested_url)
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

    # print(markdown_txt)

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
    # try:
    #     await message.bot.send_message(chat_id=message.chat.id,
    #                                    text=markdown_txt,
    #                                    parse_mode='markdown',
    #                                    disable_web_page_preview=True)
    # except BaseException as e:
    #     await message.bot.send_message(chat_id=message.chat.id,
    #                                    text=markdown_txt,
    #                                    disable_web_page_preview=True)

    for attachment in attachments_set:
        if attachment:
            attach_url = attachment.strip()
            attach_name = attach_url[attach_url.rfind('/') + 1:]
            attach_msg = '[{}]({})'.format(attach_name, attach_url)
            print(attach_msg)
        # try:
        #     await message.bot.send_message(chat_id=message.chat.id,
        #                                    text=attach_msg,
        #                                    parse_mode='markdown')
        # except BaseException as e:
        #     await message.bot.send_message(chat_id=message.chat.id,
        #                                    text=attach_url)



if __name__ == '__main__':
    str_in = "\u003chr\u003e\u003cblockquote\u003e Текст цитаты \u003c/blockquote\u003e\u003chr\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\u003cspan id=\"LevelsScenarioRepeater_ctl00_LevelTasksRepeater_ctl00_lblLevelTask\" class=\"white\"\u003eПостройте из того, что есть в Пакете №22 (в «Наборе разведчика»)\r\u003cbr/\u003e\r\u003cbr/\u003e- то, что нарисовано на схеме в задании:\r\u003cbr/\u003e\u003ca href=\"http://dekormyhome.ru/wp-content/uploads/2019/07/46e19f43fdcfe8ea9f5522f021e5ab0b.jpg\"\u003e\u003cimg src=\"http://dekormyhome.ru/wp-content/uploads/2019/07/46e19f43fdcfe8ea9f5522f021e5ab0b.jpg\" border=\"0\"\u003e\u003c/a\u003e\r\u003cbr/\u003e\r\u003cbr/\u003eПодойдите к агентам в координатах \r\u003cbr/\u003e\u003cfont color=\"gold\"\u003eN58°33\u0027 38.3\" \r\u003cbr/\u003eE59°13\u0027 54.3\"\u003c/font\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\u003cp style=\u0027text-align: justify\u0027\u003e\u003cspan style=\u0027color: #FF9933\u0027\u003e\u003cb\u003eНазвание\u003c/b\u003e\u003c/span\u003e\r\u003cbr/\u003e\u003cvideo width=\u0027640\u0027 height=\u0027360\u0027 src=\"https://youtu.be/L_LUpnjgPso\" controls autobuffer\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\u003cp\u003eЕсли видео не воспроизводится, скачайте его по ссылке: \u003ca href=\"https://youtu.be/L_LUpnjgPso\"\u003eDownload\u003c/a\u003e (РАЗМЕР Mb)\u003c/p\u003e \u003c/video\u003e\u003c/p\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\u003ciframe width=\"560\" height=\"315\" src=\"https://www.youtube.com/embed/JTjTyU_DC4k\" title=\"YouTube video player\" frameborder=\"0\" allow=\"accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen\u003e\u003c/iframe\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\u003caudio controls\u003e\u003csource src=\u0027http://d2.endata.cx/data/games/31242/%D0%95%D0%93%D0%9E%D0%A032%D0%A8%D0%98%D0%9F32-32Dior.mp3\u0027 type=\u0027audio/mp3\u0027\u003e\r\u003cbr/\u003eТег audio не поддерживается вашим браузером. \u003ca href=\u0027http://d2.endata.cx/data/games/31242/%D0%95%D0%93%D0%9E%D0%A032%D0%A8%D0%98%D0%9F32-32Dior.mp3\u0027\u003eСкачайте музыку\u003c/a\u003e\u003c/audio\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\u003ca href=\"geo:53.000000, 23.000000;\"\u003e53.000000 23.000000\u003c/a\u003e\r\u003cbr/\u003e\r\u003cbr/\u003eПоразите цель трижды. Получите код у агента. Подсказок не будет.\r\u003cbr/\u003e\r\u003cbr/\u003e\u003cb\u003eФормат ответа:\u003c/b\u003e Код. \r\u003cbr/\u003e\r\u003cbr/\u003e\u003cb\u003eВнимание опасность:\u003c/b\u003e Беречь глаза. Осторожно переходите дорогу.\r\u003cbr/\u003e\r\u003cbr/\u003e\u003cb\u003eАгент:\u003c/b\u003e Рядом с вами.\r\u003cbr/\u003e\r\u003cbr/\u003e\u003cb\u003eПримечания:\u003c/b\u003e \r\u003cbr/\u003eНичего не выбрасывать, все нужно далее!\u003c/span\u003e"
    text_handler(str_in)