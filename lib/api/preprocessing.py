# coding: utf-8

"""DRF接口预处理"""

import copy
import time
from functools import wraps

from django.http.request import QueryDict
from lib.rsa.ende_cryption import Rsa
from lib.log import Log
from lib.api.http import HttpResponse

# token过期时间
TOKEN_TIMEOUT = 60 * 60 * 2


def token_verifying(_action):
    """token校验, token码最好包含Time时间戳"""

    @wraps(_action)
    def processing(request, *args, **kwargs):
        try:
            # return True  # 调试期间先把校验关闭
            _checkKey = "token"
            data = request.data
            token = data.get(_checkKey)
            if not token:
                return HttpResponse(request).fail(info=f"校验参数缺失")
            if isinstance(data, QueryDict):
                data = data.dict()
            # 去除数据字典里的token
            dictParams = copy.deepcopy(data)
            dictParams.pop(_checkKey, None)
            # 解密出数据字典,并去除Time
            dictDecode = Rsa.decrypt(token)
            dictDecode.pop("Time", None)
            if dictParams == dictDecode:
                return _action(request, *args, **kwargs)
            return HttpResponse(request).fail(f"{_action.__doc__} 参数校验失败")
        except Exception as ex:
            Log.error(f"{_action.__doc__} 参数校验失败 {ex}")
            return False

    return processing


def token_timeout(_action):
    """token过期, token码必须包含Time时间戳"""

    @wraps(_action)
    def processing(request, *args, **kwargs):
        try:
            # return True  # 调试期间先把校验关闭
            _checkKey = "token"
            data = request.data
            token = data.get(_checkKey)
            if not token:
                return HttpResponse(request).fail(info=f"校验过期参数缺失")
            # 解密出数据字典,并去除Time
            dictDecode = Rsa.decrypt(token)
            _time = dictDecode.get("Time", None)
            if _time:
                valid_time = int(time.time()) - int(_time)
                if valid_time < TOKEN_TIMEOUT:
                    return _action(request, *args, **kwargs)
                return HttpResponse(request).fail(f"{_action.__doc__} 参数已过期")
            return HttpResponse(request).fail(f"{_action.__doc__} 过期参数校验失败")
        except Exception as ex:
            Log.error(f"{_action.__doc__} 过期参数校验失败 {ex}")
            return False

    return processing


def logging(_action):
    """日志记录"""

    @wraps(_action)
    def processing(request, *args, **kwargs):
        try:
            Log.info(f"{_action.__doc__} 请求 {request.data}")
            return _action(request, *args, **kwargs)
        except Exception as ex:
            return HttpResponse(request).fail(info=f"{_action.__doc__} 报错 {ex}")

    return processing
