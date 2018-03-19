import base64
import requests
import hashlib
from lxml import etree
from urllib import parse
def Getphoto(ID):
    headers={
        'User-Agent':'KSOAP/2.0',
         'SOAPAction':'http://service.jw.com/StudentPhotosSearch',
         'Content-Type':'text/xml',
         'HOST':'123.15.36.138:8008'
        }
    url='http://123.15.36.138:8008/zfmobile_port/webservice/jw/EducationalPortXMLService'
    stuID=str(ID)
    Rawkey=hashlib.md5((parse.quote(stuID+'DAFF8EA19E6BAC86E040007F01004EA')).encode('utf8'))
    key=(Rawkey.hexdigest()).upper()
    data='<v:Envelope xmlns:i="http://www.w3.org/2001/XMLSchema-instance" xmlns:d="http://www.w3.org/2001/XMLSchema" xmlns:c="http://schemas.xmlsoap.org/soap/encoding/" xmlns:v="http://schemas.xmlsoap.org/soap/envelope/"><v:Header /><v:Body><n0:StudentPhotosSearch id="o0" c:root="1" xmlns:n0="http://service.jw.com/"><sid i:type="d:string">{0}</sid><strKey i:type="d:string">{1}</strKey></n0:StudentPhotosSearch></v:Body></v:Envelope>'
    data=data.format(stuID,key)
    
    Rawcontent=requests.post(url,data=data.encode('utf8'),headers=headers)
    if Rawcontent.status_code==200:
        content=Rawcontent.text
        tree=etree.HTML(content)
        element=tree.xpath('//return')
        if(element):
            Base64photo=element[0].text
            photo=base64.b64decode(Base64photo)
            with open(stuID+'.jpg','wb') as f:
                f.write(photo)
                print('照片获取成功')
        else:
            print("照片获取失败！")
    else:
        print(Rawcontent.status_code)
if __name__ == '__main__':
	Getphoto('20151601****')  #此处输入要查询的学号



