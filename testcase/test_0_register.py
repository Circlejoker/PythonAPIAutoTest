import pytest
import json
import os
from Common.my_replace import replace_case_with_re
from Common.my_path import testdata_dir
from Common.my_excel import MyExcel
from Common.my_requests import MyRequests
from Common.my_assert import MyAssert
from Common.my_logger import logger
from Common.my_data import Data

# 第一步 读取excel的注册接口页中的测试数据  -是个列表，列表中的每个成员，都是一个接口用例
excel_path = os.path.join(testdata_dir,"测试用例.xlsx")
# excel_path = r"D:\计算机语言\前端\接口测试\测试用例.xlsx"
me = MyExcel(excel_path,"注册接口")
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


@pytest.mark.usefixtures("class_init")
class TestRegister:
    #发送请求
    @pytest.mark.parametrize("case",cases)
    def test_register(self,case,class_init):
        logger.info("============= 注册接口 ===============")

        # 这个share_data/class_init就是Data类实例化对象
        share_data = class_init

        # 1、接收前置的返回值 -- 上一个接口的返回值，提取出来
        case = replace_case_with_re(case, share_data)

        # 2、将替换之后的请求数据（json格式的字符串），转换成一个字典
        rep_dict = json.loads(case["req_data"])

        # 3、发送接口请求，并接收响应结果
        resp = mq.send_requests(case["url"], case["method"], rep_dict)
        # print(resp.json())

        # 结果空列表
        assert_res = []

        # 4、断言响应结果里的数据      //这步骤做了对于面试比较加分，属于自行封装断言
        if case["assert_list"]:
            response_check_res = massert.assert_response_value(case["assert_list"], resp.json())
            assert_res.append(response_check_res)

        # 5、断言数据库 -sql语句、结果实际、比对的类型
        if case["assert_db"]:
            db_check_res = massert.assert_db(case["assert_db"])
            assert_res.append(db_check_res)

        # 最终抛出异常
        if False in assert_res:
            raise AssertionError


