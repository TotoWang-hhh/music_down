#导入库
import requests
import json
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox
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
    global songNames,songmid,media_mid,songsinger
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
tree.column("序号",width=25)
tree.column("歌曲",width=100) #表示列,不显示
tree.column("艺人",width=70)
tree.heading("序号",text="序号") 
tree.heading("歌曲",text="歌曲") #显示表头
tree.heading("艺人",text="艺人")
tree.pack(fill=tk.BOTH)

ttk.Button(text='下载',command=select).pack(fill=tk.X)

win.mainloop()

def down():
    dic = douqq_post(song_mid)
    postfix, url = choice_download(dic)
    save_path = easygui.filesavebox(title='保存文件',default="../"+songname+".m4a")
    download_file(url, save_path)
