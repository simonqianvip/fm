# -*- coding: utf-8 -*-
import scrapy
import scrapy.cmdline

import logging
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from fm.items import FmItem

logger = logging.getLogger(__name__)

page_pre = "http://www.fm086.com/Company/Index?pageindex="
page_end = "&stext=&province=&sortid="
count_page = 653


class FMSpider(scrapy.Spider):
    # def __init__(self):
    #     self.driver = webdriver.Chrome(executable_path='D:\program\chromedriver_win32\chromedriver.exe')
    #     self.driver.set_page_load_timeout(10)
    #     self.driver.get("http://www.fm086.com/Company/Index")

    # http://www.fm086.com/
    name = "fm"  # 设置爬虫名称
    allowed_domains = ["fm086.com"]  # 设置允许的域名
    start_urls = [
        "http://www.fm086.com/Company/Index?pageindex=1&stext=&province=&sortid="  # 设置开始爬行的页面
    ]

    def parse(self, response):
        """
        获取下一页的link
        """
        logger.info('-----------parse page url : %s ------------' % response.url)
        sel = Selector(response)

        # count_page+1
        for i in range(1, count_page+1):
            pageURL = page_pre + str(i) + page_end
            # print(pageURL)
            yield scrapy.Request(pageURL, callback=self.parse)

        # /html/body/div[3]/div/div[1]/div[2]/ul/li[15]/div[2]/div[1]/span[1]/a
        # 获取当前列表页的所有url

        sites = sel.xpath('//*[contains(@class,"j_simc")]/span[1]/a/@href').extract()
        # print(sites)

        for site in sites:
            # logger.info("company url:%s"%site)
            yield scrapy.Request(site, callback=self.parse_content)

        '''
        wait =WebDriverWait(self.driver, 5)
        wait.until(lambda driver:driver.find_element_by_id("introduceAD"))#VIP，内容加载完成后爬取
        time.sleep(5)
        next_page =self.driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div[2]/div/div/ul/li/a[contains(@onclick,"zjr_nextPager")]').click()
        next_page.click() #模拟点击下一页
        self.driver.quit()
        '''

    def parse_content(self, response):
        """
        解析每个文章的内容
        :param response:
        :return:
        """

        company_url = response.url
        logger.info('-----------parse content url:%s ------------' % company_url)
        # time.sleep(2)
        sel = Selector(response)

        second_url = sel.xpath('//*[@id="menu"]/div/ul/li[2]/a/@href').extract()
        for u in second_url:
            all_url = company_url + str('/') + u
            # print(all_url)
            yield scrapy.Request(all_url, callback=self.parse_second_page)

    def parse_second_page(self, response):
        """
        解析二级页面
        :param response:
        :return:
        """
        logger.info('-----------parse company info url:%s ------------' % response.url)

        time.sleep(2)
        sel = Selector(response)

        company_name = sel.xpath('//table[@border="1"]/tr[1]/td[2]/text()').extract()
        # 法人 /html/body/div[6]/div[2]/div[2]/table/tbody/tr[10]/td[2]
        cr = sel.xpath('//table[@border="1"]/tr[10]/td[2]/text()').extract()
        # 注册资金 /html/body/div[6]/div[2]/div[2]/table/tbody/tr[9]/td[4]
        money = sel.xpath('//table[@border="1"]/tr[9]/td[4]/text()').extract()
        # 公司注册号 /html/body/div[6]/div[2]/div[2]/table/tbody/tr[14]/td[2]
        reg_no = sel.xpath('//table[@border="1"]/tr[14]/td[2]/text()').extract()
        # 公司网址 /html/body/div[6]/div[2]/div[2]/table/tbody/tr[7]/td[2]
        url = sel.xpath('//table[@border="1"]/tr[7]/td[2]/text()').extract()
        # 年产值 /html/body/div[6]/div[2]/div[2]/table/tbody/tr[13]/td[2]
        sale = sel.xpath('//table[@border="1"]/tr[13]/td[2]/text()').extract()

        items = []
        item = FmItem()
        item['company_name'] = [c.encode('utf-8') for c in company_name]
        item['cr'] = [c.encode('utf-8') for c in cr]
        item['money'] = [c.encode('utf-8') for c in money]
        item['reg_no'] = [c.encode('utf-8') for c in reg_no]
        item['url'] = [c.encode('utf-8') for c in url]
        item['sale'] = [c.encode('utf-8') for c in sale]

        # print(item['company_name'])
        items.append(item)
        return items


if __name__ == '__main__':
    scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'fm'])
