from lxml import etree
from matplotlib import pyplot as plt 
from PIL import Image
import requests
import re

se = requests.session()
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
}
class Spider():
    def __init__(self):
        self.login_url = "http://www.heibanke.com/accounts/login"
        self.url = 'http://www.heibanke.com/lesson/crawler_ex04/'
        self.username = "lichen123"
        self.password = "123kingstone"
    def getCsrf(self):
        res = se.get(url=self.login_url,headers=headers,timeout=30).text
        self.csrf=se.cookies['csrftoken']  
    def login(self):
        self.getCsrf()
        data = {
        "csrfmiddlewaretoken": self.csrf,
        "username": self.username,
        "password": self.password
        }
        se.post(url=self.login_url,headers=headers, data=data,timeout=30)

    def get_captcha(self):
        img=Image.open('capt.png')
        
        plt.figure("验证码")
        plt.imshow(img)
        plt.ion()
        try:
            plt.pause(3)  #暂停3秒
            plt.close()
        except Exception as e:
        	pass
        code=input('请人工识别验证码并输入:')
        return str(code)
    def saveImg(self,url):
        res=se.get(url,headers=headers,timeout=30)
        if res.status_code==200:
            with open('capt.png','wb') as f:
                f.write(res.content)
    def getInfo(self):
        res = se.get(url=self.url,headers=headers,timeout=30).text
        tree = etree.HTML(res)
        self.f_csrf = tree.xpath('/html/body/div/div/div[2]/form/input[@name="csrfmiddlewaretoken"]/@value')[0]
        img_src = tree.xpath('/html/body/div/div/div[2]/form/div[3]/img/@src')[0]
        img_url = 'http://www.heibanke.com'+img_src
        self.saveImg(img_url)
        self.img_name = tree.xpath('//*[@id="id_captcha_0"]/@value')[0]
        self.code=self.get_captcha()
    def guessNum(self,num=0):
        self.getInfo()
        data={
            "csrfmiddlewaretoken":self.f_csrf,
            "username":self.username,
            "password":str(num),
            "captcha_0":self.img_name,
            "captcha_1":self.code
        }
        res = se.post(url=self.url,headers=headers,data=data,timeout=30)
        if res.status_code == 200:
            h3 = re.findall('<h3>(.*?)</h3>',res.text)
            h3 = h3[0]
            
            if '恭喜' in h3:
            	print("正确密码是"+str(num))
                print(h3)
            elif '验证码输入错误' in h3:
                print(h3)              
                self.guessNum(num)
            else:
            	print("密码{pwd}错误".format(pwd=num))
            	self.guessNum(num+1)
        else:
            print('请求失败')
            self.guessNum(num)
Spider=Spider()
Spider.login()
Spider.guessNum()




