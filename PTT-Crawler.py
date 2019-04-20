# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 20:52:10 2019

@author: user
"""
# -*- coding: UTF-8 -*-

import requests
import pandas as pd
import re
import glob
import os
import xlrd

from pandas import DataFrame, ExcelWriter

#from pandas import ExcelWriter
from bs4 import BeautifulSoup
from bs4.element import NavigableString

PTT_URL = 'https://www.ptt.cc'


#url_link = 'https://www.ptt.cc/bbs/Gossiping/M.1555350772.A.6BD.html'




##############################################################################

def save_csv_page():
    submit = pd.DataFrame(data = list_data)
    #submit['href'] = list_data['link'].values
    #submit['title'] = list_data['title.text'].values
    submit.to_csv('D:/Desktop/WNEC/crawler_data/0.csv', encoding='utf_8_sig',index=False)
    print("save index to disk")

def save_csv_content_page(inner_data,all_Id):
    submit = pd.DataFrame(data = inner_data)
    submit.to_csv('D:/Desktop/WNEC/crawler_data/'+str(all_Id)+'.csv', encoding='utf_8_sig',index=False,header=False)
    print("save page content to disk")

##############################################################################
    
    
def context_crawler(link,all_Id):
    list_data_inner_page = []
    up_push = 0
    down_push = 0
    no_push =0
    

    Inner_page = requests.get(link, cookies={'over18': '1'})
    soup_con = BeautifulSoup(Inner_page.text, 'html.parser') 
    
    main_content = soup_con.find(id="main-content")
    
    try:
        ip = main_content.find(text=re.compile(u'※ 發信站:'))
        ip = re.search('[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*', ip).group()
    except:
        ip = "None"
    
    
    content = ""
    
    for tag in main_content:
        if type(tag) is NavigableString and tag !='\n' and tag :
            content += tag
            break

        
    for response_push in soup_con.select(".push"):
        try:
             push_content = response_push.select(".push-content")[0].contents[0][1:]
             push_user = response_push.select(".push-userid")[0].contents[0][0:]
             push_vote = response_push.select(".push-tag")[0].contents[0][0]
             push_time = response_push.select(".push-ipdatetime")[0].contents[0][1:]
             
             if(push_vote == u'推'):
                 up_push +=1
             elif(push_vote == u'噓'):
                 down_push +=1
             else:
                 no_push +=1
             
             list_data_inner_page.append((push_vote,push_user,push_content,push_time))
        except:
            print("no push content")
            pass
    all_Id +=1

    save_csv_content_page(list_data_inner_page,all_Id)
    
    
    
    
    return all_Id,ip,content,up_push,down_push,no_push

        
    '''
    for div in divs_context:
        
        try:
        
        except:
            pass
    
    return 
    '''
    
 


def main(board,start,end,all_Id):

    while(start < end+1):
        url = 'https://www.ptt.cc/bbs/'+str(board)+'/index'+str(start)+'.html'
            
        res = requests.get(url, cookies={'over18': '1'})
                
        soup = BeautifulSoup(res.text, 'html.parser')
        divs = soup.find_all("div", "r-ent")
        
        for div in divs:
            
            try:
                href = div.find('a')['href']
                link = PTT_URL+href
                title = div.find(class_="title")
                author = div.find(class_="author")
                date = div.find(class_="date")
                
                
                all_Id,ip,content,up_push,down_push,no_push = context_crawler(link,all_Id)
                
                list_data.append((all_Id,title.text,date.text,author.text,link,content,up_push,down_push,no_push))
                        #list_title.append(title.text)
                        #list_author.append(author.text)
                        #print(title.text)
                
            except:
                pass
            
        start+=1
        
    print("crawl is ending")

#time.sleep(0.1)


'''
import csv

with open("D:/Desktop/test.csv","w",newline ='') as csvfile: 
    writer = csv.writer(csvfile)

    #先写入columns_name
    writer.writerow(["index","a_name","b_name"])
    #写入多行用writerows
    writer.writerows(list_data)

'''
def get_index(board,all_Id):
        
        url = 'https://www.ptt.cc/bbs/'+str(board)+'/index.html'
        res = requests.get(url, cookies={'over18': '1'})
                
        soup = BeautifulSoup(res.text, 'html.parser')
        divs = soup.find_all("div", "r-ent")
        
        for div in divs:
            
            try:
                href = div.find('a')['href']
                link = PTT_URL+href
                title = div.find(class_="title")
                author = div.find(class_="author")
                date = div.find(class_="date")
                
                
                all_Id,ip,content,up_push,down_push,no_push = context_crawler(link,all_Id)
                
                list_data.append((all_Id,title.text,date.text,author.text,link,content,up_push,down_push,no_push))
                        #list_title.append(title.text)
                        #list_author.append(author.text)
                        #print(title.text)
                
            except:
                pass

def combine_csv():
    '''
    os.chdir("D:/Desktop/WNEC/crawler_data")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    df_from_each_file = (pd.read_csv(f) for f in all_filenames)

    for idx, df in enumerate(df_from_each_file):
        df.to_excel(writer, sheet_name='data{0}.csv'.format(idx))
    
    combined_csv.to_csv("D:/Desktop/WNEC/combined_csv.csv", index=False, encoding='utf-8-sig')
    
    '''

    writer = ExcelWriter("D:/Desktop/WNEC/combined.xlsx")

    for filename in glob.glob("D:/Desktop/WNEC/crawler_data/*.csv"):
        
        df_csv = pd.read_csv(filename)   
        (_, f_name) = os.path.split(filename)
        (f_short_name, _) = os.path.splitext(f_name)

        df_csv.to_excel(writer, f_short_name, index=False,header=False)

    
    writer.save()
    
    data_xls = pd.read_excel('D:/Desktop/WNEC/combined.xlsx', index_col=None)
    data_xls.to_csv('D:/Desktop/WNEC/csvfile.csv', encoding='utf_8_sig', index=False)


if __name__=='__main__':
    list_data = []
    list_data.append(('id', 'title','date','author','url','content','推數','噓數','箭頭數'))
    all_Id = 0
    #get_index("Gossiping",all_Id)
    main("Gossiping",39046,39047,all_Id)
    save_csv_page()
    combine_csv()
