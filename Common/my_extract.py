"""
从响应结果中提取值，并设置为全局变量(Data类作为本框架的全局变量类)
1、提取表达式：放到excel当中
    (可能提取1个，可能提取多个。。。以表达式个数为准)
2、提取出来之后，设置为Data类属性

从响应结果当中提取值，并设置为Data类的属性
    setattr(对象/类，attr属性，value)        # 给xx设置属性
    getattr(对象/类)                       # 获取xx属性
    hasattr(对象/类)                       # 判断是否有这个属性， 有就是True  没有就是False
    delattr(对象/类)                       # 删除这个属性

# setattr(全局变量类,"属性名","属性值")
# hasattr(全局变量类，"属性名")
# getattr(全局变量类，"属性名")
"""

import jsonpath
from Common.my_logger import logger

def extract_data_from_response(extract_epr,response_dict,share_data_obj):
    """
    :param extract_epr: 从excel测试用例里提取的extract列，列里是一个提取表达式，提取出来是一个字典形式的字符串。
                        key为全局变量名，value为jsonpath提取式。
                        例：'{"token":"$..token","member_id":"$..id","leave_amount":"$..leave_amount"}'
    :param response_dict: http请求之后的响应结果，字典类型
    :param share_data_obj: Data类的实例化对象，用来替换Data类 (方便多并发)
    :return: None
    """

    # 1、将提取出来的extract列由字符串转换为字典
    extract_dict = eval(extract_epr)

    # 2、遍历1中的字典，key是全局变量名,value是jsonpath表达式
    for key,value in extract_dict.items():
        # 根据jsonpath从响应结果中提取真正的值，value就是jsonpath表达式
        logger.info("提取的变量名为:{},提取的jsonpath表达式为:{}".format(key, value))
        result = jsonpath.jsonpath(response_dict,value)
        logger.info("jsonpath提取之后的值为:{}".format(result))
        # jsonpath在response响应中找到了值，就会返回列表，找不到就返回False
        # 如果提取到了真正的值，那么将它设置为Data类的属性，key是全局变量名，result[0]就是提取后的值
        if result:
            setattr(share_data_obj,key,str(result[0]))
            logger.info("提取的变量名为:{},提取的值为:{}，并设置为Data类实例化对象的属性和值".format(key, str(result[0])))



