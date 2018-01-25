#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 14:31:12 2017

@author: kmanhas
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 22:44:56 2017

@author: kmanhas
"""
from flask import Flask as fla,render_template,request
import urllib.request
import json
import matplotlib.pyplot as plt

'''
   by analayzing user profile
   find waekest area of user
'''

def process(z,area_s,area_w):
    link_to_profile='http://codeforces.com/api/user.status?handle='+z+'&from=1'
    urllib.request.urlretrieve(link_to_profile,'profile.json')
    jfile = open('profile.json')
    jstr = jfile.read()
    jdata = json.loads(jstr)
    profile=jdata['result']  
    '''
    plotting 1st graph after anayllazing user profile
    '''   
    frq = [0 for i in range(0, 5)]
    #print ('verdict of latest submission\n')
    for i in range (0,len(profile)):
        v = jdata["result"][i]["verdict"]
        if(v == 'OK'):
            frq[0] = frq[0] + 1
        elif(v == 'WRONG_ANSWER'):
            frq[1] = frq[1] + 1
        elif(v == 'RUNTIME_ERROR'):
            frq[2] = frq[2] + 1
        elif(v == 'TIME_LIMIT_EXCEEDED'):
            frq[4] = frq[4] + 1
        else:
            frq[3] = frq[3] + 1

    #print(frq)
    labels = 'AC', 'WA', 'RE', 'OTHERS', 'TLE'
    fig, ax1 = plt.subplots()
    explode = (0.1, 0, 0, 0, 0)
    ax1.pie(frq, explode, labels, autopct='%0.2f%%',
            shadow = True, startangle=90)
    ax1.axis('equal')
    fig.savefig('/home/kmanhas/sdl/static/image/graph11.jpg')
    #plt.show()
    plt.close(fig)
       
       
    '''
    plotting second graph
    
    '''   
    dict1 = {}
    
    for i in range (0,len(profile)):
       if(jdata["result"][i]["verdict"] == "OK"):
            v = jdata["result"][i]["problem"]["tags"]
            l = len(v)
            for j in range(0, l):
                if v[j] in dict1.keys():
                    dict1[v[j]] = dict1[v[j]] + 1
                else:
                    dict1[v[j]] = 1
                
            
    labels = []
    values = []
    x = len(dict1)
    for i in dict1.keys():
        values.append(dict1[i])
        labels.append(i)
        
    area_s.append(labels[0])
    area_s.append(labels[1])
    area_s.append(labels[2]) 
    
    length = len(labels)   
    
    area_w.append(labels[length-1])
    area_w.append(labels[length-2])
    area_w.append(labels[length-3])
       
    fig1, ax1 = plt.subplots()
    explode = [0 for i in range(0, x)]
    ax1.pie(values, explode, labels, autopct='%0.1f%%',
            shadow = True, startangle=90)
    ax1.axis('equal')
    fig1.savefig('/home/kmanhas/sdl/static/image/graph12.jpg')
    #plt.show()
    plt.close(fig)    
    
    '''
    reccomandation algorithm
    '''
    tagging ={}

    for i in profile:
        if i["verdict"]=="OK":
            l = len(i["problem"]["tags"])
            for w in range(0,l):
                x = i["problem"]["tags"][w]
                if x in tagging:
                    tagging[x]=tagging[x]+1
                else:
                    tagging[x]=1

    '''
      finding weakest area
    '''
    least_tag='implementation'

    for i in tagging.keys():
        if tagging[least_tag]>tagging[i]:
            least_tag=i

    p=""
    for i in least_tag:
        if(i==' '):
            p=p+'%20'
        else:
            p=p+i   
    '''        
      problem reccomanding
      
    '''  
    link_as_string ='http://codeforces.com/api/problemset.problems?tags='+p

    urllib.request.urlretrieve(link_as_string,'problems1.json');
    jfile = open('problems1.json')
    jstr = jfile.read()
    jdata = json.loads(jstr)
    problems1=jdata['result']  #list of objects

    problemDesc=[]
    l=len(problems1['problemStatistics'])

    for x in range(0,l):
        problemDesc.append((problems1['problemStatistics'][x]["solvedCount"],problems1['problemStatistics'][x]["contestId"],problems1['problemStatistics'][x]["index"]))
        
    problemDesc.sort()

    submission=[]

    for i in profile:
        if i["verdict"]=="OK":
            l=len(i["problem"]["tags"])
            for k in range(0,l):
                if i["problem"]["tags"][k]==least_tag:
                    submission.append((i["problem"]["contestId"],i["problem"]["index"]))
                    break

    (ind,i,minCnt)=(-1,0,10000000)
    for tup1 in submission:
        i=0
        for tup2 in problemDesc:
            if tup1[0]==tup2[1] and tup1[1]==tup2[2] and tup2[0]<minCnt:
                minCnt=tup2[0]
                ind=i
            i=i+1

    if ind==0:
        ind=1
    link="codeforces.com/problemset/problem/" + str(problemDesc[ind-1][1]) + "/" + str(problemDesc[ind-1][2])

    return link
    
    
def process2(p):

    z=""
    for i in p:
        if(i==' '):
            z=z+'%20'
        else:
            z=z+i  
            
    link_as_string ='http://codeforces.com/api/problemset.problems?tags='+z
    
    jfile = open('profile.json')
    jstr = jfile.read()
    jdata = json.loads(jstr)
    profile=jdata['result']
    
    urllib.request.urlretrieve(link_as_string,'problems2.json');
    jfile = open('problems2.json')
    jstr = jfile.read()
    jdata = json.loads(jstr)
    problems1=jdata['result']  #list of objects

    problemDesc=[]
    l=len(problems1['problemStatistics'])

    for x in range(0,l):
        problemDesc.append((problems1['problemStatistics'][x]["solvedCount"],problems1['problemStatistics'][x]["contestId"],problems1['problemStatistics'][x]["index"]))
        
    problemDesc.sort()

    submission=[]

    for i in profile:
        if i["verdict"]=="OK":
            l=len(i["problem"]["tags"])
            for k in range(0,l):
                if i["problem"]["tags"][k]==p:
                    submission.append((i["problem"]["contestId"],i["problem"]["index"]))
                    break

    (ind,i,minCnt)=(-1,0,10000000)
    for tup1 in submission:
        i=0
        for tup2 in problemDesc:
            if tup1[0]==tup2[1] and tup1[1]==tup2[2] and tup2[0]<minCnt:
                minCnt=tup2[0]
                ind=i
            i=i+1

    if ind==0:
        ind=1
    link="codeforces.com/problemset/problem/" + str(problemDesc[ind-1][1]) + "/" + str(problemDesc[ind-1][2])
    #print (link)
    return link
    
    
app = fla(__name__)
    
@app.route('/')
def start():
   return render_template("sdl.html")    
   
@app.route('/username', methods=['POST'])
def next():
    username1 = request.form['user']
    area_s = []
    area_w = []
    link1 =  process(username1,area_s,area_w)
    return render_template("sdl1.html", value=link1,username=username1,list_s=area_s,list_w=area_w)

@app.route('/Aboutus',methods=['POST'])
def aboutus():
    return render_template("sdl3.html")

@app.route('/tag',methods=['POST'])
def tag():
    tag_need_imp=request.form['tagg']    
    
    link2 = process2(tag_need_imp)
      
    return render_template("sdl2.html",value2=link2)
    
if __name__ == "__main__":                  #checking the which file to run 
    app.run(debug=False)                  
