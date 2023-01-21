# 导入启动页必须的库
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msgbox
import tkinter.filedialog as filebox
from PIL import Image, ImageTk
import random
import re
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
            mask.attributes("-topmost",True)
            imgf=Image.open("./icon.ico")
            imgr=imgf.resize((256,256))
            img=ImageTk.PhotoImage(image=imgr)
            mask.geometry(str(root.winfo_width())+'x'+str(root.winfo_height()+30)+'+'+str(root.winfo_x()+10)+'+'+str(root.winfo_y()))
            tk.Label(mask,text='',font=('微软雅黑',15),bg='#FFFFFF').pack()
            tk.Label(mask,image=img,font=('微软雅黑',30),bg='#FFFFFF').pack(pady=50)
            tk.Label(mask,text='正在启动',font=('微软雅黑',15),bg='#FFFFFF').pack()
            f=open("./tips.txt",'r',encoding='utf-8')
            tips=f.read()
            tiplst=tips.split('\n')
            tip=tiplst[random.randint(0,len(tiplst)-1)]
            tk.Label(mask,text=tip,font=('微软雅黑',13),bg='#FFFFFF',fg='#909090').pack(pady=30)
        else:
            mask.configure(background='#000000')
            mask.attributes("-alpha",0.7)
            mask.geometry(str(root.winfo_width())+'x'+str(root.winfo_height())+'+'+str(root.winfo_x()+10)+'+'+str(root.winfo_y()+30))
            tk.Label(mask,text='加载中',font=('微软雅黑',30),bg='#000000',fg='#FFFFFF').pack(pady=150)
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
            win_print('可忽略错误：在未设置等待时就取消设置等待')
        root.update()


root = tk.Tk()
root.title('音乐地带')
#win.iconbitmap("./icon.ico")
root.minsize(600,510)
#root.geometry('400x600')
root.iconbitmap("./icon.ico")

nb=ttk.Notebook(root)

root.update()
set_wait(True,start=True)


#导入其余的库，分为两部分是为了缩短启动界面出现前的等待时间
import requests
#import json
import webbrowser
import os
import threading
from ctypes import *
import datetime,time
import eyed3
from eyed3.id3.frames import ImageFrame
import win32clipboard
import json


#读配置
if not os.path.exists("./config.json"):
    f=open("./config.json",'w',encoding='utf-8')
    #创建默认配置
    config={'Fluent UI':False,'API Domain':'cloudmusic-api.txm.world','Use SSL':True} #默认配置
    f.write(json.dumps(config))
    f.close()

f=open("./config.json",'r',encoding='utf-8')
config_content=f.read()
config=json.loads(config_content)


def gen_settings_page(parent):
    global config,ttkstyle,conf_pts,conf_switches
    conf_pts=[] #设置的行（设置项）
    conf_switches=[] #设置项对应的开关
    conf_types=[] #设置项的类型，无法识别则存储为"unknown"
    index=0 #当前索引
    for conf in list(config.keys()):
        conf_pts.append(tk.Frame(parent,height=70))
        tk.Label(conf_pts[index],text=str(conf),font=('微软雅黑',13)).pack(side=tk.LEFT)
        conf_types.append(type(config[conf]))
        #调整设置的控件会根据数据类型而变化，故使用if语句来判断
        if type(config[conf])==bool: #布尔 -> 复选框
            conf_switches.append(ttk.Checkbutton(conf_pts[index],text='启用',takefocus=False))
            conf_switches[index].pack(side=tk.RIGHT)
            #conf_switches[index].state(['!alternate'])
            # 接下来就是根据读取的值进行填入
            if not bool(config[conf]):
                conf_switches[index].state(['!alternate'])
            elif bool(config[conf]):
                conf_switches[index].state(['!selected'])
            else:
                conf_switches[index]['state']='disabled'
                conf_switches[index]['text']='设置的值不正确'
        elif type(config[conf])==str: #字符串 -> 单行输入框
            conf_switches.append(ttk.Entry(conf_pts[index]))
            conf_switches[index].pack(side=tk.RIGHT)
            conf_switches[index].insert(tk.END,config[conf])
        else: #其他 -> 无法识别的文本提示
            conf_switches.append(tk.Label(conf_pts[index],text='无法识别此配置项，请参阅帮助文档\n这不会造成错误，因为配置内容是按需调用的',
                                 fg='#808080',justify='right'))
            conf_types[index]='unknown'
            conf_switches[index].pack(side=tk.RIGHT)
        conf_pts[index].pack(fill=tk.X,pady=5)
        index+=1


