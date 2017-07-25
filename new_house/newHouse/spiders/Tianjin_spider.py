#!usr/bin/env python
# coding:utf-8

import sys
import scrapy
import datetime
from newHouse.items import TianjinItem
from newHouse.log_package.log_file import logs
reload(sys)
sys.setdefaultencoding('utf-8')


class TianjinNewHouse(scrapy.Spider):
    name = 'TianjinSpider'
    start_urls = (
        'http://www.tjfdc.com.cn/pages/fcdt/fcdtlist.aspx?SelMnu=FCSJ_XMXX',
    )

    def parse(self, response):
        all_xq = response.xpath('//ul[@class="piclist"]/li/div[2]')
        for xq in all_xq:
            xq_name = xq.xpath('./div[1]/h3/a/text()').extract_first()
            xq_url = response.urljoin(xq.xpath('./div[1]/h3/a/@href').extract_first())
            opening_time = xq.xpath('./div[1]/span/text()').re_first('\d+.*')

            house_avg_price = xq.xpath('./div[2]//tr[1]/td[2]/span[1]/text()').extract_first()
            nothouse_avg_price = xq.xpath('./div[2]//tr[1]/td[2]/span[2]/text()').extract_first()
            structure_all_area = xq.xpath('./div[2]//tr[1]/td[4]/text()').extract_first()
            develop_company = xq.xpath('./div[2]//tr[1]/td[6]/text()').extract_first()
            part_district = xq.xpath('./div[2]//tr[2]/td[2]/text()').extract_first()
            address = xq.xpath('./div[2]//tr[2]/td[6]/text()').extract_first()

            yield scrapy.Request(xq_url, callback=self.parse_detail, meta={
                'xq_name': xq_name, 'opening_time': opening_time, 'house_avg_price': house_avg_price,
                'nothouse_avg_price': nothouse_avg_price, 'part_district': part_district,
                'structure_all_area': structure_all_area, 'develop_company': develop_company, 'address': address
            })

        total_page = response.xpath('//span[@id="SplitPageModule1_lblPageCount"]/text()').re_first('\d+')
        current_page = response.xpath('//span[@id="SplitPageModule1_lblCurrentPage"]/text()').re_first('\d+')
        logs.debug('-----------current_page: %s-------total_page: %s------------' % (current_page, total_page))

        __VIEWSTATE = response.xpath('//input[@name="__VIEWSTATE"]/@value').extract_first()
        __EVENTVALIDATION = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first()
        __EVENTTARGET = response.xpath('//input[@id="__EVENTTARGET"]/@value').extract_first()
        __VIEWSTATEGENERATOR = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
        hidCountNow = response.xpath('//input[@id="hidCountNow"]/@value').extract_first()
        hidPage = response.xpath('//input[@id="hidPage"]/@value').extract_first()
        __EVENTARGUMENT = response.xpath('//input[@id="__EVENTARGUMENT"]/@value').extract_first()

        if int(current_page) < int(total_page):
            yield scrapy.FormRequest(response.url, formdata={
                '__EVENTTARGET': 'SplitPageModule1$lbnNextPage',
                '__EVENTARGUMENT': __EVENTARGUMENT,
                '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                'hidCountNow': hidCountNow,
                'hidPage': hidPage,
                '__VIEWSTATE': __VIEWSTATE,
                '__EVENTVALIDATION': __EVENTVALIDATION,
                'hidKpzt': '',
                'txtKpzt': '',
                'txtXmmc': '',
                'hidProjecttype': '',
                'txtProjecttype': '',
                'hidBk': '',
                'txtBk': '',
                'hidXzqh': '',
                'txtXzqh': '',
                'hidQy': '',
                'txtQy': '',
                'hidDoing': ''
            }, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        item = TianjinItem()

        item['house_type'] = response.xpath('//div[@class="main_table"]//tr[5]/td[2]/span/text()').extract_first()
        item['decorate_status'] = response.xpath('//div[@class="main_table"]//tr[6]/td[2]/span/text()').extract_first()
        item['volume_rate'] = response.xpath('//div[@class="main_table"]//tr[8]/td[2]/span/text()').extract_first()
        item['green_rate'] = response.xpath('//div[@class="main_table"]//tr[9]/td[2]/span/text()').extract_first()
        item['structure'] = response.xpath('//div[@class="main_table"]//tr[10]/td[4]/span/text()').extract_first()
        item['district'] = response.xpath('//div[@class="main_table"]//tr[11]/td[4]/span/text()').extract_first()
        item['property_fee'] = response.xpath('//div[@class="main_table"]//tr[12]/td[2]/span/text()').extract_first()
        item['property_company'] = response.xpath('//div[@class="main_table"]//tr[13]/td[2]/span/text()').extract_first()
        item['property_type'] = response.xpath('//div[@class="main_table"]//tr[13]/td[4]/span/text()').extract_first()

        item['project_name'] = response.meta['xq_name']
        item['opening_date'] = response.meta['opening_time']
        item['avg_price'] = response.meta['house_avg_price']
        item['nothouse_avg_price'] = response.meta['nothouse_avg_price']
        item['building_area'] = response.meta['structure_all_area']
        item['develop_company'] = response.meta['develop_company']
        item['part_district'] = response.meta['part_district']
        item['project_address'] = response.meta['address']

        item['province'] = '天津'
        item['city'] = '天津'
        item['url'] = response.url
        item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        yield item
