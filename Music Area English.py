# 导入库
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox
import tkinter.filedialog as filebox
from PIL import Image, ImageTk
#from tkinter import *

#启动页
def set_wait(state,start=False):#可移植，icon.ico为正方形图标即可
    if state:
        global root,mask
        mask=tk.Toplevel()
        mask.overrideredirect(True)
        mask.configure(background='#000000')
        mask.attributes("-alpha",0.7)
        if start:
            global img,imgf
            mask.configure(background='#FFFFFF')
            mask.attributes("-alpha",1)
            imgf=Image.open("./icon.ico")
            imgr=imgf.resize((256,256))
            img=ImageTk.PhotoImage(image=imgr)
            mask.geometry(str(root.winfo_width())+'x'+str(root.winfo_height()+30)+'+'+str(root.winfo_x()+10)+'+'+str(root.winfo_y()))
            tk.Label(mask,text='',font=('微软雅黑',15),bg='#FFFFFF').pack()
            tk.Label(mask,image=img,font=('微软雅黑',30),bg='#FFFFFF').pack(pady=50)
            tk.Label(mask,text='Music Area',font=('微软雅黑',15),bg='#FFFFFF').pack()
        else:
            mask.configure(background='#000000')
            mask.attributes("-alpha",0.7)
            mask.geometry(str(root.winfo_width())+'x'+str(root.winfo_height())+'+'+str(root.winfo_x()+10)+'+'+str(root.winfo_y()+30))
            tk.Label(mask,text='LOADING',font=('微软雅黑',30),bg='#000000',fg='#FFFFFF').pack(pady=150)
        root.update()
        mask.update()
    else:
        try:
            if start:
                for i in range(0,10):
                    mask.attributes("-alpha",(10-i)/10)
                    time.sleep(0.02)
                    mask.update()
            mask.destroy()
        except:
            win_print('Ignorable Error: Set wait to False before setting wait to True')
        root.update()


root = tk.Tk()
root.title('Music Area')
#win.iconbitmap("./icon.ico")
root.minsize(600,510)
#root.geometry('400x600')
root.iconbitmap("./icon.ico")

nb=ttk.Notebook(root)

root.update()
set_wait(True,start=True)


import requests
#import json
import webbrowser
import os
import threading
from ctypes import *
import datetime,time
import eyed3
import win32clipboard


def delButton(tree):
    x = tree.get_children()
    for item in x:
        tree.delete(item)

def find_song(word):
    set_wait(True)
    try:
        global mids,mnames,gkw
        gkw=word
        delButton(tree)
        #load_full_t=threading.Thread(target=lambda:load_full(word))#放在前面可以尽早覆盖加载全部的进程
        res=requests.get(url="https://cloudmusic-api.txm.world/search?keywords="+word)
        json=res.json()
        mids=[]
        mnames=[]
        if json['result']=={} or json['result']['songCount']==0:
            mids.append('5221167')
            mnames.append('Could Not Find Anything')
            tree.insert("", 0, text=str(0), values=('1', 'Could Not Find Anything', 'DO NOT PLAY THIS', 'GUESS !'))  # 插入数据
        else:
            mlst=json['result']['songs']
            win_print('Found '+str(json['result']['songCount'])+' results, but only 30 of them was shown')
            for m in mlst:
                mids.append(str(m['id']))
                mnames.append(m['name'])
                ars=''
                for ar in m['ar']:
                    ars+=ar['name']+' / '
                ars=ars[0:len(ars)-3]
                no=str(mlst.index(m)+1)
                if int(m['fee'])==1:
                    no+=' | PAY'
                elif int(m['fee'])==4:
                    no+=' | PAY'
                tree.insert("", mlst.index(m), text=str(mlst.index(m)), values=(no, m['name'], ars, m['id']))  # 插入数据
            #if len(mids)>=30 and json['result']['hasMore']:
                #load_full_t.start()
    except Exception as e:
        win_print('ERROR! All useful things for developer is in the consle')
        print('Function: find_song')
        print('--------------------')
        print('Web Info.')
        print('URL: '+"https://cloudmusic-api.txm.world/search?keywords="+word)
        print('Result Data: '+str(json))
        print('--------------------')
        print('Local Info.')
        print(e)
        print('--------------------')
        print('Extra Info.')
        print('Completed: '+str(len(mids)))
        print('====================')
    set_wait(False)

