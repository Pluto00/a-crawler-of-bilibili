import pymysql


class Creat(object):
    def __init__(self):
        # 打开数据库连接
        self.db = pymysql.connect("localhost", "root", "", "bilibili", charset='utf8')
        # 创建数据表SQL语句
        self.sql = """CREATE TABLE video (
                     aid  VARCHAR(11),
                     view  VARCHAR(11),
                     danmaku VARCHAR(11),  
                     reply VARCHAR(11),
                     favorite VARCHAR(11),
                     coin VARCHAR(11),
                     share VARCHAR(11) )"""

    def run(self):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        # 如果数据表已经存在使用 execute() 方法删除表。
        cursor.execute("DROP TABLE IF EXISTS video")
        cursor.execute(self.sql)
        self.db.close()


t = Creat()
t.run()
