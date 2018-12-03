import pymysql


def creat_table():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "bilibili", charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS video")

    # 创建数据表SQL语句
    sql = """CREATE TABLE video (
             aid  int,
             view  int,
             danmaku int,  
             reply int,
             favorite int,
             coin int,
             share int )"""

    cursor.execute(sql)
    db.close()