def get_fav(usr,pwd):
    set_wait(True)
    delButton(ftree)
    try:
        global mids,mnames

        url="https://cloudmusic-api.txm.world/login?email="+usr+"&password="+pwd
        res=requests.get(url)
        json=res.json()
        cookie=json['cookie']

        url="https://cloudmusic-api.txm.world/user/account?cookie="+str(cookie)
        res=requests.get(url)
        json=res.json()
        uid=str(json['account']['id'])

        url="https://cloudmusic-api.txm.world/user/playlist?limit=1&uid="+uid
        res=requests.get(url)
        json=res.json()
        favlstid=str(json['playlist'][0]['id'])

        url="https://cloudmusic-api.txm.world/playlist/track/all?id="+favlstid+"&cookie="+cookie
        res=requests.get(url)
        json=res.json()
        
        mids=[]
        mnames=[]
        mlst=json['songs']

        url='N/A'
        #收藏音乐信息挨个存列表
        for m in mlst:
            mids.append(str(m['id']))
            mnames.append(m['name'])
            ars=''
            for ar in m['ar']:
                ars+=str(ar['name'])+' / '
            ars=ars[0:len(ars)-3]
            ftree.insert("", mlst.index(m), text=str(mlst.index(m)), values=(mlst.index(m)+1, m['name'], ars, m['id']))  # 插入数据
    except Exception as e:
        #输出信息需要把账户密码屏蔽，我并不希望在反馈信息里得到用户的账户密码
        if '&password=' in url:
            url=url.replace(usr,'[*Username*]').replace(pwd,'[*Password*]')
        win_print('ERROR! All useful things for developer is in the consle')
        print('Function: getfav')
        print('--------------------')
        print('Web Info.')
        print('URL: '+url)
        print('Result Data: '+str(json))
        print('--------------------')
        print('Local Info.')
        print(e)
        print('--------------------')
        print('Extra Info.')
        print('Completed: '+str(len(mids)))
        print('====================')
    set_wait(False)

def get_all_style():
    global styles,astree
    set_wait(True)
    delButton(astree)
    res=requests.get("https://cloudmusic-api.txm.world/style/list")
    json=res.json()
    style_lst=json['data']
    thread_list=[]
    #遍历父级
    for style in style_lst:
        #styles[style['enName']+' （'+style['tagName']+'）'+'   ID：'+str(style['tagId'])]=[]#字典中每个key都是一种风格
        lst_parent = astree.insert('', 'end', text=style['enName'],values=(style['tagName'],str(style['tagId'])))
        thread_list.append(threading.Thread(target=lambda:show_child_styles(style,lst_parent)))#绝招：多线程加载子分类
        thread_list[style_lst.index(style)].start()
    win_print('Loading more in backstage')
    #styles={}
    #tree_parent = astree.insert('', 'end', text='所有曲风')
    #json2treeview(astree,tree_parent,styles)
    set_wait(False)

def get_fav_style(usr,pwd):
    global styles,fsstree
    del_button(fstree)
    set_wait(True)
    
    url="https://cloudmusic-api.txm.world/login?email="+usr+"&password="+pwd
    res=requests.get(url)
    json=res.json()
    cookie=json['cookie']

    res=requests.get("https://cloudmusic-api.txm.world/style/preference?limit=20?cookie="+cookie)
    json=res.json()
    style_lst=json['data']['tagPreferenceVos']

    for style in style_lst:
        fstree.insert("", style_lst.index(style), text=str(style_lst.index(style)), values=(str(style_lst.index(style)+1), style['tagName'], str(style['ratio'])+'%', str(style['tagId'])))
    
    set_wait(False)

def show_child_styles(style_lst,parent):
    #遍历子风格
    for child in style_lst['childrenTags']:
        #styles[style['enName']+' （'+style['tagName']+'）'+'   ID：'+str(style['tagId'])].append(child['enName']+' （'+child['tagName']+'）'+'   ID：'+str(child['tagId']))#每个value是一个列表，存储子风格
        lst_parent=astree.insert(parent, 'end', text=child['enName'],values=(child['tagName'],str(child['tagId'])))
        if child['childrenTags']!=None:
            show_child_styles(child,lst_parent)

