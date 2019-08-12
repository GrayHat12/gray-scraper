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
        if line=='Log in to like or comment.':
            break
        if end==True:
            comments.update({(author+comment).replace(' ','+').replace('\n','*'):{"author":author,"comment":comment}})
            author=None
            comment=None
            end=False
        if line.endswith('wReply') or line.endswith('dReply') or line.endswith('yReply') or line.endswith('eReply'):
            end=True
            continue
        if userStatus==None and user==None and author==None and comment==None and end==False and likes==None:
            likes = line
            continue
        elif likes != None and (user==None or userStatus==None):
            if user == None or userStatus==None:
                if user == None:
                    user=line
                    author=line
                    comment=''
                    continue
                else :
                    userStatus=line
                    continue
        else:
            if author==None:
                author=line
                comment=''
                continue
            else :
                comment+=line
                continue
    return comments

def analyze2(content,comments):
    print(content)
    author=None
    comment = ''
    end = False
    for line in content.split('\n'):
        if line=='Log in to like or comment.':
            break
        if end==True:
            comments.update({(author+comment).replace(' ','+').replace('\n','*'):{"author":author,"comment":comment}})
            author=None
            comment=None
            end=False
        if line.endswith('wReply') or line.endswith('dReply') or line.endswith('yReply') or line.endswith('eReply'):
            end=True
            continue
        if author==None:
            author=line
            comment=''
            continue
        else :
            comment+=line
            continue
    return comments

driver = webdriver.Chrome(executable_path=r"C:\Users\Rahul\PaidProjects\PythonInstagram\gray-scraper\chromedriver.exe")
driver.get('https://www.instagram.com/p/B0MIU9oFlOG/')
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
            elem3=driver.find_element_by_id('EizgU')
            f0=open('test.txt','w',encoding='utf-8')
            f0.write(str(elem3.text))
            f0.close
            fo=open('test.txt','r',encoding='utf-8')
            st=fo.read()
            fo.close()
            replies=analyze2(st,replies)
        except Exception as err:
            print('Checked Replies')
        f0=open('test.txt','w',encoding='utf-8')
        f0.write(str(elem2.text))
        f0.close
        fo=open('test.txt','r',encoding='utf-8')
        st=fo.read()
        fo.close()
        comments=analyze(st,comments)
        print('click ',i,' Analyzed')
        elem1.click()
        #src.append(driver.page_source)
except Exception as err:
    print(err)
finally :
    comments.update({"replies":replies})
    with open('data.json', 'w') as fp:
        json.dump(comments, fp)
    print('Got ',len(comments),' comments and ',len(replies),' Replies')