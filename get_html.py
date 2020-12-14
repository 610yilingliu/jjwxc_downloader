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




