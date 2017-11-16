# -*- coding: utf-8 -*-

import json
import logging
import os
import re
import sys
import time
import ConfigParser

from scrapy.conf import settings
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spider import Spider

sys.path.append('cintcm')
from items import *

# db = 'STD_DISEASE'
# db = 'STD_SYMPTOM'
# db = 'STD_TREATMENT'
# db = 'RECIPE'
# db = 'STD_SYMPTOM_CATEGORY'
# db = 'STD_DISEASE_CATEGORY'
# db = 'MEDICINE'
# db = 'MEDICINE_PAIR'
db = 'TREATMENT'

config_parser = ConfigParser.ConfigParser()
    
class CintcmSpider(Spider):
    config_parser.read('config.txt')
    
    name = 'cintcm'
    allowed_domains = ['cowork.cintcm.com']
    start_urls = list()
    
    for i in xrange(int(config_parser.get(db, 'first_id')), int(config_parser.get(db, 'last_id')) + 1):
        url = config_parser.get(db, 'url_prefix') + str(i) + config_parser.get(db, 'url_suffix')
        print url
        start_urls.append(url)
    
    def start_requests(self):
        for url in self.start_urls:
#             yield Request(url, callback=self.parse, headers=settings['DEFAULT_REQUEST_HEADERS'], cookies=settings['COOKIES'])
            if db == 'STD_DISEASE' or db == 'STD_SYMPTOM' or db == 'STD_TREATMENT':    
                yield Request(url, callback=self.parse_term_item, cookies=settings['COOKIES'])
            elif db == 'RECIPE':
                yield Request(url, callback=self.parse_index, cookies=settings['COOKIES'])
            elif db == 'MEDICINE':
                yield Request(url, callback=self.parse_index, cookies=settings['COOKIES'])
            elif db == 'TREATMENT':
                yield Request(url, callback=self.parse_index, cookies=settings['COOKIES'])
            elif db == 'STD_SYMPTOM_CATEGORY':
                yield Request(url, callback=self.parse_symptom_category_item, cookies=settings['COOKIES'])
            elif db == 'STD_DISEASE_CATEGORY':
                yield Request(url, callback=self.parse_disease_category_item, cookies=settings['COOKIES'])
        
    def parse_index(self, response):
#         print response
        
        selector = Selector(response)            
        matches = selector.xpath('//a[@class="b12b"]').re(r'href\="\S*"')
        for match in matches:
#             print match
            # href="detail?record=1&amp;primarykeyvalue=ID%3D069007&amp;channelid=41919"
            match = match.replace('amp;', '')
            next_url = 'http://cowork.cintcm.com/engine/' + re.search(r'href\="(\S*)"', match).group(1)
            print next_url
            if db == 'RECIPE':
                yield Request(next_url, callback=self.parse_recipe_item, cookies=settings['COOKIES'])
            elif db == 'MEDICINE':
                yield Request(next_url, callback=self.parse, cookies=settings['COOKIES'])
            elif db == 'TREATMENT':
                yield Request(next_url, callback=self.parse, cookies=settings['COOKIES'])
                
    def parse_term_item(self, response):
#         print response.body_as_unicode
        
        selector = Selector(response)
        items = list()
        
        item = TermItem()
        item['term'] = selector.xpath('//html/body/table/tr/td/span/text()').extract()[0].strip()
            
        item['synonym'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="TONGYCa"]/text()').extract()[0].strip()
        item['description'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="ZHUSa"]/text()').extract()[0].strip()
        item['category'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="FENLa"]/text()').extract()[0].strip()
                    
        items.append(item)  
    
        return items  
        
    def parse_recipe_item(self, response):
