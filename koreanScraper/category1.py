import requests
import json
import errno
import os

ccid=50000000
ndict=dict()
headers={
    'Referer' : 'https://datalab.naver.com/shoppingInsight/sCategory.naver',
    'X-Requested-With' : 'XMLHttpRequest',
    'Sec-Fetch-Mode' : 'cors',
    'Content-Type' : 'application/x-www-form-urlencoded',
    'Accept' : '*/*',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

startDate=[2018,8,1]
endDate=[2019,8,15]

date=''

def formatDate():
    mnth=''
    if startDate[1]<10:
        mnth='0'+str(startDate[1])
    else:
        mnth=str(startDate[1])
    dy=''
    if startDate[2]<10:
        dy='0'+str(startDate[2])
    else:
        dy=str(startDate[2])
    date=str(startDate[0])+'-'+mnth+'-'+dy
    return date

def checkLeap():
    if (startDate[0] % 4) == 0:  
        if (startDate[0] % 100) == 0:
            if (startDate[0] % 400) == 0:
                return True  
            else:
                return False
        else:
            return True
    else:
        return False

def addYear():
    startDate[0]=startDate[0]+1

def addMonth():
    if startDate[1]<12:
        startDate[1]=startDate[1]+1
    else:
        startDate[1]=1
        addYear()

def addDay():
    if startDate[1]==2:
        if checkLeap()==False:
            if startDate[2]<28:
                startDate[2]=startDate[2]+1
            else :
                startDate[2]=1
                addMonth()
        else :
            if startDate[2]<29:
                startDate[2]=startDate[2]+1
            else :
                startDate[2]=1
                addMonth()
    elif startDate[1] in [1,3,5,7,8,10,12]:
        if startDate[2]<31:
            startDate[2]=startDate[2]+1
        else:
            startDate[2]=1
            addMonth()
    else:
        if startDate[2]<30:
            startDate[2]=startDate[2]+1
        else:
            startDate[2]=1
            addMonth()

data = {
    'cid' : None,
    'timeUnit' : 'date',
    'startDate' : '2018-01-01',
    'endDate' : '2019-08-15',
    'age' : '',
    'gender' : '',
    'device' : ''
}

def getCid(ccid,data,date):
    data.update({'cid':ccid})
    data.update({'startDate' : date})
    data.update({'endDate' : date})
    r=requests.post('https://datalab.naver.com/shoppingInsight/getCategoryKeywordRank.naver?count=500',headers=headers,data=data)
    #print(r.text)
    return json.loads(str(r.text))

def getChild(pid):
    url='https://datalab.naver.com/shoppingInsight/getCategory.naver?cid='+str(pid)
    print(pid)
    r=requests.get(url,headers=headers)
    #print(r.text)
    tdata=json.loads(r.text)
    data=tdata["childList"]
    cids=[tdata["name"]]
    for dat in data:
        cids.append([dat["cid"],dat["name"]])
    if len(cids)==1:
        return [None,cids[0]]
    else:
        return cids
    
def emptyChild(lst):
    if lst[0]==None:
        return True
    else:
        return False

def main(ccid,date):
    cid_list=[]
    adict=dict()
    while ccid<=50000010:
        print(ccid)
        bdict=dict()
        try :
            lst=getChild(ccid)
            name=lst[0]
            bdict.update({"name" : name})
            if emptyChild(lst)==False:
                for ls in lst:
                    if ls==name:
                        continue
                    lst0=getChild(ls[0])
                    cdict=dict()
                    cdict.update({"name" : ls[1]})
                    if emptyChild(lst0)==False:
                        for ls0 in lst0:
                            if ls0==ls[1]:
                                continue
                            lst1=getChild(ls0[0])
                            ddict=dict()
                            ddict.update({"name" : ls0[1]})
                            if emptyChild(lst1)==False:
                                for ls1 in lst1:
                                    if ls1==ls0[1]:
                                        continue
                                    data2=data
                                    data2.update({'gender' : 'm'})
                                    mdata=getCid(ls1[0],data2,date)
                                    print(ls1,' got male')
                                    data3=data
                                    data3.update({'gender' : 'f'})
                                    fdata=getCid(ls1[0],data3,date)
                                    print(ls1,' got female')
                                    ddict.update({ls1[0]:{"name":ls1[1],"male" : mdata,"female" : fdata}})
                            else:
                                data2=data
                                data2.update({'gender' : 'm'})
                                mdata=getCid(ls0[0],data2,date)
                                print(ls0,' got male')
                                data3=data
                                data3.update({'gender' : 'f'})
                                fdata=getCid(ls0[0],data3,date)
                                print(ls0,' got female')
                                ddict.update({"male" : mdata,"female" : fdata})
                            cdict.update({ls0[0] : ddict})
                    else:
                        data2=data
                        data2.update({'gender' : 'm'})
                        mdata=getCid(ls[0],data2,date)
                        print(ls,' got male')
                        data3=data
                        data3.update({'gender' : 'f'})
                        fdata=getCid(ls[0],data3,date)
                        print(ls,' got female')
                        cdict.update({"male" : mdata,"female" : fdata})
                    bdict.update({ls[0]:cdict})
            else:
                data2=data
                data2.update({'gender' : 'm'})
                mdata=getCid(ccid,data2,date)
                print(ccid,',',name,' got male')
                data3=data
                data3.update({'gender' : 'f'})
                fdata=getCid(ccid,data3,date)
                print(ccid,',',name,' got female')
                bdict.update({"male" : mdata,"female" : fdata})
            adict.update({bdict})
        except Exception as ex: 
            print(ex)
        finally : 
            print("finally")
            directory='./'+date+'/'
            if not os.path.exists(directory):
                os.makedirs(directory)
            filename = directory+str(ccid)+'.json'
            with open(filename,'w',encoding='utf-8') as f:
                f.write(json.dumps(bdict,ensure_ascii=False))
                print('Written ',str(ccid)+'.json')
        ccid+=1

def driver(ccid):
    while True:
        datee=formatDate()
        if startDate[0]==endDate[0] and startDate[1]==endDate[1] and startDate[2]==endDate[2]:
            main(ccid)
            print('Done for date ',startDate)
            break
        main(ccid,datee)
        print('Done for date ',startDate)
        addDay()

driver(ccid)