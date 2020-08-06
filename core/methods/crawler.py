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
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from core.variables import viclist

global domain
print(viclist)
domain = viclist[0].split("://")[1]
if "@" in domain:
    domain = domain.split("@")[1]
domain = domain.split("/")[0].split(":")[0]

class TraversalSpider(scrapy.Spider):
    name = "traversal_spider"
    start_urls = viclist

    def parse(self, response):
        le = LinkExtractor(allow=".*{}.*".format(domain)) 
        for link in le.extract_links(response):
            viclist.append(link.url)
            yield Request(link.url, callback=self.parse)