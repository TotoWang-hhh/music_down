# 优化后亲测可用！免费下载QQ音乐大部分资源
---
## 由 吾爱破解论坛 珍珠奶茶丶板牙 制作于 2018年7月
### 由 吾爱破解论坛 zac7 改于 2019年8月
### 由 CSDN博客 tt68686（即人工智障） 再改于2020年5月 （V 2.0）
### 由 人工智障 再改于2020年5月 （你正在使用的）
---
# 通知栏

因为未知问题，目前3.0及更早、4.0（未在GitHub发布）等版本<b>已经全部不可用</b>，如果您仍需要使用相关功能，可以尝试各种crx插件。<b>本人这段时间内将不再更新Music Area！</b>

底下都是历史消息，我努力地把几乎所有功能都加上了，除了帮助文档实在没时间写。

因为时间原因，目前只添加了原计划的部分功能，仅用于尝鲜，最终版本可能会增加“帮助”和“提示栏”。另外，V3.3的最终版本可能会发布打包版。敬请期待！（该版本已经过测试，绝对稳定！）

最近因为学习任务繁重（作业太多）以后会减慢更新速度（特别是打包版，可能会比Python版慢1到3倍）

---
眼看着网上许多下歌的插件用不了了，又不想买VIP，便非常着急。
突然我想到了接口这玩意儿，于是我······
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200530114833205.png)
奥我真是个人才！
突然我看见了某人写过的代码，发现部分功能已经失效了，就修复了一下。
## 版权问题（反正你们也不会看的）
这玩意儿已经被驳回了，~~被迫加上这些累赘~~ ······应该不会再有问题了。
原网页没有任何版权保护。
关于音乐，你们最好去支持正版。~~不然我一拳揍死你~~ 
**好吧如果这还能有问题我只能CV大法了**
本工具只用作个人学习研究，禁止用于商业及非法用途，如产生法律纠纷与本人无关。如果需要保存音乐，请自行去各个网站下载正版。
[TOC]
## 正在完成的更改
 - [x] 修复BUG
 - [x] 调整路径
 - [x] 脱离黑底白字（可视化界面）
 - [x] 精美界面
 - [x] 增加搜索条目数调整功能
 - [x] 删去Consle中的调试信息

## 上代码（代码为版本x.0的源码，版本可能不是最新的，敬请谅解！）

