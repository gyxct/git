#!usr/bin/env python
# coding:utf-8


import scrapy
import datetime
from newHouse.items import DalianNewhouseItem
from newHouse.log_package.log_file import logs

class DalianNewHouse(scrapy.Spider):
    name = 'dalian_new_house'
    start_urls = (
        'http://www.dlfd.gov.cn/fdc/D01XmxxAction.do?Control=select&pageNo=1',
    )

    def parse(self, response):
        page_num = response.xpath('//font[@color="#0033FF"]/text()').re_first(u'共(\d+)页')
        for i in range(1, int(page_num)+1):
            next_page_url = 'http://www.dlfd.gov.cn/fdc/D01XmxxAction.do?Control=select&pageNo=%s' + str(i)
            logs.debug("---------first--------: %s" % next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse_xiaoqu_url)

    def parse_xiaoqu_url(self, response):
        xiaoqu_url = response.xpath('//a[@class="blue12"]/@href').re('\'(\S+)\',')
        for i in xiaoqu_url:
            url = 'http://www.dlfd.gov.cn' + i
            logs.debug("---------second--------: %s" % url)
            yield scrapy.Request(url, callback=self.parse_building_url)

    def parse_building_url(self, response):
        project_name = response.xpath('//table[@width="100%" and @border="0" and @cellspacing="0" and @cellpadding="0"]/tr[1]/td/table/tr[1]/td[2]/text()').re_first('\S+')
        develop_company = response.xpath('//table[@width="100%" and @border="0" and @cellspacing="0" and @cellpadding="0"]/tr[1]/td/table/tr[2]/td[2]/text()').re_first('\S+')
        address = response.xpath('//table[@width="100%" and @border="0" and @cellspacing="0" and @cellpadding="0"]/tr[1]/td/table/tr[3]/td[2]/text()').re_first('\S+')
        district = response.xpath('//table[@width="100%" and @border="0" and @cellspacing="0" and @cellpadding="0"]/tr[1]/td/table/tr[3]/td[2]/text()').re_first(u'\S+区')
        total_house_number = response.xpath('//td[@colspan="4" and @bgcolor="#a6d0e7"]/table/tr[1]/td[2]/span/text()').re_first('\d+\.?\d*')
        house_number = response.xpath('//td[@colspan="4" and @bgcolor="#a6d0e7"]/table/tr[2]/td[2]/span/text()').re_first('\d+\.?\d*')
        un_house_number = response.xpath('//td[@colspan="4" and @bgcolor="#a6d0e7"]/table/tr[3]/td[2]/span/text()').re_first('\d+\.?\d*')
        total_area = response.xpath('//td[@colspan="4" and @bgcolor="#a6d0e7"]/table/tr[1]/td[4]/span/text()').re_first('\d+\.?\d*')
        house_area = response.xpath('//td[@colspan="4" and @bgcolor="#a6d0e7"]/table/tr[2]/td[4]/span/text()').re_first('\d+\.?\d*')
        un_house_area = response.xpath('//td[@colspan="4" and @bgcolor="#a6d0e7"]/table/tr[3]/td[4]/span/text()').re_first('\d+\.?\d*')
        sale_number = response.xpath('//td[@colspan="4" and @bgcolor="#a6d0e7"]/table/tr[1]/td[6]/span/text()').re_first('\d+\.?\d*')
        sale_house_number = response.xpath('//td[@colspan="4" and @bgcolor="#a6d0e7"]/table/tr[2]/td[6]/span/text()').re_first('\d+\.?\d*')
        sale_unhouse_number = response.xpath('//td[@colspan="4" and @bgcolor="#a6d0e7"]/table/tr[3]/td[6]/span/text()').re_first('\d+\.?\d*')
        sale_area = response.xpath('//td[@colspan="4" and @bgcolor="#a6d0e7"]/table/tr[1]/td[8]/span/text()').re_first('\d+\.?\d*')
        sale_house_area = response.xpath('//td[@colspan="4" and @bgcolor="#a6d0e7"]/table/tr[2]/td[8]/span/text()').re_first('\d+\.?\d*')
        sale_unhouse_area = response.xpath('//td[@colspan="4" and @bgcolor="#a6d0e7"]/table/tr[3]/td[8]/span/text()').re_first('\d+\.?\d*')

        building_info = response.xpath('//td[@bgcolor="#a6d0e7"]')[2].xpath('table/tr')
        for i in building_info[1:-1]:
            permit_presale = i.xpath('td[2]/text()').re_first('\S+')
            url = 'http://www.dlfd.gov.cn' + i.xpath('td[1]/a/@href').extract_first()
            logs.debug("---------third--------: %s" % url)
            yield scrapy.Request(url, callback=self.parse_iframe_url, meta={'project_name':project_name,
                                'develop_company':develop_company, 'address':address, 'district':district,
                                'permit_presale':permit_presale, 'total_house_number':total_house_number,
                                'house_number':house_number, 'un_house_number':un_house_number,
                                'total_area':total_area, 'house_area':house_area, 'un_house_area':un_house_area,
                                'sale_number':sale_number, 'sale_house_number':sale_house_number,
                                'sale_unhouse_number':sale_unhouse_number, 'sale_area':sale_area,
                                'sale_house_area':sale_house_area, 'sale_unhouse_area':sale_unhouse_area})

    def parse_iframe_url(self, response):
        iframe_url = response.xpath('//iframe/@src').extract_first()
        url = 'http://www.dlfd.gov.cn' + iframe_url
        yield scrapy.Request(url, callback=self.parse_detail_url, meta={'project_name': response.meta['project_name'],
                            'develop_company': response.meta['develop_company'],'address': response.meta['address'], 'district':response.meta['district'],
                            'permit_presale':response.meta['permit_presale'], 'total_house_number':response.meta['total_house_number'],
                            'house_number':response.meta['house_number'], 'un_house_number':response.meta['un_house_number'],
                            'total_area':response.meta['total_area'], 'house_area':response.meta['house_area'], 'un_house_area':response.meta['un_house_area'],
                            'sale_number':response.meta['sale_number'], 'sale_house_number':response.meta['sale_house_number'],
                            'sale_unhouse_number':response.meta['sale_unhouse_number'], 'sale_area':response.meta['sale_area'],
                            'sale_house_area':response.meta['sale_house_area'], 'sale_unhouse_area':response.meta['sale_unhouse_area']})

    def parse_detail_url(self, response):
        item = DalianNewhouseItem()
        lou_number = response.xpath('//span[@class="STYLE2"]/strong/text()').extract_first()
        ceng_number = response.xpath('//font[@color="#00CC00"]/text()').extract()
        for i in ceng_number[:-1]:
            item['project_name'] = response.meta['project_name']
            item['develop_company'] = response.meta['develop_company']
            item['project_address'] = response.meta['address']
            item['district'] = response.meta['district']
            item['build_number'] = lou_number
            item['unit_number'] = i
            item['province'] = '辽宁'
            item['city'] = '大连'
            item['permit_presale'] = response.meta['permit_presale']
            item['total_house_number'] = response.meta['total_house_number']
            item['house_num'] = response.meta['house_number']
            item['un_house_number'] = response.meta['un_house_number']
            item['building_area'] = response.meta['total_area']
            item['can_sale_total_area'] = response.meta['house_area']
            item['un_house_area'] = response.meta['un_house_area']
            item['can_sale_house'] = response.meta['sale_number']
            item['unsaledHouse_num'] = response.meta['sale_house_number']
            item['sale_unhouse_number'] = response.meta['sale_unhouse_number']
            item['can_sale_total_area'] = response.meta['sale_area']
            item['unsaled_area'] = response.meta['sale_house_area']
            item['sale_unhouse_area'] = response.meta['sale_unhouse_area']
            item['url'] = response.url
            item['crawl_time'] = datetime.datetime.now().strftime('%Y%m%d')
            yield item






