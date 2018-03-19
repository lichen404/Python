import requests
from lxml import etree
from bs4 import BeautifulSoup
import threading
import re
import time

se = requests.session()
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
}
login_url = "http://www.heibanke.com/accounts/login"
url = 'http://www.heibanke.com/lesson/crawler_ex03/pw_list/'
username = "lichen123"
password = "123kingstone"

res = se.get(url=login_url,headers=headers,timeout=30).text
csrf=se.cookies['csrftoken']   
data = {
    "csrfmiddlewaretoken": csrf,
    "username": username,
    "password": password
    }
se.post(url=login_url,headers=headers, data=data,timeout=30)

class MyThread(threading.Thread):
    def __init__(self,pn,se):
        threading.Thread.__init__(self)
        self.se = se
        self.pn=pn
    def run(self):
        global count
        global pwdlist
        while count < 100:
            ruler = re.compile(r'.*>(\d*)<.*')
            payload={'page':self.pn}
            pwdpage = self.se.get(url,params=payload,timeout=30).text
            time.sleep(2)
            password_pos = BeautifulSoup(pwdpage, 'html.parser').findAll('td', {'title': 'password_pos'})
            password_val = BeautifulSoup(pwdpage, 'html.parser').findAll('td', {'title': 'password_val'})
            password_pos_list = []  # 密码位置list
            password_val_list = []  # 密码值list
            if password_pos:
                for i in password_pos:
                        password_pos_list.append(ruler.findall(str(i))[0])
                for j in password_val:
                        password_val_list.append(ruler.findall(str(j))[0])
                
                for index in range(0, len(password_pos_list)):
                        if pwdlist[int(password_pos_list[index]) - 1] == 'x':
                                count += 1
                                pwdlist[int(password_pos_list[index]) - 1] = password_val_list[index]
               
       

if __name__ == '__main__':
    
    start = time.time()
    count = 0
    threadList=[]
    pwdlist = ['x' for i in range(100)]
    for pn in range(1,14):  # 线程数,可自定义
        thread = MyThread(pn,se)
        thread.start()
        time.sleep(2)
        threadList.append(thread)
    for t in threadList:
        t.join()
    end = time.time()
    print('获取密码耗费时间',end-start)
    pwd= ''.join(pwdlist)

    print(pwd)
    se.get(url,headers=headers,timeout=30)
    csrf = se.cookies['csrftoken']


    
    data = {
        "csrfmiddlewaretoken":csrf,
        "username":"lichen",
        "password":pwd
    }
    res = se.post('http://www.heibanke.com/lesson/crawler_ex03/',headers=headers,data=data,timeout=30).text
    
    tree = etree.HTML(res)
    h3 = tree.xpath('/html/body/div/div/div[2]/h3/text()')[0]
    if not '错误' in h3:
        print(h3)
        

    else:
       print('密码{}错误'.format(pwd))
    
        

  