```python
#导入库
import requests
import json
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox
import tkinter.filedialog as filebox
from tkinter import *

def getPos(value,in_list):
    pos=0
    for i in in_list:
        if i==value:
            break
        else:
            pos+=1
    return pos

def delButton(tree):
    x=tree.get_children()
    for item in x:
        tree.delete(item)

headers = {
    'Host': 'c.y.qq.com',
    'Referer': 'http://c.y.qq.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
    'Safari/537.36 '
}

def douqq_post(mid):
    """
    返回歌曲下载url
    :param mid:歌曲mid
    :return: 字典
    """
    post_url = 'http://www.douqq.com/qqmusic/qqapi.php'
    data = {'mid': mid}
    res = requests.post(post_url, data=data)
    get_json = json.loads(res.text)
    return eval(get_json)

def find_song(word):
    global songNames,songmid,media_mid
    delButton(tree)
    """
    查找歌曲
    :param word: 歌曲名
    :return: 返回歌曲mid
    """
    get_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n' \
        '=20&w=' + word
    try:
        res1 = requests.get(get_url, headers=headers)
        get_json = json.loads(res1.text.strip('callback()[]'))
        jsons = get_json['data']['song']['list']
        songNames=[]
        songmid = []
        media_mid = []
        song_singer = []
        i = 1
        for song in jsons:
            # print(i, ':' + song['songname'], '---', song['singer'][0]['name'], song['songmid'], song['media_mid'])
            tree.insert("",i,text=str(i) ,values=(i,song['songname'],song['singer'][0]['name'])) #插入数据
            songNames.append(song['songname'])
            songmid.append(song['songmid'])
            media_mid.append(song['media_mid'])
            song_singer.append(song['singer'][0]['name'])
            i = i + 1
    except Exception as e:
        print(e)
        msgbox.showerror('错误','歌曲查找函数发生错误！')

def select():
    for item in tree.selection():
        item_text = tree.item(item,"values")
        print(item_text[0])
    select=int(item_text[0])
    print(select)
    print(type(select))
    #return songmid[select-1], song_singer[select-1]
    song_mid=songmid[select-1]
    song_name=songNames[select-1]
    dic=douqq_post(song_mid)
    postfix, url=choice_download(dic)
    save_path=filebox.asksaveasfilename(title='保存音乐',initialfile=song_name+".m4a",filetypes=[('M4A音频文件','.m4a')])
    download_file(url, save_path)

def download_file(src, file_path):
        """
    歌曲下载
    :param src: 下载链接
    :param file_path: 存储路径
    :return: 文件路径
    """
        r = requests.get(src, stream=True)
        f = open(file_path, "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        return file_path

def choice_download(dic):
        src = dic['m4a']
        postfix='.m4a'
        return postfix, src.replace('\/\/', '//').replace('\/', '/')

def search():
    songname=nameEnter.get()
    print(songname)
    #song_mid, singer = find_song(songname)
    find_song(songname)

win=tk.Tk()
win.title('音乐下载器')
win.geometry('400x500')
win.resizable(0,0)

searchPart=tk.Frame(win)
nameEnter=ttk.Entry(searchPart)
nameEnter.pack(side=tk.LEFT,fill=tk.X)
ttk.Button(searchPart,text='搜索',command=search).pack(side=tk.RIGHT)
searchPart.pack(fill=tk.X)

tree=ttk.Treeview(win,show="headings")#表格
tree["columns"]=("序号","歌曲","艺人")
tree.column("序号",width=20)
tree.column("歌曲",width=100) #表示列,不显示
tree.column("艺人",width=70)
tree.heading("序号",text="序号") 
tree.heading("歌曲",text="歌曲") #显示表头
tree.heading("艺人",text="艺人")
tree.pack(fill=tk.BOTH)

ttk.Button(text='下载',command=select).pack(fill=tk.X)

win.mainloop()

#def down():


```
原版来自吾爱破解论坛，这里修改了一些内容（详见“修改内容”）。
[原版链接](https://www.52pojie.cn/thread-1008496-1-1.html)
## 修改内容
 - 删除失效部分
 - 添加路径选择功能（文件路径选择窗口哦！）
 - 对部分位置进行汉化
 - 添加可视化界面
## 原网页上也有人修复过
```python
import os

import requests
import json

headers = {
    'Host': 'c.y.qq.com',
    'Referer': 'http://c.y.qq.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                  'Safari/537.36 '
}


def douqq_post(mid):
    """
返回歌曲下载url
:param mid:歌曲mid
:return: 字典
"""
    post_url = 'http://www.douqq.com/qqmusic/qqapi.php'
    data = {'mid': mid}
    res = requests.post(post_url, data=data)
    get_json = json.loads(res.text)
    return eval(get_json)


def download_file(src, file_path):
    """
歌曲下载
:param src: 下载链接
:param file_path: 存储路径
:return: 文件路径
"""
    r = requests.get(src, stream=True)
    f = open(file_path, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
    return file_path


def choice_download(dic):
    print('1. m4a视频')
    print('2. mp3普通品质')
    print('3. mp3高品质')
    print('4. ape高品无损')
    print('5. flac无损音频')
    select = int(input("请选择需要下载的音乐音质:"))
    src = ''
    postfix = ''
    if select == 1:
        src = dic['m4a']
        postfix = '.m4a'
    if select == 2:
        src = dic['mp3_l']
        postfix = '.mp3'
    if select == 3:
        src = dic['mp3_h']
        postfix = '.mp3'
    if select == 4:
        src = dic['ape']
        postfix = '.ape'
    if select == 5:
        src = dic['flac']
        postfix = '.flac'
    return postfix, src.replace('\/\/', '//').replace('\/', '/')


def find_song(word):
    """
查找歌曲
:param word: 歌曲名
:return: 返回歌曲mid
"""
    get_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n' \
              '=20&w=' + word
    try:
        res1 = requests.get(get_url, headers=headers)
        get_json = json.loads(res1.text.strip('callback()[]'))
        jsons = get_json['data']['song']['list']
        songmid = []
        media_mid = []
        song_singer = []
        i = 1
        for song in jsons:
            # 特殊情况下搜索条件会为空，测试的时候报错了几次跳过即可
            if song['albumid'] == 0:
                continue
            print(i, ':' + song['songname'], '---', song['singer'][0]['name'])
            songmid.append(song['songmid'])
            media_mid.append(song['media_mid'])
            song_singer.append(song['singer'][0]['name'])
            i = i + 1
        select = int(input("请输入您的选择:")) - 1
        return songmid[select], song_singer[select], jsons[select]['albumname']
    except Exception as e:
        print(f'歌曲查找有误：{e}')
        return None


if __name__ == '__main__':
    while True:
        songname = input("请输入需要下载的音乐的名字:")
        song_mid, singer,songname = find_song(songname)
        dic = douqq_post(song_mid)
        postfix, url = choice_download(dic)
        save_path = "D:\\Music\\"
        # 判断文件夹是否存在，不存在则创建文件夹
        if not os.path.exists(save_path):
            # 不存在则创建
            os.makedirs(save_path)
        download_file(url, save_path + songname + ' - ' + singer + postfix)
        print('下载完成啦，自动保存在D盘的Music文件夹下面', end='\n')
        print('是否继续下载？: y/n', end='\n')
        con = input()
        if con == 'n':
            print('结束')
            break
```

> 修复了两个使用的时候出现的BUG，可能还不完善求大佬改良1、修改搜索部分歌名会报错NoneType' object is not iterabl的问题 详情见89行注释2、修复文件夹不存在报错问题，目前解决方法如不存在则自动在D盘路径下创建一个Music文件夹[/mw_shl_code]3、另修改了一下下载后保存文件名为自己输入的名字而不是原本音乐名字的BUG 详情见98行

 ——Protoss_krz 发表于 2019-11-21 10:00
以上代码会询问下载格式，请选择1（“M4A视频”），放心吧，不是视频，估计是作者敲错了。另外，其他格式下下来听不了。
也欢迎你在评论区贡献完美的代码。

## 原版代码

```python
#-*- coding:utf-8 -*-# author:**ZLH**
# datetime:2019/8/2 16:47
# software: PyCharm
 
import requests
import json
headers = {
    'Host': 'c.y.qq.com',
    'Referer': 'http://c.y.qq.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
    'Safari/537.36 '
}
def douqq_post(mid):
        """
    返回歌曲下载url
    :param mid:歌曲mid
    :return: 字典
    """
        post_url = 'http://www.douqq.com/qqmusic/qqapi.php'
        data = {'mid': mid}
        res = requests.post(post_url, data=data)
        get_json = json.loads(res.text)
        return eval(get_json)
 
 
def download_file(src, file_path):
        """
    歌曲下载
    :param src: 下载链接
    :param file_path: 存储路径
    :return: 文件路径
    """
        r = requests.get(src, stream=True)
        f = open(file_path, "wb")
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        return file_path
 
def choice_download(dic):
        print('1. m4a视频')
        print('2. mp3普通品质')
        print('3. mp3高品质')
        print('4. ape高品无损')
        print('5. flac无损音频')
        select = int(input("请输入您的选择:"))
        src = ''
        postfix = ''
        if select == 1:
            src = dic['m4a']
            postfix = '.m4a'
        if select == 2:
            src = dic['mp3_l']
            postfix = '.mp3'
        if select == 3:
            src = dic['mp3_h']
            postfix = '.mp3'
        if select == 4:
            src = dic['ape']
            postfix = '.ape'
        if select == 5:
            src = dic['flac']
            postfix = '.flac'
        return postfix, src.replace('\/\/', '//').replace('\/', '/')
 
def find_song(word):
        """
    查找歌曲
    :param word: 歌曲名
    :return: 返回歌曲mid
    """
        get_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n' \
        '=20&w=' + word
        try:
            res1 = requests.get(get_url, headers=headers)
            get_json = json.loads(res1.text.strip('callback()[]'))
            jsons = get_json['data']['song']['list']
            songmid = []
            media_mid = []
            song_singer = []
            i = 1
            for song in jsons:
                # print(i, ':' + song['songname'], '---', song['singer'][0]['name'], song['songmid'], song['media_mid'])
                print(i, ':' + song['songname'], '---', song['singer'][0]['name'])
                songmid.append(song['songmid'])
                media_mid.append(song['media_mid'])
                song_singer.append(song['singer'][0]['name'])
                i = i + 1
            select = int(input("请输入您的选择:")) - 1
            return songmid[select], song_singer[select]
        except Exception as e:
            print(f'歌曲查找有误：{e}')
            return None
 
 
if __name__ == '__main__':
# songname = '叹云兮'
    while True:
        songname = input("Please input the music name:")
        song_mid, singer = find_song(songname)
        dic = douqq_post(song_mid)
        # {
        # "mid":"004FjJo32TISsY",
        # "m4a":"http:\/\/dl.stream.qqmusic.qq.com\/C400004FjJo32TISsY.m4a?guid=2095717240&vkey=0B599CA74745F8A27A33A1FED2C7F6925FFFE8ED040569FB3540EB011FE9C5A3D7F36EAE4BDBD450F25076A23EBAF95A5ECB54B22C5E8F10&uin=0&fromtag=38",
        # "mp3_l":"http:\/\/dl.stream.qqmusic.qq.com\/M500004FjJo32TISsY.mp3?guid=2095717240&vkey=0B599CA74745F8A27A33A1FED2C7F6925FFFE8ED040569FB3540EB011FE9C5A3D7F36EAE4BDBD450F25076A23EBAF95A5ECB54B22C5E8F10&uin=0&fromtag=53",
        # "mp3_h":media_mid"http:\/\/dl.stream.qqmusic.qq.com\/M800004FjJo32TISsY.mp3?guid=2095717240&vkey=0B599CA74745F8A27A33A1FED2C7F6925FFFE8ED040569FB3540EB011FE9C5A3D7F36EAE4BDBD450F25076A23EBAF95A5ECB54B22C5E8F10&uin=0&fromtag=53",
        # "ape":"http:\/\/dl.stream.qqmusic.qq.com\/A000004FjJo32TISsY.ape?guid=2095717240&vkey=0B599CA74745F8A27A33A1FED2C7F6925FFFE8ED040569FB3540EB011FE9C5A3D7F36EAE4BDBD450F25076A23EBAF95A5ECB54B22C5E8F10&uin=0&fromtag=53",
        # "flac":"http:\/\/dl.stream.qqmusic.qq.com\/F000004FjJo32TISsY.flac?guid=2095717240&vkey=0B599CA74745F8A27A33A1FED2C7F6925FFFE8ED040569FB3540EB011FE9C5A3D7F36EAE4BDBD450F25076A23EBAF95A5ECB54B22C5E8F10&uin=0&fromtag=53",
        # "pic":"https:\/\/y.gtimg.cn\/music\/photo_new\/T002R300x300M000003NZyTh4eMMsp.jpg?max_age=2592000"
        # }
        # print('mid:'+dic['mid'])
        postfix, url = choice_download(dic)
        save_path = "D:\\Music\\"
        download_file(url, save_path + songname + ' - ' + singer + postfix)
        con = input('Download success or not continue: y/n')
        if con == 'n':
            break
```
## 下载
代码在上面，自己复制，没有EXE，Pyinstaller没法打包，在想办法。
下载链接提供一键安装库功能。请自己下载
诚通网盘
https://n802.com/dir/27256477-39300593-4f1b29
## 2020/06/02 追
好吧······我竟然才发现：
我参考了吾爱破解论坛的一个帖子，但原文写道

> 首先这个帖子的代码大不部分是参考@珍珠奶茶丶板牙的，我当时下载的他的源码。
然后用着不是特别方便，就自己改良了一下下，然后又打包成无需环境的exe程序，让我朋友们使用。

原文给了作者参考的文章地址，我进去看了看······发现

> 下午闲着无聊，看到了@丸子吃枣药丸 他发的文章， API采用QQMusic，我将Python 实现了他的功能，更方便大家下载

我是真的无语了······

[转自我的CSDN](https://blog.csdn.net/tt68686/article/details/106439303)
