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


import scrapy, logging
import json, os, time
import subprocess

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from multiprocessing.pool import ThreadPool as Pool

from core.variables import viclist, processes, stable, cachedir, payloadlist
from core.colors import color
from core.methods.attack import phase1, resetCounter
from core.methods.cache import parseUrl
from core.methods.cookie import getCookie
from core.methods.list import listsplit

global domain

domain = viclist[0].split("://")[1]
if "@" in domain:
    domain = domain.split("@")[1]
domain = domain.split("/")[0].split(":")[0]


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class UrlSpider(scrapy.Spider):
    name = "vailyn_url_spider"
    start_urls = viclist

    def parse(self, response):
        le = LinkExtractor(allow=".*{}.*".format(domain)) 
        for link in le.extract_links(response):
            if link.url not in viclist:
                viclist.append(link.url)
                print("{0}[INFO]{1} found{4}|{2} {3}".format(color.RD, color.END + color.O, color.END, link.url, color.END+color.RD))
            yield Request(link.url, callback=self.parse)

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
    if post:
        with open(cachedir+subdir+"spider-phase5.json") as f:
            siteparams = json.load(f)
    else:
        with open(cachedir+subdir+"spider-phase1.json") as f:
            siteparams = json.load(f)
    assert siteparams != None
    return siteparams

def analyzeParam(siteparams, victim2, verbose, depth, file, authcookie, gui=None):
    result = {}
    subdir = parseUrl(viclist[0])
    with Pool(processes=processes) as pool:
        for victim, paramlist in siteparams.items():
            sub = {}
            print("\n{0}[INFO]{1} param{4}|{2} Attacking {3}".format(color.RD, color.END + color.O, color.END, victim, color.END+color.RD))
            time.sleep(0.5)
            for param in paramlist:
                payloads = []
                nullbytes = []
                paysplit = listsplit(payloadlist, round(len(payloadlist)/processes))
                print("\n{0}[INFO]{1} param{4}|{2} Using {3}\n".format(color.RD, color.END + color.O, color.END, param, color.END+color.RD))
                time.sleep(1.0)
                resetCounter()
                res = [pool.apply_async(phase1, args=(1,victim,victim2,param,None,"",verbose,depth,l,file,authcookie,"",gui,)) for l in paysplit]
                for i in res:
                    #fetch results
                    tuples = i.get()
                    payloads += tuples[0]
                    nullbytes += tuples[1]
                payloads = list(set(payloads))
                nullbytes = list(set(nullbytes))
                sub[param] = (payloads, nullbytes)
            result[victim] = sub
    if not os.path.exists(cachedir+subdir):
        os.makedirs(cachedir+subdir)
    with open(cachedir+subdir+"spider-phase2.json", "w+") as f:
        json.dump(result, f, sort_keys=True, indent=4)
    return result

def analyzePath(victim2, verbose, depth, file, authcookie, gui=None):
    result = {}
    subdir = parseUrl(viclist[0])
    with Pool(processes=processes) as pool:
        for victim in viclist:
            payloads = []
            nullbytes = []
            print("\n{0}[INFO]{1} path{4}|{2} Attacking {3}\n".format(color.RD, color.END + color.O, color.END, victim, color.END+color.RD))
            time.sleep(1.0)
            paysplit = listsplit(payloadlist, round(len(payloadlist)/processes))
            resetCounter()
            res = [pool.apply_async(phase1, args=(2,victim,victim2,"",None,"",verbose,depth,l,file,authcookie,"",gui,)) for l in paysplit]
            for i in res:
                #fetch results
                tuples = i.get()
                payloads += tuples[0]
                nullbytes += tuples[1]
            payloads = list(set(payloads))
            nullbytes = list(set(nullbytes))
            result[victim] = (payloads, nullbytes)
    if not os.path.exists(cachedir+subdir):
        os.makedirs(cachedir+subdir)

    with open(cachedir+subdir+"spider-phase3.json", "w+") as f:
        json.dump(result, f, sort_keys=True, indent=4)
    return result

def analyzeCookie(victim2, verbose, depth, file, authcookie, gui=None):
    result = {}
    subdir = parseUrl(viclist[0])
    with Pool(processes=processes) as pool:
        for victim in viclist:
            sub = {}
            cookie = getCookie(victim)
            if len(cookie.keys()) < 1:
                print("\n{0}[INFO]{1} cookie{4}|{2} No cookies available for {3}.\n".format(color.RD, color.END + color.O, color.END, victim, color.END+color.RD))
                continue
            print("\n{0}[INFO]{1} cookie{4}|{2} Attacking {3}\n".format(color.RD, color.END + color.O, color.END, victim, color.END+color.RD))
            time.sleep(0.5)
            for key in cookie.keys():
                payloads = []
                nullbytes = []
                print("\n{0}[INFO]{1} cookie{4}|{2} Using {3}\n".format(color.RD, color.END + color.O, color.END, key, color.END+color.RD))
                time.sleep(1.0)
                paysplit = listsplit(payloadlist, round(len(payloadlist)/processes))
                resetCounter()
                res = [pool.apply_async(phase1, args=(3,victim,victim2,"",cookie,key,verbose,depth,l,file,authcookie,"",gui,)) for l in paysplit]
                for i in res:
                    #fetch results
                    tuples = i.get()
                    payloads += tuples[0]
                    nullbytes += tuples[1]
                payloads = list(set(payloads))
                nullbytes = list(set(nullbytes))
                sub[key] = (payloads, nullbytes)
            result[victim] = sub
    if not os.path.exists(cachedir+subdir):
        os.makedirs(cachedir+subdir)
    with open(cachedir+subdir+"spider-phase4.json", "w+") as f:
        json.dump(result, f, sort_keys=True, indent=4)
    return result

def analyzePost(siteparams, victim2, verbose, depth, file, authcookie, gui=None):
    result = {}
    subdir = parseUrl(viclist[0])
    with Pool(processes=processes) as pool:
        for victim, paramlist in siteparams.items():
            sub = {}
            print("\n{0}[INFO]{1} post{4}|{2} Attacking {3}".format(color.RD, color.END + color.O, color.END, victim, color.END+color.RD))
            time.sleep(0.5)
            for param in paramlist:
                payloads = []
                nullbytes = []
                print("\n{0}[INFO]{1} post{4}|{2} Using {3}\n".format(color.RD, color.END + color.O, color.END, param, color.END+color.RD))
                time.sleep(1.0)
                paysplit = listsplit(payloadlist, round(len(payloadlist)/processes))
                resetCounter()
                res = [pool.apply_async(phase1, args=(4,victim,victim2,"",None,"",verbose,depth,l,file,authcookie,param+"=INJECT",gui,)) for l in paysplit]
                for i in res:
                    #fetch results
                    tuples = i.get()
                    payloads += tuples[0]
                    nullbytes += tuples[1]
                payloads = list(set(payloads))
                nullbytes = list(set(nullbytes))
                sub[param] = (payloads, nullbytes)
            result[victim] = sub
    if not os.path.exists(cachedir+subdir):
        os.makedirs(cachedir+subdir)
    with open(cachedir+subdir+"spider-phase2.json", "w+") as f:
        json.dump(result, f, sort_keys=True, indent=4)
    return result