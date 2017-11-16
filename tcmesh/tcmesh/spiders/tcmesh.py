import json
import logging
import os
import re
import time

from scrapy.conf import settings
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spider import Spider
  
class TcmeshSpider(Spider):  
    id_set = set()
    pEvent = 'FETCH_CONCEPT'
#     pEvent = 'FETCH_QUALIFIERLIST'
    
    cookie = settings['COOKIE']
    
    name = 'tcmesh'
    allowed_domains = ['tcmesh.org']  
#     start_urls = [
#         'http://tcmesh.org',
#         'http://tcmesh.org/mvccontroller?pEvent=USER_LOGIN'
#         'http://tcmesh.org/mvccontroller?pEvent=TREE_DATA'
#     ]
    if pEvent == 'FETCH_CONCEPT':
        start_urls = ['http://tcmesh.org/mvccontroller?pEvent=FETCH_CONCEPT&conceptId=26349']
    elif pEvent == 'FETCH_QUALIFIERLIST':
        start_urls = ['http://tcmesh.org/mvccontroller?pEvent=FETCH_QUALIFIERLIST&sortBy=1']
    
    def start_requests(self):
#         yield Request(self.start_urls[0], callback=self.parse_welcome, cookies=self.cookie)
        yield Request(self.start_urls[0], callback=self.parse, cookies=self.cookie)
                     
#     def parse_welcome(self, response):
#         return FormRequest.from_response(
#             response,
#                formdata={'pEvent': 'CLIENT_VALIDATE', 'loginName': 'huxiaoming', 'password': 'huxiaoming123'}
#         )
    
    def parse_item(self, response):
        qualifier = json.loads(response.body_as_unicode())

        return qualifier
    
    def parse(self, response):
#       print response.body
       
        if self.pEvent == 'FETCH_CONCEPT':
            selector = Selector(response)
            matches = selector.xpath('//html/body/table/tr/td/div/div/span').re(r'onclick\="linkClickHandler\(\d+\)"')
            for match in matches:
                id = re.search(r'\d+', match).group()
#                 logging.debug(id)
            
                if id in self.id_set:
#                     logging.debug('skip')
                    continue
            
                next_url = 'http://tcmesh.org/mvccontroller?pEvent=FETCH_CONCEPT&conceptId=' + id
                yield Request(next_url, callback=self.parse, cookies=self.cookie)            
            
            id = re.search(r'\d+', response.url).group()
            filename = 'download/concept/' + id + '.html'
            if os.path.exists(filename):
# 				logging.debug('exist')
                pass
            else:
                open(filename, 'w').write(response.body)    
            self.id_set.add(id)
            logging.debug(id + ' done')
            
        elif self.pEvent == 'FETCH_QUALIFIERLIST':
            qualifier_list = json.loads(response.body_as_unicode())['list']
            
            for qualifier in qualifier_list:
                id = str(qualifier['qualifierId'])
                next_url = 'http://tcmesh.org/mvccontroller?pEvent=FETCH_QUALIFIER&qualifierId=' + id
                yield Request(next_url, callback=self.parse_item, cookies=self.cookie)
        