import requests
from Get_ip import IpPool
import random
import pymysql
import time


class GetInfo(object):
    def __init__(self):
        self.ip_pool = IpPool()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
            'Connection': 'keep-alive',
            'Host': 'api.bilibili.com',
            'Origin': 'https://www.bilibili.com',
        }
        self.URL_VIDinfo = "http://api.bilibili.com/archive_stat/stat?aid="  # b站视频信息api

        self.db = pymysql.connect("localhost", "root", "", "bilibili", charset='utf8')
        self.cursor = self.db.cursor()
        self.sql = """insert into video
                    (aid, view, danmaku, reply, favorite, coin, share)
                    values(%s, %s, %s, %s, %s, %s, %s)"""

    def download(self, start, end):
        for video_id in range(start, end):
            try:
                video_list = []
                proxies = random.choice(self.ip_pool.ip_pool)
                response = requests.get(url=self.URL_VIDinfo + str(video_id), headers=self.headers,
                                        proxies=proxies).json()

                data = response['data']
                video_info = (
                    data['aid'], data['view'], data['danmaku'],
                    data['reply'], data['favorite'], data['coin'], data['share'])
                video_list.append(video_info)
            except:
                print("AV:%09d 视频已不存在" % video_id)
            else:
                try:
                    for row in video_list:
                        self.cursor.execute(self.sql, row)
                except Exception as e:
                    print(e)
                else:
                    time.sleep(1)
        self.cursor.close()
        self.db.commit()
        self.db.close()  # 关闭数据库