def save_settings():
    global config,conf_switches,conf_types
    print(conf_switches[0].state())
    #print(conf_switches)
    config_new=config #修改过的设置（保险起见，在原先的config上做修改）
    index=0 #当前索引
    for conf in list(config.keys()):
        #按照生成设置界面的代码，判断数据类型，决定如何获取输入的值
        if type(config[conf])==bool: #布尔 -> 直接获取config内的对应内容（CheckButton只能与变量绑定）
            config_new[conf]=bool(conf_switches[index].state())
        elif type(config[conf])==str: #字符串 -> Entry.get()
            config_new[conf]=str(conf_switches[index].get())
        index+=1
    win_print("将保存配置信息，内容："+json.dumps(config_new))
    f=open("./config.json",'w',encoding='utf-8')
    f.write(json.dumps(config_new))
    f.close()


def delButton(tree):
    x = tree.get_children()
    for item in x:
        tree.delete(item)

def find_song(word):
    global config,apiurl
    set_wait(True)
    try:
        global mids,mnames,gkw
        gkw=word
        delButton(tree)
        #load_full_t=threading.Thread(target=lambda:load_full(word))#放在前面可以尽早覆盖加载全部的进程
        res=requests.get(url=apiurl+"/search?keywords="+word)
        json=res.json()
        mids=[]
        mnames=[]
        if json['result']=={}:# or json['result']['songCount']==0:
            mids.append('5221167')
            mnames.append('未找到任何内容')
            tree.insert("", 0, text=str(0), values=('1', '未找到任何内容', '不要听这个', '你猜'))  # 插入数据
        else:
            mlst=json['result']['songs']
            win_print('共找到 '+str(json['result']['songCount'])+' 条结果，当前显示30条，完整结果在后台加载')
            for m in mlst:
                #由于网易云的接口返回信息的结构有时候隔几天就会有细微变化，歌手与专辑的键一下是ar和al，一下是全称，所以让程序自己随机应变吧
                if 'ar' in list(m.keys()):
                    mar=m['ar']
                    #mal=m['al']
                if 'artists' in list(m.keys()):
                    mar=m['artists']
                    #mal=m['album']
                else:
                    msgbox.showerror('错误','程序无法理解接口返回的数据')
                mids.append(str(m['id']))
                mnames.append(m['name'])
                ars=''
                for ar in mar:
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
        print('出错函数：find_song')
        print('--------------------')
        print('网络信息：')
        print('访问链接：'+"https://cloudmusic-api.txm.world/search?keywords="+word)
        print('返回数据不显示，以免进一步引发错误')
        print('--------------------')
        print('本地报错信息：')
        print(e)
        print('--------------------')
        print('额外信息：')
        #print('当前结果数：'+str(len(mids)))
        print('====================')
    set_wait(False)

def get_fav(usr,pwd):
    global config,apiurl
    set_wait(True)
    delButton(ftree)
    try:
        global mids,mnames

        url=apiurl+"/login?email="+usr+"&password="+pwd
        res=requests.get(url)
        json=res.json()
        cookie=json['cookie']

        url=apiurl+"/user/account?cookie="+str(cookie)
        res=requests.get(url)
        json=res.json()
        uid=str(json['account']['id'])

        url=apiurl+"/user/playlist?limit=1&uid="+uid
        res=requests.get(url)
        json=res.json()
        favlstid=str(json['playlist'][0]['id'])

        url=apiurl+"/playlist/track/all?id="+favlstid+"&cookie="+cookie
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
        print('返回数据不显示，以免进一步引发错误')
        print('--------------------')
        print('本地报错信息：')
        print(e)
        print('--------------------')
        print('额外信息：')
        #print('当前结果数：'+str(len(mids)))
        print('====================')
    set_wait(False)

