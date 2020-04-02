# coding: utf-8

"""日志配置"""

import os

from django3template.setting import BASE_DIR


def __LOG_CONFIG(type, level, name):
    def log_full_path(*paths, filename=None):
        """获取文件/文件夹完整路径，若文件/文件夹不存在则创建"""
        path = os.path.join(BASE_DIR, *paths)
        if not os.path.exists(path):
            os.makedirs(path)
        if filename:
            return os.path.join(path, filename)
        return path

    if type == "handler":
        return {
            'level': level,
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 时间拆分日志
            'filename': log_full_path('log', name, filename=f'{name}.log'),
            'when': 'midnight',  # 零点rotate
            'interval': 1,
            'backupCount': 7,  # 7天循环覆盖
            'formatter': 'standard',
        }
    elif type == "logger":
        return {
            'handlers': ['console', name],
            'level': level,
            'propagate': True,
        }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] [%(module)s.%(funcName)s:%(lineno)d] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'django': __LOG_CONFIG("handler", "DEBUG", "django"),
        'logger': __LOG_CONFIG("handler", "DEBUG", "logger"),
    },
    'loggers': {
        'django': __LOG_CONFIG("logger", "INFO", "django"),
        'logger': __LOG_CONFIG("logger", "INFO", "logger"),
    },
}
