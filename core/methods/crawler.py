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


import scrapy
import json, os, time
import subprocess

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from multiprocessing.pool import ThreadPool as Pool

from core.variables import viclist, processes, stable, cachedir
from core.colors import color
from core.methods.attack import phase1
from core.methods.cache import parseUrl
from core.methods.cookie import getCookie

global domain

domain = viclist[0].split("://")[1]
if "@" in domain:
    domain = domain.split("@")[1]
domain = domain.split("/")[0].split(":")[0]

class UrlSpider(scrapy.Spider):
    name = "vailyn_url_spider"
    start_urls = viclist

    def parse(self, response):
        le = LinkExtractor(allow=".*{}.*".format(domain)) 
        for link in le.extract_links(response):
            if link.url not in viclist:
                viclist.append(link.url)
            yield Request(link.url, callback=self.parse)

class FormSpider(scrapy.Spider):
    name = "vailyn_form_spider"
    start_urls = viclist

    def parse(self, response):
        return

def arjunEnum(post=False):
    subdir = parseUrl(viclist[0])
    if not os.path.exists(cachedir+subdir):
        os.makedirs(cachedir+subdir)
    with open(cachedir+subdir+"spider-phase0.txt", "w") as vicfile:
        for target in viclist:
            vicfile.write(target + "\n")
    if post:
        if stable:
            subprocess.run(["python3", "lib/Arjun/arjun.py", "-o", cachedir+subdir+"spider-phase5.json", "--urls", cachedir+subdir+"spider-phase0.txt", "--post", "-f", "lib/Arjun/db/params.txt"])
        else:
            subprocess.run(["python3", "lib/Arjun/arjun.py", "-t", str(processes), "-o", cachedir+subdir+"spider-phase5.json", "--urls", cachedir+subdir+"spider-phase0.txt", "--post", "-f", "lib/Arjun/db/params.txt"])
    else:
        if stable:
            subprocess.run(["python3", "lib/Arjun/arjun.py", "-o", cachedir+subdir+"spider-phase1.json", "--urls", cachedir+subdir+"spider-phase0.txt", "--get", "-f", "lib/Arjun/db/params.txt"])
        else:
            subprocess.run(["python3", "lib/Arjun/arjun.py", "-t", str(processes), "-o", cachedir+subdir+"spider-phase1.json", "--urls", cachedir+subdir+"spider-phase0.txt", "--get", "-f", "lib/Arjun/db/params.txt"])
    

    siteparams = None
    with open(cachedir+subdir+"spider-phase1.json") as f:
        siteparams = json.load(f)
    assert siteparams != None
    return siteparams

def analyzeParam(siteparams, paysplit, victim2, verbose, depth, file, authcookie):
    result = {}
    subdir = parseUrl(viclist[0])
    for victim, paramlist in siteparams.items():
        sub = {}
        print("\n{0}[INFO]{1} param{4}|{2} Attacking {3}".format(color.RD, color.END + color.O, color.END, victim, color.END+color.RD))
        time.sleep(1.5)
        for param in paramlist:
            payloads = []
            nullbytes = []
            print("\n{0}[INFO]{1} param{4}|{2} Using {3}\n".format(color.RD, color.END + color.O, color.END, param, color.END+color.RD))
            time.sleep(1.5)
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(phase1, args=(1,victim,victim2,param,None,"",verbose,depth,l,file,authcookie,"",)) for l in paysplit]
                for i in res:
                    #fetch results
                    tuples = i.get()
                    payloads += tuples[0]
                    nullbytes += tuples[1]
            sub[param] = (payloads, nullbytes)
            time.sleep(3)
        result[victim] = sub
    if not os.path.exists(cachedir+subdir):
        os.makedirs(cachedir+subdir)
    with open(cachedir+subdir+"spider-phase2.json", "w+") as f:
        json.dump(result, f, sort_keys=True, indent=4)
    return result

def analyzePath(paysplit, victim2, verbose, depth, file, authcookie):
    result = {}
    subdir = parseUrl(viclist[0])
    for victim in viclist:
        payloads = []
        nullbytes = []
        print("\n{0}[INFO]{1} path{4}|{2} Attacking {3}\n".format(color.RD, color.END + color.O, color.END, victim, color.END+color.RD))
        time.sleep(1.5)
        with Pool(processes=processes) as pool:
            res = [pool.apply_async(phase1, args=(2,victim,victim2,"",None,"",verbose,depth,l,file,authcookie,"",)) for l in paysplit]
            for i in res:
                #fetch results
                tuples = i.get()
                payloads += tuples[0]
                nullbytes += tuples[1]
        result[victim] = (payloads, nullbytes)
        time.sleep(3)
    if not os.path.exists(cachedir+subdir):
        os.makedirs(cachedir+subdir)

    with open(cachedir+subdir+"spider-phase3.json", "w+") as f:
        json.dump(result, f, sort_keys=True, indent=4)
    return result

def analyzeCookie(paysplit, victim2, verbose, depth, file, authcookie):
    result = {}
    subdir = parseUrl(viclist[0])
    for victim in viclist:
        sub = {}
        cookie = getCookie(victim)
        if len(cookie.keys()) < 1:
            print("\n{0}[INFO]{1} cookie{4}|{2} No cookies available for {3}.\n".format(color.RD, color.END + color.O, color.END, victim, color.END+color.RD))
            continue
        print("\n{0}[INFO]{1} cookie{4}|{2} Attacking {3}\n".format(color.RD, color.END + color.O, color.END, victim, color.END+color.RD))
        time.sleep(1.5)
        for key in cookie.keys():
            payloads = []
            nullbytes = []
            print("\n{0}[INFO]{1} cookie{4}|{2} Using {3}\n".format(color.RD, color.END + color.O, color.END, key, color.END+color.RD))
            time.sleep(1.5)
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(phase1, args=(3,victim,victim2,"",cookie,key,verbose,depth,l,file,authcookie,"",)) for l in paysplit]
                for i in res:
                    #fetch results
                    tuples = i.get()
                    payloads += tuples[0]
                    nullbytes += tuples[1]
            sub[key] = (payloads, nullbytes)
        result[victim] = sub
    if not os.path.exists(cachedir+subdir):
        os.makedirs(cachedir+subdir)
    with open(cachedir+subdir+"spider-phase4.json", "w+") as f:
        json.dump(result, f, sort_keys=True, indent=4)
    return result

def analyzePost(siteparams, paysplit, victim2, verbose, depth, file, authcookie):
    result = {}
    subdir = parseUrl(viclist[0])
    for victim, paramlist in siteparams.items():
        sub = {}
        print("\n{0}[INFO]{1} post{4}|{2} Attacking {3}".format(color.RD, color.END + color.O, color.END, victim, color.END+color.RD))
        time.sleep(1.5)
        for param in paramlist:
            payloads = []
            nullbytes = []
            print("\n{0}[INFO]{1} post{4}|{2} Using {3}\n".format(color.RD, color.END + color.O, color.END, param, color.END+color.RD))
            time.sleep(1.5)
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(phase1, args=(4,victim,victim2,"",None,"",verbose,depth,l,file,authcookie,param+"=INJECT",)) for l in paysplit]
                for i in res:
                    #fetch results
                    tuples = i.get()
                    payloads += tuples[0]
                    nullbytes += tuples[1]
            sub[param] = (payloads, nullbytes)
            time.sleep(3)
        result[victim] = sub
    if not os.path.exists(cachedir+subdir):
        os.makedirs(cachedir+subdir)
    with open(cachedir+subdir+"spider-phase2.json", "w+") as f:
        json.dump(result, f, sort_keys=True, indent=4)
    return result