# 导入库
import requests
#import json
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox
import tkinter.filedialog as filebox
from tkinter import *
import webbrowser
import os
import threading
from ctypes import *
import datetime
import eyed3
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32


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
            mnames.append('呕吼 嘛也没找到')
            tree.insert("", 0, text=str(0), values=('1 | 这不是结果', '呕吼 嘛也没找到', '不要听这个', '你猜'))  # 插入数据
        else:
            mlst=json['result']['songs']
            win_print('共找到 '+str(json['result']['songCount'])+' 条结果，当前显示30条，完整结果在后台加载')
            for m in mlst:
                mids.append(str(m['id']))
                mnames.append(m['name'])
                ars=''
                for ar in m['artists']:
                    ars+=ar['name']+' / '
                ars=ars[0:len(ars)-3]
                no=str(mlst.index(m)+1)
                if int(m['fee'])==1:
                    no+=' | 试听'
                elif int(m['fee'])==4:
                    no+=' | 付费'
                tree.insert("", mlst.index(m), text=str(mlst.index(m)), values=(no, m['name'], ars, m['id']))  # 插入数据
            #if len(mids)>=30 and json['result']['hasMore']:
                #load_full_t.start()
    except Exception as e:
        win_print('程序出错，对开发者来说，最有用的东西都在控制台')
        print('出错函数：loadfull')
        print('--------------------')
        print('网络信息：')
        print('访问链接：'+"https://cloudmusic-api.txm.world/search?keywords="+word)
        print('返回数据：'+str(json))
        print('--------------------')
        print('本地报错信息：')
        print(e)
        print('--------------------')
        print('额外信息：')
        print('当前结果数：'+str(len(mids)))
        print('====================')
    set_wait(False)

def get_fav(usr,pwd):
    set_wait(True)
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
        win_print('程序出错，对开发者来说，最有用的东西都在控制台')
        print('出错函数：getfav')
        print('--------------------')
        print('网络信息：')
        print('访问链接：'+url)
        print('返回数据：'+str(json))
        print('--------------------')
        print('本地报错信息：')
        print(e)
        print('--------------------')
        print('额外信息：')
        print('当前结果数：'+str(len(mids)))
        print('====================')
    set_wait(False)

def load_full(kw):
    win_print('可忽略的错误：load_full()函数内含未知错误，现已暂时禁用')
    return
    global mids,mnames
    try:
        t=0
        while True:
            if gkw!=kw:#我劝你耗子尾汁（指当检查到用户再次搜索时，直接自己退出
                break
            res=requests.get(url="https://cloudmusic-api.txm.world/search?keywords="+kw+"&limit=1&offset="+str(t+30-1))
            json=res.json()
            if json['result']=={}:
                break
            m=json['result']['songs'][0]
            if m['id'] not in mids:#避免重复
                mids.append(str(m['id']))
                mnames.append(m['name'])
                ars=''
                for ar in m['artists']:
                    ars+=ar['name']+' / '
                ars=ars[0:len(ars)-3]
                no=str(t+31)
                if int(m['fee'])==1:
                    no+=' | 试听'
                tree.insert("", t+30, text=str(t+30), values=(no, m['name'], ars, m['id']))  # 插入数据
            t+=1
        win_print('完整结果加载完毕，共找到 '+str(len(mids))+' 条结果')
    except Exception as e:
        win_print('程序出错，对开发者来说，最有用的东西都在控制台')
        print('出错函数：loadfull')
        print('--------------------')
        print('网络信息：')
        print('访问链接：'+"https://cloudmusic-api.txm.world/search?keywords="+kw+"&limit=1&offset="+str((t+1)*30-1))
        print('返回数据：'+str(json))
        print('--------------------')
        print('本地报错信息：')
        print(e)
        print('--------------------')
        print('额外信息：')
        print('当前结果数：'+str(len(mids)))
        print('====================')

