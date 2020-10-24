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
import logging
import json
import os
import time
import subprocess

from scrapy import Request, signals
from scrapy.linkextractors import LinkExtractor
from multiprocessing.pool import ThreadPool as Pool
from pydispatch import dispatcher

from core.variables import viclist, processes, stable, cachedir, payloadlist
from core.colors import color
from core.methods.attack import phase1, resetCounter
from core.methods.cache import parseUrl
from core.methods.cookie import getCookie
from core.methods.list import listsplit


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class UrlSpider(scrapy.Spider):
    """
    URL crawler - enumerates all links related to the target for further analysis
    """
    name = "vailyn_url_spider"
    start_urls = []
    cookiedict = {}
    domain = ""
    subdir = ""

    def __init__(self, cookiedict=None, url=None, *args, **kwargs):
        super(UrlSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.closed, signals.spider_closed)
        if cookiedict:
            self.cookiedict = cookiedict
        assert url != None
        self.start_urls.append(url)
        dom = url.split("://")[1]
        if "@" in dom:
            dom = dom.split("@")[1]
        dom = dom.split("/")[0].split(":")[0]
        self.domain = dom
        assert self.domain != ""
        self.subdir = parseUrl(url)
        if not os.path.exists(cachedir+self.subdir):
            os.makedirs(cachedir+self.subdir)

    def start_requests(self):
        for target in self.start_urls:
            yield Request(target, callback=self.parse, cookies=self.cookiedict)

    def parse(self, response):
        le = LinkExtractor(allow=".*{}.*".format(self.domain))
        for link in le.extract_links(response):
            if link.url not in self.start_urls:
                self.start_urls.append(link.url)
                print("{0}[INFO]{1} found{4}|{2} {3}".format(color.RD, color.END + color.O,
                       color.END, link.url, color.END+color.RD))
            yield Request(link.url, callback=self.parse, cookies=self.cookiedict)

    def closed(self):
        with open(cachedir+self.subdir+"spider-phase0.txt", "w") as vicfile:
            for link in self.start_urls:
                vicfile.write(link + "\n")


def arjunEnum(post=False, cookiejar=None):
    """
    enumerate GET and POST parameters using Arjun by s0md3v to attack in respective phase
    """
    subdir = parseUrl(viclist[0])

    command = ["python3", "lib/Arjun/arjun.py", "--urls", cachedir + subdir + "spider-phase0.txt",
               "-f", "lib/Arjun/db/params.txt"]
    if post:
        command += ["-o", cachedir+subdir+"spider-phase5.json", "--post"]
    else:
        command += ["-o", cachedir+subdir+"spider-phase1.json", "--get"]

    if stable:
        command += ["--stable"]
    else:
        command += ["-t", str(processes)]

    if cookiejar:
        command += ["--cookies", cookiejar]

    subprocess.run(command)

    siteparams = None
    if post:
        with open(cachedir+subdir+"spider-phase5.json") as f:
            siteparams = json.load(f)
    else:
        with open(cachedir+subdir+"spider-phase1.json") as f:
            siteparams = json.load(f)
    assert siteparams is not None
    return siteparams


