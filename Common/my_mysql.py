import pymysql
import os
from Common.myConf import MyConf
from Common.my_path import conf_dir

class MyMySql:
    def __init__(self):
        # 实例化配置类对象
        conf = MyConf(os.path.join(conf_dir,"mysql.ini"))

        # 连接数据库
        # 1、连接数据库  -  占用数据库资源，所以注意在连接数据库得到查询结果后要断开连接，避免继续占用资源
        self.db = pymysql.connect(
            host=conf.get("mysql","host"),
            user=conf.get("mysql","user"),
            password=conf.get("mysql","passwd"),
            # 注意这里获得端口号是int型的格式，所以得用getint，用get得到字符串导致连接数据库出现问题会报错
            port=conf.getint("mysql","port"),
            database=conf.get("mysql","database"),
            charset="utf8",
            # 因为游标查询值返回的数据类型默认是元组，但改成字典类型更好，所以通过修改 cursorclass 使数据类型改变
            cursorclass=pymysql.cursors.DictCursor
        )

        # 2、创建游标
        self.cur = self.db.cursor()
        pass

    # 根据需求写一些方法
    # 如 返回数据库查询结果  、 返回一条数据，字典类型 、 返回多条数据   、 更新事务  、 关闭数据库连接

    # 返回数据库查询结果
    def get_count(self,sql):
        count = self.cur.execute(sql)
        return count

    # 返回一条数据库查询数据
    def get_one_data(self,sql):
        self.cur.execute(sql)
        return self.cur.fetchone()

    # 返回多条数据
    def get_many_data(self,sql,size=None):
        self.cur.execute(sql)
        if size:
            return self.cur.fetchmany(size)
        else:
            return self.cur.fetchmany()

    # 涉及到事务
    # 提交commit、回滚rollback
    # 没有执行成功就回滚，执行成功就提交
    def update_data(self, sql):
        try:
            self.cur.execute(sql)
        except:
            self.db.rollback()
        else:
            self.db.commit()

    # 关闭数据库连接
    def close_conn(self):
        self.cur.close()
        self.db.close()