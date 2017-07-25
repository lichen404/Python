import zipfile
import argparse
from threading import Thread
def extractFile(zFile,password):
    try:
        zFile.extractall(pwd=password)
        print ('[+] Password = ' + password.decode('utf-8') + '\n')
        exit(0)
    except Exception as e:
        pass
        

def main(dictionary,Zip):
    zFile = zipfile.ZipFile(Zip)
    passFile = open(dictionary)
    for line in passFile.readlines():
        password = line.strip('\n').encode()
        t = Thread(target=extractFile, args=(zFile,password))
        t.start()
        
if __name__ == '__main__':
    parser=argparse.ArgumentParser(usage='python demo.py  -d 字典名 -z 文件名')
    parser.add_argument("-d",type=str)
    parser.add_argument("-z",type=str)
    args = parser.parse_args()
    dictionary=args.d
    Zip=args.z
    main(dictionary,Zip)
 
