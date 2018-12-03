import pymysql


def creat_table(video_list):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "", "bilibili", charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = """insert into video 
            (aid, view, danmaku, reply, favorite, coin, share) 
            values(%s, %s, %s, %s, %s, %s, %s)"""
    for row in video_list:
        try:
            cursor.execute(sql, row)
        except:
            db.rollback()
    cursor.execute(sql)
    db.close()