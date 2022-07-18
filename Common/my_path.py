"""
全局路径配置
"""

import os

# basedir  项目根路径
# abspath()  得到当前文件路径

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 拼接配置路径
# join是支持多个路径拼接的，进源码可以看到  join(xxxx,*path：xxx)

conf_dir = os.path.join(basedir,"Conf")

# 拼接 测试数据路径
testdata_dir = os.path.join(basedir,"testdatas")

# 日志路径
log_dir = os.path.join(basedir,"outputs","logs")

# 报告路径
report_dir = os.path.join(basedir,"outputs","reports")