def get_style_music(tagid):
    set_wait(True)
    try:
        global mids,mnames,gkw
        gkw=tagid
        delButton(tree)
        #load_full_t=threading.Thread(target=lambda:load_full(word))#放在前面可以尽早覆盖加载全部的进程
        res=requests.get(url="https://cloudmusic-api.txm.world/style/song?tagId="+tagid)
        json=res.json()
        mids=[]
        mnames=[]
        if json['data']['songs']==[]:
            mids.append('5221167')
            mnames.append('Could Not Find Anything')
            tree.insert("", 0, text=str(0), values=('1', 'Could Not Find Anything', 'DO NOT PLAY THIS', 'GUESS !'))  # 插入数据
        else:
            mlst=json['data']['songs']
            for m in mlst:
                mids.append(str(m['id']))
                mnames.append(m['name'])
                ars=''
                for ar in m['ar']:
                    ars+=ar['name']+' / '
                ars=ars[0:len(ars)-3]
                no=str(mlst.index(m)+1)
                if int(m['fee'])==1:
                    no+=' | PAY'
                elif int(m['fee'])==4:
                    no+=' | PAY'
                smtree.insert("", mlst.index(m), text=str(mlst.index(m)), values=(no, m['name'], ars, m['id']))  # 插入数据
            #if len(mids)>=30 and json['result']['hasMore']:
                #load_full_t.start()
    except Exception as e:
        win_print('ERROR! All useful things for developer is in the consle')
        print('Function: get_style_music')
        print('--------------------')
        print('Web Info.')
        print('URL: '+"https://cloudmusic-api.txm.world/search?keywords="+tagid)
        print('Result Data: '+str(json))
        print('--------------------')
        print('Local Info.')
        print(e)
        print('--------------------')
        print('Extra Info: ')
        print('Complete: '+str(len(mids)))
        print('====================')
    set_wait(False)

def down():
    global nb
    set_wait(True)
    if int(nb.index(nb.select()))==0:#搜索下载
        for item in tree.selection():
            item_text = tree.item(item, "values")
    elif int(nb.index(nb.select()))==1:#收藏下载
        for item in ftree.selection():
            item_text = ftree.item(item, "values")
    elif int(nb.index(nb.select()))==2:#曲风搜歌
        if int(swin.index(swin.select()))==2:#该风格的歌曲
            for item in smtree.selection():
                item_text = smtree.item(item, "values")
        else:
            msgbox.showerror('Local Error','Can not use this function on this page')
            return
    else:
        msgbox.showerror('Local Error','Can not use this function on this page')
        return
    select = item_text[0]
    select=select.split(' | ')[0]
    select=int(select)
    # return songmid[select-1], song_singer[select-1]
    mid = mids[select - 1]
    mname = mnames[select - 1]
    res=requests.get(url="https://cloudmusic-api.txm.world/song/url?id="+mid+"&br=320000")#+'&cookie='+cookie)
    json=res.json()
    murl=json['data'][0]['url']
    set_wait(False)
    if 'freeTrialInfo' in list(json['data'][0].keys()):
        if json['data'][0]['freeTrialInfo']!=None:
            freesec=json['data'][0]['freeTrialInfo']['end']-json['data'][0]['freeTrialInfo']['start']
            cdown=msgbox.askyesno('Attention!','You can only play'+str(freesec)+' seconds of this music\nAre you sure to download this?')
            if not bool(cdown):
                return
    save_path = filebox.asksaveasfilename(title='Save Music', initialfile=mname + ".mp3", filetypes=[('MP3 Audio File', '.mp3')])
    set_wait(True)
    win_print('Downloading {name} to {path} ......'.format(name=mname, path=save_path))
    infres=requests.get(url="https://cloudmusic-api.txm.world/song/detail?ids="+mid)
    infjson=infres.json()
    inf=infjson['songs'][0]
    ars=''
    if inf['publishTime']!=0:#如果年份未知，则API返回0，程序会将年份误标为1970，故加上判断
        pubyear=datetime.datetime.fromtimestamp(inf['publishTime']/1000.0).strftime('%Y')
    else:
        pubyear=''
    for i in inf['ar']:
        ars+=i['name']+';'
    ars=ars[0:len(ars)-1]
    res=requests.get(inf['al']['picUrl'])
    img=res.content
    if murl==None:
        win_print(mname+' is not able to download or play on Netease CloudMusic')
        msgbox.showerror('Not Able to Download or Play',mname+' is not able to download or play on Netease CloudMusic')
    else:
        res=requests.get(url=murl)
        m=res.content
        f=open(save_path,'wb')
        f.write(m)
        f.close()
        #编辑信息
        audiofile = eyed3.load(save_path)
        audiofile.initTag()
        audiofile.tag.title = inf['name']
        audiofile.tag.artist = ars
        audiofile.tag.album = inf['al']['name']
        audiofile.tag.images.set(type_=3,img_data=img,mime_type='image/jpeg')  # 封面
        audiofile.tag.recording_date = str(pubyear)  # 年份
        audiofile.tag.save()
    set_wait(False)