def get_all_style():
    global config,apiurl,styles,astree
    set_wait(True)
    delButton(astree)
    res=requests.get(apiurl+"/style/list")
    json=res.json()
    style_lst=json['data']
    thread_list=[]
    #遍历父级
    for style in style_lst:
        #styles[style['enName']+' （'+style['tagName']+'）'+'   ID：'+str(style['tagId'])]=[]#字典中每个key都是一种风格
        lst_parent = astree.insert('', 'end', text=style['enName'],values=(style['tagName'],str(style['tagId'])))
        thread_list.append(threading.Thread(target=lambda:show_child_styles(style,lst_parent)))#绝招：多线程加载子分类
        thread_list[style_lst.index(style)].start()
    win_print('顶级曲风分类加载完毕，更多曲风将在后台加载')
    #styles={}
    #tree_parent = astree.insert('', 'end', text='所有曲风')
    #json2treeview(astree,tree_parent,styles)
    set_wait(False)

def get_fav_style(usr,pwd):
    global config,apiurl,styles,fsstree
    delButton(fstree)
    set_wait(True)
    
    url=apiurl+"/login?email="+usr+"&password="+pwd
    res=requests.get(url)
    json=res.json()
    cookie=json['cookie']

    res=requests.get(apiurl+"/style/preference?limit=20?cookie="+cookie)
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
    global config,apiurl
    set_wait(True)
    try:
        global mids,mnames,gkw
        gkw=tagid
        delButton(smtree)
        #load_full_t=threading.Thread(target=lambda:load_full(word))#放在前面可以尽早覆盖加载全部的进程
        res=requests.get(url=apiurl+"/style/song?tagId="+tagid)
        json=res.json()
        mids=[]
        mnames=[]
        if json['data']['songs']==[]:
            mids.append('5221167')
            mnames.append('未找到任何内容')
            tree.insert("", 0, text=str(0), values=('1', '未找到任何内容', '不要听这个', '你猜'))  # 插入数据
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
                    no+=' | 试听'
                elif int(m['fee'])==4:
                    no+=' | 付费'
                smtree.insert("", mlst.index(m), text=str(mlst.index(m)), values=(no, m['name'], ars, m['id']))  # 插入数据
            #if len(mids)>=30 and json['result']['hasMore']:
                #load_full_t.start()
    except Exception as e:
        win_print('程序出错，对开发者来说，最有用的东西都在控制台')
        print('出错函数：get_style_music')
        print('--------------------')
        print('网络信息：')
        print('访问链接：'+"https://cloudmusic-api.txm.world/search?keywords="+tagid)
        print('返回数据不显示，以免进一步引发错误')
        print('--------------------')
        print('本地报错信息：')
        print(e)
        print('--------------------')
        print('额外信息：')
        #print('当前结果数：'+str(len(mids)))
        print('====================')
    set_wait(False)

def down():
    global config,apiurl,nb
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
            msgbox.showerror('本地错误','您不能在本页使用此功能！')
            return
    else:
        msgbox.showerror('本地错误','您不能在本页使用此功能！')
        return
    select = item_text[0]
    select=select.split(' | ')[0]
    select=int(select)
    # return songmid[select-1], song_singer[select-1]
    mid = mids[select - 1]
    mname = mnames[select - 1]
    res=requests.get(url=apiurl+"/song/url?id="+mid+"&br=320000")#+'&cookie='+cookie)
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
    if murl==None:
        msgbox.showerror('错误',mname+' 无版权')
        win_print(mname+' 无版权')
    else:
        res=requests.get(url=murl)
        m=res.content
        f=open(save_path,'wb')
        f.write(m)
        f.close()
    infres=requests.get(url=apiurl+"/song/detail?ids="+mid)
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
    #f=open("./cache.jpg",'wb')
    #f.write(img)
    #f.close()
    if murl==None:
        win_print(mname+' 无版权')
        msgbox.showerror('音乐无版权',mname+' 无版权，没有音频可供下载')
    else:
        res=requests.get(url=murl)
        m=res.content
        #编辑信息
        audiofile = eyed3.load(save_path)
        audiofile.initTag()
        audiofile.tag.title = inf['name']
        audiofile.tag.artist = ars
        audiofile.tag.album = inf['al']['name']
        audiofile.tag.images.set(ImageFrame.FRONT_COVER, img, 'image/jpeg')
        audiofile.tag.recording_date = str(pubyear)  # 年份
        audiofile.tag.save(version=eyed3.id3.ID3_V2_3)
    set_wait(False)

