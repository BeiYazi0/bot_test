# -*- coding:utf-8 -*-
import os
import random as rd

from PIL import Image


png_dir = os.getcwd() + '\\princessimage\\'

gacya3 = ['中二.png',
        '狐狸.png',
        '妹弓.png',
        '星法.png',
        '驴.png',
        '魅魔.png',
        '咲恋.png',
        '望.png',
        '扇子.png',
        '哈哈剑.png',
        'xcw.png',
        '智.png',
        '狼.png',
        '伊利亚.png',
        '黑骑.png',
        '姐姐.png',
        '毛二力.png',
        '流夏.png',
        '吉塔.png',
        '亚里莎.png',
        '龙拳.png',
        '龙锤.png',
        '水女仆.png',
        '水猫剑.png'
        '安.png',
        '古蕾娅.png',
        '江m.png',
        '忍扇.png',
        '生菜.png',
        '华哥.png',
        '切噜.png',
        'u2.png',
        '万圣兔.png',
        '露娜.png',
        '圣伊.png',
        '魔驴.png',
        '武松.png',
        '奶牛骑.png',
        '爽弓.png',
        '水七七香.png',
        '水纯.png']

gacya2 = ['跳跳虎.png',
        '妹法.png',
        '布丁.png',
        '雪哥.png',
        '七七香.png',
        '圣母.png',
        '暴击弓.png',
        '狗拳.png',
        '美美.png',
        '熊锤.png',
        '松鼠.png',
        '病娇.png',
        '忍.png',
        '真阳.png',
        '栞.png',
        '千歌.png',
        '空花.png',
        '猫剑.png',
        '子龙.png',
        '深月.png',
        '裁缝.png']

gacya1 = ['猫拳.png',
        '剑圣.png',
        '炸弹人.png',
        '铃铛.png',
        '姐法.png',
        '女仆.png',
        '黄骑.png',
        '香菜.png',
        '大眼.png',
        '羊驼.png',
        '路人妹.png']

fesgacya = ['克总.png',
        '511.png',
        '似似花.png',
        '公主佩可.png',
        '蝶妈.png',
        '公主优衣.png']

ups=['凛','春妈','春猫','水狼','圣锤','水流夏','水猫剑','水吃','圣克','卯月','情姐','环奈',
     '万圣忍','春环','蕾姆','水星','水电','春黑','水暴','艾米莉亚','春田','圣千','水女仆',
     '水黑','水狐','万圣大眼','猫仓唯']

up = ['猫仓唯.png']
fes = 0
isdouble = 0
background = Image.new('RGBA',(330,135),color='lavenderblush')
#up,3星,2星,1星
ordinary=[0.7,1.8,20.5,77]#普通
double=[1.4,3.6,18,77]#双倍

def gacya():
    gacya_3= gacya3
    result = []
    msg=''
    p=ordinary
    sup,s3,s2=100-p[0],100-p[0]-p[1],p[3]
    if fes==1:
        p=double
        gacya_3+=fesgacya
    if isdouble==1:
        p=double
    for n in range(9):
        i = rd.random()*100
        if i >= sup:                     #up
            result.append(rd.choice(up))
        elif i >= s3 and i < sup:       #3星
            result.append(rd.choice(gacya_3))
        elif i >= s2 and i < s3:       #2星
            result.append(rd.choice(gacya2))
        else :                           #1星
            result.append(rd.choice(gacya1))
    result.append(rd.choice(gacya2)) if (rd.random()*100 < s3) else result.append(rd.choice(gacya_3+up))
    a=0
    for x in range(5):
        for y in range(2):
            pic=Image.open(png_dir+result[a])

            background.paste(pic,(x*65+5,y*65+5))
            a+=1
    background.save(png_dir+'out.png')
    
def set_gacya(content:str):
    global fes,isdouble,up
    if content=='fes':
        fes=1
        isdouble=0
        up=[fesgacya[-1]]
        return '设定完成，现在是fes池，up角色为'+up[0].replace('.png','')
    elif content=='双倍':
        fes=0
        isdouble=1
        up=[ups[-1]+'.png']
        return '设定完成，现在是双倍池，up角色为'+ups[-1]
    elif content=='普通':
        fes=0
        isdouble=0
        up=[ups[-1]+'.png']
        return '设定完成，现在是普通up池，up角色为'+ups[-1]
    elif content=='':
        if fes==1:
            return '当前为fes池，up角色为'+fesgacya[-1].replace('.png','')
        elif isdouble==1:
            res=''
            for obj in up:
                res+=obj.replace('.png',' ')
            return '当前为双倍池，up角色为'+res
        else:
            res=''
            for obj in up:
                res+=obj.replace('.png',' ')
            return '当前为普通up池，up角色为'+res
    else:
        return '没有这样设置的卡池哦'

def upset(content:str):
    if fes==1:
        return 'fes池以最新fes角色作为up，不可设置'
    if content=='':
        return '当前可设置up角色：\n'+' '.join(ups)
    item=content.split()
    items=[]
    for obj in item:
        if obj not in ups:
            return obj+'不在可设置的up角色中，请在以下角色中选择\n'+' '.join(ups)
        items.append(obj+'.png')
    global up
    up=items
    return 'up设置成功，up角色为\n'+content


