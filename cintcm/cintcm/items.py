# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CintcmItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TermItem(Item):  
    term = Field()
    synonym = Field()  
    description = Field()  
    category = Field()  

class RecipeItem(Item):
    term = Field()
    
    bieming = Field()
    chufanglaiyuan = Field()
    yaowuzucheng = Field()
    jiajian = Field()
    gongxiao = Field()
    zhuzhi = Field()
    zhibeifangfa = Field()
    yongfayongliang = Field()
    yongyaojinji = Field()
    linchuangyingyong = Field()
    yaolizuoyong = Field()
    gejialunshu = Field()
    beizhu = Field()

class MedicineItem(Item):
    term = Field()
    
    bieming = Field()
    hanyupinyin = Field()
    yingwenming = Field()
    yaocaijiyuan = Field()
    dongzhiwuxingtai = Field()
    ziyuanfenbu = Field()
    shengtaihuanjing = Field()
    yaoyongzhiwuzaipei = Field()
    caishouhechucang = Field()
    yaoyongbuwei = Field()
    shengyaocaijianding = Field()
    zhongyaohuaxuechengfen = Field()
    lihuaxingzhi = Field()
    zhongyaohuaxuejianding = Field()
    zhongyaoyouxiaochengfenjiegoushideceding = Field()
    paozhifangfa = Field()
    jixing = Field()
    zhongyaozhiyaogongyi = Field()
    yaolizuoyong = Field()
    yaolixue = Field()
    yaodaidonglixue = Field()
    dulixue = Field()
    yaowupeiwu = Field()
    yaoxing = Field()
    guijing = Field()
    gongxiao = Field()
    gongxiaofenlei = Field()
    zhuzhi = Field()
    yongfayongliang = Field()
    yongyaojinji = Field()
    buliangfanyingjizhiliao = Field()
    xuanfang = Field()
    linchuangyunyong = Field()
    gejialunshu = Field()
    kaozheng = Field()
    yaowuyingyongjianbie = Field()
    yaodianshoulu = Field()
    yaocailadingming = Field()
    ladingzhiwudongwukuangwuming = Field()
    keshufenlei = Field()
    chuchu = Field()
    
class SymptomCategoryItem(Item):
    term = Field()
    
    daima = Field()
    zhenghoufenlei = Field()
    fenlei = Field()

class DiseaseCategoryItem(Item):
    term = Field()
    
    daima = Field()    
    zhongyizhuankeyijifenlei = Field()
    zhongyizhuankeerjifenlei = Field()