def play():
    global config,apiurl,nb
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
            msgbox.showerror('本地错误','您不能在本页使用此功能！')
            return
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
    res=requests.get(url=apiurl+"/song/url?id="+mid+"&br=320000")#+'&cookie='+cookie)
    json=res.json()
    murl=json['data'][0]['url']
    if murl==None:
        msgbox.showerror('错误',mname+' 无版权')
        win_print(mname+' 无版权')
    else:
        res=requests.get(url=murl)
        m=res.content
        f=open(save_path,'wb')
        f.write(m)
        f.close()
    infres=requests.get(url=apiurl+"/song/detail?ids="+mid)
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
        audiofile.tag.artist = '这可不能怪我哦'
        audiofile.tag.album = '这是你自愿上钩的啊！'
    else:
        audiofile.tag.artist = ars
        audiofile.tag.album = inf['al']['name']
    imgf=open("./cache.jpg",'wb')  # 封面
    imgf.write(img)
    imgf.close()
    audiofile.tag.recording_date = str(pubyear)  # 年份
    audiofile.tag.save()
    set_wait(False)
    win_print('下载完成，启动播放器')
    os.popen('ma_player.exe')

def openweb():
    global config,apiurl,nb
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
            msgbox.showerror('本地错误','您不能在本页使用此功能！')
            return
    else:
        msgbox.showerror('本地错误','您不能在本页使用此功能！')
        return
    select = item_text[0]
    select=select.split(' | ')[0]
    select=int(select)
    # return songmid[select-1], song_singer[select-1]
    mid = mids[select - 1]
    webbrowser.open("https://music.163.com/#/song?id="+mid)
    set_wait(False)

def copyid():
    global config,apiurl,nb
    id_index=3
    if int(nb.index(nb.select()))==0:#搜索下载
        for item in tree.selection():
            item_text = tree.item(item, "values")
        idtype='歌曲'
    elif int(nb.index(nb.select()))==1:#收藏下载
        for item in ftree.selection():
            item_text = ftree.item(item, "values")
        idtype='歌曲'
    elif int(nb.index(nb.select()))==2:#曲风搜歌
        if int(swin.index(swin.select()))==0:#所有曲风
            for item in astree.selection():
                item_text = astree.item(item, "values")
            id_index=1
            idtype='风格'
        elif int(swin.index(swin.select()))==1:#曲风偏好
            for item in fstree.selection():
                item_text = fstree.item(item, "values")
            idtype='风格'
        elif int(swin.index(swin.select()))==2:#该风格的歌曲
            for item in smtree.selection():
                item_text = smtree.item(item, "values")
            idtype='歌曲'
        else:
            msgbox.showerror('本地错误','您不能在本页使用此功能！')
            return
    else:
        msgbox.showerror('本地错误','您不能在本页使用此功能！')
        return
    mid = item_text[id_index]
    ###
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(str(mid))
    win32clipboard.CloseClipboard()
    msgbox.showinfo('复制完成','已将'+str(idtype)+'ID（'+str(mid)+'）复制到剪切板')

#https://www.jianshu.com/p/c6aae4d3f80d上有好东西，它原本在这里

def win_print(word):
    global consle
    console['state']='normal'
    console.insert('end', word)
    console.insert('end', '\n')
    console.see(tk.END)
    console['state']='disabled'
    win.update()

