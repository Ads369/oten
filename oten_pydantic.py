# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
import oten_request
import html2text


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))


# class StartTime(BaseModel):
class UnixTime(BaseModel):
    value: float

    class Config:
        alias_generator = to_camel


class Task(BaseModel):
    replace_nl_to_br: int
    task_text: str
    task_text_formatted: str

    class Config:
        alias_generator = to_camel


class Massage(BaseModel):
    owner_id: int
    owner_login: str
    message_id: int
    message_text: str
    wrapped_text: str
    replace_nl_2_br: bool

    class Config:
        alias_generator = to_camel


class MixedActions(BaseModel):
    action_id: int
    level_id: int
    level_number: int
    user_id: int
    kind: int
    login: str
    answer: str
    # answ_form: Optional[int] = None
    enter_date_time: UnixTime
    loc_date_time: Optional[str] = None
    is_correct: bool
    # award: Optional[int] = None
    # loc_award: Optional[int] = None
    penalty: int

    class Config:
        alias_generator = to_camel


class Answer(BaseModel):
    answer: str
    answer_date_time: UnixTime
    login: str
    user_id: int
    loc_date_time: Optional[str] = None

    class Config:
        alias_generator = to_camel


class Sector(BaseModel):
    sector_id: int
    order: int
    name: str
    answer: Optional[Answer] = None
    is_answered: bool

    class Config:
        alias_generator = to_camel


class Hint(BaseModel):
    help_id: int
    number: int
    help_text: Optional[str] = None
    is_penalty: bool
    penalty: int
    penalty_comment: Optional[str] = None
    request_confirm: bool
    penalty_help_state: int
    remain_seconds: int
    penalty_message: Optional[str] = None

    class Config:
        alias_generator = to_camel


class Bonus(BaseModel):
    bonus_id: int
    name: Optional[str] = None
    number: int
    task: Optional[str] = None
    help: Optional[str] = None
    is_answered: int
    expired: bool
    seconds_to_start: int
    seconds_left: int
    award_time: int
    answer: Optional[Answer] = []

    class Config:
        alias_generator = to_camel


class Level(BaseModel):
    level_id: int
    name: str
    number: int
    timeout: int
    timeout_seconds_remain: int
    timeout_award: int
    is_passed: bool
    dismissed: bool
    start_time: UnixTime
    has_answer_block_rule: bool
    block_duration: int
    block_target_id: int
    attemts_number: int
    attemts_period: int
    required_sectors_count: int
    passed_sectors_count: int
    sectors_left_to_close: int
    tasks: List[Task] = []
    mixed_actions: List[MixedActions] = []
    messages: Optional[List[Massage]] = []
    sectors: Optional[List[Sector]] = []
    helps: Optional[List[Hint]] = []
    penalty_helps: Optional[List[Hint]] = []
    bonuses: Optional[List[Bonus]] = []

    class Config:
        alias_generator = to_camel
        # arbitrary_types_allowed = True


class LevelsList(BaseModel):
    level_id: int
    level_number: int
    level_name: str
    dismissed: bool
    is_passed: bool
    task: Optional[str] = None
    level_action: Optional[int] = None

    class Config:
        alias_generator = to_camel


class LevelAction(BaseModel):
    answer: Optional[str] = None
    is_correct_answer: Optional[bool] = None

    class Config:
        alias_generator = to_camel


class BonusAction(BaseModel):
    answer: Optional[str] = None
    is_correct_answer: Optional[bool] = None

    class Config:
        alias_generator = to_camel


class PenaltyAction(BaseModel):
    penalty_id: int
    action_type: int

    class Config:
        alias_generator = to_camel


class EngineAction(BaseModel):
    level_number: int
    level_action: LevelAction
    bonus_action: BonusAction
    penalty_action: PenaltyAction
    game_id: int
    level_id: int

    class Config:
        alias_generator = to_camel


class EngineEN(BaseModel):
    level: Optional[Level]
    levels: Optional[List[LevelsList]]
    game_id: int
    game_type_id: int
    game_zone_id: int
    game_number: int
    game_title: str
    level_sequence: int
    user_id: int
    team_id: Optional[int] = None
    engine_action: EngineAction
    event: int

    class Config:
        alias_generator = to_camel

