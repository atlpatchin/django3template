# coding: utf8

"""封装日志"""

import logging
import requests
import time
import socket
import json

LogDjango = logging.getLogger("django")


class LogService(object):
    """对接日志服务"""
    # 日志服务注册的资源id
    LogServiceResourceID = ""

    def __init__(self, logType="error"):
        super(LogService, self).__init__()
        self.url = ""
        self.postData = {"resource_id": self.LogServiceResourceID,
                         "log_type": logType,  # info
                         "content": "",
                         "operation_ip": self.__get_ip(),
                         "operation_stamp": time.time(),
                         }

    def __get_ip(self):
        """获取局域网地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('', 1))
            return s.getsockname()[0]
        except:
            return '127.0.0.1'
        finally:
            s.close()

    def send(self, msg):
        """发送日志"""
        try:
            self.postData.update(
                {
                    "content": msg,
                    "operation_stamp": time.time()
                }
            )
            headers = {"Content-Type": "application/json"}
            res = requests.post(url=self.url,
                                data=json.dumps(self.postData),
                                headers=headers)
        except Exception as ex:
            LogDjango.error(f"发送日志报错, {self.postData}, {ex}, {res.text}")


class Logger(object):
    """简单日志封装类"""

    def __init__(self, name="logger"):
        super(Logger, self).__init__()
        self._logger = logging.getLogger(name)

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)
        LogService(logType="info").send(msg)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)
        LogService(logType="error").send(msg)


# 日志实例化在此声明，需修改settings文件的LOGGING配置中handlers参数和loggers参数
Log = Logger("logger")

if __name__ == "__main__":
    pass