def play():
    global nb
    set_wait(True)
    if int(nb.index(nb.select()))==0:#搜索下载
        for item in tree.selection():
            item_text = tree.item(item, "values")
    elif int(nb.index(nb.select()))==1:#收藏下载
        for item in ftree.selection():
            item_text = ftree.item(item, "values")
    elif int(nb.index(nb.select()))==2:#曲风搜歌
        if int(swin.index(swin.select()))==2:#该风格的歌曲
            for item in smtree.selection():
                item_text = smtree.item(item, "values")
        else:
            msgbox.showerror('Local Error','Can not use this function on this page')
            return
    else:
        msgbox.showerror('Local Error','Can not use this function on this page')
        return
    select = item_text[0]
    select=select.split(' | ')[0]
    select=int(select)
    # return songmid[select-1], song_singer[select-1]
    mid = mids[select - 1]
    mname = mnames[select - 1]
    save_path = "./cache.mp3"
    win_print('Downloading {name} to {path} for PLAYING as CACHE'.format(name=mname, path=save_path))
    res=requests.get(url="https://cloudmusic-api.txm.world/song/url?id="+mid+"&br=320000")#+'&cookie='+cookie)
    json=res.json()
    murl=json['data'][0]['url']
    if murl==None:
        win_print(mname+'  is not able to download or play on Netease CloudMusic')
    else:
        res=requests.get(url=murl)
        m=res.content
        f=open(save_path,'wb')
        f.write(m)
        f.close()
    infres=requests.get(url="https://cloudmusic-api.txm.world/song/detail?ids="+mid)
    infjson=infres.json()
    inf=infjson['songs'][0]
    ars=''
    if inf['publishTime']!=0:#如果年份未知，则API返回0，程序会将年份误标为1970，故加上判断
        pubyear=datetime.datetime.fromtimestamp(inf['publishTime']/1000.0).strftime('%Y')
    else:
        pubyear=''
    for i in inf['ar']:
        ars+=i['name']+';'
    ars=ars[0:len(ars)-1]
    res=requests.get(inf['al']['picUrl'])
    img=res.content
    #编辑信息
    audiofile = eyed3.load(save_path)
    audiofile.initTag()
    audiofile.tag.title = inf['name']
    if inf['name']=='Never Gonna Give You Up':
        audiofile.tag.artist = 'hmm'
        audiofile.tag.album = 'U R Interesting!'
    else:
        audiofile.tag.artist = ars
        audiofile.tag.album = inf['al']['name']
    imgf=open("./cache.jpg",'wb')  # 封面
    imgf.write(img)
    imgf.close()
    audiofile.tag.recording_date = str(pubyear)  # 年份
    audiofile.tag.save()
    set_wait(False)
    win_print('Download Completed! Starting Player')
    os.popen('ma_player.exe')

