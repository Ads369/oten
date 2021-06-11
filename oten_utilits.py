#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import asyncio
from aiogram import types as aitype


def cords_dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd


def cords_dd2dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]


def find_coordinate_in_text(str_in):
    # This Pattern develop for BOND game
    PATTERN = re.compile(r"""
    [N]((?:[\+-]?[0-9]*[\.,][0-9]+)|(?:[\+-]?[0-9]+))[°]((?:[\+-]?[0-9]*[\.,][0-9]+)|(?:[\+-]?[0-9]+))[' ]*((?:[\+-]?[0-9]*[\.,][0-9]+)|(?:[\+-]?[0-9]+))["\s]*[E]((?:[\+-]?[0-9]*[\.,][0-9]+)|(?:[\+-]?[0-9]+))[°]((?:[\+-]?[0-9]*[\.,][0-9]+)|(?:[\+-]?[0-9]+))[' ]*((?:[\+-]?[0-9]*[\.,][0-9]+)|(?:[\+-]?[0-9]+))["]
    """, re.VERBOSE)

    values = PATTERN.findall(str_in)

    # print(values)
    return values


def gps_dms2dd():
    print('-')


async def text2gps(str_in, message: aitype.Message):
    gps_list = find_coordinate_in_text(str_in)
    for gps in gps_list:
        latitude = cords_dms2dd(gps[0], gps[1], gps[2], '-')
        longitude = cords_dms2dd(gps[3], gps[4], gps[5], '-')
        await message.answer('{}, {}'.format(latitude, longitude))
        await message.bot.send_location(chat_id=message.chat.id,
                                        longitude=longitude,
                                        latitude=latitude)


def test():
    str = """
        50d4m17.698N 14d24m2.826E
        40:26:46N,79:56:55W
        40:26:46.302N 79:56:55.903W
        49°59'56.948"N, 15°48'22.989"E
        50d4m17.698N 14d24m2.826E
        49.9991522N, 15.8063858E
        N 49° 59.94913', E 15° 48.38315'
        40°26′47″N 79°58′36″W
        40d 26′ 47″ N 79d 58′ 36″ W
        40.446195N 79.948862W
        40,446195° 79,948862°
        40° 26.7717, -79° 56.93172
        40.446195, -79.948862
        53.000000 23.000000
    
        Подойдите к агентам в координатах   
        N58°33' 38.3"   
        E59°13' 54.3"   

        Корды локации:  53.000000 23.000000 () 
    """
    gps_list = find_coordinate_in_text(str)
    for gps in gps_list:
        latitude = cords_dms2dd(gps[0], gps[1], gps[2], '-')
        longitude = cords_dms2dd(gps[3], gps[4], gps[5], '-')
        print(latitude, longitude)


if __name__ == '__main__':
    test()
