# coding: utf-8

"""

"""

import hashlib
import hmac
from urllib import parse
import requests

from lib.log import Log

key = ""
pay_center_url = ""
order_status_url = ""
_hash = lambda s: hmac.new(key.encode(), s.encode(), hashlib.sha256).hexdigest()