def copyid():
    global nb
    id_index=3
    if int(nb.index(nb.select()))==0:#搜索下载
        for item in tree.selection():
            item_text = tree.item(item, "values")
        idtype='Music'
    elif int(nb.index(nb.select()))==1:#收藏下载
        for item in ftree.selection():
            item_text = ftree.item(item, "values")
        idtype='Music'
    elif int(nb.index(nb.select()))==2:#曲风搜歌
        if int(swin.index(swin.select()))==0:#所有曲风
            for item in astree.selection():
                item_text = astree.item(item, "values")
            id_index=1
            idtype='Style'
        elif int(swin.index(swin.select()))==1:#曲风偏好
            for item in fstree.selection():
                item_text = fstree.item(item, "values")
            idtype='Style'
        elif int(swin.index(swin.select()))==2:#该风格的歌曲
            for item in smtree.selection():
                item_text = smtree.item(item, "values")
            idtype='Music'
        else:
            msgbox.showerror('Local Error','Can not use this function on this page')
            return
    else:
        msgbox.showerror('Local Error','Can not use this function on this page')
        return
    mid = item_text[id_index]
    ###
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(str(mid))
    win32clipboard.CloseClipboard()
    msgbox.showinfo('Copied','Copied '+str(idtype)+' ID ('+str(mid)+') to Clipboard')

def json2treeview(tree, parent, node):#感谢来自简书的WangLane，原链接https://www.jianshu.com/p/c6aae4d3f80d
    """
    Populate tree view by given json object.
    :param tree: treeview widget.
    :param parent: parent node of treeview.
    :param node: node should be a dict object.
    :return:
    """
    # 如果没有父节点，建立一个父节点
    if parent is None:
        parent = tree.insert('', 'end', text='Json')

    # 由于node一定是dict，直接迭代
    for item in node:
        value = node.get(item)
        if isinstance(value, dict):
            cur = tree.insert(parent, 'end', text=str(item), values=(str(value).replace("'", '"'), type(value).__name__))
            populate_treeview(tree, cur, value)
        elif isinstance(value, list):
            cur = tree.insert(parent, 'end', text=item, values=(str(value).replace("'", '"'), type(value).__name__))
            for each in value:
                if isinstance(each, dict):
                    tmp = tree.insert(cur, 'end', text='{}')
                    populate_treeview(tree, tmp, each)
                else:
                    tree.insert(cur, 'end', text=str(each), values=(str(value).replace("'", '"'), type(value).__name__))
        elif isinstance(value, int) or isinstance(value, str) or isinstance(value, bool):
            # tmp = str(item) + ':' + str(value)
            tmp = str(item)
            tree.insert(parent, 'end', text=tmp, values=(str(value).replace("'", '"'), type(value).__name__))

def search(event=''):
    songname = nameEnter.get()
    # song_mid, singer = find_song(songname)
    find_song(songname)

def win_print(word):
    global consle
    console['state']='normal'
    console.insert('end', word)
    console.insert('end', '\n')
    console.see(tk.END)
    console['state']='disabled'
    win.update()


btnpt=tk.Frame(root)

ttk.Button(btnpt, text='DOWNLOAD', command=down).pack(fill=tk.X,side=tk.LEFT,expand=True)
ttk.Button(btnpt, text='PLAY', command=play).pack(fill=tk.X,side=tk.LEFT,expand=True)
ttk.Button(btnpt, text='COPY ID', command=copyid).pack(fill=tk.X,side=tk.LEFT,expand=True)

btnpt.pack(fill=tk.X,side=tk.BOTTOM)


#搜索下载
win=tk.Frame(nb)
nb.add(win, text='Search')

searchPart = tk.Frame(win)
ttk.Button(searchPart, text='Search', command=search, width=12).pack(side=tk.RIGHT, fill=tk.Y)
nameEnter = ttk.Entry(searchPart)
nameEnter.pack(fill=tk.X)

searchPart.pack(fill=tk.BOTH)

nameEnter.bind('<Return>', search)

tree = ttk.Treeview(win, show="headings")  # 表格
tree["columns"] = ("序号", "歌曲", "艺人","歌曲ID")
tree.column("序号", width=10)
tree.column("歌曲", width=100)  # 表示列,不显示
tree.column("艺人", width=70)
tree.column("歌曲ID", width=10)
tree.heading("序号", text="No.")
tree.heading("歌曲", text="Title")  # 显示表头
tree.heading("艺人", text="Artist")
tree.heading("歌曲ID", text="Music ID")

