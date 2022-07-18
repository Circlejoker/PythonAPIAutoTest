"""
要替换数据的来源有：
1、来自响应结果当中提取
2、来自脚本生成的数据(如phone)
3、来自配置文件..

替换，需要用到  re正则表达式   ，正则表达式 识别的变量是字符串类型 ，通过正则识别后返回的是列表，列表里的数据就是mark变量
"""
import re
import time
from faker import Faker
from Common.my_logger import logger
from Common.handle_phone import get_new_phone

def replace_case_with_re(case_dict,share_data_object):
    """
    将传进来的每条字典格式的用例，一条一条遍历，将里面 含有标记符mark的值都替换掉，从全局变量类里获取对应的值进行替换
    替换的值，来源于：
    1、如果是#phone#，则来自于脚本生成。需要一个未注册的手机号码  (这里根据项目业务来，本项目是 phone手机号)
    2、其他的mark，均从Data类的属性中获取

    :param case_dict: 从excel里读取出来的每一条用例，是字典格式
    :param share_data_object:  Data类的对象
    :return: 替换回去的测试数据  ，类型也为字典
    """
    # 第一步，将字典格式的用例case_dict转换为字符串
    case_str = str(case_dict)

    # 第二步，将替换后的字符串格式的用例数据进行标识符识别替换
    to_replace_mark_list = re.findall('#(\w+)#',case_str)

    # 第三步，依次判断是否有特殊的标识符需要单独替换，否则依次遍历从data类的实例变量进行替换值
    if to_replace_mark_list:
        logger.info("要替换的标识符有：{}".format(to_replace_mark_list))

        # 这里是做判断，该条用例中是否有phone这个标识符，如果有，调用生成手机号的脚本，然后替换
        if 'phone' in to_replace_mark_list:
            new_phone = get_new_phone()
            logger.info("有#phone#标识符，需要生成新的手机号码{}".format(new_phone))
            case_str = case_str.replace(f'#phone#',new_phone)

        if 'random_str' in to_replace_mark_list:
            # 生成随机数：今天的日期_20个随机字母
            cur_time = time.strftime("%Y%m%d", time.localtime())
            cur_str = Faker().pystr()
            random_str = cur_time + "_" + cur_str
            logger.info("有#random_str#标识符，需要生成新的随机数{}".format(random_str))
            case_str = case_str.replace(f'#random_str#',random_str)


        for mark in to_replace_mark_list:
            # 如果全局变量Data中有mark这个属性名
            if hasattr(share_data_object,mark):
                logger.info("将标识符{} 替换为{}".format(mark,getattr(share_data_object,mark)))
                # 使用全局变量Data类的mark属性值，去替换测试用例当中的#mark#  ;这里不用replace方法也可以，可以用正则的 sub也行
                # 这个部分  f"#{mark}#"   是指格式化 mark这个标识符，这样才能在依次遍历后找到要替换掉的标识符
                # 如果只是单纯的写成 “#mark#”,那表示去case_str里找  #mark# 这个字符串，但此时mark不是动态的，所以需要格式化使其动态的变成各种各样的标识符
                case_str = case_str.replace(f"#{mark}#", getattr(share_data_object,mark))
        logger.info("替换之后的用例数据为： \n{}".format(case_str))

    # 第四步，将已替换完成的字符串格式的用例数据转回字典格式
    new_case_str = eval(case_str)
    return new_case_str