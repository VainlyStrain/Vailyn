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


import sys
import requests
import subprocess
from urllib.request import urlopen
import core.variables as vars
from core.colors import color


"""Returns session for IP change verification"""
def presession():
    presess = requests.session()
    if vars.tor:
        presess.proxies['http'] = 'socks5h://localhost:9050'
        presess.proxies['https'] = 'socks5h://localhost:9050'
        presess.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
    return presess

"""Detect if the Tor service is active and running"""
def torpipe(controller):
    try:
        status = subprocess.check_output(['systemctl','status','tor'])
        #status = subprocess.check_output(['service','tor','status'])
        if "active (running)" in str(status):
            return True
        else:
            print(color.R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Tor service not running. Aborting..."+color.END)
            return False
    except subprocess.CalledProcessError:
        print(color.R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Tor service not installed or running. Aborting..."+color.END)
        return False

"""grab real attacker IP to verify if Tor works"""
def initcheck():
    ipaddr = urlopen('http://ip.42.pl/raw').read()
    vars.initip = str(ipaddr).split("'")[1]

"""verify if Tor works by comparing current IP with IP from initcheck()"""
def torcheck():
    #try:
    s = presession()
    ipaddr = s.get('http://ip.42.pl/raw').text
    #ip = str(ipaddr).split("'")[1].strip()
    if vars.initip.strip() != ipaddr:
        vars.torip = ipaddr
    else:
        print(color.R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "Not connected to Tor: Attacker IP used: {}. Aborting.{}".format(ipaddr, color.END))
        sys.exit()
    #except:
    #    print(R + " [-] " + "\033[0m" + color.UNDERLINE + "\033[1m" + "IPcheck socket failure.")
    #    torcheck() 
