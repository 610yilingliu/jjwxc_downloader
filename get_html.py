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

def get_urls(cat_url, header):
    r = requests.get(cat_url, headers = header)
    r.encoding = 'gb2312'
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title').getText()
    summary = soup.find('tr').getText() + '\n\n\n'
    pref = title + '\n\n\n\n' + summary
    urls = soup.findAll(name = 'a')
    to_find = []
    for u in urls:
        txt = u.get('href')
        if txt:
            if 'chapterid' in txt:
                to_find.append(txt)
        else:
            if 'rel' in u.attrs:
                if  u.attrs['rel']:
                    link = u.attrs['rel'][0]
                    if 'buy' not in link:
                        to_find.append(link)
    text_name = title + '.txt'
    invalid_chars = '|><&'
    for char in invalid_chars:
        text_name = text_name.replace(char, ' ')
    # if any content in the target file, cover it
    f = open(text_name, 'w', encoding= 'utf-8')
    f. write(pref)
    f.close()

    for link in to_find:
        content = get_source(link, header)
        with open(text_name, 'a', encoding= 'utf-8') as f:
            f.write(content)


def get_source(url, header):
    r = requests.get(url, headers = header)
    r.encoding = 'gb2312'
    html = r.text

    soup = BeautifulSoup(html,'html.parser')
    text = soup.find(class_="noveltext")
    content_inside_text = text.prettify()
    soup = BeautifulSoup(content_inside_text, 'html.parser')
    # remove JJ attributes
    rm_jj_attr = soup.find_all('div', attrs = {"style": "width: 100%; text-align: center;"})
    for match in rm_jj_attr:
        match.decompose()
    # remove script, span, links
    to_del = soup.findAll(['script', 'span', 'a'])
    for match in to_del:
        match.decompose()
    # remove float comments
    to_del2 = soup.findAll(class_="float_comment")
    for match in to_del2:
        match.decompose()
    clean_text = soup.get_text()
    clean_text = clean_text.lstrip()
    # remove extra white space at the start of novel
    clean_text = clean_text.replace('\n\n\n\n\n\n\n\n', '\n\n\n', 1)
    # remove extra space in zuohua
    clean_text = clean_text.replace('\n\n\n\n\n\n\n\n\n', '\n\n', 1)
    clean_text += '\n\n\n\n\n'
    return clean_text




if __name__ == '__main__':
    cookie = "__cfduid=d827ac22305d70a3712d3681b956f5caf1607762122; __gads=ID=fbafde2c32391030:T=1607762130:S=ALNI_MYYdBt93gH5AYoyekLYyo8KPd0yHQ; UM_distinctid=17656174925b38-09c8968744b308-4313f6b-1fa400-17656174926aa3; timeOffset_o=1108.5; CNZZDATA30075907=cnzz_eid%3D904510376-1607760153-http%253A%252F%252Fmy.jjwxc.net%252F%26ntime%3D1607916757; testcookie=yes; Hm_lvt_bc3b748c21fe5cf393d26c12b2c38d99=1607762121,1607921296; nicknameAndsign=2%257E%2529%2524%25E9%25A3%258E%25E9%2580%259D%25E6%2597%25A0%25E6%25AE%2587; token=Mzk2OTEyOTh8OGI3ZTI2MmQ5MWM0ZWQxOTFlZDg2NjBlYzY1MDMzZjV8fHx8NDMyMDB8MXx8fFFR55So5oi3fDF8dGVuY2VudHwx; JJEVER=%7B%22fenzhan%22%3A%22noyq%22%2C%22ispayuser%22%3A%2239691298-1%22%2C%22foreverreader%22%3A%2239691298%22%2C%22desid%22%3A%22Mu2xJjeIHWhlg7eJ5VbdLSNrArpgUrVu%22%2C%22sms_total%22%3A%222%22%2C%22user_signin_days%22%3A%2220201214_39691298_0%22%7D; JJSESS=%7B%22nicknameAndsign%22%3A%22undefined%7E%29%2524%22%2C%22clicktype%22%3A%22%22%2C%22sidkey%22%3A%227XRuaPxhbwWlLoOFYdfG5IDmSvCVinzt0yM%22%7D; Hm_lpvt_bc3b748c21fe5cf393d26c12b2c38d99=1607921374"
    h = modify_headers(cookie)
    url = "http://www.jjwxc.net/onebook.php?novelid=2423737"
    get_urls(url, h)
    # with open('test.txt', 'w', encoding = 'utf-8') as f:
    #     f.write(text)
