from urllib import request,parse
from bs4 import BeautifulSoup
url='http://www.heibanke.com/lesson/crawler_ex01/'
num=1
while num<=30:
    data=parse.urlencode([('username','lichen'),('password',num)])
    urlhd=request.Request(url)
    with request.urlopen(urlhd,data=data.encode('utf-8')) as f:
                         soup=BeautifulSoup(f,'html.parser',from_encoding='utf-8')
                         print(soup.h3.string)
    num+=1
    
        