def compare_ver(ver1, ver2):
    """
    传入不带英文的版本号,特殊情况："10.12.2.6.5">"10.12.2.6"
    :param ver1: 版本号1
    :param ver2: 版本号2
    :return: ver1< = >ver2返回-1/0/1
    """
    list1 = str(ver1).split(".")
    list2 = str(ver2).split(".")
    #print(list1)
    #print(list2)
    # 循环次数为短的列表的len
    for i in range(len(list1)) if len(list1) < len(list2) else range(len(list2)):
        if int(list1[i]) == int(list2[i]):
            pass
        elif int(list1[i]) < int(list2[i]):
            return -1
        else:
            return 1
    # 循环结束，哪个列表长哪个版本号高
    if len(list1) == len(list2):
        return 0
    elif len(list1) < len(list2):
        return -1
    else:
        return 1

def chkupd():
    global nowver,newver
    nowver='5.3.4'
    res=requests.get("https://api.github.com/repos/totowang-hhh/music_down/releases/latest", verify=False) #该站SSL无效
    json=res.json()
    #print(json)
    newver=json['tag_name'].replace('v','')
    if compare_ver(nowver,newver)==-1:
        return True
    elif compare_ver(nowver,newver)==1:
        msgbox.showwarning('警告','您的版本（'+nowver+'）大于最新版（'+newver+'），若您未征得作者许可，请停止使用内部版本！')
        return False
    else:
        return False

def chkupdui(start=False):
    if chkupd():
        if bool(msgbox.askyesno('版本更新','您的版本（'+nowver+'）小于最新版（'+newver+'），\n这说明有版本更新可用，您需要前往新版下载页吗？')):
            webbrowser.open("http://www.github.com/totowang-hhh/music_down/releases/latest")
    else:
        if not start:
            msgbox.showinfo('恭喜','您正在使用的版本是最新的')


btnpt=tk.Frame(root)

ttk.Button(btnpt, text='下载', command=down).pack(fill=tk.X,side=tk.LEFT,expand=True)
ttk.Button(btnpt, text='收听', command=play).pack(fill=tk.X,side=tk.LEFT,expand=True)
ttk.Button(btnpt, text='复制ID', command=copyid).pack(fill=tk.X,side=tk.LEFT,expand=True)
ttk.Button(btnpt, text='在网页中查看', command=openweb).pack(fill=tk.X,side=tk.LEFT,expand=True)

btnpt.pack(fill=tk.X,side=tk.BOTTOM)


#搜索下载
win=tk.Frame(nb)
nb.add(win, text='搜索下载')

searchPart = tk.Frame(win)
ttk.Button(searchPart, text='搜索', command=lambda:find_song(nameEnter.get()), width=12).pack(side=tk.RIGHT, fill=tk.Y)
nameEnter = ttk.Entry(searchPart)
nameEnter.pack(fill=tk.X)

searchPart.pack(fill=tk.BOTH)

nameEnter.bind('<Return>', lambda event:find_song(nameEnter.get()))

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

tree.pack(fill=tk.BOTH,expand=True)#最后pack，让它充满页面且不出错


#收藏下载
fwin=tk.Frame(nb)
nb.add(fwin, text='收藏下载')

loginPart = tk.Frame(fwin)
ttk.Button(loginPart, text='登录并\n查看收藏', command=lambda:get_fav(usrEnter.get(),pwdEnter.get()), width=12).pack(side=tk.RIGHT, fill=tk.Y)
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


#曲风搜歌
swin=ttk.Notebook(nb)
nb.add(swin, text='曲风搜歌')

#全部曲风
aswin=tk.Frame(swin)
swin.add(aswin,text='全部曲风')

astree = ttk.Treeview(aswin)  #树状图
astree["columns"] = ("译名", "曲风ID")
astree.column("译名", width=100)
astree.column("曲风ID", width=50)
astree.heading("译名", text="译名")
astree.heading("曲风ID", text="曲风ID")

ttk.Button(aswin,text='获取所有曲风',command=get_all_style).pack(side=tk.BOTTOM,fill=tk.X)

