"""
python多线程插件
官方文档：  https://pypi.org/project/pytest-parallel/

多线程
但本次不用它，
用多线程threading 和 线程池ThreadPoolExecutor

线程池：一个池子，可以开5个线程，异步执行

解决了什么问题呢？
每个表单和表单之间可以异步执行，表单内部是顺序/同步执行的

1、设置线程池数目：
executor = concurrent.futures.ThreadPoolExecutor(max_worker=5)

2、使用submit函数来提交线程需要执行的任务到线程池中，并返回该任务的句柄；
executor.submit(函数名,参数)

3、通过使用done()方法判断该任务是否结束

4、as_completed()方法，当某个任务结束了，就给主线程返回结果。
直接用result()获得返回结果
as_completed()方法是一个生成器，在没有任务完成的时候，会一直阻塞



注意:
每一个表单下的用例是一个任务，有多少个表单就有多少任务
1、pytest.ini 中添加标记
2、测试类添加标记

"""

import concurrent.futures
import pytest
import os

from Common.my_path import basedir
from Common.myConf import MyConf

# 从配置文件里读取所有的标签名字，本项目放在了pytest.ini里,意味着有多少个任务
marks_str = MyConf(os.path.join(basedir,"pytest.ini")).get("pytest","markers")
marks =marks_str.split("\n")[1:]
print(marks)


# 定义一个方法,此方法用来收集每个接口的测试用例，并执行它
# 需要事先准备：接口名称
def run_cases(mark_name):
    pytest.mark(["--alluredir=outputs/reports","-m","{}".format(mark_name)])


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_cases = {}
    # 提交子任务
    for mark in marks:
        task = executor.submit(run_cases,mark)
        future_to_cases[task] = mark

    print(future_to_cases)
    # 等待子任务完成
    for future in concurrent.futures.as_completed(future_to_cases):
        # mark = future_to_cases[future]
        try:
            res = future.result()
            print(res)
        except Exception as exc:
            print('generated an exception: %s' % (exc))