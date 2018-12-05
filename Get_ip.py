import requests
from bs4 import BeautifulSoup
import telnetlib


class IP(object):
    def __init__(self):
        self.url = 'http://www.xicidaili.com/wn/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
        }
        self.ip_list = []
        self.ip_proxies = []
        self.get_ip_proxies()

    def get_ip_proxies(self):
        html = requests.get(url=self.url, headers=self.headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        trs = soup.find_all('tr')
        for tr in trs:
            try:
                tds = tr.find_all('td')
                # 连接Telnet服务器测试ip是否可用
                telnetlib.Telnet(tds[1].text, port=tds[2].text, timeout=5)
            except:
                pass
            else:
                self.ip_list.append(tds[1].text + ':' + tds[2].text)
        for ip in self.ip_list:
            proxies = {
                'https': "https://" + ip
            }
            self.ip_proxies.append(proxies)
        return self.ip_proxies
