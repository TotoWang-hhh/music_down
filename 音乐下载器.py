#导入库
import requests
import json
import easygui
import tkinter as tk
from tkinter import ttk


srd=[]#SRD=Seach Result Display

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

def find_song(word,*args):
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
                srd.append((i, ':' + song['songname'], '---', song['singer'][0]['name']))#SRD=Seach Result Display
                songmid.append(song['songmid'])
                media_mid.append(song['media_mid'])
                song_singer.append(song['singer'][0]['name'])
                i=i + 1
                result_list.insert('','end',values=[song['songname'],song['singer'][0]['name']])
            select = result_list.selection()[0]
            select=int(filter(str.isdigit,select))
            print(select)
            print(type(select))
            print(select)
            print(type(select))
            select=int(select.split(',')[0].strip('('))
            print(select)
            return songmid[select], song_singer[select]
        except Exception as e:
            print(f'歌曲查找函数发生致命的错误-Stop Code:{e}')
            return None

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

def start():
    global song_mid,singer
    songname=name_enterbox.get()
    song_mid, singer = find_song(songname)

def down(event):
    global dic,postfix,url
    print(result_list.selection())
    print(type(result_list.selection()[0]))
    select=filter(str.isdigit,result_list.selection()[0])
    print(select)
    print(type(select))
    print(int(select))
    string.set(result_list.selection()[0])
    string.set(result_list.focus())
    dic = douqq_post(song_mid)
    postfix, url = choice_download(dic)
    save_path = easygui.filesavebox(title='保存文件',default=songname+".m4a")
    download_file(url, save_path)

window=tk.Tk()
window.geometry('800x450')
window.title('音乐下载器')
#名称输入
enter_name_tip=tk.Label(window,text='请输入音乐名称')
enter_name_tip.place(x=10,y=10)
name_enterbox=tk.Entry(window,bd=2,show=None,width=70)
name_enterbox.place(x=10,y=30)
#搜索按钮
search_btn=tk.Button(window,text='搜索',bd=3,width=10,height=2,command=start)
search_btn.place(x=10,y=60)
#搜索结果列表
string = tk.StringVar()
title=['1','2']
result_list=ttk.Treeview(window,columns=title)
result_list.place(x=10,y=120)
result_list.heading('1',text='名称')
result_list.heading('2',text='艺人')
result_list.bind("<ButtonRelease-1>",down)
#主循环
window.mainloop()