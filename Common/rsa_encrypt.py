import rsa
import base64
from time import time

"""
RSA加密：http://testingpai.com/article/1595507230322

入门了解：http://testingpai.com/article/1595507276916


pip install rsa
"""

def rsaEncrypt(msg):
    """
    公钥加密
    @param msg:要加密的内容
    @type msg: str
    @return: 加密之后的密文
    """

    # 公钥找公司开发要即可
    server_pub_key = """
    -----BEGIN PUBLIC KEY-----
    MIG.....
    -----END PUBLIC KEY-----
    """

    # 生成公钥对象
    pub_key_byte = server_pub_key.encode("utf-8")
    # print(pub_key_byte)
    pub_key_obj  = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key_byte)

    # 要加密的数据转成字节对象
    content = msg.encode("utf-8")

    # 加密，返回加密文本
    cryto_msg = rsa.encrypt(content,pub_key_obj)
    # base64编码
    cipher_base64 = base64.b64encode(cryto_msg)
    # 转成字符串
    return cipher_base64.decode()


def generator_sign(token):
    # 获取token的前50位
    token_50 = token[:50]
    # 生成时间戳
    timestamp = int(time())
    # 拼接token前50位和时间戳
    msg = token_50 + str(timestamp)
    print(msg)
    # 进行RSA加密
    sign = rsaEncrypt(msg)
    return sign,timestamp
