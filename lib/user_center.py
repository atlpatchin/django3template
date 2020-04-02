# coding: utf-8

"""用户中心"""

import requests
import hashlib

from lib.log import Log

md5 = lambda s: hashlib.md5(s.encode()).hexdigest()
_hash = lambda s: hashlib.sha256(s.encode()).hexdigest()


class UserCenter(object):
    """用户中心类"""
    pass
