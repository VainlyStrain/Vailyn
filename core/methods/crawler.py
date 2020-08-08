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
import json, os
import subprocess

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from multiprocessing.pool import ThreadPool as Pool

from core.variables import viclist, processes, stable, cachedir
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
            viclist.append(link.url)
            yield Request(link.url, callback=self.parse)

class FormSpider(scrapy.Spider):
    name = "vailyn_form_spider"
    start_urls = viclist

    def parse(self, response):
        return

def arjunEnum():
    with open("core/tmp/in.txt", "w") as vicfile:
        for target in viclist:
            vicfile.write(target + "\n")
    if stable:
        subprocess.run(["python3", "lib/Arjun/arjun.py", "-o", "core/tmp/out.json", "--urls", "core/tmp/in.txt", "--get"])
    else:
        subprocess.run(["python3", "lib/Arjun/arjun.py", "-t", str(processes), "-o", "core/tmp/out.json", "--urls", "core/tmp/in.txt", "--get"])
    
    siteparams = json.load("core/tmp/out.json")
    return siteparams

def analyzeParam(siteparams, paysplit, victim2, verbose, depth, file, authcookie):
    result = {}
    subdir = parseUrl(viclist[0])
    for victim, paramlist in siteparams.items():
        sub = {}
        for param in paramlist:
            payloads = []
            nullbytes = []
            with Pool(processes=processes) as pool:
                res = [pool.apply_async(phase1, args=(1,victim,victim2,param,None,"",verbose,depth,l,file,authcookie,"",)) for l in paysplit]
                for i in res:
                    #fetch results
                    tuples = i.get()
                    payloads += tuples[0]
                    nullbytes += tuples[1]
            sub[param] = (payloads, nullbytes)
        result[victim] = sub
    if not os.path.exists(cachedir+subdir):
        os.makedirs(cachedir+subdir)
    json.dump(result, cachedir+subdir+"spider-phase1.json", sort_keys=True, indent=4)
    return result

def analyzePath(paysplit, victim2, verbose, depth, file, authcookie):
    result = {}
    subdir = parseUrl(viclist[0])
    for victim in viclist:
        payloads = []
        nullbytes = []
        with Pool(processes=processes) as pool:
            res = [pool.apply_async(phase1, args=(2,victim,victim2,"",None,"",verbose,depth,l,file,authcookie,"",)) for l in paysplit]
            for i in res:
                #fetch results
                tuples = i.get()
                payloads += tuples[0]
                nullbytes += tuples[1]
        result[victim] = (payloads, nullbytes)
    if not os.path.exists(cachedir+subdir):
        os.makedirs(cachedir+subdir)
    json.dump(result, cachedir+subdir+"spider-phase2.json", sort_keys=True, indent=4)
    return result

def analyzeCookie(paysplit, victim2, verbose, depth, file, authcookie):
    result = {}
    subdir = parseUrl(viclist[0])
    for victim in viclist:
        sub = {}
        cookie = getCookie(victim)
        for key in cookie.keys():
            payloads = []
            nullbytes = []
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
    json.dump(result, cachedir+subdir+"spider-phase2.json", sort_keys=True, indent=4)
    return result