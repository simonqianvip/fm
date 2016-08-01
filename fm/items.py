# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class FmItem(scrapy.Item):
    '''
    单位名称：	山西盂县西小坪耐火材料有限公司
    公司类别：	制品企业
    省/市：	山西/阳泉
    详细地址：	山西省阳泉市盂县西小坪
    邮政编码：	045100
    公司邮箱：	xxp@xxpnc.com
    公司网址：	http://www.xxpnc.com
    经营模式：	生产加工
    公司成立时间：	1995年1月1日	注册资金：	6000万元 人民币
    法人代表/负责人：	郝良军	员工人数：	2000
    管理体系认证：	IS9001:2008质量管理体系认证；ISO14001:2004环境管理体系认证；GB/T28001_2001职业健康安全管理体系	经营品牌：	京武牌”焦炉硅砖
    主要市场：	国内国际	主要客户：	国内国际
    公司年产值：		年出口额：
    公司注册号：	140322200001216	经营范围：	不详
    '''
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_name = scrapy.Field() #公司名称
    cr = scrapy.Field() #法人
    mail = scrapy.Field() #邮箱
    url = scrapy.Field() #官网地址
    reg_no = scrapy.Field() #公司注册号
    money = scrapy.Field() #注册资金
    sale = scrapy.Field() #年产值
    # content = Field()
    pass