tree.pack(fill=tk.BOTH,expand=True)#最后pack，让它充满页面且不出错


#收藏下载
fwin=tk.Frame(nb)
nb.add(fwin, text='Favourites')

loginPart = tk.Frame(fwin)
ttk.Button(loginPart, text='Login and\nList Favourites', command=lambda:get_fav(usrEnter.get(),pwdEnter.get()), width=12).pack(side=tk.RIGHT, fill=tk.Y)
tippt=tk.Frame(loginPart)
tk.Label(tippt,text='Account  ').pack()
tk.Label(tippt,text='Password ').pack()
tippt.pack(side=tk.LEFT)
usrEnter = ttk.Entry(loginPart)
usrEnter.pack(fill=tk.X)
pwdEnter = ttk.Entry(loginPart,show='●')
pwdEnter.pack(fill=tk.X)

loginPart.pack(fill=tk.BOTH)

usrEnter.bind('<Return>', lambda event:pwdEnter.focus())
pwdEnter.bind('<Return>', lambda event:get_fav(usrEnter.get(),pwdEnter.get()))

ftree = ttk.Treeview(fwin, show="headings")  # 表格
ftree["columns"] = ("序号", "歌曲", "艺人","歌曲ID")
ftree.column("序号", width=10)
ftree.column("歌曲", width=100)  # 表示列,不显示
ftree.column("艺人", width=70)
ftree.column("歌曲ID", width=50)
ftree.heading("序号", text="No.")
ftree.heading("歌曲", text="Title")  # 显示表头
ftree.heading("艺人", text="Artist")
ftree.heading("歌曲ID", text="Music ID")

#btnpt=tk.Frame(fwin)

ftree.pack(fill=tk.BOTH,expand=True)#最后pack，让它充满页面且不出错


#曲风搜歌
swin=ttk.Notebook(nb)
nb.add(swin, text='Search By Style')

#全部曲风
aswin=tk.Frame(swin)
swin.add(aswin,text='All Style')

astree = ttk.Treeview(aswin)  #树状图
astree["columns"] = ("译名", "曲风ID")
astree.column("译名", width=100)
astree.column("曲风ID", width=50)
astree.heading("译名", text="Translated (Chinese)")
astree.heading("曲风ID", text="Style ID")

ttk.Button(aswin,text='Show / Refresh',command=get_all_style).pack(side=tk.BOTTOM,fill=tk.X)

astree.pack(fill=tk.BOTH,expand=True)

#曲风偏好
fswin=tk.Frame(swin)
swin.add(fswin,text='Favourite Styles')

fsloginPart = tk.Frame(fswin)
ttk.Button(fsloginPart, text='Login and List\nFavourite Styles', command=lambda:get_fav_style(fsusrEnter.get(),fspwdEnter.get()), width=15).pack(side=tk.RIGHT, fill=tk.Y)
fstippt=tk.Frame(fsloginPart)
tk.Label(fstippt,text='Account ').pack()
tk.Label(fstippt,text='Password ').pack()
fstippt.pack(side=tk.LEFT)
fsusrEnter = ttk.Entry(fsloginPart)
fsusrEnter.pack(fill=tk.X)
fspwdEnter = ttk.Entry(fsloginPart,show='●')
fspwdEnter.pack(fill=tk.X)

fsloginPart.pack(fill=tk.BOTH)

fsusrEnter.bind('<Return>', lambda event:fspwdEnter.focus())
fspwdEnter.bind('<Return>', lambda event:get_fav_style(fsusrEnter.get(),fspwdEnter.get()))

tk.Label(fswin,text='Netease CloudMusic Account Required',fg='#0000FF').pack(fill=tk.X)

fstree = ttk.Treeview(fswin, show="headings")  # 表格
fstree["columns"] = ("序号", "名称", "收听百分比","曲风ID")
fstree.column("序号", width=10)
fstree.column("名称", width=100)  # 表示列,不显示
fstree.column("收听百分比", width=70)
fstree.column("曲风ID", width=50)
fstree.heading("序号", text="No.")
fstree.heading("名称", text="Name (Chinese)")  # 显示表头
fstree.heading("收听百分比", text="Percentage")
fstree.heading("曲风ID", text="Style ID")

