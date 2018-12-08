import requests
from bs4 import BeautifulSoup
import telnetlib


class IpPool(object):
    def __init__(self):
        # 爬虫开始准备
        self.url = 'http://www.xicidaili.com/wn/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
        }
        self.ip_list = []
        self.ip_pool = []
        self.get_ip_proxies()

    def get_ip_proxies(self):
        print("开始爬取ip.....")
        html = requests.get(url=self.url, headers=self.headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        trs = soup.find_all('tr')
        for tr in trs:
            try:
                tds = tr.find_all('td')
                # 连接Telnet服务器测试ip是否可用
                telnetlib.Telnet(tds[1].text, port=tds[2].text, timeout=1)
            except:
                pass
            else:
                # 把可以用的ip放进列表
                self.ip_list.append(tds[1].text + ':' + tds[2].text)

        for ip in self.ip_list:  # 把ip设置为字典，方便调用
            proxies = {
                'https': "https://" + ip
            }
            self.ip_pool.append(proxies)
        print("ip爬取结束.....")
        return self.ip_pool
