# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 16:08:44 2018

@author: dingru1
"""
import re
import requests  
import pandas as pd
from bs4 import BeautifulSoup 

#获取网页源码
def getHtmlCode(url):  # 该方法传入url，返回url的html的源码  
    headers = {  
        'User-Agent': 'MMozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'  
    }  
    r= requests.get(url,headers=headers)  
    r.encoding='UTF-8'  
    page = r.text  
    
    return page 


#用BeautifulSoup解析数据    
def getData(url,web_type): 
    #调用getSoup函数获取网页源码
    soup = BeautifulSoup(getHtmlCode(url),'lxml')
    ftx_infos = pd.DataFrame()
    ftx_infos_new = pd.DataFrame()
    huxings,jiages,dizhis,hrefs,types = [],[],[],[],[]
    if web_type == 'Anjuke':
        infos = soup.find_all('p',attrs={"class": "details-item tag"})
        prices = soup.find_all(attrs={"class": "zu-side"})
        addresses = soup.find_all('address',attrs={"class": "details-item"})
        exd_infos = soup.find_all('p',attrs={"class": "details-item bot-tag clearfix"})
    
        for info,price,address,exd_info in zip(infos,prices,addresses,exd_infos):
            huxings.append(info.text)
            jiages.append(price.strong.text)
            dizhis.append(address.text)
            hrefs.append(address.a)
            types.append(exd_info.span)
        ftx_dic = {
                    '户型': huxings,
                    '价格': jiages,
                    '地址': dizhis,
                    '链接': hrefs,
                    '类型': types
                  }
        
        ftx_infos = pd.DataFrame(ftx_dic)
        ftx_infos['户型_type'] = ftx_infos['户型'].apply(lambda x: x.split('\n')[1].strip().split('|')[0])
        ftx_infos['户型_area'] = ftx_infos['户型'].apply(lambda x: x.split('\n')[1].strip().split('|')[1])
        ftx_infos['户型_floor'] = ftx_infos['户型'].apply(lambda x: x.split('\n')[1].strip().split('|')[2].split('层')[0])
        del ftx_infos['户型']
        ftx_infos['价格'] = ftx_infos['价格'].astype('int')
        ftx_infos['地址_小区'] = ftx_infos['地址'].apply(lambda x: x.split('\n')[1])
        del ftx_infos['地址']
    elif web_type == 'ziru':
        
        
    
    ftx_infos_new['户型_type'] = ftx_infos['户型_type']
    ftx_infos_new['户型_area'] = ftx_infos['户型_area']
    ftx_infos_new['户型_floor'] = ftx_infos['户型_floor']
    ftx_infos_new['价格'] = ftx_infos['价格']
    ftx_infos_new['地址_小区'] = ftx_infos['地址_小区']
    ftx_infos_new['web_type'] = web_type
    
    return ftx_infos_new

if __name__ == '__main__':

    #网站URL
    url1 = 'https://bj.zu.anjuke.com/fangyuan/majuqiao/p'
    url2 = 'http://www.ziroom.com/z/nl/z3-d23008625-b18335778.html?p='
    web_type = ['Anjuke','ziru']
    urls1,urls2 = [],[]
    info_sum = pd.DataFrame()

    for i in range(1,101,1):
        urls1.append(url1+str(i))
        urls2.append(url2+str(i))
        
    
    for url in urls:
        info_sum.append(getData(url,'Anjuke'))




    soup = 
    
#huxings,areas,districts,dizhis,dess = [],[],[],[],[]
#cls1s,cls2s,cls3s,jiges,links = [],[],[],[],[]

    
//*[@id="houseList"]/li[1]/div[2]/h4/a
#houseList > li:nth-child(1) > div.txt > h4 > a
    
ftx_infos = pd.DataFrame(ftx_dic)
ftx_infos['户型_type'] = ftx_infos['户型'].apply(lambda x: x.split('\n')[1].strip().split('|')[0])
ftx_infos['户型_area'] = ftx_infos['户型'].apply(lambda x: x.split('\n')[1].strip().split('|')[1])
ftx_infos['户型_floor'] = ftx_infos['户型'].apply(lambda x: x.split('\n')[1].strip().split('|')[2].split('层')[0])
del ftx_infos['户型']
ftx_infos['价格'] = ftx_infos['价格'].astype('int')
#ftx_infos['链接'] = ftx_infos['链接'].astype('str').apply(lambda x: x.split('"')[1])
ftx_infos['地址_小区'] = ftx_infos['地址'].apply(lambda x: x.split('\n')[1])
#ftx_infos['地址_详情'] = ftx_infos['地址'].apply(lambda x: x.split('\n')[2].strip())
del ftx_infos['地址']

ftx_infos_new = pd.DataFrame()
ftx_infos_new['户型_type'] = ftx_infos['户型_type']
ftx_infos_new['户型_area'] = ftx_infos['户型_area']
ftx_infos_new['户型_floor'] = ftx_infos['户型_floor']
ftx_infos_new['价格'] = ftx_infos['价格']
ftx_infos_new['地址_小区'] = ftx_infos['地址_小区']


    
    
    
    
    
    



//*[@id="list-content"]/div[3]/div[2]/p/strong
#soup.find(class='zu-info')

for div in soup.find_all('div', {'class' : 'content'}):
    print div.text.strip()
soup.findall('div', {'class' : 'content'})

