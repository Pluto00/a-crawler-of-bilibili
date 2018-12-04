import requests
from bs4 import BeautifulSoup


def get_ip_list(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
    }

    html = requests.get(url, headers=headers)

    soup = BeautifulSoup(html.text, 'html.parser')

    trs = soup.find_all('tr')

    ip_list = []

    for tr in trs:
        try:

            tds = tr.find_all('td')

            ip_list.append(tds[1].text + ':' + tds[2].text)

        except:
            pass

    return ip_list


if __name__ == '__main__':

    url = 'http://www.xicidaili.com/wn/'

    ip_list = get_ip_list(url)

    for ip in ip_list:
        proxies = {
            'https': "https://" + ip
        }
        print(proxies)
