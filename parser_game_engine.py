#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import re
from bs4 import BeautifulSoup


def load_json_from_file(file_path):
    with open(file_path, encoding="utf8") as json_file:
        data = json.load(json_file)
    return data


def handling_attachments(html_block):
    result = []

    # Convert to soup
    soup = BeautifulSoup(html_block, 'lxml')

    # Find all IMG
    imgs = soup.findAll('img')
    for each in imgs:
        # Add imgs to result
        result.append(each['src'])

        # Get name file from URL
        name_file_pos = each['src'].rfind('/') + 1
        name_file = each['src'][name_file_pos:]

        # Replace tags for MarkDown
        each.replace_with('[{0}]({1})'.format(name_file, each['src']))

    # Replace A(href) tags for MarkDown format
    for a in soup.find_all('a', href=True, text=True):
        a.string.replace_with('[{0}]({1})'.format(a.string, a['href']))

    """
    # Заготовка под корды
    # strings = soup.find_all(string=re.compile('BSD'))
    # ([\d]+\.[\d]{4,}[\D\W]{0,3}[\d]+\.[\d]{4,})
    cords = re.findall(r'([\d]+\.[\d]{4,}[\D\W]{0,3}[\d]+\.[\d]{4,})', task)
    for each in cords:
        result.append(each)
    """

    # Take text from html by BS
    text = soup.text

    return text, result


def get_level_task(data):
    """
    Take main level information
    :param data: json
    :return: array: array of string for TG
    """
    result = []

    # Check events by EN engine
    # Event=0 - Game play (all good)
    if data['Event'] == 0:

        # Take TaskText from json and parse it BS
        task = data['Level']['Tasks'][0]['TaskText']
        text, attachments = handling_attachments(task)

        result.extend(attachments)

        # Format Message about select level
        text_level = 'Уровень: {0}({1}/{2})\n' \
                     'Секторов: {4}({3})\n' \
                     'АвтоПереход через {5}\n' \
                     'Подсказки: {6}\n' \
                     'Бонусы: {7}\n\n' \
                     'Задание:\n{8}'.format(data['Level']['Name'],  # Название уровня
                                            data['Level']['Number'],  # Номер уровня
                                            len(data['Levels']),  # Количество уровней в игре
                                            data['Level']['RequiredSectorsCount'],
                                            # Кол-во секторов необходимых для закрытия
                                            len(data['Level']['Sectors']),  # Всего секторов
                                            data['Level']['Timeout'],  # ? автопереход
                                            len(data['Level']['Helps']),  # Количество подсказок
                                            len(data['Level']['Bonuses']),  # Количество подсказок
                                            text
                                            )
        result.insert(0, text_level)

    # Event 5 - game don't start yet
    elif data['Event'] == 5:
        result.append('Игра начнется через ...')

    # Event 6 - game over already
    elif data['Event'] == 6:
        result.append('Игра уже закончилась')

    # Event 6 - WTF admin! =)
    elif data['Event'] == 5:
        result.append('Администратор игры всё ещё не допустил вас к игре, вы не можете принимать в ней участие')

    return result


def get_level_helps(data):
    """
    Take level helps
    :param data: json
    :return: array: array of string for TG
    """
    result = []

    helps_array = data['Level']['Helps']

    for help in helps_array:
        # Take TaskText from json and parse it BS
        help_text = help['HelpText']

    return result


def check_change_level(old_data, new_data):
    is_changed = False
    result = []

    if old_data['Level']['Number'] != new_data['Level']['Number']:
        is_changed = True
        result.append(get_level_task(new_data))
        return is_changed, result

    if old_data['Level']['Helps'] != new_data['Level']['Helps']:
        is_changed = True

    return None


def get_level_gps(data):
    task = data['Level']['Tasks'][0]['TaskText']
    result = []
    cords = re.findall(r'([\d]+\.[\d]{4,}[\D\W]{0,2}[\s][\d]+\.[\d]{4,})', task)
    if cords:
        for each in cords:
            cord = re.sub(r'[^0-9.\s]+', r'', each)
            result.append(cord)
        return result
    else:
        None


def get_short_info_game(data):
    """
    Handler data and return only important information
    :param data:
    :return:  'lvl_num':
              'lvl_sum':
              'lvl_nam':
              'time_out':
              'sec_sum':
              'sec_done':
              'sec_left':
              'bonus_sum':
              'bonus_done':
              'bonus_left':
              'hint_sum':
              'hint_done':
              'hint_left':
              'pen_hint_sum':
              'messages':
    """
    bonus_list = data['Level']['Bonuses']
    bonus_done = list(bonus['BonusId'] for bonus in bonus_list if bonus['IsAnswered'])
    bonus_left = list(bonus['BonusId'] for bonus in bonus_list if not bonus['IsAnswered'])

    hint_list = data['Level']['Helps']
    hint_done = list(hint['HelpId'] for hint in hint_list if hint['HelpText'] is not None)
    hint_left = list(hint['RemainSeconds'] for hint in hint_list if hint['HelpText'] is None)

    pen_hint_list = data['Level']['Helps']

    msgs_list = data['Level']['Messages']
    msgs_list_text = list(msg['MessageText'] for msg in msgs_list)

    short_info = {'lvl_num': data['Level']['Number'],
                  'lvl_sum': len(data['Levels']),
                  'lvl_nam': data['Level']['Name'],
                  'time_out': data['Level']['Timeout'],
                  'sec_sum': len(data['Level']['Sectors']),
                  'sec_done': data['Level']['PassedSectorsCount'],
                  'sec_left': data['Level']['SectorsLeftToClose'],
                  'bonus_sum': len(data['Level']['Bonuses']),
                  'bonus_done': len(bonus_done),
                  'bonus_left': len(bonus_left),
                  'hint_sum': len(data['Level']['Helps']),
                  'hint_done': len(hint_done),
                  'hint_left': len(hint_left),
                  'pen_hint_sum': len(data['Level']['PenaltyHelps']),
                  'messages': msgs_list_text
                  }
    return short_info


def check_answer(data, answer=None):
    """
    Take information about correct answer
    :param answer:
    :param data: json
    :return: string: msg of string for TG
    """
    answer_list = data['Level']['MixedActions']


    res = next((answ for answ in answer_list if answ['Answer'] == answer), None)
    if res['IsCorrect']:

        result_msg = '✅ код _{0}_ закрыл:\n'.format(answer)

        sectors_list = data['Level']['Sectors']
        sectors_done = list(sector['Name'] for sector in sectors_list if sector['IsAnswered'] and
                            sector['Answer']['Answer'] == answer)

        if len(sectors_done) > 0:
            result_msg += 'Сектор(а):\n'
            result_msg += '\n'.join(sectors_done)

        bonuses_list = data['Level']['Bonuses']
        bonus_strings = ''
        for bonus in bonuses_list:
            if bonus['IsAnswered'] and bonus['Answer']['Answer'] == answer:
                if bonus['Help'] is not None:
                    bonus_help = '📬'
                else:
                    bonus_help = ''

                bonus_strings += '{0} ({1}){2}\n'.format(bonus['Name'], bonus['AwardTime'], bonus_help)

        if bonus_strings != '':
            result_msg += 'Бонус(ы):\n' + bonus_strings

        return result_msg
    else:
        return '❌ код _{0}_ неверный'.format(answer)


# test block


def main():
    data = load_json_from_file()
    msg = get_level_task(data)
    return msg


def local_test():
    data = load_json_from_file("data_file2.json")
    #get_short_info_game(data)
    msg = check_answer(data, '123')
    print(msg)


if __name__ == '__main__':
    local_test()
