# 使用pytest收集所有的用例并运行，输出allure报告
import os
import pytest
from Common.my_path import report_dir

if __name__ == '__main__':
    pytest.main(['-s','-v','./testcase',"allure={}".format(report_dir)])