# Event 5 - До начала игры ....
# Event 6 - Игра окончена или не подана заявка
# Event 9 - Администратор игры всё ещё не допустил вас к игре, вы не можете принимать в ней участие.
empty_data = {
    "Level": None,
    "Levels": [],
    "GameId": 0,
    "GameTypeId": 0,
    "GameZoneId": 0,
    "GameNumber": 0,
    "GameTitle": "_",
    "LevelSequence": 0,
    "UserId": 0,
    "TeamId": None,
    "EngineAction": {
        "LevelNumber": 0,
        "LevelAction": {
            "Answer": None,
            "IsCorrectAnswer": None
        },
        "BonusAction": {
            "Answer": None,
            "IsCorrectAnswer": None
        },
        "PenaltyAction": {
            "PenaltyId": 0,
            "ActionType": 0
        },
        "GameId": 0,
        "LevelId": 0
    },
    "Event": 0
}
empty_data_not = {
   "Level":{
      "LevelId":1326279,
      "Name":"",
      "Number":34,
      "Timeout":432000,
      "TimeoutSecondsRemain":16827,
      "TimeoutAward":0,
      "IsPassed":False,
      "Dismissed":False,
      "StartTime":{
         "Value":63757980000000
      },
      "HasAnswerBlockRule":False,
      "BlockDuration":0,
      "BlockTargetId":1,
      "AttemtsNumber":0,
      "AttemtsPeriod":0,
      "RequiredSectorsCount":3,
      "PassedSectorsCount":0,
      "SectorsLeftToClose":3,
      "Tasks":[
         
      ],
      "MixedActions":[
         {
            "ActionId":198224581,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"газпромбанк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382960417
            },
            "LocDateTime":"04.06 8:56:00",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224580,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"втб",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382954160
            },
            "LocDateTime":"04.06 8:55:54",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224579,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"банк втб",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382952440
            },
            "LocDateTime":"04.06 8:55:52",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224578,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"сбербанк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382948420
            },
            "LocDateTime":"04.06 8:55:48",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224576,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"альфа",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382943630.008
            },
            "LocDateTime":"04.06 8:55:43",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224575,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"альфа-банк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382940770
            },
            "LocDateTime":"04.06 8:55:40",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224574,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"россельхозбанк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382936197.008
            },
            "LocDateTime":"04.06 8:55:36",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224573,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"банк \"открытие\"",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382923570
            },
            "LocDateTime":"04.06 8:55:23",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224572,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"промсвязьбанк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382916573.008
            },
            "LocDateTime":"04.06 8:55:16",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224571,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"совкомбанк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382907397.008
            },
            "LocDateTime":"04.06 8:55:07",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224570,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"росбанк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382900080
            },
            "LocDateTime":"04.06 8:55:00",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224569,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"тинькофф банк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382897313
            },
            "LocDateTime":"04.06 8:54:57",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224568,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"ак барс",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382889973.008
            },
            "LocDateTime":"04.06 8:54:49",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224567,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"ак барс банк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382888457
            },
            "LocDateTime":"04.06 8:54:48",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224566,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"почта",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382885213.008
            },
            "LocDateTime":"04.06 8:54:45",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224565,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"почта банк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382883803
            },
            "LocDateTime":"04.06 8:54:43",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224564,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"русский стандарт",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382879990.008
            },
            "LocDateTime":"04.06 8:54:39",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224563,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"хоум кредит",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382874837.008
            },
            "LocDateTime":"04.06 8:54:34",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224562,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"хоум кредит банк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382873030.008
            },
            "LocDateTime":"04.06 8:54:33",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224561,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"убрир",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382864367.008
            },
            "LocDateTime":"04.06 8:54:24",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224560,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"восточный",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382856080
            },
            "LocDateTime":"04.06 8:54:16",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224559,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"восточный банк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382854573.008
            },
            "LocDateTime":"04.06 8:54:14",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224558,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"ренессанс кредит банк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382849750.008
            },
            "LocDateTime":"04.06 8:54:09",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224557,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"ренессанс кредит",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382847637.008
            },
            "LocDateTime":"04.06 8:54:07",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224556,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"росгосстрах",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382840203
            },
            "LocDateTime":"04.06 8:54:00",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224555,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"росгосстрах банк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382838043
            },
            "LocDateTime":"04.06 8:53:58",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224553,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"отп банк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382830680
            },
            "LocDateTime":"04.06 8:53:50",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224552,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"финсервис",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382817917.008
            },
            "LocDateTime":"04.06 8:53:37",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224551,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"банк финсервис",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382816140.008
            },
            "LocDateTime":"04.06 8:53:36",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224550,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"скб",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382810520
            },
            "LocDateTime":"04.06 8:53:30",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224549,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"скб-банк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382808300.008
            },
            "LocDateTime":"04.06 8:53:28",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224548,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"тойота",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382804297
            },
            "LocDateTime":"04.06 8:53:24",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224547,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"тойота банк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382802357.008
            },
            "LocDateTime":"04.06 8:53:22",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224546,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"премьер бкс",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382798007.008
            },
            "LocDateTime":"04.06 8:53:18",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224545,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"бкс банк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382791453.008
            },
            "LocDateTime":"04.06 8:53:11",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224544,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"кольцо урала",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382782917.008
            },
            "LocDateTime":"04.06 8:53:02",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224543,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"быстробанк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382776737
            },
            "LocDateTime":"04.06 8:52:56",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224542,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"агропромкредит",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382768980
            },
            "LocDateTime":"04.06 8:52:48",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224541,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"байкалинвестбанк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382762773.008
            },
            "LocDateTime":"04.06 8:52:42",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224540,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"реалист банк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382754990.008
            },
            "LocDateTime":"04.06 8:52:34",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224539,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"пойдем!",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382747263.008
            },
            "LocDateTime":"04.06 8:52:27",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224538,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"оренбург",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382743260.008
            },
            "LocDateTime":"04.06 8:52:23",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224537,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"банк оренбург",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382741657
            },
            "LocDateTime":"04.06 8:52:21",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224536,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"нико-банк",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382735847.008
            },
            "LocDateTime":"04.06 8:52:15",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224535,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"форштадт",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382731377
            },
            "LocDateTime":"04.06 8:52:11",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224534,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"финам",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382723813.008
            },
            "LocDateTime":"04.06 8:52:03",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224533,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"банк финам",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382721960
            },
            "LocDateTime":"04.06 8:52:01",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224532,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"юнистрим",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382718680
            },
            "LocDateTime":"04.06 8:51:58",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224531,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"авангард",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758382709667
            },
            "LocDateTime":"04.06 8:51:49",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224505,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"банк открытие",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758381548357.008
            },
            "LocDateTime":"04.06 8:32:28",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         },
         {
            "ActionId":198224504,
            "LevelId":1326279,
            "LevelNumber":0,
            "UserId":1515235,
            "Kind":1,
            "Login":"dust1q",
            "Answer":"открытие",
            "AnswForm":None,
            "EnterDateTime":{
               "Value":63758381526813.008
            },
            "LocDateTime":"04.06 8:32:06",
            "IsCorrect":False,
            "Award":None,
            "LocAward":None,
            "Penalty":0
         }
      ],
      "Messages":[
         
      ],
      "Sectors":[
         {
            "SectorId":2812918,
            "Order":1,
            "Name":"Промежуточный 1",
            "Answer":None,
            "IsAnswered":False
         },
         {
            "SectorId":2812919,
            "Order":2,
            "Name":"Промежуточный 2",
            "Answer":None,
            "IsAnswered":False
         },
         {
            "SectorId":2812920,
            "Order":3,
            "Name":"Итоговый",
            "Answer":None,
            "IsAnswered":False
         }
      ],
      "Helps":[
         {
            "HelpId":1974714,
            "Number":1,
            "HelpText":"\u003ca href=\" http://d1.endata.cx/data/games/71527/34_1_3987355346.png \" target=\"_blank\"\u003e\u003cimg style=\"width: 200px; height:200px;\" src=\" http://d1.endata.cx/data/games/71527/34_1_3987355346.png \"\u003e\u003c/a\u003e\u003ca href=\" http://d1.endata.cx/data/games/71527/34_2_9384796837.png \" target=\"_blank\"\u003e\u003cimg style=\"width: 200px; height:200px;\" src=\" http://d1.endata.cx/data/games/71527/34_2_9384796837.png \"\u003e\u003c/a\u003e \u003ca href=\" http://d1.endata.cx/data/games/71527/34_3_5867389768.png \" target=\"_blank\"\u003e\u003cimg style=\"width: 200px; height:200px;\" src=\" http://d1.endata.cx/data/games/71527/34_3_5867389768.png \"\u003e\u003c/a\u003e\u003ca href=\" http://d1.endata.cx/data/games/71527/34_4_9853798366.png \" target=\"_blank\"\u003e\u003cimg style=\"width: 200px; height:200px;\" src=\" http://d1.endata.cx/data/games/71527/34_4_9853798366.png \"\u003e\u003c/a\u003e\u003cbr\u003e\r\u003cbr/\u003e\u003ca href=\" http://d1.endata.cx/data/games/71527/34_5_5768573335.png\" target=\"_blank\"\u003e\u003cimg style=\"width: 200px; height:200px;\" src=\" http://d1.endata.cx/data/games/71527/34_5_5768573335.png \"\u003e\u003c/a\u003e\u003ca href=\"http://d1.endata.cx/data/games/71527/34_6_5487698372.png \" target=\"_blank\"\u003e\u003cimg style=\"width: 200px; height:200px;\" src=\" http://d1.endata.cx/data/games/71527/34_6_5487698372.png \"\u003e\u003c/a\u003e \u003ca href=\" http://d1.endata.cx/data/games/71527/34_7_9857787524.png \" target=\"_blank\"\u003e\u003cimg style=\"width: 200px; height:200px;\" src=\" http://d1.endata.cx/data/games/71527/34_7_9857787524.png\"\u003e\u003c/a\u003e\u003ca href=\" http://d1.endata.cx/data/games/71527/34_8_8776893766.png \" target=\"_blank\"\u003e\u003cimg style=\"width: 200px; height:200px;\" src=\" http://d1.endata.cx/data/games/71527/34_8_8776893766.png \"\u003e\u003c/a\u003e\u003cbr\u003e\r\u003cbr/\u003e\u003ca href=\" http://d1.endata.cx/data/games/71527/34_9_5738753755.png \" target=\"_blank\"\u003e\u003cimg style=\"width: 200px; height:200px;\" src=\" http://d1.endata.cx/data/games/71527/34_9_5738753755.png \"\u003e\u003c/a\u003e\u003ca href=\" http://d1.endata.cx/data/games/71527/34_10_843975735.png \" target=\"_blank\"\u003e\u003cimg style=\"width: 200px; height:200px;\" src=\" http://d1.endata.cx/data/games/71527/34_10_843975735.png \"\u003e\u003c/a\u003e \u003ca href=\" http://d1.endata.cx/data/games/71527/34_11_049358335.png \" target=\"_blank\"\u003e\u003cimg style=\"width: 200px; height:200px;\" src=\" http://d1.endata.cx/data/games/71527/34_11_049358335.png \"\u003e\u003c/a\u003e\u003ca href=\" http://d1.endata.cx/data/games/71527/34_12_053883853.png \" target=\"_blank\"\u003e\u003cimg style=\"width: 200px; height:200px;\" src=\" http://d1.endata.cx/data/games/71527/34_12_053883853.png \"\u003e\u003c/a\u003e\u003cbr\u003e\r\u003cbr/\u003e\u003cbr\u003e\r\u003cbr/\u003eЗнаки. Они повсюду.\u003cbr\u003e\r\u003cbr/\u003e\r\u003cbr/\u003e\u003cspan style=color:yellow;\u003e\u003cb\u003eФО промежуточного 1:\u003c/b\u003e название банка\u003c/span\u003e\u003cbr\u003e\r\u003cbr/\u003e\u003cspan style=color:yellow;\u003e\u003cb\u003eФО промежуточного 2:\u003c/b\u003e название французского аналога\u003c/span\u003e\u003cbr\u003e\r\u003cbr/\u003e\u003cspan style=color:yellow;\u003e\u003cb\u003eФО итогового:\u003c/b\u003e интервьюер интервьюируемый через пробелы\u003c/span\u003e",
            "IsPenalty":False,
            "Penalty":0,
            "PenaltyComment":None,
            "RequestConfirm":False,
            "PenaltyHelpState":0,
            "RemainSeconds":0,
            "PenaltyMessage":None
         },
         {
            "HelpId":1976685,
            "Number":2,
            "HelpText":"По номерам выпусков соберите координаты, в этом вам поможет одежда ведущего. Банк рядом зайдет в промежуточный. Найдите знак, он подскажет вам эпизод. Чтобы закрыть итоговый, ищите в сериале то, с чего начинали.",
            "IsPenalty":False,
            "Penalty":0,
            "PenaltyComment":None,
            "RequestConfirm":False,
            "PenaltyHelpState":0,
            "RemainSeconds":0,
            "PenaltyMessage":None
         }
      ],
      "PenaltyHelps":[
         
      ],
      "Bonuses":[
         {
            "BonusId":1664140,
            "Name":None,
            "Number":1,
            "Task":None,
            "Help":None,
            "IsAnswered":False,
            "Expired":True,
            "SecondsToStart":0,
            "SecondsLeft":0,
            "AwardTime":0,
            "Answer":None
         },
         {
            "BonusId":1664142,
            "Name":"Промежуточный 1 после подсказки (20 минут)",
            "Number":2,
            "Task":"",
            "Help":None,
            "IsAnswered":False,
            "Expired":False,
            "SecondsToStart":0,
            "SecondsLeft":0,
            "AwardTime":0,
            "Answer":None
         },
         {
            "BonusId":1670373,
            "Name":None,
            "Number":3,
            "Task":None,
            "Help":None,
            "IsAnswered":False,
            "Expired":True,
            "SecondsToStart":0,
            "SecondsLeft":0,
            "AwardTime":0,
            "Answer":None
         },
         {
            "BonusId":1670374,
            "Name":"Промежуточный 2 после подсказки (20 минут)",
            "Number":4,
            "Task":"",
            "Help":None,
            "IsAnswered":False,
            "Expired":False,
            "SecondsToStart":0,
            "SecondsLeft":0,
            "AwardTime":0,
            "Answer":None
         },
         {
            "BonusId":1670375,
            "Name":None,
            "Number":5,
            "Task":None,
            "Help":None,
            "IsAnswered":False,
            "Expired":True,
            "SecondsToStart":0,
            "SecondsLeft":0,
            "AwardTime":0,
            "Answer":None
         },
         {
            "BonusId":1670376,
            "Name":"Итоговый после подсказки (20 минут)",
            "Number":6,
            "Task":"",
            "Help":None,
            "IsAnswered":False,
            "Expired":False,
            "SecondsToStart":0,
            "SecondsLeft":0,
            "AwardTime":0,
            "Answer":None
         }
      ]
   },
   "Levels":[
      {
         "LevelId":1320456,
         "LevelNumber":1,
         "LevelName":"",
         "Dismissed":False,
         "IsPassed":False,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1320540,
         "LevelNumber":2,
         "LevelName":"Дорога на работу",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1320905,
         "LevelNumber":3,
         "LevelName":"Профессии",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1320914,
         "LevelNumber":4,
         "LevelName":"Рафаэлло",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1320998,
         "LevelNumber":5,
         "LevelName":"Новости",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1321458,
         "LevelNumber":6,
         "LevelName":"Следствие вели",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326284,
         "LevelNumber":7,
         "LevelName":"Коллеги",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1322951,
         "LevelNumber":8,
         "LevelName":"Кубрая",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1322963,
         "LevelNumber":9,
         "LevelName":"Свари мне",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1322977,
         "LevelNumber":10,
         "LevelName":"Неоконченный роман",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1324105,
         "LevelNumber":11,
         "LevelName":"Burning man",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1324177,
         "LevelNumber":12,
         "LevelName":"Питерский",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1324289,
         "LevelNumber":13,
         "LevelName":"Небольшой",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1324300,
         "LevelNumber":14,
         "LevelName":"У-Дали",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1324353,
         "LevelNumber":15,
         "LevelName":"На три буквы",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1325510,
         "LevelNumber":16,
         "LevelName":"Газета",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1325513,
         "LevelNumber":17,
         "LevelName":"Реактор",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1325514,
         "LevelNumber":18,
         "LevelName":"На ковёр",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1325515,
         "LevelNumber":19,
         "LevelName":"Шнобель",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1325516,
         "LevelNumber":20,
         "LevelName":"Сальдо",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1325523,
         "LevelNumber":21,
         "LevelName":"Схема",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1325544,
         "LevelNumber":22,
         "LevelName":"Гимн",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1325689,
         "LevelNumber":23,
         "LevelName":"Лекция ",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1325698,
         "LevelNumber":24,
         "LevelName":"To do list",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326144,
         "LevelNumber":25,
         "LevelName":"Корпорат",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326146,
         "LevelNumber":26,
         "LevelName":"Мелодия",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326167,
         "LevelNumber":27,
         "LevelName":"Задание",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326273,
         "LevelNumber":28,
         "LevelName":"День сурка",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326274,
         "LevelNumber":29,
         "LevelName":"Город грехов",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326275,
         "LevelNumber":30,
         "LevelName":"Папа вам не мама",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326276,
         "LevelNumber":31,
         "LevelName":"Елизавета",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326277,
         "LevelNumber":32,
         "LevelName":"",
         "Dismissed":False,
         "IsPassed":False,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326278,
         "LevelNumber":33,
         "LevelName":"",
         "Dismissed":False,
         "IsPassed":False,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326279,
         "LevelNumber":34,
         "LevelName":"",
         "Dismissed":False,
         "IsPassed":False,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326280,
         "LevelNumber":35,
         "LevelName":"",
         "Dismissed":False,
         "IsPassed":False,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326281,
         "LevelNumber":36,
         "LevelName":"Телефоны",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326282,
         "LevelNumber":37,
         "LevelName":"Морской бой",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326283,
         "LevelNumber":38,
         "LevelName":"",
         "Dismissed":False,
         "IsPassed":False,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1322201,
         "LevelNumber":39,
         "LevelName":"",
         "Dismissed":False,
         "IsPassed":False,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1326285,
         "LevelNumber":40,
         "LevelName":"",
         "Dismissed":False,
         "IsPassed":False,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1327836,
         "LevelNumber":41,
         "LevelName":"",
         "Dismissed":False,
         "IsPassed":False,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1327837,
         "LevelNumber":42,
         "LevelName":"",
         "Dismissed":False,
         "IsPassed":False,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1328865,
         "LevelNumber":43,
         "LevelName":"",
         "Dismissed":False,
         "IsPassed":False,
         "Task":None,
         "LevelAction":None
      },
      {
         "LevelId":1329849,
         "LevelNumber":44,
         "LevelName":"Техничка",
         "Dismissed":False,
         "IsPassed":True,
         "Task":None,
         "LevelAction":None
      }
   ],
   "GameId":71527,
   "GameTypeId":1,
   "GameZoneId":1,
   "GameNumber":362,
   "GameTitle":"Пятидневка [Увлекательно-познавательно-развивательно-любопытное состязание]",
   "LevelSequence":3,
   "UserId":1529484,
   "TeamId":165713,
   "EngineAction":{
      "LevelNumber":34,
      "LevelAction":{
         "Answer":None,
         "IsCorrectAnswer":None
      },
      "BonusAction":{
         "Answer":None,
         "IsCorrectAnswer":None
      },
      "PenaltyAction":{
         "PenaltyId":0,
         "ActionType":0
      },
      "GameId":71527,
      "LevelId":0
   },
   "Event":0
}


