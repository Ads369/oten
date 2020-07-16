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


def get_short_information_msg(data=None):
    """ Get short and beautiful info about level"""
    if data is not None:
        info = get_short_info_game(data)

        result = "Уровень {0} из {1}: {2}\n" \
                 "⏳:{3}\n" \
                 "----------------------------------------------\n" \
                 "🔑:{4} | ✅ ‍:{5} | ☑️:{6}\n" \
                 "🎁:{7} | ✅ ‍:{8} | ☑️:{9}\n" \
                 "----------------------------------------------\n" \
                 "Подсказки{10}{11}".format(info['lvl_num'],
                                            info['lvl_sum'],
                                            info['lvl_nam'],
                                            info['time_out_str'],
                                            info['sec_sum'],
                                            info['sec_done'],
                                            info['sec_left'],
                                            info['bonus_sum'],
                                            info['bonus_done'],
                                            info['bonus_left'],
                                            info['hint_str'],
                                            info['messages']
                                            )
        return result
    else:
        return "Уровень не загружен"


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

        # Get short information for header message
        text_level = get_short_information_msg(data)

        # Format Message about select level
        text_level += '\n----------------------------------------------\n' \
                      'Задание:\n{0}'.format(text)
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

    # Convert info about HINTs from json to string
    hint_info_msg = ':\n'
    for hint in hint_list:
        if hint['RemainSeconds'] == 0:
            hint_info_msg += '📥 Подсказка {0}\n'.format(hint['Number'])
        else:
            hint_info_msg += '⏳ Подсказка {0} через {1}\n'.format(hint['Number'],
                                                                  second_to_string(hint['RemainSeconds']))

    # Convert info about PENT_HINTS from json to string
    pen_hint_list = data['Level']['PenaltyHelps']
    for hint in pen_hint_list:
        hint_info_msg += '💲 Подсказка {0} штраф {1}\n'.format(hint['Number'], second_to_string(hint['Penalty']))

    msgs_list = data['Level']['Messages']

    if msgs_list:
        msgs_list_list = list(msg['MessageText'] for msg in msgs_list)
        msgs_list_text = '\n'.join(msgs_list_list)
        msgs_list_text = '\nСообщение от авторов:\n' + msgs_list_text
    else:
        msgs_list_text = ''

    # Formatting for good look results
    if hint_info_msg == ':\n':
        hint_info_msg = ' отсутствуют\n'

    short_info = {'lvl_num': data['Level']['Number'],
                  'lvl_sum': len(data['Levels']),
                  'lvl_nam': data['Level']['Name'],
                  'time_out': data['Level']['Timeout'],
                  'time_out_str': second_to_string(data['Level']['Timeout']),
                  'sec_sum': len(data['Level']['Sectors']),
                  'sec_done': data['Level']['PassedSectorsCount'],
                  'sec_left': data['Level']['SectorsLeftToClose'],
                  'bonus_sum': len(data['Level']['Bonuses']),
                  'bonus_done': len(bonus_done),
                  'bonus_left': len(bonus_left),
                  'hint_sum': len(data['Level']['Helps']),
                  'hint_done': len(hint_done),
                  'hint_left': len(hint_left),
                  'hint_str': hint_info_msg,
                  'pen_hint_sum': len(data['Level']['PenaltyHelps']),
                  'messages': msgs_list_text
                  }
    return short_info


def get_bonus_list(data):
    bonuses = data['Level']['Bonuses']
    closed_bonuses_names = [i['Name'] for i in bonuses if i['IsAnswered']]
    not_closed_bonuses_names = [i['Name'] for i in bonuses if not i['IsAnswered']]

    result_str = 'Бонусы:\n✅:{0}\n{1}\n———————————\n☑️:{2}\n{3}'.format(str(len(closed_bonuses_names)),
                                                                        '\n'.join(closed_bonuses_names),
                                                                        str(len(not_closed_bonuses_names)),
                                                                        '\n'.join(not_closed_bonuses_names))

    return result_str


