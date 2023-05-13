import re
import sqlite3
import socket
import random
import json,html
from time import ctime,time
from urllib.request import urlretrieve

import cv2
import requests
from bs4 import BeautifulSoup
from PIL import Image,ImageSequence

import cardpool
import translate
from calculate import calc
from baike import download,get_data
from imgurl import imgurlget
from RUA import rua
from Fortune import drawing


def my_math(eps:str):
    if eps:
        return calc(eps)
    else:
        return '格式错误'

def timecheck(content:str):
    xpos=[200,150,280,80,122,160,200,200,275,250]
    ypos=[325,190,480,150,155,290,350,205,310,455]
    size=[1.8,1.6,2.7,1.6,1.3,2,2,1.6,3,2.9]
    maxn=10
    if content:
        n=int(content)
    else:
        n=random.randint(1,maxn)
    if n>maxn:
        n=maxn
    if n==7:
        n=6
    file='./time/%d.jpg'%n
    bk_img = cv2.imread(file)
    time=ctime().split(' ')[3]
    pos=(xpos[n-1],ypos[n-1])
    bk_img2=cv2.putText(bk_img,time, pos, cv2.FONT_HERSHEY_SIMPLEX, 
    size[n-1],(0,0,0), 5, cv2.LINE_AA)
    time_img="./time/time.jpg"
    cv2.imwrite(time_img,bk_img2)
    with open(time_img,'rb') as img:
        image=img.read()
    return image

def stfind(content:str):
    maxn=1125
    if content:
        n=int(content)
    else:
        n=random.randint(1,maxn)
    if n>maxn:
        n=maxn
    print(n)
    file='./imgs/%d.jpg'%n
    with open(file,'rb') as img:
        image=img.read()
    return image

def dbupdate(content:str):
    dbdic={'丁真':'./mydb/丁真库.db','抽卡':'./mydb/抽卡库.db',
           #'报时':'./mydb/time库.db'
           '萌图':'./mydb/萌图库.db'}
    error=''
    if len(content)>10:
        content=content.rstrip().replace('\n','')
        dicobj=content[0:2]
        urls=content[2:].split()
        if dbdic.get(dicobj):
            dbobj=dbdic[dicobj]
            curdb=sqlite3.connect(dbobj)
            for i,url in enumerate(urls):
                if url[0:8]!=r'https://' and url[0:7]!=r'http://':
                    error+='图%d'%(i+1)
                    continue
                sql = '''insert into relationship (url) values ("%s")''' %url
                curdb.execute(sql)
                curdb.commit()
        else:
            return '不存在该库'
    else:
        return '洗入格式错误'
    if error=='':
        return '洗入成功'
    else:
        return error+'洗入失败'

def DZ():
    curdb=sqlite3.connect('./mydb/丁真库.db')
    xka = curdb.cursor()
    xka.execute("select * from relationship")
    result = xka.fetchall()
    xka.close()
    maxn=len(result)
    random.seed(time())
    n=random.randint(1,maxn)
    url=result[n-1][1]
    return url

def CK():
    curdb=sqlite3.connect('./mydb/抽卡库.db')
    xka = curdb.cursor()
    xka.execute("select * from relationship")
    result = xka.fetchall()
    xka.close()
    maxn=len(result)
    random.seed(time())
    n=random.randint(1,maxn)
    url=result[n-1][1]
    return url

def songplay(content:str):
    command_len = content.split()
    base_url = "https://c.y.qq.com/splcloud/fcgi-bin/smartbox_new.fcg"
    music_data = requests.get(url=base_url, params={"key": command_len[0].strip()})
    music_datas = music_data.json()["data"]["song"]["itemlist"]
    try:
        music_name = music_datas[0]["name"]
        music_singer = music_datas[0]["singer"]
        music_url = "https://y.qq.com/n/ryqq/songDetail/" + music_datas[0]["mid"]
        music_mid = music_datas[0]["mid"]
        if len(command_len) > 1:
            for music_data in music_datas:
                if command_len[1].strip() in music_data["singer"]:
                    music_name = music_data["name"]
                    music_singer = music_data["singer"]
                    music_url = "https://y.qq.com/n/ryqq/songDetail/" + music_data["mid"]
                    music_mid = music_data["mid"]
    except IndexError:
        return "未找到该音乐",''
    music_url='https://api.qrserver.com/v1/create-qr-code/?data='+music_url
    mycontent='歌名：%s\n演唱：%s\n'%(music_name,music_singer)
    print(music_url)
    return mycontent,music_url

