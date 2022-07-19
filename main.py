# 使用pytest收集所有的用例并运行，输出allure报告
import pytest


if __name__ == '__main__':
    pytest.main(['-s','-v','./testcase','--alluredir=outputs/reports'])



