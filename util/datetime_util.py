# coding: utf-8

"""通用日期处理工具"""

import time
from typing import Generator
from datetime import datetime, timedelta

from util import add_decorator_for_public_method

add_decorator_for_public_method(staticmethod)
class DateTimeUtil(object):
    """日期工具类"""

    # 当前日期
    now = datetime.now()
    # 当前日期字符串
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 3位精度数日期时间字符串
    now_float3 = datetime.now().__str__()[:-3]
    # 当前时间戳浮点型
    time_float = time.time()
    # 当前时间戳整数
    time_int = int(time.time())

    def datetimeToStr(_datetime: datetime, data=False, hour=False, minute=False) -> str:
        """
        日期时间对象转字符串, 年:月:日 时:分:秒
        :param _datetime: 日期时间
        :param data: 输出精确到日
        :param hour: 输出精确到时
        :param minute: 输出精确到时分
        :return: 日期时间字符串
        """
        if data:
            return _datetime.strftime("%Y-%m-%d")
        if hour:
            return f"""{_datetime.strftime("%Y-%m-%d %H")}时"""
        if minute:
            return _datetime.strftime("%Y-%m-%d %H:%M")
        return _datetime.strftime("%Y-%m-%d %H:%M:%S")

    def dateStrToTimestamp(dateStr: str, days=0) -> float:
        """
        日期字符串转时间戳
        :param dateStr: 日期字符串, 示例:2019-07-11
        :param days: 日期变动天数, 正数往后, 负数往前, 示例:1 或者 -1
        :return: 时间戳浮点
        """
        date = datetime.strptime(dateStr, "%Y-%m-%d") + timedelta(days=days)
        return time.mktime(date.timetuple())

    def timestampToDateStr(_timestamp: (int, float)) -> str:
        """
        时间戳转日期字符串
        :param _timestamp: 时间戳数字或浮点数字, 示例:1562806800.0
        :return: 日期字符串  示例:2019-07-11
        """
        return datetime.fromtimestamp(_timestamp).strftime("%Y-%m-%d")

    def dateRangeStr(startDateStr: str, endDateStr: str, toDict=False) -> Generator:
        """
        日期范围内的日期字符串
        :param startDateStr: 起始日期字符串
        :param endDateStr: 结束日期字符串
        :param toDict: 输出为日期字符串字典列表
        :return: 日期字符串列表或key="Date"的字典 生成器
        """
        startDate = datetime.strptime(startDateStr, "%Y-%m-%d")
        endDate = datetime.strptime(endDateStr, "%Y-%m-%d")

        def date_range(start, end, step):
            while start <= end:
                dataStr = start.strftime("%Y-%m-%d")
                yield {"Date": dataStr} if toDict else dataStr
                start += step

        return date_range(startDate, endDate, timedelta(days=1))

    def datetimeStrToDateStr(datetimeStr: str) -> str:
        """
        日期时间字符串转日期字符串
        :param datetimeStr: 日期时间字符串 年-月-日 时:分:秒
        :return: 日期字符串 年-月-日
        """
        return datetime.strptime(datetimeStr, "%Y-%m-%d %H:%M:%S").date().__str__()

    def strToDate(strDate: str):
        """
        字符串转为日期
        :param strDate: 字符串
        :return: 日期
        """
        Date = datetime.strptime(strDate, "%Y-%m-%d")
        ret = datetime.date(Date)
        return ret

    def timestampToDateTime(_timestamp: int) -> datetime:
        """
        时间戳转日期时间对象
        :param _timestamp: 时间戳整数
        :return: 日期时间对象
        """
        return datetime.fromtimestamp(_timestamp)


if __name__ == "__main__":
    # print(dateStrToTimestamp("2019-07-11 09:00:00"))
    # print(timestampToDateStr(1562806800.0))
    print(DateTimeUtil.now)
    print(DateTimeUtil.now_str)
    print(DateTimeUtil.now_float3)
    print([d for d in DateTimeUtil.dateRangeStr("2019-07-11", "2019-08-11")])
