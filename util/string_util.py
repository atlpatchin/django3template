# coding: utf-8

"""通用字符串处理工具"""

import uuid
import hashlib

from util import add_decorator_for_public_method

add_decorator_for_public_method(staticmethod)


class StringUtil(object):
    """字符串处理类"""

    def conceal(_str) -> str:
        """
        遮掩字符串中间部分为*号
        :param _str: 要处理的字符串
        :return: 最长三位的字符串, 如果***表示失败
        """
        try:
            value_str = str(_str)
            if len(value_str) > 2:
                return f"{value_str[0]}*{value_str[-1]}"
            elif len(value_str) > 0:
                return f"*{value_str[-1]}"
            else:
                return value_str
        except Exception as ex:
            return "***"

    @staticmethod
    def md5(_str: str, upper=False):
        """
        对字符串md5
        :param _str: 要处理的字符串
        :param upper: 是否全转为大写
        :return: md5处理后字符串
        """
        md5str = hashlib.md5(_str.encode()).hexdigest()
        if upper:
            return md5str.upper()
        return md5str

    @staticmethod
    def hash(_str: str, upper=False):
        """
        对字符串md5
        :param _str: 要处理的字符串
        :param upper: 是否全转为大写
        :return: md5处理后字符串
        """
        sha256str = hashlib.sha256(_str.encode()).hexdigest()
        if upper:
            return sha256str.upper()
        return sha256str

    @staticmethod
    def uuid1(sep=False):
        """
        生成唯一uuid1码
        :param sep: 包含分隔符
        :return: uuid码，不带分隔符长度32，带分隔符36
        """
        uuid_str = uuid.uuid1().__str__()
        if sep:
            return uuid_str
        return uuid_str.replace("-", "")

    @staticmethod
    def uuid5(sep=False, namespace=""):
        """
        生成唯一uuid5码
        :param sep: 包含分隔符
        :param namespace:   命名空间字符串，
        :return: uuid码，不带分隔符长度32，带分隔符36
        """
        uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS, namespace).__str__()
        if sep:
            return uuid_str
        return uuid_str.replace("-", "")


if __name__ == "__main__":
    pass
