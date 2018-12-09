import urllib.request
import argparse
import json
guess='https://www.kuaidi100.com/autonumber/autoComNum?text={0}'
query='https://www.kuaidi100.com/query?type={0}&postid={1}'
def kd100_query(code,company=None):
    company_possible=[ ]
    if company==None:
        f=urllib.request.urlopen(guess.format(code))
        content=json.loads(f.read().decode('utf-8'))
        try:
            for  x in content['auto']:
                company_possible.append(x['comCode'])
            print('possible company:'+str(company_possible))
        except:
            print('please check your  input')
        for p in company_possible:
            f=urllib.request.urlopen(query.format(p,code))
            content=json.loads(f.read().decode('utf-8'))
            if content['com'] != '':
                try:
                    print(content['com'])
                    print('-'*40)
                    for x in content['data']:
                        time=x['time']
                        context=x['context']
                        location=x['location']
                        print(time,context)
                    print('-'*40)
                except:
                    pass
        
    else:
        company=str(company)
        f=urllib.request.urlopen(query.format(company,code))
        content=json.loads(f.read().decode('utf-8'))
        try:
            print(content['com'])
            print('-'*40)
           
            for x in content['data']:
                time=x['time']
                context=x['context']
                location=x['location']
                print(time,context)
            print('-'*40)
            if int(content['status']) != 200:
                print('the company\'s name  may be wrong')
        except:
            print('please check your input')
if __name__=='__main__':
    parser=argparse .ArgumentParser(description='query express info use kuaidi100 api')
    parser.add_argument('-c','--code',type=str,help='express code')
    parser.add_argument('-p', '--company', type=str,
                        help='express company, will auto '
                             'guess company if not provided',
                        default=None)
   
    args = parser.parse_args()
    code=args.code
    company=args.company
 
    kd100_query(code,company=company)
            
         
        
        
        
        
            
              
       
    


        


        
            
              
       
    


        
