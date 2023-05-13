import re

import requests


#下载网页内容
def download(url):
    if url is None:
        return None
    # 浏览器请求头
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
    headers={'User-Agent':user_agent}
    r = requests.get(url,headers=headers)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        return r.text
    return None

#提取百科词条简介
def get_data(html):
    #regex = re.compile('<meta name="description" content="(.*?)">')
    regex = re.compile('<div class="lemma-summary" label-module="lemmaSummary">(\s*)<div class="para" label-module="para">([\s\S]*?)</div>(\s*)</div>')
    #data = [('\n', 'Python是一种计算机程序设计语言。是一种动态的、面向对象的脚本语言，最初被设计用于编写自动化脚本(shell)，随着版本的不断更新和语言新功能的添加，越来越多被用于独立的、大型项目的开发。', '\n')]
    data = re.findall(regex, html)[0][1]
    return data
