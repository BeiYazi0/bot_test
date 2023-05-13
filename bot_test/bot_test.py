import typing
import sqlite3

import botpy
from botpy.message import Message

from config import appid,token
import myfun


def contentproc(content:str) -> typing.Tuple[str,str,str]:
    funs1={'一言':myfun.oneword,'洗入':myfun.dbupdate,'发病':myfun.essayget,
           '天气':myfun.cityweather,'历史':myfun.History,'热搜':myfun.resou,
           '运算':myfun.my_math,'身份':myfun.identify,'翻译':myfun.transproc,
           '百科':myfun.baikedataget,'卡池':myfun.cardpoolset}
    funs2={'丁真':myfun.DZ,'抽卡':myfun.CK,'萌图':myfun.randomimg}
    funs3={'报时':myfun.timecheck,'美图':myfun.stfind,'十连':myfun.tencards,
           '运势':myfun.fortuneget}
    funs4={'点歌':myfun.songplay,'颜值':myfun.facecheck,
           '二维':myfun.qrcodecreate,'动态':myfun.dynamic}
    funs5={"摸头":myfun.ruacreate}
    mycontent,url,localfile='','',''
    pat=content[0:2]
    infoproc=content[2:]
    curfun=funs1.get(pat)
    if curfun:
        mycontent=curfun(infoproc)
    curfun=funs2.get(pat)
    if curfun:
        mycontent='<@!%s> 你抽到了'%author
        url=curfun()
    curfun=funs3.get(pat)
    if curfun:
        if pat!='报时':
            mycontent='<@!%s> 你抽到了'%author
        localfile=curfun(infoproc)
    curfun=funs4.get(pat)
    if curfun:
        mycontent,url=curfun(infoproc)
    curfun=funs5.get(pat)
    if curfun:
        mycontent,url,localfile=curfun(infoproc)
    return mycontent,url,localfile

def funscheck():
    file='./help/funstable.txt'
    f=open(file)
    text=f.read()
    f.close()
    return '小鲨鱼有以下功能可用\n'+text

def helptxt():
    url='https://api.qrserver.com/v1/create-qr-code/?data=https://docs.qq.com/doc/DTUhNVVFNVGF0Y0du'
    return url

class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        funs={'帮助':helptxt}
        silencedic={'精致睡眠':'28800','午休':'3600','回笼觉':'1800'}
        _content = message.content.split(' ')
        _content = ' '.join(_content[1:])
        
        if _content=='憨批':
            user=message.author
            mycontent='哼！%s，人家不理你了'%user.username
            await self.api.post_message(channel_id=message.channel_id,content=mycontent,msg_id=message.id)
            try:
                await self.api.mute_member(guild_id=message.guild_id, user_id=user.id, mute_seconds='60')
            except:
                mycontent='仗着自己是管理员就欺负人家，真不要脸'
                await self.api.post_message(channel_id=message.channel_id,content=mycontent,msg_id=message.id)
        if silencedic.get(_content):
            user=message.author
            try:
                await self.api.mute_member(guild_id=message.guild_id, user_id=user.id, mute_seconds=silencedic[_content])
                mycontent='想睡就睡咯，%s'%user.username
                await self.api.post_message(channel_id=message.channel_id,content=mycontent,msg_id=message.id)
            except:
                mycontent='身为管理员还想要休息，给我去996'
                await self.api.post_message(channel_id=message.channel_id,content=mycontent,msg_id=message.id)
        if funs.get(_content):
            url=funs[_content]()
            await self.api.post_message(channel_id=message.channel_id,image=url,msg_id=message.id)
    
    async def on_message_create(self, message: Message):
        _content = message.content
        if _content==None or len(_content)<2:
            return
        if _content=='功能确认':
            funs=funscheck()
            await self.api.post_message(channel_id=message.channel_id,content=funs,msg_id=message.id)
        global author
        author=message.author.id
        _mentions = message.mentions
        if _mentions:
            try:
                _content=_content.split()[0]+_mentions[0].avatar
            except:
                return
        _attachment=message.attachments
        if _attachment:
            for obj in _attachment:
                _content=_content+'https://'+obj.url+' '
        mycontent,url,localfile=contentproc(_content)
        try:
            if localfile:
                 await self.api.post_message(channel_id=message.channel_id,content=mycontent,file_image=localfile,msg_id=message.id)
            elif url:
                 await self.api.post_message(channel_id=message.channel_id,content=mycontent,image=url,msg_id=message.id)
            elif mycontent:
                 await self.api.post_message(channel_id=message.channel_id,content=mycontent,msg_id=message.id)
        except:
            await self.api.post_message(channel_id=message.channel_id, content='发送失败', msg_id=message.id)



author=None
intents = botpy.Intents.all()
client = MyClient(intents=intents)
client.run(appid=appid, token=token)

