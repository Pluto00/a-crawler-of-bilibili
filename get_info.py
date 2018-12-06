import requests


class Get_info(object):
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
            'Connection': 'keep-alive',
            'Host': 'api.bilibili.com',
            'Origin': 'https://www.bilibili.com',
        }
        self.video_list = []

        self.URL_VIDinfo = "http://api.bilibili.com/archive_stat/stat?aid="  # b站视频信息api

    def download(self):
        for video_id in range(1, 10):
            try:
                response = requests.get(url=self.URL_VIDinfo + str(video_id), headers=self.headers).json()
                data = response['data']
                video_info = (
                    data['aid'], data['view'], data['danmaku'],
                    data['reply'], data['favorite'], data['coin'], data['share'])
                self.video_list.append(video_info)
            except:
                print("AV:%09d 视频已不存在" % video_id)