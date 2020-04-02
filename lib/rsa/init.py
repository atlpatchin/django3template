# coding: utf-8

"""初始化秘钥文件, 注意:不可随意修改秘钥, 更改时需要通知下游."""

from Crypto.PublicKey import RSA

if __name__ == "__main__":
    # 新建公私钥
    _rsa = RSA.generate(2048)
    private_key = _rsa.export_key()  # 私钥
    public_key = _rsa.publickey().export_key()  # 公钥

    # 写入文件
    with open("private.pem", "wb") as pf:
        pf.write(private_key)
    with open("public.pem", "wb") as pf:
        pf.write(public_key)