def analyzeParam(siteparams, victim2, verbose, depth, file, authcookie, gui=None):
    """
    attack each GET parameter found for each target URL
    """
    result = {}
    subdir = parseUrl(viclist[0])
    with Pool(processes=processes) as pool:
        for victim, paramlist in siteparams.items():
            sub = {}
            print("\n{0}[INFO]{1} param{4}|{2} Attacking {3}".format(color.RD, color.END + color.O,
                   color.END, victim, color.END+color.RD))
            if gui:
                gui.crawlerResultDisplay.append("\n[Info] param| Attacking {}".format(victim))
                gui.show()
            time.sleep(0.5)
            for param in paramlist:
                payloads = []
                nullbytes = []
                paysplit = listsplit(payloadlist, round(len(payloadlist)/processes))
                print("\n{0}[INFO]{1} param{4}|{2} Using {3}\n".format(color.RD, color.END + color.O,
                       color.END, param, color.END+color.RD))
                if gui:
                    gui.crawlerResultDisplay.append("[Info] param| Using {}".format(param))
                    gui.show()
                time.sleep(1.0)
                resetCounter()
                res = [pool.apply_async(phase1, args=(1, victim, victim2, param, None, "", verbose,
                       depth, l, file, authcookie, "", gui,)) for l in paysplit]
                for i in res:
                    # fetch results
                    tuples = i.get()
                    payloads += tuples[0]
                    nullbytes += tuples[1]
                payloads = list(set(payloads))
                nullbytes = list(set(nullbytes))
                sub[param] = (payloads, nullbytes)
                if payloads and gui:
                    gui.crawlerResultDisplay.append("[+] Vulnerable!")
                    gui.crawlerResultDisplay.append("Payloads: {}\nNullbytes: {}".format(payloads, nullbytes))
                    gui.show()
            result[victim] = sub
    if not os.path.exists(cachedir+subdir):
        os.makedirs(cachedir+subdir)
    with open(cachedir+subdir+"spider-phase2.json", "w+") as f:
        json.dump(result, f, sort_keys=True, indent=4)
    return result


def analyzePath(victim2, verbose, depth, file, authcookie, gui=None):
    """
    attack each URL using the path vector
    """
    result = {}
    subdir = parseUrl(viclist[0])
    with Pool(processes=processes) as pool:
        pathviclist = []
        for victim in viclist:
            # only root directory, else false positives
            splitted = victim.split("://")
            ulist = splitted[1].split("/")
            last = ulist[-1]
            # delete file, but not hidden directory
            if "." in last and not last.startswith("."):
                del ulist[-1]
            url = splitted[0] + "://" + "/".join(ulist)
            if url not in pathviclist:
                pathviclist.append(url)
        for victim in pathviclist:
            payloads = []
            nullbytes = []
            print("\n{0}[INFO]{1} path{4}|{2} Attacking {3}\n".format(color.RD, color.END + color.O,
                   color.END, victim, color.END+color.RD))
            if gui:
                gui.crawlerResultDisplay.append("\n[Info] path| Attacking {}".format(victim))
                gui.show()
            time.sleep(1.0)
            paysplit = listsplit(payloadlist, round(len(payloadlist)/processes))
            resetCounter()
            res = [pool.apply_async(phase1, args=(2, victim, victim2, "", None, "", verbose, depth,
                   l, file, authcookie, "", gui,)) for l in paysplit]
            for i in res:
                # fetch results
                tuples = i.get()
                payloads += tuples[0]
                nullbytes += tuples[1]
            payloads = list(set(payloads))
            nullbytes = list(set(nullbytes))
            result[victim] = (payloads, nullbytes)
            if payloads and gui:
                gui.crawlerResultDisplay.append("[+] Vulnerable!")
                gui.crawlerResultDisplay.append("Payloads: {}\nNullbytes: {}".format(payloads, nullbytes))
                gui.show()
    if not os.path.exists(cachedir + subdir):
        os.makedirs(cachedir + subdir)

    with open(cachedir + subdir + "spider-phase3.json", "w+") as f:
        json.dump(result, f, sort_keys=True, indent=4)
    return result


