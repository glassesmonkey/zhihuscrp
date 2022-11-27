import requests,json
import datetime
import pandas as pd
from selectolax.parser import HTMLParser
import random
import tkinter as tk
import tkinter.messagebox

def crawler(start,url,headers,source_url):
    print(start)
    global df
    data= {
        'include':'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,vip_info,badge[*].topics;data[*].settings.table_of_content.enabled',
        'offset':start,
        'limit':20,
        'sort_by':'default',
        'platform':'desktop'
    }

    #将携带的参数传给params
    r = requests.get(url, params=data,headers=headers)
    res = json.loads(r.text)

    with open('data.txt','w',encoding='utf-8') as f:    #设置文件对象
        f.write(r.text)                 #将字符串写入文件中
        f.close()

    if res['data']:
        for answer in res['data']:
            author = answer['author']['name']
            fans = answer['author']['follower_count']
            content = answer['excerpt']
            # content = HTMLParser(answer['content']).text()
            #content = answer['content']
            created_time = datetime.datetime.fromtimestamp(answer['created_time'])
            updated_time = datetime.datetime.fromtimestamp(answer['updated_time'])
            comment = answer['comment_count']
            voteup = answer['voteup_count']
            link = source_url+str(answer['id'])
            # islab = answer['is_labeled']
            try:
                isyx = answer["paid_info"]["has_purchased"]
            except KeyError:
                continue
            else:
                row = {
                    'author':[author],
                    'fans_count':[fans],
                    'content':[content],
                    'created_time':[created_time],
                    'updated_time':[updated_time],
                    'comment_count':[comment],
                    'voteup_count':[voteup],
                    'url':[link],
                    # 'islab':[islab],
                    'yanxuan':[isyx]
                }
                df = df.append(pd.DataFrame(row),ignore_index=True)

        if len(res['data'])==20:
            crawler(start+20,url,headers,source_url)
    else:
        print(res)

def get_source_path():
    global df
    entry1.get()
    session_id = entry1.get()
    url = f'https://www.zhihu.com/api/v4/questions/{session_id}//answers'
    source_url=f'https://www.zhihu.com/question/{session_id}/answer/'
    headers = {
        'Host':'www.zhihu.com',
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'referer':f'https://www.zhihu.com/question/{session_id}'
    }
    crawler(0,url,headers,source_url)
    salt = ranstr(5)
    df.to_csv(f'{salt}_{session_id}_{datetime.datetime.now().strftime("%Y-%m-%d")}.csv',index=False)
    print("done~")
    tk.messagebox.showinfo('提示','任务完成')

def ranstr(num):#返回一个随机字串，用于生成随机文件名
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'
    result1 = list(H)
    salt = ''
    for i in range(num):
        salt =salt + random.choice(result1)
    return salt

df = pd.DataFrame(columns=('author','fans_count','content','created_time','updated_time','comment_count','voteup_count','url'))
root_window = tk.Tk()
root_window.title('作者：高超')
root_window.geometry('450x300')
labe1 = tk.Label(root_window,text="输入问题ID")
labe1.grid(row=0)
labe2 =tk.Label(root_window,text="zhihu.com/question/284666658，后面这个数字就是问题ID")
labe2.grid(row=1)
entry1 = tk.Entry(root_window)
entry1.grid(row=0,column=1)


button1=tk.Button(root_window,text="运行",command=get_source_path)
button1.grid(row=2,column=1)

root_window.mainloop()