#!/usr/bin/env python
# coding: utf-8
from typing import List, Any

import lxml
import re
import math
import requests as req
from bs4 import BeautifulSoup


"""
{teamname:
    { 
        id: int
        current_lvl: int
        current_lvl_name: str
        position: int
        position_bonus: int
        time: str
        time_lag: str 
        bonus_time: str
    }
}
"""

class StatisticsMonitor:

    def __init__(self,
                 url=None,
                 file=None,
                 page=None):
        self.url = url
        self.file = file
        self.page = page
        self.teams_stats = {}
        self.online = False
        self.error_log = []

    def get_error_logs(self):
        """
        Return all errors which happened to web-parsing
        :return: String
        """
        result = '\n'.join(self.error_logs)
        self.error_logs.clear()
        return result

    @staticmethod
    def lvl_num(obj):
        """Исправляет неправельный подсчет уровней"""
        lvl = len(obj) - 2
        return lvl

    def set_game(self, str_in):
        """Choose it's online or offline monitoring mode"""
        if 'en.cx' in str_in:
            self.url = str_in
            self.online = True
        else:
            self.file = str_in
            self.online = False

    def load_page_file(self):
        if self.file is None:
            print('Файл пустой')
            return None

        with open(self.file, 'r', encoding='utf-8') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')
            print(soup.find("a", id="lnkGameName").text)
            self.page = soup

    def load_page(self):
        if self.online:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/53.0.2785.89 '
                              'Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
            }
            resp = req.get(self.url, headers=headers)
            self.page = BeautifulSoup(resp.text, 'lxml')
        else:
            self.load_page_file()
            if self.page is not None:
                return True
            else:
                False

    def add_team(self, string):
        """Add team with id"""
        value = string.split(':')
        dict_team = {
                    'id': value[1],
                    'current_lvl': 0,
                    'current_lvl_name': '',
                    'position': 0,
                    'position_bonus': 0,
                    'time': '',
                    'time_lag': '',
                    'bonus_time': '',
                    'penalty_time': ''
        }
        return self.teams_stats.update({value[0]: dict_team})

    def show_teams(self):
        """show list teams with id"""
        return self.teams_stats

    def return_stats_teams(self, team_name, team_checkpoints, levels_text):
        """
        Method for visualisation statistic of team

        :param team_name:
        :param team_checkpoints:
        :param levels_text:
        :return: str: {0} - {1} ({2}/{3}): 0 - Team name
                                           1 - Current Level name
                                           2 - Current Level number
                                           3 - Total levels number
        """
        return '{0} - {1} ({2}/{3})'.format(team_name,  # Team name
                                            levels_text[self.lvl_num(team_checkpoints)],  # Current Level name
                                            self.lvl_num(team_checkpoints),  # Current Level number
                                            len(levels_text) - 4  # Total levels number
                                            )

    def stats_for_team(self, team_name, team_id):

        # Find stats table
        table = self.page.find("table", id="GameStatObject_DataTable")

        # Find all levels and them name
        levels_tr = table.find("tr", {"class": "levelsRow"})
        levels_text = [e.text for e in levels_tr.children if e.name is not None]

        # Find Checkpoint of team
        class_id_for_team = 'id{0}'.format(team_id)
        team_checkpoints = table.findAll("td", {"class": class_id_for_team})

        result = []

        if self.online:
            # If it's online mode just return statistic
            return self.return_stats_teams(team_name, team_checkpoints, levels_text)
        else:
            # If Offline mode need to filter checkpoints by "display:none"
            team_checkpoints_display = []
            for e in team_checkpoints:
                test = e.find("div", {"style": "display: none;"})
                if test is None:
                    team_checkpoints_display.append(e)
            return self.return_stats_teams(team_name, team_checkpoints_display, levels_text)

    def show_stats(self):
        """
        Main function for take stats
        :return:
        """
        self.load_page()
        if self.page is None:
            return "Пустая страница"

        if len(self.teams_stats) < 1:
            return "Команды для мониторинга отсутствуют"

        result = []
        for key, value in self.teams_stats.items():
            result.append(self.stats_for_team(key, value))
        return '\n'.join(result)

    def show_position_teams(self):
        table = self.page.find("table", id="GameStatObject_DataTable")

        levels_tr = table.find("tr", {"class": "levelsRow"})
        total = table.findAll("td", {"class": "totalCell"})

        team_list = []
        time_list = []

        for key, value in self.teams_stats.items():
            # Search cell for team
            class_select_team = 'totalCell id{0}'.format(value)
            total_select_team = table.findAll("td", {"class": class_select_team})

            # Search position in result table
            finish_position = math.ceil((total.index(total_select_team[0]) + 1) / 2)
            finish_position_with_bonus = math.ceil((total.index(total_select_team[1]) + 1) / 2)
            team_list.append('{0} - {1}|{2}'.format(key, finish_position, finish_position_with_bonus))

            # Search time lag
            cell_text = total_select_team[0].get_text(' ')
            time = self.take_int_from_string(cell_text)
            time_list.append(time)

        result = []
        index = 0
        for item in time_list:
            # If there is not bonus
            if len(item) > 1:
                item.append(0)

            if index == 0:
                result.append("{0}\t Time:{1}, Bonus: {2}".format(team_list[index],
                                                             self.second_to_string(item[0]),
                                                             self.second_to_string(item[1]))
                              )
            else:
                lag = (item[0] - time_list[index - 1][0])
                result.append("{0}\t Time:{1} (+{3}), Bonus: {2}".format(team_list[index],
                                                                   self.second_to_string(item[0]),
                                                                   self.second_to_string(item[1]),
                                                                   self.second_to_string(lag))
                              )
            index += 1

        return '\n'.join(result)

    def show_time_lags(self):
        table = self.page.find("table", id="GameStatObject_DataTable")

        levels_tr = table.find("tr", {"class": "levelsRow"})
        total = table.findAll("td", {"class": "totalCell"})

        time_list = []

        for key, value in self.teams_stats.items():
            class_select_team = 'totalCell id{0}'.format(value)
            total_select_team = table.findAll("td", {"class": class_select_team})

            cell_text = total_select_team[0].get_text(' ')
            time = self.take_int_from_string(cell_text)
            time_list.append(time)

        index = 0
        result = []
        for item in time_list:
            index += 1
            if index == 1:
                result.append("{0}, Bonus: {1}".format(self.second_to_string(item[0]),
                                                       self.second_to_string(item[1]))
                              )
            else:
                lag = (item[0] - time_list[index - 2][0])
                result.append("{0} ({2}), Bonus: {1}".format(self.second_to_string(item[0]),
                                                             self.second_to_string(item[1]),
                                                             self.second_to_string(lag))
                              )

        return result

    def take_stats(self, page=None):
        if page is not None:
            # Find stats table
            table = self.page.find("table", id="GameStatObject_DataTable")

            # Find all levels, them name and count
            levels_tr = table.find("tr", {"class": "levelsRow"})
            levels_text: List[Any] = [e.text for e in levels_tr.children if e.name is not None]
            count_level = len(levels_text)

            # Find finish cells
            total = table.findAll("td", {"class": "totalCell"})

            team_list = []
            time_list = []

            # Block for each Teams
            teams_list = self.teams_stats.keys()
            for team in teams_list:
                team_id = self.teams_stats[team]['id']

                # This block search current level

                # Find Checkpoint of team
                class_id_for_team = 'id{0}'.format(team_id)
                team_checkpoints = table.findAll("td", {"class": class_id_for_team})


                # Various methods for offline and online mode
                if self.online:
                    # If it's online mode just return statistic

                    self.teams_stats[team]['current_lvl'] = self.lvl_num(team_checkpoints)
                    self.teams_stats[team]['current_lvl_name'] = levels_text[self.teams_stats[team]['current_lvl']]

                else:
                    # If Offline mode need to filter checkpoints by "display:none"
                    team_checkpoints_display = []
                    for e in team_checkpoints:
                        test = e.find("div", {"style": "display: none;"})
                        if test is None:
                            team_checkpoints_display.append(e)

                    self.teams_stats[team]['current_lvl'] = self.lvl_num(team_checkpoints_display)
                    self.teams_stats[team]['current_lvl_name'] = levels_text[self.teams_stats[team]['current_lvl']]

                # This block search total time

                # create a class for html search
                class_select_team = 'totalCell id{0}'.format(team_id)
                # Find all TOTAL cell for team: [0] - without bonus [1] - with bonus
                total_select_team = table.findAll("td", {"class": class_select_team})

                # Find position in result table
                # Used some method for count a position in total table
                self.teams_stats[team]['position'] = math.ceil((total.index(total_select_team[0]) + 1) / 2)
                self.teams_stats[team]['position_bonus'] = math.ceil((total.index(total_select_team[1]) + 1) / 2)

                # Search time
                # Get text in found cell of team
                cell_text = total_select_team[0].get_text(' ')
                print(cell_text)

                # Get array: [0] - time [1] - bonus (if there is)
                time = self.take_int_from_string(team, cell_text)

                # Add time for select team in totaly
                # time_list.append(time)

                

            result = []
            return True
        else:
            self.error_log.append('Пустая страница для статистики')
            return None




    @staticmethod
    def string_to_second(d=0, h=0, m=0, s=0):
        """
        Convert time to coun seconds
        :param d:
        :param h:
        :param m:
        :param s:
        :return: int: count seconds
        """
        d = int(d)
        h = int(h)
        m = int(m)
        s = int(s)
        result_seconds = (((((d * 24) + h) * 60) + m) * 60) + s
        return int(result_seconds)

    @staticmethod
    def second_to_string(seconds=None, granularity=2):
        intervals = (
            # ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('days', 86400),  # 60 * 60 * 24
            ('hours', 3600),  # 60 * 60
            ('minutes', 60),
            ('seconds', 1),
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

    @staticmethod
    def take_digital_by_string(instr):
        print(instr)
        # Time
        d, h, m, s = '0', '0', '0', '0'

        match = re.search(r'\d+\sд', instr)
        if match:
            d = match.group(0)[:-2]

        match = re.search(r'\d+\sч', instr)
        if match:
             h = match.group(0)[:-2]

        match = re.search(r'\d+\sм', instr)
        if match:
            m = match.group(0)[:-2]

        match = re.search(r'\d+\sc', instr)
        if match:
            s = match.group(0)[:-2]

        return d, h, m, s

    def take_int_from_string(self, team, instr):
        """
        Search time in input string and convert it to count sec
        If there is bonus return array of time (second) and bonus (second)

        :param team:
        :param instr:
        :return: tuple: [0] - time in second
                        [1] - bonus in second
        """

        index_of_bracket = instr.index(')')
        d, h, m, s = self.take_digital_by_string(instr[:index_of_bracket])
        time = StatisticsMonitor.string_to_second(d=d, h=h, m=m, s=s)
        self.teams_stats[team]['time'] = self.second_to_string(time)

        if 'бонус' in instr:
            d, h, m, s = self.take_digital_by_string(instr[index_of_bracket:])
            time = StatisticsMonitor.string_to_second(d=d, h=h, m=m, s=s)
            self.teams_stats[team]['bonus_time'] = self.second_to_string(time)

        if 'штраф' in instr:
            d, h, m, s = self.take_digital_by_string(instr[index_of_bracket:])
            time = StatisticsMonitor.string_to_second(d=d, h=h, m=m, s=s)
            self.teams_stats[team]['penalty_time'] = self.second_to_string(time)

        return True


def set_preset(obj, i=0):
    if i == 1:
        obj.set_game(r'offline site\Статистика игры о-10 д-9 м-8 (278).html')
        obj.add_team("О.Т. Win Team:146267")
        obj.add_team("MARS`o`HOT:10301")
        obj.add_team("ДИВ:117667")
    if i == 2:
        obj.set_game('http://demo.en.cx/GameStat.aspx?type=own&gid=30415')
        obj.add_team("Test:158204")
    if i == 3:
        # obj.set_game(r'offline site\Статистика игры о-10 д-9 м-8 (278).html')
        obj.add_team("О.Т. Win Team:146267")
        obj.add_team("MARS`o`HOT:10301")
        obj.add_team("ДИВ:117667")
        obj.add_team("TopChi:33464")
        obj.add_team("RG:4393")
        obj.add_team("BM:173249")
    if i == 4:
        obj.set_game(r'http://72.en.cx/GameStat.aspx?type=own&gid=69489')
        obj.add_team("О.Т. Win Team:146267")
        obj.add_team("ДИВ:117667")


def main():
    o1 = StatisticsMonitor()
    set_preset(o1, 4)
    o1.load_page()
    result = o1.show_teams()
    print(result)
    result_stats = o1.take_stats(o1.page)
    if result_stats is not None:
        result = o1.show_teams()
        print(result)
    else:
        print(o1.get_error_logs())


if __name__ == '__main__':
    main()