def analyzeCookie(victim2, verbose, depth, file, authcookie, gui=None):
    """
    attack each cookie delivered by the site
    """
    result = {}
    subdir = parseUrl(viclist[0])
    with Pool(processes=processes) as pool:
        for victim in viclist:
            sub = {}
            cookie = getCookie(victim)
            if len(cookie.keys()) < 1:
                print("\n{0}[INFO]{1} cookie{4}|{2} No cookies available for {3}.\n".format(color.RD,
                       color.END + color.O, color.END, victim, color.END+color.RD))
                if gui:
                    gui.crawlerResultDisplay.append("\n[Info] cookie| No cookies available for {}".format(victim))
                    gui.show()
                continue
            print("\n{0}[INFO]{1} cookie{4}|{2} Attacking {3}\n".format(color.RD, color.END + color.O,
                   color.END, victim, color.END+color.RD))
            if gui:
                gui.crawlerResultDisplay.append("\n[Info] cookie| Attacking {}".format(victim))
                gui.show()
            time.sleep(0.5)
            for key in cookie.keys():
                payloads = []
                nullbytes = []
                print("\n{0}[INFO]{1} cookie{4}|{2} Using {3}\n".format(color.RD, color.END + color.O,
                       color.END, key, color.END+color.RD))
                if gui:
                    gui.crawlerResultDisplay.append("[Info] cookie| Using {}".format(key))
                    gui.show()
                time.sleep(1.0)
                paysplit = listsplit(payloadlist, round(len(payloadlist)/processes))
                resetCounter()
                res = [pool.apply_async(phase1, args=(3, victim, victim2, "", cookie, key, verbose, depth,
                       l, file, authcookie, "", gui,)) for l in paysplit]
                for i in res:
                    # fetch results
                    tuples = i.get()
                    payloads += tuples[0]
                    nullbytes += tuples[1]
                payloads = list(set(payloads))
                nullbytes = list(set(nullbytes))
                sub[key] = (payloads, nullbytes)
                if payloads and gui:
                    gui.crawlerResultDisplay.append("[+] Vulnerable!")
                    gui.crawlerResultDisplay.append("Payloads: {}\nNullbytes: {}".format(payloads, nullbytes))
                    gui.show()
            result[victim] = sub
    if not os.path.exists(cachedir+subdir):
        os.makedirs(cachedir+subdir)
    with open(cachedir+subdir+"spider-phase4.json", "w+") as f:
        json.dump(result, f, sort_keys=True, indent=4)
    return result


def analyzePost(siteparams, victim2, verbose, depth, file, authcookie, gui=None):
    """
    attack each POST parameter found for each target URL
    """
    result = {}
    subdir = parseUrl(viclist[0])
    with Pool(processes=processes) as pool:
        for victim, paramlist in siteparams.items():
            sub = {}
            print("\n{0}[INFO]{1} post{4}|{2} Attacking {3}".format(color.RD, color.END + color.O,
                   color.END, victim, color.END+color.RD))
            if gui:
                gui.crawlerResultDisplay.append("\n[Info] post| Attacking {}".format(victim))
                gui.show()
            time.sleep(0.5)
            for param in paramlist:
                payloads = []
                nullbytes = []
                print("\n{0}[INFO]{1} post{4}|{2} Using {3}\n".format(color.RD, color.END + color.O,
                       color.END, param, color.END+color.RD))
                if gui:
                    gui.crawlerResultDisplay.append("\n[Info] post| Using {}".format(param))
                    gui.show()
                time.sleep(1.0)
                paysplit = listsplit(payloadlist, round(len(payloadlist)/processes))
                resetCounter()
                res = [pool.apply_async(phase1, args=(4, victim, victim2, "", None, "", verbose, depth,
                       l, file, authcookie, param + "=INJECT", gui,)) for l in paysplit]
                for i in res:
                    # fetch results
                    tuples = i.get()
                    payloads += tuples[0]
                    nullbytes += tuples[1]
                payloads = list(set(payloads))
                nullbytes = list(set(nullbytes))
                sub[param] = (payloads, nullbytes)
                if payloads and gui:
                    gui.crawlerResultDisplay.append("[+] Vulnerable!")
                    gui.crawlerResultDisplay.append("Payloads: {}\nNullbytes: {}".format(payloads, nullbytes))
                    gui.show()
            result[victim] = sub
    if not os.path.exists(cachedir + subdir):
        os.makedirs(cachedir + subdir)
    with open(cachedir + subdir + "spider-phase6.json", "w+") as f:
        json.dump(result, f, sort_keys=True, indent=4)
    return result