fstree.pack(fill=tk.BOTH,expand=True)

#该曲风的音乐
smwin=tk.Frame(swin)
swin.add(smwin, text='Find Music By Style ID')

smsearchPart = tk.Frame(smwin)
ttk.Label(smsearchPart, text='Style ID').pack(side=tk.LEFT, fill=tk.Y)
ttk.Button(smsearchPart, text='Search', command=lambda:get_style_music(smnameEnter.get())).pack(side=tk.RIGHT, fill=tk.Y)
smnameEnter = ttk.Entry(smsearchPart)
smnameEnter.pack(fill=tk.X)

smsearchPart.pack(fill=tk.BOTH)

nameEnter.bind('<Return>', lambda event:get_style_music(smnameEnter.get()))

smtree = ttk.Treeview(smwin, show="headings")  # 表格
smtree["columns"] = ("序号", "歌曲", "艺人","歌曲ID")
smtree.column("序号", width=10)
smtree.column("歌曲", width=100)  # 表示列,不显示
smtree.column("艺人", width=70)
smtree.column("歌曲ID", width=10)
smtree.heading("序号", text="No.")
smtree.heading("歌曲", text="Title")  # 显示表头
smtree.heading("艺人", text="Artist(s)")
smtree.heading("歌曲ID", text="Music ID")

smtree.pack(fill=tk.BOTH,expand=True)


#控制台
console = tk.Text(nb,font=('consolas', '10'),height=10)
nb.add(console, text='User-friendly Output')


#关于
aroot=tk.Frame(nb)
awin=tk.Frame(aroot,width=400,height=500)
awin.pack()
nb.add(aroot, text='About')

#tk.Label(awin,text='',font=('微软雅黑',15)).pack(padx=25)
tk.Label(awin,text='Music Area',font=('微软雅黑',25)).pack(padx=25,pady=15)
tk.Label(awin,text='Ver. 5.3.0   Player: 0.1.0').pack(padx=25)
tk.Label(awin,text='2022 By rgzz666').pack(padx=25)

ttk.Button(awin, text='My Site (Chinese)', command=lambda: webbrowser.open("http://rgzz.great-site.net/")).pack(padx=25,pady=15)

ttk.Separator(awin).pack(fill=tk.X,padx=50,pady=10)

tk.Label(awin,text='Thanks',font=('微软雅黑',15)).pack(padx=25,pady=5)
tk.Button(awin,text='Vercel — API Deploy',bd=0,command=lambda:webbrowser.open("https://www.vercel.com")).pack(padx=25)
tk.Button(awin,text='Heymu — Player',bd=0,command=lambda:webbrowser.open("https://teameow.xyz/")).pack(padx=25)
tk.Button(awin,text='AXIOMXS — Domain',bd=0,command=lambda:msgbox.showinfo('About Him','AXIOMXS, who has already deleted his site\nand changes his nickname once a month\n\nContact info is not provided, \nbecause Im not sure if this is private for him.')).pack(padx=25)
tk.Button(awin,text='Netease CloudMusic API — The Base of Everyhing',bd=0,command=lambda:webbrowser.open("https://github.com/Binaryify/NeteaseCloudMusicApi")).pack(padx=25)

ttk.Separator(awin).pack(fill=tk.X,padx=50,pady=10)

tk.Label(aroot,text='Attention',font=('微软雅黑',15)).pack(padx=25,pady=5)
tk.Label(aroot,text='DO NOT SELL ANY MUSIC DOWNLOADED BY THIS SOFWARE',fg='#FF0000').pack()
tk.Label(aroot,text='THE SOFWARE IS FREE AND OPEN SOURCE, IF YOU BOUGHT THIS, PLEASE REPORT TO ME',fg='#FF0000').pack()


#win.pack(fill=tk.BOTH)
nb.pack(fill=tk.BOTH,expand=True)
win_print('Software Started')

#print(nb.index(nb.select()))

time.sleep(0.5)
set_wait(False,start=True)

win.mainloop()

# def down():