def randomimg():
    try:
        url = 'http://www.dmoe.cc/random.php'
        params = {'return': 'json'}
        res = requests.get(url, params=params).json()
        image_url=res['imgurl']
        content='萌图%s'%image_url
        dbupdate(content)
    except:
        image_url='-'
    return image_url

def cityweather(content:str):
    # 1、发送请求，获取数据
    url = f'http://wthrcdn.etouch.cn/weather_mini?city={content}'
    res = requests.get(url)
    res.encoding = 'utf-8'
    res_json = res.json()

    # 2、数据格式化
    if not res_json.get('data'):
        return '获取失败'
    data = res_json['data']
    city = f"城市：{data['city']}\n"  
    # 字符串格式化的一种方式 f"{}" 通过字典传递值

    today = data['forecast'][0]
    date = f"日期：{today['date']}\n"  
    now = f"实时温度：{data['wendu']}度\n"
    temperature = f"温度：{today['high']} {today['low']}\n"
    fengxiang = f"风向：{today['fengxiang']}\n"
    types = f"天气：{today['type']}\n"
    tips = f"贴士：{data['ganmao']}"

    result = city + date + now + temperature + fengxiang + types + tips
    return result

def History(content:str):
    month,day='',''
    if content!='':
        try:
            month,day=content.split('-')
        except:
            return '格式错误'
    result=''
    for i in range(1, 3):
        url = "http://jintian.160.com/ashx/GreatThing.ashx?act=getgreatthinglist&page=%s&m=%s&d=%s&c=" % (str(i), month, day)
        params = {'return': 'json'}
        data = requests.get(url,params=params).json()
        if data["data"]=='':
            return '请求错误'
        html = BeautifulSoup(data["data"],"html.parser")
        data_li = html.find_all("li")
        for li in data_li:
            r = li.text[1:]
            tmp = r.split()
            year = tmp[0].split("年")[0]
            temp=' '.join(tmp[1:])
            result += '\n'+year+'年 '+temp.replace("（图）",'')
    res='历史上的今天：'+tmp[0].split("年")[1]+result
    print(res)
    return res

def oneword(content:str):
    suo_url='https://v1.hitokoto.cn'
    dic={'动画':'a','漫画':'b','游戏':'c','文学':'d','原创':'e','网络':'f',
         '其他':'g','影视':'h','诗词':'i','网易云':'j','哲学':'k','抖机灵':'l'}
    r=dic.get(content)
    params={'c':r}
    try:
        res = requests.get(suo_url,params=params)
    except:
        return '请求失败'
    res.encoding = 'utf-8'
    r = res.json()
    res=r['hitokoto']+'\n出处：'+r['from']+'\n作者：'
    if r['from_who']:
        res+=r['from_who']
    else:
        res+='无'
    return res

def resou(content:str):
    url='https://tenapi.cn/resou'
    res = requests.get(url)
    if str(res)!='<Response [200]>':
        return '请求失败'
    r=res.json()["list"]
    result='微博热搜榜'
    for i,obj in enumerate(r):
        result+='\n%d、%s %d'%(i+1,obj["name"],obj["hot"])
    return result

def ruacreate(content:str):
    if content:
        filename='./rua/source.png'
        try:
            urlretrieve(content,filename=filename)
        except:
            return '格式错误','',''
        au=rua(filename).add_gif()
        file='./rua/dem.gif'
        #方案：本地直接传
        with open(file,'rb') as img:
            image=img.read()
        return '','',image
        #curdb=sqlite3.connect('./mydb/摸头库.db')
        #xka = curdb.cursor()
        #xka.execute("select * from relationship")
        #result = xka.fetchall()
        #xka.close()
        #maxn=len(result)
        #key='dem%d.gif'%maxn
        #备选方案：借助七牛云获取链接
        #url=imgurlget(file,key)
        #sql = '''insert into relationship (url) values ("%s")''' %url
        #curdb.execute(sql)
        #curdb.commit()
    else:   
        curdb=sqlite3.connect('./mydb/摸头库.db')
        xka = curdb.cursor()
        xka.execute("select * from relationship")
        result = xka.fetchall()
        xka.close()
        maxn=len(result)
        random.seed(time())
        n=random.randint(1,maxn)
        url=result[n-1][1]
        print(url)
    return '',url,''