def down():
    global nb
    set_wait(True)
    if int(nb.index(nb.select()))==0:#搜索下载
        for item in tree.selection():
            item_text = tree.item(item, "values")
    elif int(nb.index(nb.select()))==1:#收藏下载
        for item in ftree.selection():
            item_text = ftree.item(item, "values")
    else:
        msgbox.showerror('本地错误','您不能在本页使用此功能！')
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
            cdown=msgbox.askyesno('请注意','该音乐仅可试听 '+str(freesec)+' 秒，您确定要下载吗？')
            if not bool(cdown):
                return
    save_path = filebox.asksaveasfilename(title='保存音乐', initialfile=mname + ".mp3", filetypes=[('MP3音频文件', '.mp3')])
    set_wait(True)
    win_print('正在将 {name} 下载到 {path} ......'.format(name=mname, path=save_path))
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
        win_print(mname+' 无版权')
        msgbox.showerror('音乐无版权',mname+' 无版权，没有音频可供下载')
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
    else:
        msgbox.showerror('本地错误','您不能在本页使用此功能！')
        return
    select = item_text[0]
    select=select.split(' | ')[0]
    select=int(select)
    # return songmid[select-1], song_singer[select-1]
    mid = mids[select - 1]
    mname = mnames[select - 1]
    save_path = "./cache.mp3"
    win_print('将 {name} 下载到 {path} 以试听'.format(name=mname, path=save_path))
    res=requests.get(url="https://cloudmusic-api.txm.world/song/url?id="+mid+"&br=320000")#+'&cookie='+cookie)
    json=res.json()
    murl=json['data'][0]['url']
    if murl==None:
        win_print(mname+' 无版权')
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
    audiofile.tag.artist = ars
    audiofile.tag.album = inf['al']['name']
    imgf=open("./cache.jpg",'wb')  # 封面
    imgf.write(img)
    imgf.close()
    audiofile.tag.recording_date = str(pubyear)  # 年份
    audiofile.tag.save()
    set_wait(False)
    win_print('下载完成，启动播放器')
    set_wait(True,player=True)
    os.popen('ma_player.exe')
    set_wait(False)

def copyid():
    global nb
    if int(nb.index(nb.select()))==0:#搜索下载
        for item in tree.selection():
            item_text = tree.item(item, "values")
    elif int(nb.index(nb.select()))==1:#收藏下载
        for item in ftree.selection():
            item_text = ftree.item(item, "values")
    else:
        msgbox.showerror('本地错误','您不能在本页使用此功能！')
        return
    select = item_text[0]
    select=select.split(' | ')[0]
    select=int(select)
    # return songmid[select-1], song_singer[select-1]
    mid = mids[select - 1]
    ###
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(mid)
    win32clipboard.CloseClipboard()
    msgbox.showinfo('复制完成','已将歌曲ID（'+str(mid)+'）复制到剪切板')

def get_clipboard():
    user32.OpenClipboard(c_int(0))
    contents = c_char_p(user32.GetClipboardData(c_int(1))).value
    user32.CloseClipboard()
    return contents
def empty_clipboard():
    user32.OpenClipboard(c_int(0))
    user32.EmptyClipboard()
    user32.CloseClipboard()

def set_clipboard(data):
    user32.OpenClipboard(c_int(0))
    user32.EmptyClipboard()
    alloc = kernel32.GlobalAlloc(0x2000, len(bytes(data, encoding='utf_8'))+1)
    # alloc = kernel32.GlobalAlloc(0x2000, len(data)+1)
    lock = kernel32.GlobalLock(alloc)
    cdll.msvcrt.strcpy(c_char_p(lock),bytes(data, encoding='utf_8'))
    # cdll.msvcrt.strcpy(c_char_p(lock), data)
    kernel32.GlobalUnlock(alloc)
    user32.SetClipboardData(c_int(1),alloc)
    user32.CloseClipboard()

def search(event=''):
    songname = nameEnter.get()
    # song_mid, singer = find_song(songname)
    find_song(songname)

def set_wait(state,player=False):
    if state:
        global root,mask
        mask=tk.Tk()
        mask.overrideredirect(True)
        mask.geometry(str(root.winfo_width())+'x'+str(root.winfo_height())+'+'+str(root.winfo_x()+10)+'+'+str(root.winfo_y()+30))
        mask.configure(background='#000000')
        mask.attributes("-alpha",0.7)
        if player:
            tk.Label(mask,text='请关闭播放器后操作',font=('微软雅黑',20),bg='#000000',fg='#FFFFFF').pack(pady=150)
        else:
            tk.Label(mask,text='请稍候',font=('微软雅黑',30),bg='#000000',fg='#FFFFFF').pack(pady=150)
        root.update()
        mask.update()
    else:
        try:
            mask.destroy()
        except:
            win_print('可忽略错误：在未设置等待时就取消设置等待')
        root.update()

def win_print(word):
    global consle
    console['state']='normal'
    console.insert('end', word)
    console.insert('end', '\n')
    console.see(tk.END)
    console['state']='disabled'
    win.update()

root = tk.Tk()
root.title('音乐地带')
#win.iconbitmap("./icon.ico")
root.minsize(600,510)
#root.geometry('400x600')
root.iconbitmap("./icon.ico")