def get_sector_list(data):
    bonuses = data['Level']['Sectors']
    closed_bonuses_names = [i['Name'] for i in bonuses if i['IsAnswered']]
    not_closed_bonuses_names = [i['Name'] for i in bonuses if not i['IsAnswered']]

    result_str = 'Сектора:\n✅:{0}\n{1}\n———————————\n☑️:{2}\n{3}'.format(str(len(closed_bonuses_names)),
                                                                         '\n'.join(closed_bonuses_names),
                                                                         str(len(not_closed_bonuses_names)),
                                                                         '\n'.join(not_closed_bonuses_names))

    return result_str


def second_to_string(seconds=None, granularity=2):
    """ Convert string of second to normal string"""
    if seconds > 0:
        intervals = (
            # ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('д', 86400),  # 60 * 60 * 24
            ('ч', 3600),  # 60 * 60
            ('м', 60),
            ('с', 1),
        )
        result = []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{}{}".format(value, name[:1]))
        return ' '.join(result[:granularity])
    else:
        return '0'


def is_old_answer(data, answer=None):
    answer_list = data['Level']['MixedActions']
    correct_answer_list = list(answ for answ in answer_list if answ['Answer'] == answer and answ['IsCorrect'])
    if len(correct_answer_list) > 0:
        return True
    else:
        return False


def check_answer(data, answer=None, is_old_answer=False):
    """
    Take information about correct answer
    :param answer:
    :param data: json
    :return: string: msg of string for TG
    """
    answer_list = data['Level']['MixedActions']

    # res = next((answ for answ in answer_list if answ['Answer'] == answer), None)
    # if res['IsCorrect']:
    # Get last answer in history

    if is_old_answer:
        return '🔄 код _{0}_ уже был\n'.format(answer)
    else:

        # Try get list correct answer
        correct_answer_list = list(answ for answ in answer_list if answ['Answer'] == answer and answ['IsCorrect'])

        if len(correct_answer_list) > 0:
            result_msg = '✅ код _{0}_ верный\n———————————\n'.format(answer)

            # Try get sectors was closing this answer
            sectors_list = data['Level']['Sectors']
            sectors_done = list(sector['Name'] for sector in sectors_list if sector['IsAnswered'] and
                                sector['Answer']['Answer'] == answer)

            # If answer closed sectors
            if len(sectors_done) > 0:
                result_msg += 'Сектор(а):\n'
                result_msg += '\n'.join(sectors_done) + '\n'

            # Try get bonuses was closing this answer
            bonuses_list = data['Level']['Bonuses']
            bonus_strings = ''
            for bonus in bonuses_list:

                # If answer closed bonuses
                if bonus['IsAnswered'] and bonus['Answer']['Answer'] == answer:
                    # Check:  has bonus helps
                    if bonus['Help'] is not None:
                        bonus_help = '📬'
                    else:
                        bonus_help = ''

                    # Add bonus to result
                    bonus_strings += '{0} ({1}){2}\n'.format(bonus['Name'], second_to_string(bonus['AwardTime']),
                                                             bonus_help)

            # If answer closed sectors
            if bonus_strings != '':
                result_msg += 'Бонус(ы):\n' + bonus_strings

            # Add block about left codes on lvl
            info = get_short_info_game(data)
            result_msg += "———————————\n" \
                          "🔑:{0} | ✅ ‍:{1} | ☑️:{2}\n" \
                          "🎁:{3} | ✅ ‍:{4} | ☑️:{5}\n".format(info['sec_sum'],
                                                               info['sec_done'],
                                                               info['sec_left'],
                                                               info['bonus_sum'],
                                                               info['bonus_done'],
                                                               info['bonus_left'],
                                                               )

            return result_msg

        else:
            return '❌ код _{0}_ неверный'.format(answer)


# test block


def main():
    data = load_json_from_file()
    msg = get_level_task(data)
    return msg


def local_test():
    data = load_json_from_file("data_file.json")
    # get_short_info_game(data)
    # msg = check_answer(data, '123')
    msg = get_short_information_msg(data)
    msg = get_sector_list(data)
    print(msg)


if __name__ == '__main__':
    local_test()
