import pytest
import json
import os
from Common.my_requests import MyRequests
from Common.my_excel import MyExcel
from Common.my_assert import MyAssert
from Common.my_logger import logger
from Common.my_path import testdata_dir
from Common.myConf import MyConf
from Common.my_path import conf_dir
from Common.my_data import Data
from Common.my_extract import extract_data_from_response
from Common.my_replace import replace_case_with_re
from Common.my_mysql import MyMySql
"""
新增业务

前置：登录成功(意味着要鉴权)
步骤：
断言：
后置：

1、类级别的前置 -- 所有的充值用例，只需要登录一次就够了
    登录账号：
        1、用固定的账号 - 配置化(Conf目录下，data.ini里配置用户)
        2、已配置的账号，如何保证它是已经存在的？
            用之前，查一下数据库，如果没有，就注册(session前置)

2、接口关联处理 -- 登录接口的返回值，要提取出来，然后作为充值接口的请求参数

准备知识：re正则表达式、postman是如何处理参数传递的(接口关联的)

"""
# 第一步 读取excel的注册接口页中的测试数据  -是个列表，列表中的每个成员，都是一个接口用例
excel_path = os.path.join(testdata_dir, "测试用例.xlsx")
# excel_path = r"D:\计算机语言\前端\接口测试\测试用例.xlsx"
me = MyExcel(excel_path,"添加项目")
cases = me.read_data()

# 第二步，遍历测试数据，每一组数据，发起一个http的接口请求
# 实例化请求对象
mq = MyRequests()
massert= MyAssert()

@pytest.fixture(scope="class")
def class_init():
    # 实例化Data类对象，作为每一个测试类的类级别的变量
    class_share_data = Data()
    yield class_share_data

@pytest.mark.addloan
@pytest.mark.usefixtures("class_init")
class TestAddLoan:
    @pytest.mark.parametrize("case",cases)
    def test_add_loan(self, case,class_init):
        # 这个share_data/class_init就是Data类实例化对象
        share_data = class_init
        # 1、接受前置的返回值 -- 上一个接口的返回值，提取出来
        case=replace_case_with_re(case,share_data)

        # 2、将替换之后的请求数据（json格式的字符串），转换成一个字典
        rep_dict = json.loads(case["req_data"])

        # 执行前置sql,
        if case.get("pre_sql"):
            MyMySql().update_data(case.get("pre_sql"))

        # 3、发起请求，并接收响应请求
        if hasattr(share_data,"token"):
            resp = mq.send_requests(case["url"],case["method"], rep_dict ,token=getattr(share_data, "token"))
        else:
            resp = mq.send_requests(case["url"],case["method"],rep_dict)
            # logger.info(resp.json())

        # 4、提取响应结果中的数据
        if case["extract"]:
            extract_data_from_response(case["extract"], resp.json(),share_data)

        # 结果空列表
        assert_res = []

        # 5、断言响应结果里的数据      //这步骤做了对于面试比较加分，属于自行封装断言
        if case["assert_list"]:
            response_check_res = massert.assert_response_value(case["assert_list"],resp.json())
            assert_res.append(response_check_res)

        if False in assert_res:
            pass
        else:
            # 提取响应结果里的数据，并设置为全局变量
            if case["extract"]:
                # 调用提取处理函数
                extract_data_from_response(case["extract"],resp.json(),share_data)

        # 6、断言数据库 -sql语句、结果实际、比对的类型
        if case["assert_db"]:
            db_check_res= massert.assert_db(case["assert_db"])
            assert_res.append(db_check_res)

        # 最终抛出异常
        if False in assert_res:
            raise AssertionError