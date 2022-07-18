import requests
import os
from Common.my_logger import logger
from Common.my_path import conf_dir
from Common.myConf import MyConf
from Common.rsa_encrypt import generator_sign

class MyRequests:
    # 初始化
    def __init__(self):
        # 请求头
        self.headers = {"X-Lemonban-Media-Type": "lemonban.v2"}

        # 读取配置文件当中的，server地址
        self.base_url = MyConf(os.path.join(conf_dir, "conf.ini")).get("server", "host")

    def __deal__header(self,token=None):
        if token:
            # 因为开发定义的token相关的格式就是，设置Authorization请求头时，对应值必须是Bearer + 空格 +token，空格是不能省略的
            self.headers["Authorization"] = "Bearer {}".format(token)

    def __deal_url(self,api_url):
        if api_url.startswith("https://") or api_url.startswith("http://"):
            return api_url
        else:
            url = self.base_url + api_url
            return url

    def send_requests(self,api_url,method,data,token=None):
        # 处理请求头中的token鉴权
        self.__deal__header(token)
        # 处理url
        url = self.__deal_url(api_url)
        logger.info("请求url：\n{}".format(url))
        logger.info("请求方法：\n{}".format(method))
        logger.info("请求数据：\n{}".format(data))

        # 如果是v3版本，则需要向请求体当中，添加timestamp和sign字段
        if self.headers.get("X-Lemonban-Media-Type") == "lemonban.v3" and token:
            logger.info("使用RSA加密")
            sign, timestamp = generator_sign(token)
            data["sign"] = sign
            data["timestamp"] = timestamp
            logger.info("请求数据：\n{}".format(data))

        # 调用requests的方法去发起一个请求，并得到响应结果
        # 注意：这里params，json都是字典类型，所以传进来的data也得是字典类型
        if method.upper() == "GET":
            resp = requests.request(method,url,params=data,headers=self.headers)
        else:
            resp = requests.request(method,url,json=data,headers=self.headers)
        logger.info("响应结果为：{} \n 响应数据为{}".format(resp,resp.json()))
        return resp