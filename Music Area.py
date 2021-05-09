# 导入库
import requests
import json
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox
import tkinter.filedialog as filebox
from tkinter import *
import webbrowser
import time
import os


def sift(mlist):
    # 获取筛选内容
    singer = singer_enter.get()
    # 判断用户是否设定筛选要求
    if singer != '':
        # 设置一个空列表，用于存储符合条件的结果
        siftRes = []
        # 逐个判断是否满足要求
        for i in mlist:
            if i['singer'][0]['name'] == singer:
                siftRes.append(i)
        # 遍历结束之后返回筛选过的列表
        return siftRes
    # 如果用户未设置筛选，则将列表照原样返回
    else:
        return mlist


def getPos(value, in_list):
    pos = 0
    for i in in_list:
        if i == value:
            break
        else:
            pos += 1
    return pos


def delButton(tree):
    x = tree.get_children()
    for item in x:
        tree.delete(item)


defult_font = ("./fonts/defult.ttf", 10)
title_font = ("./fonts/defult.ttf", 14)

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
    global songNames, songmid, media_mid
    delButton(tree)
    """
    查找歌曲
    :param word: 歌曲名
    :return: 返回歌曲mid
    """
    get_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n' \
              '=' + numEnter.get() + '&w=' + word
    try:
        res1 = requests.get(get_url, headers=headers)
        get_json = json.loads(res1.text.strip('callback()[]'))
        jsons = get_json['data']['song']['list']
        songNames = []
        songmid = []
        media_mid = []
        song_singer = []
        i = 1
        jsons_sift = sift(jsons)
        for song in jsons_sift:
            # print(i, ':' + song['songname'], '---', song['singer'][0]['name'], song['songmid'], song['media_mid'])
            tree.insert("", i, text=str(i), values=(i, song['songname'], song['singer'][0]['name']))  # 插入数据
            songNames.append(song['songname'])
            songmid.append(song['songmid'])
            media_mid.append(song['media_mid'])
            song_singer.append(song['singer'][0]['name'])
            i = i + 1
    except Exception as e:
        win_print('歌曲查找函数发生错误！')
        win_print(e)


def down():
    for item in tree.selection():
        item_text = tree.item(item, "values")
    select = int(item_text[0])
    # return songmid[select-1], song_singer[select-1]
    song_mid = songmid[select - 1]
    song_name = songNames[select - 1]
    dic = douqq_post(song_mid)
    postfix, url = choice_download(dic)
    save_path = filebox.asksaveasfilename(title='保存音乐', initialfile=song_name + ".m4a", filetypes=[('M4A音频文件', '.m4a')])
    win_print('正在将 {name} 下载到 {path} ......'.format(name=song_name, path=save_path))
    download_file(url, save_path)
    win_print('下载完成！')


def play():
    for item in tree.selection():
        item_text = tree.item(item, "values")
    select = int(item_text[0])
    # return songmid[select-1], song_singer[select-1]
    song_mid = songmid[select - 1]
    song_name = songNames[select - 1]
    dic = douqq_post(song_mid)
    postfix, url = choice_download(dic)
    save_path = "./audio_cache.m4a"
    win_print('收听选中内容')
    win_print('正在缓存......')
    download_file(url, save_path)
    win_print('下载完成！')
    win_print('正在启动播放器......')
    os.system("audio_cache.m4a")


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
    postfix = '.m4a'
    return postfix, src.replace('\/\/', '//').replace('\/', '/')


def search(event=''):
    songname = nameEnter.get()
    # song_mid, singer = find_song(songname)
    find_song(songname)


def win_print(word, warn=False):
    consle.insert('end', word)
    consle.insert('end', '\n')
    consle.see(tk.END)
    win.update()
    if warn:
        consle['fg'] = 'red'
        win.update()
        time.sleep(1)
        consle['fg'] = 'green'
        win.update()
        consle.see(tk.END)


win = tk.Tk()
win.title('音乐地带')
win.iconbitmap("./icon.ico")
win.geometry('400x550')

searchPart = tk.Frame(win)
tk.Button(searchPart, text='搜索', command=search, font=("./fonts/defult.ttf", 10,), relief='solid', width=12, bd=1,
          bg='LawnGreen').pack(side=tk.RIGHT, fill=tk.Y)
nameEnter = ttk.Entry(searchPart)
nameEnter.pack(fill=tk.X)

searchPart_rowB = tk.Frame(searchPart)

tk.Label(searchPart_rowB, text='搜索条目数：', font=("./fonts/defult.ttf", 10)).pack(side=tk.LEFT)
numEnter = ttk.Entry(searchPart_rowB)
numEnter.pack(fill=tk.X)
numEnter.insert(tk.END, '20')

siftPart = ttk.LabelFrame(searchPart,text='筛选')
tk.Label(siftPart, text='通过艺人筛选', font=("./fonts/defult.ttf", 10)).pack(side=tk.LEFT,padx=3,pady=3)
singer_enter = ttk.Entry(siftPart)
singer_enter.pack(fill=tk.X,padx=3,pady=3)

searchPart_rowB.pack(fill=tk.X)
siftPart.pack(fill=tk.X,padx=5,pady=3)
searchPart.pack(fill=tk.X)

win.bind('<Return>', search)

tree = ttk.Treeview(win, show="headings")  # 表格
tree["columns"] = ("序号", "歌曲", "艺人")
tree.column("序号", width=10)
tree.column("歌曲", width=100)  # 表示列,不显示
tree.column("艺人", width=70)
tree.heading("序号", text="序号")
tree.heading("歌曲", text="歌曲")  # 显示表头
tree.heading("艺人", text="艺人")
tree.pack(fill=tk.BOTH)

tk.Button(win, text='下载选定内容', command=down, font=("./fonts/defult.ttf", 10), relief='solid', bd=1).pack(fill=tk.X)
tk.Button(win, text='收听选定内容', command=play, font=("./fonts/defult.ttf", 10), relief='solid', bd=1).pack(fill=tk.X)

tk.Button(win, text='By 人工智障', command=lambda: webbrowser.open("rgzz.great-site.net"),
          font=("./fonts/defult.ttf", 10), relief='solid', bd=1).pack(fill=tk.X)

consle = tk.Text(win, bg='black', fg='green', font=('courier new', '15'))
consle.pack(fill=tk.BOTH)

win.update()

win_print('2020 By 人工智障')

win.mainloop()

# def down():