astree.pack(fill=tk.BOTH,expand=True)

#曲风偏好
fswin=tk.Frame(swin)
swin.add(fswin,text='曲风偏好')

fsloginPart = tk.Frame(fswin)
ttk.Button(fsloginPart, text='登录并查看\n曲风偏好', command=lambda:get_fav_style(fsusrEnter.get(),fspwdEnter.get()), width=12).pack(side=tk.RIGHT, fill=tk.Y)
fstippt=tk.Frame(fsloginPart)
tk.Label(fstippt,text='账户 ').pack()
tk.Label(fstippt,text='密码 ').pack()
fstippt.pack(side=tk.LEFT)
fsusrEnter = ttk.Entry(fsloginPart)
fsusrEnter.pack(fill=tk.X)
fspwdEnter = ttk.Entry(fsloginPart,show='●')
fspwdEnter.pack(fill=tk.X)

fsloginPart.pack(fill=tk.BOTH)

fsusrEnter.bind('<Return>', lambda event:fspwdEnter.focus())
fspwdEnter.bind('<Return>', lambda event:get_fav_style(fsusrEnter.get(),fspwdEnter.get()))

tk.Label(fswin,text='理论上每次获取的数据不同，实际上会因为API缓存，再一段时间（2分钟）内获取到相同数据',fg='#0000FF').pack(fill=tk.X)

fstree = ttk.Treeview(fswin, show="headings")  # 表格
fstree["columns"] = ("序号", "名称", "收听百分比","曲风ID")
fstree.column("序号", width=10)
fstree.column("名称", width=100)  # 表示列,不显示
fstree.column("收听百分比", width=70)
fstree.column("曲风ID", width=50)
fstree.heading("序号", text="序号")
fstree.heading("名称", text="名称")  # 显示表头
fstree.heading("收听百分比", text="收听百分比")
fstree.heading("曲风ID", text="曲风ID")

fstree.pack(fill=tk.BOTH,expand=True)

#该曲风的音乐
smwin=tk.Frame(swin)
swin.add(smwin, text='该曲风的音乐')

smsearchPart = tk.Frame(smwin)
ttk.Label(smsearchPart, text='曲风ID').pack(side=tk.LEFT, fill=tk.Y)
ttk.Button(smsearchPart, text='获取该曲风的歌曲', command=lambda:get_style_music(smnameEnter.get())).pack(side=tk.RIGHT, fill=tk.Y)
smnameEnter = ttk.Entry(smsearchPart)
smnameEnter.pack(fill=tk.X)

smsearchPart.pack(fill=tk.BOTH)

smnameEnter.bind('<Return>', lambda event:get_style_music(smnameEnter.get()))

smtree = ttk.Treeview(smwin, show="headings")  # 表格
smtree["columns"] = ("序号", "歌曲", "艺人","歌曲ID")
smtree.column("序号", width=10)
smtree.column("歌曲", width=100)  # 表示列,不显示
smtree.column("艺人", width=70)
smtree.column("歌曲ID", width=10)
smtree.heading("序号", text="序号")
smtree.heading("歌曲", text="歌曲")  # 显示表头
smtree.heading("艺人", text="艺人")
smtree.heading("歌曲ID", text="歌曲ID")

smtree.pack(fill=tk.BOTH,expand=True)


#控制台
console = tk.Text(nb,font=('consolas', '10'),height=10)
nb.add(console, text='友好输出')


#关于
aroot=tk.Frame(nb)
awin=tk.Frame(aroot,width=400,height=500)
awin.pack()
nb.add(aroot, text='关于')

#tk.Label(awin,text='',font=('微软雅黑',15)).pack(padx=25)
tk.Label(awin,text='音乐地带',font=('微软雅黑',25)).pack(padx=25,pady=15)
tk.Button(awin,text='版本：5.3.4   配套播放器：0.1.1',bd=0,command=chkupdui).pack(padx=25)
tk.Label(awin,text='2022 By 真_人工智障').pack(padx=25)

