# coding: utf-8

"""http请求和返回"""

import inspect

from lib.api import call_me
from lib.log import Log
from rest_framework.views import status
from rest_framework.response import Response
from rest_framework import exceptions, response
from rest_framework.views import exception_handler as base_exception_handler


class JResponse(Response):
    """指定drf框架的Json返回格式"""

    def __init__(self, data=None, code=None, msg=None, status=status.HTTP_200_OK,
                 info=None):
        super().__init__(None, status=status)
        self.data = {"ActionStatus": msg,
                     "ErrorCode": code,
                     "ErrorInfo": info,
                     "Data": data}


class HttpResponse(object):
    """Http请求返回处理类"""

    def __init__(self, request=None):
        super(HttpResponse, self).__init__()
        self.request = request

    def fail(self, data={}, info=""):
        """请求返回失败"""
        if not isinstance(data, dict):
            data = {}
        frame = inspect.stack()[1].frame
        Log.error(f"{self.fail.__doc__} {call_me(frame)} {data} {info}")
        return JResponse(msg="FAIL", code=-1, info=info, data=data)

    def ok(self, data={}):
        """请求返回成功"""
        if not isinstance(data, (dict, list)):
            data = {}
        frame = inspect.stack()[1].frame
        logStr = f"{self.ok.__doc__} {call_me(frame)} {data}"
        logLen = 500  # 截取日志长度
        Log.info(logStr if len(logStr) <= logLen else f"{logStr[:logLen]}...")
        return JResponse(msg="OK", data=data)


def exception_handler(exc, context):
    """rest api异常处理

    :param exc: 异常
    :param context: 上下文
    :return: 请求响应
    """
    response = base_exception_handler(exc, context)
    if isinstance(exc, exceptions.APIException):
        if isinstance(exc.detail, (list, dict)):
            data = exc.get_full_details()
        else:
            data = {'__global': exc.get_full_details()}
        response.data = data.update({"code": 1})
    else:
        # 在此处补充自定义的异常处理
        if response is not None:
            response.data.update({"ActionStatus": "FAIL",
                                  "ErrorCode": -1,
                                  "Data": ""})
    return response
