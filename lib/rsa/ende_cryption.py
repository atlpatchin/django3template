# coding: utf-8

"""
RSA加解密
https://blog.csdn.net/sc_lilei/article/details/83027970
作用：对信息进行公钥加密，私钥解密。
应用场景：
    A想要加密传输一份数据给B，担心使用对称加密算法易被他人破解（密钥只有一份，一旦泄露，则数据泄露），
    故使用非对称加密。信息接收方可以生成自己的秘钥对，即公私钥各一个，然后将公钥发给他人，私钥自己保留。

    A使用公钥加密数据，然后将加密后的密文发送给B，B再使用自己的私钥进行解密，这样即使A的
    公钥和密文均被第三方得到，第三方也要知晓私钥和加密算法才能解密密文，大大降低数据泄露风险。
"""

import json
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5  # 用于加密
from Crypto import Random
from typing import Any

from lib.log import Log
from lib.rsa import private, public


class Rsa(object):
    """RSA加解密类"""

    @staticmethod
    def encrypt(plainText: (str, dict), _public_key=public.api_key) -> str:
        """公钥加密"""
        if isinstance(plainText, dict):
            plainText = json.dumps(plainText)
        if not isinstance(plainText, str):
            raise ("明文无法序列化成字符串")
        cipher_pub_obj = PKCS1_v1_5.new(RSA.import_key(_public_key))
        _secret_byte_obj = cipher_pub_obj.encrypt(plainText.encode("utf-8"))
        encryptCode = base64.b64encode(_secret_byte_obj)
        return str(encryptCode, "utf-8")

    @staticmethod
    def decrypt(encryptCode: str, _private_key=private.api_key) -> Any:
        """私钥解密"""
        try:
            _secret_byte_obj = base64.b64decode(encryptCode)
            cipher_pri_obj = PKCS1_v1_5.new(RSA.import_key(_private_key))
            _byte_obj = cipher_pri_obj.decrypt(_secret_byte_obj, Random.new().read)
            plain_text = _byte_obj.decode("utf-8")
            Log.info(f"RSA加密信息结果：{plain_text}")
            return json.loads(plain_text)
        except Exception as ex:
            Log.error(f"解析RSA加密信息失败：{ex}")
            return {}


if __name__ == '__main__':
    data = {"user_id": 190}
    code = Rsa.encrypt(data)
    print(Rsa.decrypt(code))