def facecheck(content:str):
    url='https://yang520.ltd/api/XiaoIceBeauty.php'
    params={'url':content}
    res=requests.get(url,params=params)
    r=res.json()
    if r["code"]==200:
        return '',r["url"]
    else:
        if r["message"]:
            return r["message"],''
        else:
            return '请求失败，换一张试试',''

def identify(content:str):
    url='http://yuanxiapi.cn/api/idcard/'
    params={'number':content}
    print(content)
    res=requests.get(url,params)
    r=res.json()
    if r["msg"]!='查询成功':
        return r["msg"]
    result='查询成功\n身份证号：%s\n性别：%s\n出生日期：%s\n年龄：%s\n生肖：%s\n星座：%s\n地区：%s'%(
        r["num"],r["sex"],r["time"],r["age"],r["animal"],r["sign"],r["add"])
    return result

def baikedataget(keyword:str):
    url = 'http://baike.baidu.com/item/{}'.format(keyword)
    html_cont = download(url)
    try:
        data = get_data(html_cont)
        data = re.sub(r'<([\s\S]*?)>|&nbsp;|\n','',data)
        return data
    except Exception as e:
        return keyword+'词条不存在，爬取失败'

def qrcodecreate(content:str):
    url='https://api.qrserver.com/v1/create-qr-code/?data='
    code=str(content.encode('utf-8'))[2:-1]
    code=code.replace('\\x','%')
    return '',url+code

def transproc(content:str) -> str:
    if content=='谢谢小鲨鱼':
        global modedic
        modedic[idx]=1
        return '不用谢，已退出翻译模式'
    dic={'英中':1,'中英':2,'日英':3,'日中':4}
    transmode=dic.get(content[0:2],0)
    if transmode==0:
        return '无法以指定语言翻译'
    content=content[2:]
    if content=='':
        return '格式错误'
    if transmode==1:
        content=content.split('.')
        opr='.'
    else:
        content=content.split('。')
        opr='。'
    if content[-1]==opr:
        content=content[:-1]
    res=''
    for obj in content:
        ok, strs = translate.trans(obj+opr,transmode)
        if ok:
            res+=strs
        else:
            res+='对不起，翻译失败。'
    return res

def essayget(content:str):
    if content=='':
        return '格式错误'
    curdb=sqlite3.connect('./mydb/发病库.db')
    xka = curdb.cursor()
    xka.execute("select * from relationship")
    result = xka.fetchall()
    xka.close()
    maxn=len(result)
    random.seed(time())
    n=random.randint(1,maxn)
    text=result[n-1][1]
    text=text.replace('镜华',content)
    return text

def dynamic(content:str):
    if content:return '',''
    url='https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history'
    params={'host_uid':353840826}
    res=requests.get(url,params)
    r=res.json()['data']["cards"][0]
    source='https://t|bilibili|com/'+r["desc"]["dynamic_id_str"]
    p=json.loads(r["card"])
    try:
        text=p["item"]["description"].replace('.','|')
        url=p["item"]["pictures"][0]["img_src"]
    except:
        try:
            p=json.loads(p["origin"])
            text=p["item"]["description"].replace('.','|')
            url=p["item"]["pictures"][0]["img_src"]
        except:
            try:
                text=p["dynamic"].replace('.','|')
                url=p["pic"]
            except:
                return '获取失败',''
    result='公主连结ReDive的bilibili动态:\n'+source+'\n---------\n'+text
    return result,url

def tencards(content:str):
    if content:return
    cardpool.gacya()
    file='./princessimage/out.png'
    with open(file,'rb') as img:
        image=img.read()
    return image

def cardpoolset(content:str):
    pat=content[0:2]
    info=content[2:]
    if pat=='设定':
        return cardpool.set_gacya(info)
    elif pat=='up':
        return cardpool.upset(info)

def fortuneget(content:str):
    if content: return
    drawing()
    file='./pcr-fortune/output.png'
    with open(file,'rb') as img:
        image=img.read()
    return image

    