#         print response.body_as_unicode
        
        selector = Selector(response)
        items = list()
        
        item = RecipeItem()
        item['term'] = selector.xpath('//html/body/table/tr/td/span/text()').extract()[0].strip()
        
        item['bieming'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="BIEMa"]/text()').extract()[0].strip()
        item['chufanglaiyuan'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="CHUFLYa"]/text()').extract()[0].strip()
        item['yaowuzucheng'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YAOWZCa"]/text()').extract()[0].strip()
        item['jiajian'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="JIAJa"]/text()').extract()[0].strip()
        item['gongxiao'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="GONGXa"]/text()').extract()[0].strip()
        item['zhuzhi'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="ZUZa"]/text()').extract()[0].strip()
        item['zhibeifangfa'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="ZHIBFFa"]/text()').extract()[0].strip()
        item['yongfayongliang'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YONGFYLa"]/text()').extract()[0].strip()
        item['yongyaojinji'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YONGYJJa"]/text()').extract()[0].strip()
        item['linchuangyingyong'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="LINCYYa"]/text()').extract()[0].strip()
        item['yaolizuoyong'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YAOLZYa"]/text()').extract()[0].strip()
        item['gejialunshu'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="GEJLSa"]/text()').extract()[0].strip()
        item['beizhu'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="BEIZa"]/text()').extract()[0].strip()            
            
        items.append(item)  
    
        return items  

#     def parse_medicine_item(self, response):
# #         print response.body_as_unicode
#         
#         selector = Selector(response)
#         items = list()
#         
#         item = MedicineItem()
#         item['term'] = selector.xpath('//html/body/table/tr/td/span/text()').extract()[0].strip()
#         
#         item['bieming'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="BMa"]/text()').extract()[0].strip()
#         item['hanyupinyin'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="HYPYa"]/text()').extract()[0].strip()
#         item['yingwenming'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YWMa"]/text()').extract()[0].strip()
#         item['yaocaijiyuan'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YCJYa"]/text()').extract()[0].strip()
#         item['dongzhiwuxingtai'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="DZWXTa"]/text()').extract()[0].strip()
#         item['ziyuanfenbu'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="ZYFBa"]/text()').extract()[0].strip()
#         item['shengtaihuanjing'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="STHJa"]/text()').extract()[0].strip()
#         item['yaoyongzhiwuzaipei'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YYZWZPa"]/text()').extract()[0].strip()
#         item['caishouhechucang'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="CSYZCa"]/text()').extract()[0].strip()
#         item['yaoyongbuwei'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YYBWa"]/text()').extract()[0].strip()
#         item['shengyaocaijianding'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="SYCJDa"]/text()').extract()[0].strip()
#         item['zhongyaohuaxuechengfen'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="ZYHXCFa"]/text()').extract()[0].strip()
#         item['lihuaxingzhi'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="LHXZa"]/text()').extract()[0].strip()            
#         item['zhongyaohuaxuejianding'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="ZYHXJDa"]/text()').extract()[0].strip()
#         item['zhongyaoyouxiaochengfenjiegoushideceding'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="ZYYXCFJGSCDa"]/text()').extract()[0].strip()
#         item['paozhifangfa'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="PZFFa"]/text()').extract()[0].strip()
#         item['jixing'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="JXa"]/text()').extract()[0].strip()
#         item['zhongyaozhiyaogongyi'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="ZYZYGYa"]/text()').extract()[0].strip()
#         item['yaolizuoyong'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YWZYa"]/text()').extract()[0].strip()
#         item['yaolixue'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YLXa"]/text()').extract()[0].strip()
#         item['yaodaidonglixue'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YDDLXa"]/text()').extract()[0].strip()
#         item['dulixue'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="DLXa"]/text()').extract()[0].strip()
#         item['yaowupeiwu'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YWPWa"]/text()').extract()[0].strip()
#         item['yaoxing'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YXa"]/text()').extract()[0].strip()
#         item['guijing'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="GJa"]/text()').extract()[0].strip()
#         item['gongxiao'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="GXa"]/text()').extract()[0].strip()            
#         item['gongxiaofenlei'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="GXFLa"]/text()').extract()[0].strip()
#         item['zhuzhi'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="ZZa"]/text()').extract()[0].strip()
#         item['yongfayongliang'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YFYLa"]/text()').extract()[0].strip()
#         item['yongyaojinji'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YYJJa"]/text()').extract()[0].strip()
#         item['buliangfanyingjizhiliao'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="BLFYJZLa"]/text()').extract()[0].strip()
#         item['xuanfang'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="XFa"]/text()').extract()[0].strip()
#         item['linchuangyunyong'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="LCYYa"]/text()').extract()[0].strip()
#         item['gejialunshu'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="GJLSa"]/text()').extract()[0].strip()
#         item['kaozheng'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="KZa"]/text()').extract()[0].strip()
#         item['yaowuyingyongjianbie'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YWYYJBa"]/text()').extract()[0].strip()
#         item['yaodianshoulu'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YDSLa"]/text()').extract()[0].strip()
#         item['yaocailadingming'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="YCLDMa"]/text()').extract()[0].strip()
#         item['ladingzhiwudongwukuangwuming'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="LDZWDWKWMa"]/text()').extract()[0].strip()            
#         item['keshufenlei'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="KSFLa"]/text()').extract()[0].strip()
#         item['chuchu'] = selector.xpath('//html/body/table/tbody/tr/td/div[@id="CCa"]/text()').extract()[0].strip()
#             
#         items.append(item)  
#     
#         return items  

    def parse(self, response):
#         print response.body_as_unicode

        id = response.url[len('http://cowork.cintcm.com/engine/detail?record=1&primarykeyvalue=ID%3D'):response.url.find(config_parser.get(db, 'url_suffix'))]        
        filename = config_parser.get(db, 'path') + id + '.html'
        if os.path.exists(filename):
# 				logging.debug('exist')
            pass
        else:
            open(filename, 'w').write(response.body)    

    def parse_symptom_category_item(self, response):
#         print response.body_as_unicode
        
        selector = Selector(response)
        items = list()
        
        item = SymptomCategoryItem()
        item['term'] = selector.xpath('//html/body/table/tr/td/span/text()').extract()[0].strip()
        
        item['daima'] = selector.xpath('//div[@id="DAIMAa"]/text()').extract()[0].strip()
        item['zhenghoufenlei'] = selector.xpath('//div[@id="ZHENGHFLa"]/text()').extract()[0].strip()
        item['fenlei'] = selector.xpath('//div[@id="FENLa"]/text()').extract()[0].strip()
            
        items.append(item)
    
        return items  

    def parse_disease_category_item(self, response):
#         print response.body_as_unicode
        
        selector = Selector(response)
        items = list()
        
        item = DiseaseCategoryItem()
        item['term'] = selector.xpath('//html/body/table/tr/td/span/text()').extract()[0].strip()
        
        item['daima'] = selector.xpath('//div[@id="DAIMAa"]/text()').extract()[0].strip()
        item['zhongyizhuankeyijifenlei'] = selector.xpath('//div[@id="YIJFLa"]/text()').extract()[0].strip()
        item['zhongyizhuankeerjifenlei'] = selector.xpath('//div[@id="ERJFLa"]/text()').extract()[0].strip()
            
        items.append(item)
    
        return items  
