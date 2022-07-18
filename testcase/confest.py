import pytest
from Common.my_logger import logger
from Common.my_data import Data
from Common.my_requests import MyRequests
from Common.handle_phone import is_exist_phone
"""
这个配置可加可不加，只是针对这个项目，加了可移植性强，代码健壮性强
比如公司数据时不时需要清一下数据的时候，这个配置就有必要存在了
"""
@pytest.fixture(scope="session",autouse=True)
def global_init():
    # 配置的全局用户信息是要确保一定存在的
    # 1、从Data里拿出来用户数据
    # 2、调用sql从数据库查询，如果不在则注册
    for user in Data.global_user:
        res = is_exist_phone(user)
        if not res:
            logger.info("全局账号使用 {} 不存在,现在注册一个用户".format(user))
            # 如果这个号码不存在，就去注册
            req_data= {"mobile_phone":user,"pwd":"12345678"}
            res =MyRequests.send_requests("http://api.lemonban.com/futureloan/member/register",
                                          "post",
                                          req_data)
            logger.info("注册结果为:{}".format(res.text))

# 这个属于优化部分，当接口框架要做多并发的时候，大家都进Data全局变量类去存取user时，会出错
@pytest.fixture(scope="class")
def class_init():
    # 实例化Data类对象，作为每一个测试类的类级别的变量
    class_share_data = Data()
    yield class_share_data
