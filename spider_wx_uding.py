# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 14:01:15 2018

@author: dingru1
"""
# -*- coding: utf-8 -*-
import re
import time
import requests
import pandas as pd
import urllib
import socket #用于设置爬虫等待超时时间
from urllib import request
from bs4 import BeautifulSoup 
from urllib.request import urlopen
"""
问题：通常趴几个网页后，会被远程主机强迫关闭一个现有连接，导致程序需要人为重启
"""


def headers_to_dict(headers):
    """
    将字符串
    '''
    Host: mp.weixin.qq.com
    Connection: keep-alive
    Cache-Control: max-age=
    '''
    转换成字典类型
    :param headers: str
    :return: dict
    """
    headers = headers.split("\n")
    d_headers = dict()
    for h in headers:
        h = h.strip()
        if h:
            k, v = h.split(":", 1)
            d_headers[k] = v.strip()
    return d_headers


def extract_data(html_content):
    """
    从html页面中提取历史文章数据
    :param html_content 页面源代码
    :return: 历史文章列表
    """
    import html
    import json

    rex = "msgList = '({.*?})'"
    pattern = re.compile(pattern=rex, flags=re.S)
    match = pattern.search(html_content)
    if match:
        data = match.group(1)
        data = html.unescape(data)
        data = json.loads(data)
        articles = data.get("list")
        for item in articles:
            print(item)
        return articles


def crawl(url,headers):
    response = requests.get(url, headers=headers, verify=False)
    # print(response.text) #打印返回全部的内容
    if '<title>验证</title>' in response.text:  # 如果提示失败了，请检查请求头，看下Cookie是否失效
        raise Exception("获取微信公众号文章失败，可能是因为你的请求参数有误，请重新获取")
    data = extract_data(response.text)
    url_title = []
    for item in data:
        try:
            url_title.append([item['app_msg_ext_info']['title'],item['app_msg_ext_info']['content_url']])
        except:
            pass
    url_info = pd.DataFrame(url_title,columns=['title','url'])
    response.close()
    return url_info


def mkdir(path):
    import os
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)  
        return True
    else:
        return False


#获取网页源码
def getHtmlCode(url,headers):  # 该方法传入url，返回url的html的源码  

    r= requests.get(url,headers=headers)  
    r.encoding='UTF-8'  
    page = r.text
    
    return page 


#用BeautifulSoup公众号文本信息
def getData(url,i,headers): 
    #调用getSoup函数获取网页源码
    soup = BeautifulSoup(getHtmlCode(url,headers),'lxml')
    p_c = soup.find_all("p")
    contents = []
    for content in p_c:
        contents.append(content.text)
    file = open('{}/text.txt'.format(i),'w')  
    try:
        file.write(str(contents))
    except UnicodeError as u:
        pass
    file.close()
    

#用BeautifulSoup公众号图片信息
def getImg(url,s): 
    #调用getSoup函数获取网页源码
    soup = BeautifulSoup(getHtmlCode(url),'lxml')
    p_c = soup.find_all("img")
    img_srcs = []
    for img_src in p_c:
        try:
            img_srcs.append(img_src.attrs['data-src'])
            time.sleep(1)
        except:
            pass
    i = 1 
    for img in img_srcs:
        request.urlretrieve(img,"{}/img/{}.jpg".format(s,i))
        time.sleep(1)  #防止出现远程主机强迫关闭
        i = i+1
  

def getHtml(url,file_name):
    html = urllib.request.urlopen(url)
    with open(file_name + ".html", "wb") as f:    #写文件用bytes而不是str，所以要转码    
        f.write(html.read())
    html.close()   #防止出现远程主机强迫关闭
    

if __name__ == '__main__':
    socket.setdefaulttimeout(20)    
    # headers中的参数需要根据自己的情况做调整
    # header 通过fiddler抓包获取，方法与下面的url获取方法相同 
    headers = """
    Host: mp.weixin.qq.com
    Cookie: wxuin=2736537080;devicetype=Windows7;version=6206021b;lang=zh_CN;pass_ticket=43OC8b0wJ8JZ18/1oUdoTLXK5KjQcUACeD76iiCEnHz6TKb9QKDukJX8r2nPueB4;wap_sid2=CPj78JgKElxVUnFtMXBxbWN5ZjliMEhEVEUtT1o1OURsUElNQ3hfNk5DeWlqLTk3VlpKbWNKLUFjSEVUR3lEcWNHbVRncDVZMUtyUFQ3WjFCdnp5SVBTSkJsS2x3OUFEQUFBfjDZ4qzdBTgNQJVO
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400
    Accept-Language:  zh-cn
    Accept-Encoding:  gzip, deflate
    Connection: keep-alive
    """
    headers = headers_to_dict(headers)
    url_infos = pd.DataFrame()
    for i in range(0,300,10):  #历史文章超过10篇需要设置offset(距第一篇文章的距离)爬取10篇之后的历史文章
        # url中的参数需要根据自己的情况做调整，
        #电脑端打开fiddler
        #电脑端打开要爬取的微信公总号历史文章所在页
        #电脑端下拉历史文章
        #分析fiddler中爬取的含 “https://mp.weixin.qq.com/mp/profile_ext?”网页的url特点
        url = "https://mp.weixin.qq.com/mp/profile_ext?" \
              "action=getmsg&" \
              "__biz=MzA3NTUxODkzOA==&" \
              "scene=124&" \
              "devicetype=Windows 7&" \
              "version=6206021b&" \
              "lang=zh_CN&" \
              "a8scene=7&" \
              "offset={}&" \
              "count=10&" \
              "pass_ticket=43OC8b0wJ8JZ18/1oUdoTLXK5KjQcUACeD76iiCEnHz6TKb9QKDukJX8r2nPueB4" \
              "appmsg_token=976".format(i)
        url_info = crawl(url,headers) #  爬取历史文章标题及其网页链接
        url_infos = url_infos.append(url_info)
    url_infos['url'] = url_infos['url'].str.replace('\\','')
    url_infos.to_csv('uding_url_list.csv') # 保存历史文章标题及其网页链接为csv文件
    urls = url_infos['url'].values.tolist()
    num = range(1,len(urls)+1)
    #==============================================================================
    # 23 28 33 
    #==============================================================================
    for (url,i) in zip(urls[59:],num[59:]):
        print(i)
        if mkdir(str(i)):   #为每一个历史文章创建文件夹
            getHtml(url,'{}/{}'.format(i,i))#保存历史文章为HTML
            getData(url,i,headers) # 保存历史文章的文本内容
            if mkdir('{}/img'.format(i)):
                getImg(url,i) #保存历史文章的图片内容