def test():
    external_data = {
        "Level": {
            "LevelId": 310661,
            "Name": "Название уровня",
            "Number": 1,
            "Timeout": 1296000,
            "TimeoutSecondsRemain": 1295876,
            "TimeoutAward": -3661,
            "IsPassed": False,
            "Dismissed": False,
            "StartTime": {
                "Value": 63757809120000
            },
            "HasAnswerBlockRule": False,
            "BlockDuration": 0,
            "BlockTargetId": 0,
            "AttemtsNumber": 0,
            "AttemtsPeriod": 0,
            "RequiredSectorsCount": 2,
            "PassedSectorsCount": 0,
            "SectorsLeftToClose": 2
        },
        "Levels": [
            {
                "LevelId": 310661,
                "LevelNumber": 1,
                "LevelName": "Название уровня",
                "Dismissed": False,
                "IsPassed": False,
                "Task": None,
                "LevelAction": None
            },
            {
                "LevelId": 310662,
                "LevelNumber": 2,
                "LevelName": "Название уровня",
                "Dismissed": False,
                "IsPassed": False,
                "Task": None,
                "LevelAction": None
            },
            {
                "LevelId": 310663,
                "LevelNumber": 3,
                "LevelName": "Название уровня",
                "Dismissed": False,
                "IsPassed": False,
                "Task": None,
                "LevelAction": None
            },
            {
                "LevelId": 310664,
                "LevelNumber": 4,
                "LevelName": "Название уровня",
                "Dismissed": False,
                "IsPassed": False,
                "Task": None,
                "LevelAction": None
            },
            {
                "LevelId": 310665,
                "LevelNumber": 5,
                "LevelName": "Название уровня",
                "Dismissed": False,
                "IsPassed": False,
                "Task": None,
                "LevelAction": None
            },
            {
                "LevelId": 310666,
                "LevelNumber": 6,
                "LevelName": "Название уровня",
                "Dismissed": False,
                "IsPassed": False,
                "Task": None,
                "LevelAction": None
            }
        ],
        "GameId": 31224,
        "GameTypeId": 0,
        "GameZoneId": 0,
        "GameNumber": 25325,
        "GameTitle": "Test_engine",
        "LevelSequence": 0,
        "UserId": 163129,
        "TeamId": None,
        "EngineAction": {
            "LevelNumber": 0,
            "LevelAction": {
                "Answer": None,
                "IsCorrectAnswer": None
            },
            "BonusAction": {
                "Answer": None,
                "IsCorrectAnswer": None
            },
            "PenaltyAction": {
                "PenaltyId": 0,
                "ActionType": 0
            },
            "GameId": 31224,
            "LevelId": 0
        },
        "Event": 0
    }
    external_data_2 = {
        "Level": None,
        "Levels": [

        ],
        "GameId": 31224,
        "GameTypeId": 0,
        "GameZoneId": 0,
        "GameNumber": 25325,
        "GameTitle": "Test_engine",
        "LevelSequence": 0,
        "UserId": 0,
        "TeamId": None,
        "EngineAction": {
            "LevelNumber": 0,
            "LevelAction": {
                "Answer": None,
                "IsCorrectAnswer": None
            },
            "BonusAction": {
                "Answer": None,
                "IsCorrectAnswer": None
            },
            "PenaltyAction": {
                "PenaltyId": 0,
                "ActionType": 0
            },
            "GameId": 31224,
            "LevelId": 0
        },
        "Event": 5
    }
    external_data_3 = {
        "Level": {
            "LevelId": 310661,
            "Name": "Название уровня",
            "Number": 1,
            "Timeout": 1296000,
            "TimeoutSecondsRemain": 1287456,
            "TimeoutAward": -3661,
            "IsPassed": False,
            "Dismissed": False,
            "StartTime": {
                "Value": 63757809120000
            },
            "HasAnswerBlockRule": False,
            "BlockDuration": 0,
            "BlockTargetId": 0,
            "AttemtsNumber": 0,
            "AttemtsPeriod": 0,
            "RequiredSectorsCount": 2,
            "PassedSectorsCount": 1,
            "SectorsLeftToClose": 1,
            "Tasks": [
                {
                    "ReplaceNlToBr": True,
                    "TaskText": "Тест Задания Уровня",
                    "TaskTextFormatted": "Тест Задания Уровня"
                }
            ],
            "MixedActions": [
                {
                    "ActionId": 169814,
                    "LevelId": 310661,
                    "LevelNumber": 0,
                    "UserId": 163129,
                    "Kind": 2,
                    "Login": "forcabarca",
                    "Answer": "йцу",
                    "AnswForm": None,
                    "EnterDateTime": {
                        "Value": 63757817655720
                    },
                    "LocDateTime": "28.05 19:54:15",
                    "IsCorrect": True,
                    "Award": None,
                    "LocAward": None,
                    "Penalty": 0
                },
                {
                    "ActionId": 2926959,
                    "LevelId": 310661,
                    "LevelNumber": 0,
                    "UserId": 163129,
                    "Kind": 1,
                    "Login": "forcabarca",
                    "Answer": "йфя",
                    "AnswForm": None,
                    "EnterDateTime": {
                        "Value": 63757817435767.008
                    },
                    "LocDateTime": "28.05 19:50:35",
                    "IsCorrect": True,
                    "Award": None,
                    "LocAward": None,
                    "Penalty": 0
                },
                {
                    "ActionId": 169813,
                    "LevelId": 310661,
                    "LevelNumber": 0,
                    "UserId": 163129,
                    "Kind": 2,
                    "Login": "forcabarca",
                    "Answer": "йфя",
                    "AnswForm": None,
                    "EnterDateTime": {
                        "Value": 63757817435767.008
                    },
                    "LocDateTime": "28.05 19:50:35",
                    "IsCorrect": True,
                    "Award": None,
                    "LocAward": None,
                    "Penalty": 0
                },
                {
                    "ActionId": 2926958,
                    "LevelId": 310661,
                    "LevelNumber": 0,
                    "UserId": 163129,
                    "Kind": 1,
                    "Login": "forcabarca",
                    "Answer": "kod2",
                    "AnswForm": None,
                    "EnterDateTime": {
                        "Value": 63757817207913
                    },
                    "LocDateTime": "28.05 19:46:47",
                    "IsCorrect": False,
                    "Award": None,
                    "LocAward": None,
                    "Penalty": 0
                },
                {
                    "ActionId": 2926957,
                    "LevelId": 310661,
                    "LevelNumber": 0,
                    "UserId": 163129,
                    "Kind": 1,
                    "Login": "forcabarca",
                    "Answer": "kod1",
                    "AnswForm": None,
                    "EnterDateTime": {
                        "Value": 63757817203767.008
                    },
                    "LocDateTime": "28.05 19:46:43",
                    "IsCorrect": False,
                    "Award": None,
                    "LocAward": None,
                    "Penalty": 0
                }
            ],
            "Messages": [
                {
                    "OwnerId": 163129,
                    "OwnerLogin": "forcabarca",
                    "MessageId": 4267,
                    "MessageText": "Сообщения от авторов на уровне",
                    "WrappedText": "Сообщения от авторов на уровне",
                    "ReplaceNl2Br": True
                }
            ],
            "Sectors": [
                {
                    "SectorId": 299056,
                    "Order": 1,
                    "Name": "Сектор 1",
                    "Answer": {
                        "Answer": "йфя",
                        "AnswerDateTime": {
                            "Value": 63757817435767.008
                        },
                        "Login": "forcabarca",
                        "UserId": 163129,
                        "LocDateTime": None
                    },
                    "IsAnswered": True
                },
                {
                    "SectorId": 299057,
                    "Order": 2,
                    "Name": "сектор 2",
                    "Answer": None,
                    "IsAnswered": False
                }
            ],
            "Helps": [
                {
                    "HelpId": 262686,
                    "Number": 1,
                    "HelpText": "Это подсказка доступна через 360ч",
                    "IsPenalty": False,
                    "Penalty": 0,
                    "PenaltyComment": None,
                    "RequestConfirm": False,
                    "PenaltyHelpState": 0,
                    "RemainSeconds": 0,
                    "PenaltyMessage": None
                },
                {
                    "HelpId": 262685,
                    "Number": 2,
                    "HelpText": "Эта подсказка доступна через одну секунду",
                    "IsPenalty": False,
                    "Penalty": 0,
                    "PenaltyComment": None,
                    "RequestConfirm": False,
                    "PenaltyHelpState": 0,
                    "RemainSeconds": 0,
                    "PenaltyMessage": None
                }
            ],
            "PenaltyHelps": [
                {
                    "HelpId": 262687,
                    "Number": 1,
                    "HelpText": None,
                    "IsPenalty": True,
                    "Penalty": 7200,
                    "PenaltyComment": "Описание: штрафная подсказка №1",
                    "RequestConfirm": True,
                    "PenaltyHelpState": 0,
                    "RemainSeconds": 0,
                    "PenaltyMessage": None
                },
                {
                    "HelpId": 262688,
                    "Number": 2,
                    "HelpText": None,
                    "IsPenalty": True,
                    "Penalty": 7200,
                    "PenaltyComment": "Описание: штрафная подсказка №2",
                    "RequestConfirm": True,
                    "PenaltyHelpState": 0,
                    "RemainSeconds": 31095456,
                    "PenaltyMessage": None
                }
            ],
            "Bonuses": [
                {
                    "BonusId": 229342,
                    "Name": "Название: бонус 1",
                    "Number": 1,
                    "Task": "Задание: бонус 1",
                    "Help": "подсказака для бонуса\r\n",
                    "IsAnswered": True,
                    "Expired": False,
                    "SecondsToStart": 0,
                    "SecondsLeft": 0,
                    "AwardTime": 60,
                    "Answer": {
                        "Answer": "йцу",
                        "AnswerDateTime": {
                            "Value": 63757817655720
                        },
                        "Login": "forcabarca",
                        "UserId": 163129
                    }
                },
                {
                    "BonusId": 229343,
                    "Name": "Название Бонуса 2",
                    "Number": 2,
                    "Task": "Задание для бонуса 2",
                    "Help": None,
                    "IsAnswered": False,
                    "Expired": False,
                    "SecondsToStart": 0,
                    "SecondsLeft": 1287456,
                    "AwardTime": 0,
                    "Answer": None
                },
                {
                    "BonusId": 229354,
                    "Name": "бонус 3",
                    "Number": 3,
                    "Task": "задание бонус 3",
                    "Help": "подсказка бонус 3",
                    "IsAnswered": True,
                    "Expired": False,
                    "SecondsToStart": 0,
                    "SecondsLeft": 0,
                    "AwardTime": 60,
                    "Answer": {
                        "Answer": "йфя",
                        "AnswerDateTime": {
                            "Value": 63757817435767.008
                        },
                        "Login": "forcabarca",
                        "UserId": 163129
                    }
                }
            ]
        },
        "Levels": [
            {
                "LevelId": 310661,
                "LevelNumber": 1,
                "LevelName": "Название уровня",
                "Dismissed": False,
                "IsPassed": False,
                "Task": None,
                "LevelAction": None
            },
            {
                "LevelId": 310662,
                "LevelNumber": 2,
                "LevelName": "Название уровня",
                "Dismissed": False,
                "IsPassed": False,
                "Task": None,
                "LevelAction": None
            },
            {
                "LevelId": 310663,
                "LevelNumber": 3,
                "LevelName": "Название уровня",
                "Dismissed": False,
                "IsPassed": False,
                "Task": None,
                "LevelAction": None
            },
            {
                "LevelId": 310664,
                "LevelNumber": 4,
                "LevelName": "Название уровня",
                "Dismissed": False,
                "IsPassed": False,
                "Task": None,
                "LevelAction": None
            },
            {
                "LevelId": 310665,
                "LevelNumber": 5,
                "LevelName": "Название уровня",
                "Dismissed": False,
                "IsPassed": False,
                "Task": None,
                "LevelAction": None
            },
            {
                "LevelId": 310666,
                "LevelNumber": 6,
                "LevelName": "Название уровня",
                "Dismissed": False,
                "IsPassed": False,
                "Task": None,
                "LevelAction": None
            }
        ],
        "GameId": 31224,
        "GameTypeId": 0,
        "GameZoneId": 0,
        "GameNumber": 25325,
        "GameTitle": "Test_engine",
        "LevelSequence": 0,
        "UserId": 163129,
        "TeamId": None,
        "EngineAction": {
            "LevelNumber": 0,
            "LevelAction": {
                "Answer": None,
                "IsCorrectAnswer": None
            },
            "BonusAction": {
                "Answer": None,
                "IsCorrectAnswer": None
            },
            "PenaltyAction": {
                "PenaltyId": 0,
                "ActionType": 0
            },
            "GameId": 31224,
            "LevelId": 0
        },
        "Event": 0
    }

    # een = EngineEN(**external_data)
    # een2 = EngineEN(**external_data_2)
    # een3 = EngineEN(**external_data_3)

    data = oten_request.get_json_from_file('materials/пятидневный/level_4.json')
    een3 = EngineEN(**data)

    level_name = een3.level.name
    timeout_left = een3.level.timeout_seconds_remain
    answer_block = een3.level.has_answer_block_rule
    sectors_count = len(een3.level.sectors)
    required_sectors_count = een3.level.required_sectors_count
    passed_sectors_count = een3.level.passed_sectors_count
    left_sectors_count = een3.level.sectors_left_to_close
    task2 = een3.level.tasks[0].task_text_formatted
    task2 = html2text.html2text(task2)
    hint_counts = len(een3.level.helps)
    bonus_count = len(een3.level.bonuses)

    print(bonus_count)


if __name__ == '__main__':
    test()

"""
kind=2 - bonus
kind=1 - main
"""
