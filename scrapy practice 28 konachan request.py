# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 13:25:32 2020

@author: 83930
"""
import os
import requests
import json
import time

#请求头
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
}

proxies_v2ray = {
'http':'socks5://127.0.0.1:10808',
'https':'socks5://127.0.0.1:10808',
}

proxies_ssr={
'http':'socks5://127.0.0.1:10807',
'https':'socks5://127.0.0.1:10807',
}

tags=input('Input:请输入您的tags（默认为空则爬取整个konachan站）:')
pages_num=int(input('Input:请输入您爬取的页数，默认为所有页数'))

if tags==None:
    final_folder = './Konachan/'
else:
    final_folder = './Konachan/'+tags+'/'

os.makedirs(final_folder, exist_ok=True)

if pages_num<11486:
    pages_num=pages_num+1
else:
    pages_num=11487


for n in range(1,pages_num):#range的pages需要调整一下，自动爬取,2020.03.28数据为11486
    url_com='https://konachan.com/post.json?page='+str(n)+'&tags='+tags#com:18+
    url_net='https://konachan.com/post.json?page='+str(n)+'&tags='+tags#net:健全
#    req = urllib.request.Request(url)
#    html = urllib.request.urlopen(req,timeout=500).read()
    req=requests.get(url_net,headers=headers,proxies=proxies_v2ray).content
    jsonlist=json.loads(req)
    #print(jsonlist)
    if len(jsonlist)==0:
        break
    else:
        for i in range(len(jsonlist)):
            #print(jsonlist[i]['file_url'])
            id_number=jsonlist[i]['id']
            file_suffix = os.path.splitext(jsonlist[i]['file_url'])[1]
            #print(file_suffix)
            if os.access(final_folder+'%s'%id_number+file_suffix, os.F_OK):
                print('图片{}存在，跳过'.format(id_number))
            else:
                r=requests.get(jsonlist[i]['file_url'],headers=headers,proxies=proxies_v2ray)
                print('下载{}图片'.format(id_number))
                with open(final_folder+'%s'%id_number+file_suffix, 'wb') as f:
                    f.write(r.content)
    
    print('进入休眠3s')
    time.sleep(3)

print('Finish!')