ttk.Button(awin, text='我的官网', command=lambda: webbrowser.open("http://rgzz.likesyou.org/")).pack(padx=25,pady=5)
ttk.Button(awin, text='项目GitHub', command=lambda: webbrowser.open("https://github.com/totowang-hhh/music_down/")).pack(padx=25,pady=5)

ttk.Separator(awin).pack(fill=tk.X,padx=50,pady=10)

tk.Label(awin,text='鸣谢',font=('微软雅黑',15)).pack(padx=25,pady=5)
tk.Button(awin,text='Vercel — API部署',bd=0,command=lambda:webbrowser.open("https://www.vercel.com")).pack(padx=25)
tk.Button(awin,text='Heymu — 播放器',bd=0,command=lambda:webbrowser.open("https://teameow.xyz/")).pack(padx=25)
tk.Button(awin,text='AXIOMXS — 二级域名',bd=0,command=lambda:msgbox.showinfo('关于他','AXIOMXS，官网已删，网名频繁修改\n为尊重隐私，故不提供联系方式')).pack(padx=25)
tk.Button(awin,text='网易云音乐 NodeJS 版 API — 一切之本',bd=0,command=lambda:webbrowser.open("https://github.com/Binaryify/NeteaseCloudMusicApi")).pack(padx=25)

ttk.Separator(awin).pack(fill=tk.X,padx=50,pady=10)

tk.Label(aroot,text='声明',font=('微软雅黑',15)).pack(padx=25,pady=5)
tk.Label(aroot,text='请勿将任何下载的音乐用于商业用途，出现任何版权问题作者概不负责',fg='#FF0000').pack()
tk.Label(aroot,text='作者承诺软件无强制性收费且开源，若您为购买所得，请立即向平台或作者举报！',fg='#FF0000').pack()


seroot=tk.Frame(nb)
nb.add(seroot, text='设置')

ttk.Button(seroot,text='应用（部分设置重启后生效）',command=save_settings).pack(side=tk.BOTTOM,fill=tk.X)

sewin=tk.Frame(seroot)
gen_settings_page(sewin)
sewin.pack(fill=tk.BOTH,expand=True,padx=50,pady=30)

#sewin.pack()


#win.pack(fill=tk.BOTH)
nb.pack(fill=tk.BOTH,expand=True)
win_print('程序启动完成')

#print(nb.index(nb.select()))


#大部分配置被使用的位置
if bool(config['Fluent UI']): #根据配置信息使用Fluent UI主题（注：本主题设置窗口大小会卡顿，主题作者已发现该问题，并认为暂时无解）
    import sv_ttk
    sv_ttk.set_theme("light")

if bool(config['Use SSL']): #根据配置信息决定是否使用SSL（即使用http还是https）
    apiurl="https://"+str(config['API Domain'])
else:
    apiurl="http://"+str(config['API Domain'])

if not re.match(r"^https?:/{2}\w.+$",apiurl): #必需先确认是否为有效的配置项，因为此配置若出现错误会导致软件无法使用
    #配置信息内容有误则会直接使用默认（域名cloudmusic-api.txm.world，使用SSL）
    win_print("API域名配置有误，将使用默认域名。详细信息请参阅帮助文档。")
    apiurl="https://cloudmusic-api.txm.world"

win_print("将使用网址为 "+apiurl+" 的API，您可以检查其可用性")


#消除启动页并检查更新
time.sleep(1)
try:
    chkupdui(start=True)
    set_wait(False,start=True)
except:
    set_wait(False,start=True)
    msgbox.showwarning('警告','无法检测更新。\n这意味着您似乎未连接到互联网，可能无法使用软件。\n\n如果您位于中国大陆且未使用网络加速工具，则该问题可能因为无法连接GitHub所导致，'+
                       '这种情况下您将无法检测更新，但仍可使用软件。\n\n如果您正在使用较久远的版本，也可能是因为版本命名规则有变，该版本无法识别最新版本号。')


#窗口主循环
win.mainloop()

# def down():   注：这条注释可能在3.x开始开发时就已经存在于该文件中了，可以算是整个文件最久远的一条注释……目前我不打算删除……
