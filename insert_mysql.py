import pymysql


class Insert(object):
    def __init__(self):
        # 打开数据库连接
        self.db = pymysql.connect("localhost", "root", "", "bilibili", charset='utf8')
        self.sql = """insert into video 
                        (aid, view, danmaku, reply, favorite, coin, share) 
                        values(%s, %s, %s, %s, %s, %s, %s)"""

    def run(self,video_list):
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        for row in video_list:
            try:
                cursor.execute(self.sql, row)
            except:
                self.db.rollback()
        self.db.close()
