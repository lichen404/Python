from urllib import request
from bs4 import BeautifulSoup
import re
num=1
url='http://www.heibanke.com/lesson/crawler_ex00/'
while(num):
   
    f=request.Request(url)
    page=request.urlopen(f)
    soup=BeautifulSoup(page,'html.parser',from_encoding='utf-8')
    content=soup.find_all('h3')
    content=str(content)
    p=re.compile('<[^>]+>')
    content=p.sub("",content)
    print(content)
    num=re.findall(r"\d+\.?\d*",content)
    num=str(num)
    print(num)
    num=re.sub(r"\D","",num)
    url='http://www.heibanke.com/lesson/crawler_ex00/'
    url=url+num

