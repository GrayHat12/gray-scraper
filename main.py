from selenium import webdriver
import json

def analyze(content,comments):
    user=None
    userStatus=None
    author=None
    likes = None
    comment = ''
    end = False
    for line in content.split('\n'):
        if not line.strip():
            continue
        if line=='Log in to like or comment.':
            break
        if end==True:
            comments.update({(author+comment).replace(' ','+').replace('\n','*'):{"author":author,"comment":comment}})
            author=None
            comment=''
            end=False
        if line.endswith('wReply') or line.endswith('dReply') or line.endswith('yReply') or line.endswith('eReply') or line.endswith('mReply') or line.endswith('sReply') or line.endswith('hReply'):
            end=True
            continue
        if author==user and author!=None and user!=None and comment and userStatus!=None :
            end=True
            continue
        if author!=None and user!=None and comment and userStatus!=None and likes!=None:
            end=True
            continue
        if userStatus==None and user==None and author==None and not comments and end==False and likes==None:
            likes = line
            continue
        elif likes != None and (user==None or userStatus==None):
            if user == None or userStatus==None:
                if user == None:
                    user=line
                    author=line
                    continue
                else :
                    userStatus=line
                    continue
        else:
            if author==None:
                author=line
                continue
            else :
                comment+=line
                continue
    return comments

def analyze2(content,comments):
    user=None
    userStatus=None
    author=None
    likes = None
    comment = ''
    end = False

driver = webdriver.Chrome(executable_path=r"C:\Users\Rahul\PaidProjects\PythonInstagram\gray-scraper\chromedriver.exe")
driver.get('https://www.instagram.com/p/B0OsWFXlPqq/')
i=0
comments = dict()
replies=dict()
try:
    elem2 = driver.find_element_by_class_name('eo2As')
    f0=open('test.txt','w',encoding='utf-8')
    f0.write(str(elem2.text))
    f0.close
    fo=open('test.txt','r',encoding='utf-8')
    st=fo.read()
    fo.close()
    comments=analyze(st,comments)
    while driver.find_elements_by_class_name('Igw0E.IwRSH.YBx95._4EzTm.MGdpg.NUiEW')!=None:
        #print('HERE')
        i+=1
        elem1 = driver.find_element_by_class_name('Igw0E.IwRSH.YBx95._4EzTm.MGdpg.NUiEW')
        elem2 = driver.find_element_by_class_name('eo2As')
        try :
            elem3=driver.find_element_by_class_name('Igw0E.IwRSH.eGOV_.ybXk5._4EzTm')
            elem3.click()
            elem3=driver.find_element_by_class_name('TCSYW')
            f0=open('test.txt','w',encoding='utf-8')
            f0.write(str(elem3.text))
            f0.close
            fo=open('test.txt','r',encoding='utf-8')
            st=fo.read()
            fo.close()
            replies=analyze(st,replies)
            print('Analyzed Replies',end='\n')
        except Exception as err:
            print('No Replies',end='\n')
        f0=open('test.txt','w',encoding='utf-8')
        f0.write(str(elem2.text))
        f0.close
        fo=open('test.txt','r',encoding='utf-8')
        st=fo.read()
        fo.close()
        comments=analyze(st,comments)
        print('click ',i,' Analyzed ',len(comments),' Comments in total recieved',end='\n')
        elem1.click()
        #src.append(driver.page_source)
except Exception as err:
    print(err)
finally :
    comments.update({"replies":replies})
    with open('data.json', 'w',encoding='utf-8') as fp:
        json.dump(comments, fp)
    print('Got ',len(comments),' comments and ',len(replies),' Replies')
