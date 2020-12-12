import requests
from bs4 import BeautifulSoup

def modify_headers(cookie_str):
    """
    :type cookie_str: String, cookie copy from chrome dev tool
    :rtype headers: Dictionary, generated header information
    """
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
    }
    if cookie_str:
        headers["Cookie"] = cookie_str
    return headers

def get_source(url, header):
    r = requests.get(url, headers = header)
    r.encoding = 'gb2312'
    html = r.text
    soup = BeautifulSoup(html,'html.parser')



if __name__ == '__main__':
    cookie = "__cfduid=d827ac22305d70a3712d3681b956f5caf1607762122; Hm_lvt_bc3b748c21fe5cf393d26c12b2c38d99=1607762121; testcookie=yes; __gads=ID=fbafde2c32391030:T=1607762130:S=ALNI_MYYdBt93gH5AYoyekLYyo8KPd0yHQ; UM_distinctid=17656174925b38-09c8968744b308-4313f6b-1fa400-17656174926aa3; CNZZDATA30075907=cnzz_eid%3D1115529935-1607760153-http%253A%252F%252Fwww.jjwxc.net%252F%26ntime%3D1607760153; timeOffset_o=799.800048828125; token=Mzk2OTEyOTh8NDBjYmM1Y2QwMTg2YjJiZjFhZjU4NWUyNGE2ODZiYmJ8fHx8NDMyMDB8MXx8fFFR55So5oi3fDF8dGVuY2VudHwx; JJEVER=%7B%22fenzhan%22%3A%22noyq%22%2C%22ispayuser%22%3A%2239691298-1%22%2C%22foreverreader%22%3A%2239691298%22%2C%22desid%22%3A%224wTKVJKx6%2BUx5%5C%2FSbp5d%2BIMyqThsfTgqL%22%2C%22sms_total%22%3A%222%22%2C%22user_signin_days%22%3A%2220201212_39691298_0%22%7D; JJSESS=%7B%22sidkey%22%3A%22yMilCs7mINTVLSGpEYgUqZ4PnB8rR1%22%2C%22nicknameAndsign%22%3A%222%257E%2529%2524%25E9%25A3%258E%25E9%2580%259D%25E6%2597%25A0%25E6%25AE%2587%22%2C%22clicktype%22%3A%22%22%7D; Hm_lpvt_bc3b748c21fe5cf393d26c12b2c38d99=1607764200"
    h = modify_headers(cookie)
    url = "http://my.jjwxc.net/onebook_vip.php?novelid=3999464&chapterid=34"
    get_source(url, h)
    
