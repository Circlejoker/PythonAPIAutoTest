"""
得到没有注册过的手机
1.通过fake库得到一个随机生成的手机号
2.调用mysql数据库操作，判断数据库中是否已存在该手机号，如果没有，则表示该手机号未注册，返回该手机号即可
"""
from faker import Faker
from Common.my_mysql import MyMySql

def get_new_phone():
    while True:
        phone = Faker("zh_CN").phone_number()
        sql = "select * from member where mobile_phone={}".format(phone)
        res = MyMySql().get_count(sql)
        if res == 0:
            return phone


def is_exist_phone(phone_num):
    """
        得到没有注册过的手机号码
        @param phone_num: 传入要验证的手机号码
        @return: True   or  False       其中True表示未注册过，False表示已注册
        1、使用Faker生成手机号码
        2、调用mysql数据库操作，去判断是否在数据库中存在，如果不在，表示没有注册
        """
    sql = "select id from member where mobile_phone={}".format(phone_num)
    res = MyMySql().get_count(sql)
    if res == 0:
        return True
    else:
        return False
