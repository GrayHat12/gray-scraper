"""fashion clothing>>>womens>>tshirt>"""
import requests
import json

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

data = {
    'cid' : None,
    'timeUnit' : 'date',
    'startDate' : '2019-07-14',
    'endDate' : '2019-08-14',
    'age' : '',
    'gender' : '',
    'device' : ''
}

def getCid(ccid,data):
    data.update({'cid':ccid})
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
    cids=[]
    for dat in data:
        cids.append(dat["cid"])
    if len(cids)==0:
        return None
    else:
        return cids

def main(ccid):
    cid_list=[]
    adict=dict()
    while ccid<=50000000:
        print(ccid)
        bdict=dict()
        ncid=getChild(ccid)
        print()
        if ncid!=None:
            cdict=dict()
            for n_ncid in ncid:
                try:
                    nncid=getChild(n_ncid)
                    if nncid!=None:
                        #cid_list.extend(nncid)
                        ddict=dict()
                        for cid in nncid:
                            data2=data
                            data2.update({'gender' : 'm'})
                            mdata=getCid(cid,data2)
                            print(cid,' got male')
                            data3=data
                            data3.update({'gender' : 'f'})
                            fdata=getCid(cid,data3)
                            print(cid,' got female')
                            ddict.update({cid : {'male' : mdata, 'female' : fdata}})
                            cdict.update({n_ncid:ddict})
                            bdict.update(cdict)
                except Exception as err:
                    print(err)
                finally :
                    adict.update({ccid : bdict})
        with open(str(ccid)+'.json','w',encoding='utf-8') as f:
            #json.dump(bdict,f)
            f.write(json.dumps(bdict,ensure_ascii=False))
            print('Written ',str(ccid)+'.json')
        ccid+=1
        cid_list=[]

main(ccid)