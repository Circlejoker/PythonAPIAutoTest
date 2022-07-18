import ast
import jsonpath
from decimal import Decimal
from Common.my_logger import logger
from Common.my_mysql import MyMySql
class MyAssert:

    # 响应结果断言
    def assert_response_value(self,check_str,response_dict):
        """
        :param check_str:       从测试用例excel中读取对应的断言列，这是一个列表形式的字符串，里面的成员是一个断言
        :param response_dict:   发送用例接口请求后返回的响应数据，是一个字典类型
        :return:                None
        1.将check_str转成python对象（列表），通过eval
        2.遍历 1. 中的列表，访问每一组作比对，通过比对方式得出比对结果
        3.将比对结果传给 check_res结果列表并返回

        引入了ast库，目的是 用 ast.literal_eval()这个方法  可以将字符串转换成python列表   ，比eval()更安全些

        引入了jsonpath库 ，  目的是 从响应结果中提取值，并设置为全局变量(Data类作为本框架的全局变量类)

        Decimal的作用，因为考虑到数据库断言中，当查询数据库结果中有Decimal类型，则可以将它转为float类型
        """
        # 字符串转为列表
        check_list = ast.literal_eval(check_str)

        # 所有断言比对的结果，放在一个列表里
        check_res = []

        # 遍历列表check_list，检查各值是否符合期望
        for check in check_list:
            logger.info("要断言的内容为：\n{}".format(check))
            # 通过jsonpath表达式，从响应结果response_dict当中拿到了实际结果,并作列表值赋值给actual
            actual = jsonpath.jsonpath(response_dict,check["expr"])
            logger.info("此时actual的值为：\n{}".format(actual))

            # 判断actual是否经jsonpath验证成功转为了列表值，是的话，actual的值就是 [0]
            if isinstance(actual,list):
                actual = actual[0]
            logger.info("经过判断，从响应结果当中提取到的值为：\n{}".format(actual))
            logger.info("期望结果为：\n{}".format(check["expected"]))

            # 与实际结果作比对,当对比方法为 相等处理时
            if check["type"] == "eq":
                logger.info("比对2个值是否相等")
                logger.info("比对结果为：\n{}".format(actual == check["expected"]))
                check_res.append(actual == check["expected"])
            # 与实际结果作比对,当对比方法为 判断实际值是否存在时
            if check["type"] == "count":
                try:
                    actual
                except NameError:
                    check_res.append(False)
                    logger.info("actual不存在")
                else:
                    check_res.append(True)

        if False in check_res:
            logger.info("部分断言失败,请查看断言结果为False的值")
            # 抛出断言异常
            return False
        else:
            logger.info("断言成功！")
            return True



    # 数据库断言
    def assert_db(self, check_db_str):
        """
        :param check_db_str:    从测试用例excel中读取对应的数据库断言列，这是一个列表形式的字符串，里面的成员是一个断言
        :return:
        1.将check_db_str转成python对象（列表），通过eval
        2.遍历 1. 中的列表，访问每一组db比对
        3.对于每一组来讲  1)调用数据库类，执行sql语句，调哪个方法，根据type来决定，得到实际结果
                       2)与期望结果比对
        """
        # 字符串转为列表
        check_db_list = ast.literal_eval(check_db_str)

        # 所有断言的比对结果，放在一个列表里
        check_db_res = []

        # 实例化数据库,初始化自动连接数据库
        db = MyMySql()

        # 遍历列表check_db_list，检查各值是否符合期望
        for check_db_dict in check_db_list:
            logger.info("当前要比对的sql语句：\n{}".format(check_db_dict["sql"]))
            logger.info("当前执行sql的查询类型(查询结果条数/查询某个值.)\n{}".format(check_db_dict["db_type"]))
            logger.info("期望结果为：{}".format(check_db_dict["expected"]))
            if check_db_dict["db_type"] == "count":
                logger.info("比对数据库查询的结果条数,是否符合预期")
                # 执行sql语句，查询结果是一个整数
                res = db.get_count(check_db_dict["sql"])
            elif check_db_dict["db_type"] == "eq":
                logger.info("比对数据库查询语句是否相等")
                # 执行sql语句，查询结果是一个字典key-value
                res = db.get_one_data(check_db_dict["sql"])
                # 对于数据库查询结果当中，如果有Decimal类型，则将他转化为float类型
                for key, value in res.items():
                    if isinstance(value, Decimal):
                        res[key] = float(value)
            else:
                logger.info("不支持数据库比对类型！请检查你的用例断言写法")
                raise Exception

            # 将比对结果添加到结果列表里
            check_db_res.append(res == check_db_dict["expected"])
            logger.info("比对结果为：{}".format(check_db_res[-1]))
        # 关闭数据库
        db.close_conn()

        if False in check_db_res:
            logger.info("部分断言失败，请查看数据库比对结果为False的")
            return False
        else:
            logger.info("断言成功！")
            return True






