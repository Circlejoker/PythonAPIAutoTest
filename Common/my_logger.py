"""
1、设置日志的收集级别
2、可以将日志输出到文件和控制台

3、以下这些方法，对应日志的五个级别，由低到高：
    debug()      ：程序调试bug时使用
    info()       ：程序正常运行时使用
    warning      ：程序未按预期运行时使用，但并不是错误，如:用户登录密码错误
    error()      ：程序出错误时使用，如:IO操作失败

    critical()   ：特别严重的问题，导致程序不能再继续运行时使用，如:磁盘空间为空，一般很少使用

额外拓展：单例模式
"""
import logging
from logging import Logger

class MyLogger(Logger):
    def __init__(self):
        file = "api.log"
        # 1、设置日志名字  日志的收集级别
        super().__init__("api",logging.INFO)

        # 2、将日志输出到文件和控制台   自定义日志格式(Formatter)
        fmt_str = "%(asctime)s - %(levelname)s - %(lineno)d - %(funcName)s - %(message)s"
        # 实例化 日志格式, 输出日志记录
        formatter = logging.Formatter(fmt_str)

        # 实例化处理(Handle)
        # 控制台(StreamHandle)
        handle1 = logging.StreamHandler()
        # 设置渠道当中的日志显示格式
        handle1.setFormatter(formatter)
        # 将渠道与日志收集封装起来
        self.addHandler(handle1)

        if file:
            # 文件渠道(FileHandle)
            handle2 = logging.FileHandler(file, encoding="utf-8")
            # 设置渠道当中的日志显示格式
            handle2.setFormatter(formatter)
            self.addHandler(handle2)

logger = MyLogger()