nb=ttk.Notebook(root)


#搜索下载
win=Frame(nb)
nb.add(win, text='搜索下载')

searchPart = tk.Frame(win)
ttk.Button(searchPart, text='搜索', command=search, width=12).pack(side=tk.RIGHT, fill=tk.Y)
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
tree.heading("序号", text="序号")
tree.heading("歌曲", text="歌曲")  # 显示表头
tree.heading("艺人", text="艺人")
tree.heading("歌曲ID", text="歌曲ID")

btnpt=tk.Frame(root)

ttk.Button(btnpt, text='下载', command=down).pack(fill=tk.X,side=tk.LEFT,expand=True)
ttk.Button(btnpt, text='收听', command=play).pack(fill=tk.X,side=tk.LEFT,expand=True)
ttk.Button(btnpt, text='复制歌曲ID', command=copyid).pack(fill=tk.X,side=tk.LEFT,expand=True)

btnpt.pack(fill=tk.X,side=tk.BOTTOM)
tree.pack(fill=tk.BOTH,expand=True)#最后pack，让它充满页面且不出错


#收藏下载
fwin=Frame(nb)
nb.add(fwin, text='收藏下载')

loginPart = tk.Frame(fwin)
ttk.Button(loginPart, text='登录并查看收藏', command=lambda:get_fav(usrEnter.get(),pwdEnter.get()), width=12).pack(side=tk.RIGHT, fill=tk.Y)
tippt=tk.Frame(loginPart)
tk.Label(tippt,text='账户 ').pack()
tk.Label(tippt,text='密码 ').pack()
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
ftree.heading("序号", text="序号")
ftree.heading("歌曲", text="歌曲")  # 显示表头
ftree.heading("艺人", text="艺人")
ftree.heading("歌曲ID", text="歌曲ID")

#btnpt=tk.Frame(fwin)

ftree.pack(fill=tk.BOTH,expand=True)#最后pack，让它充满页面且不出错


#控制台
console = tk.Text(nb,font=('consolas', '10'),height=10)
nb.add(console, text='友好输出')


#关于
aroot=Frame(nb)
awin=Frame(aroot,width=400,height=500)
awin.pack()
nb.add(aroot, text='关于')

#tk.Label(awin,text='',font=('微软雅黑',15)).pack(padx=25)
tk.Label(awin,text='音乐地带',font=('微软雅黑',25)).pack(padx=25,pady=15)
tk.Label(awin,text='版本：5.2.0').pack(padx=25)
tk.Label(awin,text='2022 By 真_人工智障').pack(padx=25)

ttk.Button(awin, text='我的官网', command=lambda: webbrowser.open("http://rgzz.great-site.net/")).pack(padx=25,pady=15)

ttk.Separator(awin).pack(fill=tk.X,padx=50,pady=10)

tk.Label(awin,text='鸣谢',font=('微软雅黑',15)).pack(padx=25,pady=5)
tk.Button(awin,text='Vercel — API部署',bd=0,command=lambda:webbrowser.open("https://www.vercel.com")).pack(padx=25)
tk.Button(awin,text='Heymu — 播放器',bd=0,command=lambda:webbrowser.open("https://teameow.xyz/")).pack(padx=25)
tk.Button(awin,text='AXIOMXS — 二级域名',bd=0,command=lambda:msgbox.showinfo('关于他','AXIOMXS，官网已删，网名频繁修改\n为尊重隐私，故不提供联系方式')).pack(padx=25)
tk.Button(awin,text='网易云音乐 NodeJS 版 API — 一切之本',bd=0,command=lambda:webbrowser.open("https://github.com/Binaryify/NeteaseCloudMusicApi")).pack(padx=25)

ttk.Separator(awin).pack(fill=tk.X,padx=50,pady=10)

tk.Label(awin,text='声明',font=('微软雅黑',15)).pack(padx=25,pady=5)
tk.Label(awin,text='请勿将任何下载的音乐用于商业用途，出现任何版权问题作者概不负责',fg='#FF0000').pack()
tk.Label(awin,text='作者承诺软件无强制性收费且开源，若您为购买所得，请立即向平台或作者举报！',fg='#FF0000').pack()


#win.pack(fill=tk.BOTH)
nb.pack(fill=tk.BOTH,expand=True)

win_print('音乐地带')
win_print('版本：5.2.0')
win_print('作者：真_人工智障')
win_print('====================')
win_print('程序启动完成')

#print(nb.index(nb.select()))

win.mainloop()

# def down():
