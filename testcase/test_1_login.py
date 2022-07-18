"""
1、在excel中准备测试数据  - 登录接口
2、在excel中读取测试数据  - 登录接口
3、定义一个测试类TestLogin，使用参数化
4、在类内部：
    4.1、 如果有替换的占位符，那么要先替换掉占位符。  -- 也要准备占位符对应的数据
    4.2、 把替换之后的请求数据(json格式的字符串)转换成一个字典
    4.3、 发起请求，并接收响应结果
    4.4、 定义空列表，存放响应断言和数据库断言的最终结果
    4.5、 处理响应结果断言
    4.6、 处理数据库断言
    4.7、 检查4.4存放响应断言和数据库断言的列表，如果有False，抛出AssertionError
"""
import pytest
import json
import os
from Common.my_requests import MyRequests
from Common.my_excel import MyExcel
from Common.my_assert import MyAssert
from Common.my_logger import logger
from Common.my_path import testdata_dir

# 第一步 读取excel的注册接口页中的测试数据  -是个列表，列表中的每个成员，都是一个接口用例
excel_path = os.path.join(testdata_dir, "测试用例.xlsx")
# excel_path = r"D:\计算机语言\前端\接口测试\测试用例.xlsx"
me = MyExcel(excel_path,"登录接口")
cases = me.read_data()

# 第二步，遍历测试数据，每一组数据，发起一个http的接口请求
# 实例化请求对象
mq = MyRequests()
massert= MyAssert()

@pytest.mark.login
class TestLogin:
    # 发送登录请求
    @pytest.mark.parametrize("case",cases)
    def test_login(self,case):
        logger.info("============= 登录接口 ===============")
        # 1、将替换之后的请求数据（json格式的字符串），转换成一个字典
        rep_dict = json.loads(case["req_data"])

        # 2、发送接口请求，并接收响应结果
        resp = mq.send_requests(case["url"],case["method"],rep_dict)
        logger.info("接口响应结果为：{}".format(resp.json()))
        a= resp.json()
        print(a)

        # 结果空列表
        assert_res = []

        # 3、断言响应结果里的数据
        if case["assert_list"]:
            response_check_res= massert.assert_response_value(case["assert_list"],resp.json())
            assert_res.append(response_check_res)

        # 最终抛出异常：
        if False in assert_res:
            raise AssertionError
