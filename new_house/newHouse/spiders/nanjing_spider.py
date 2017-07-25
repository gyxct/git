# -*- coding: utf-8 -*-
import scrapy
import logging

from newHouse.items import NJNewHouseItem


class NJNewHouse(scrapy.Spider):
    name = 'nanjing_data'
    start_urls = (
        'http://newhouse.njhouse.com.cn/kpgg/?id=xw',
    )

    def parse(self, response):
        all_district = response.xpath('//body/table[2]/tr[1]/td/table/tr/td/font/a/@href').extract()
        for part_url in all_district:
            # print part_url
            next_url = response.urljoin(part_url)
            yield scrapy.Request(next_url, callback=self.get_xiaoqu_url)

    def get_xiaoqu_url(self, response):
        each_xiaoqu = response.xpath('/html/body/table[3]/tr[2]/td/table/tr/td[2]/a/@href').extract()
        for part_url in each_xiaoqu:
            next_url = response.urljoin(part_url)
            yield scrapy.Request(next_url, callback=self.full_items)

    def full_items(self, response):
        url = response.url
        project_addr = response.xpath(
            '//table[3]/tr[1]/td[2]/table/tr[4]/td[2]/table/tr[3]/td[1]/table/tr[1]/td[2]/text()').extract_first()
        use_condition = response.xpath(
            '//table[3]/tr[1]/td[2]/table/tr[4]/td[2]/table/tr[3]/td[1]/table/tr[2]/td[2]/text()').extract_first()
        district = response.xpath(
            '//table[3]/tr[1]/td[2]/table/tr[4]/td[2]/table/tr[3]/td[1]/table/tr[3]/td[2]/text()').extract_first()

        iframe_list = response.xpath('//iframe[@align="left"]/@src')
        project_name = response.xpath('//title/text()').extract_first()
        meta = {'project_addr': project_addr, 'use_condition': use_condition, 'district': district,
                'project_name': project_name, 'key_url': iframe_list[1].extract(), 'url': url}
        if len(iframe_list) == 2:
            start_sale_time_url = iframe_list[0].extract()
            response.meta['key_url'] = iframe_list[1].extract()
            yield scrapy.Request(start_sale_time_url, meta=meta, callback=self.get_start_sale_time)

    def get_start_sale_time(self, response):
        start_sale_time = response.xpath('/html/body/table/tr[3]/td[4]/text()').re_first('\S+')
        develop_company = response.xpath('/html/body/table/tr[1]/td[2]/a/text()').extract_first()

        # 开售时间
        response.meta['start_sale_time'] = start_sale_time
        response.meta['develop_company'] = develop_company

        next_url = response.meta['key_url']
        yield scrapy.Request(next_url, meta=response.meta, callback=self.get_price_true_url)

    def get_price_true_url(self, response):
        part_url = response.xpath('//iframe/@src').extract_first()
        next_url = response.urljoin(part_url)
        yield scrapy.Request(next_url, meta=response.meta, callback=self.get_some_price)

    def get_some_price(self, response):
        meta = response.meta
        items = NJNewHouseItem()
        items['opening_date'] = meta.get('start_sale_time')
        items['province'] = '江苏省'
        items['url'] = meta.get('url')
        items['city'] = '南京市'
        items['project_name'] = meta.get('project_name')
        items['project_address'] = meta.get('project_addr')
        items['use_for'] = meta.get('use_condition')
        items['develop_company'] = meta.get('develop_company')
        items['district'] = meta.get('district')
        items['all_avg_price'] = response.xpath('//table[2]/tr[4]/td[2]/text()').extract_first()
        items['deal_num'] = response.xpath('//table[2]/tr[3]/td[2]/text()').extract_first()
        items['deal_area'] = response.xpath('//table[2]/tr[3]/td[4]/text()').re_first('\d+')
        items['can_sale_total_area'] = response.xpath('//table[2]/tr[2]/td[2]/text()').extract_first()
        items['avg_price'] = response.xpath('//table[2]/tr[4]/td[4]/text()').extract_first()
        items['office_avg_price'] = response.xpath('//table[2]/tr[5]/td[2]/text()').extract_first()
        items['shop_avg_price'] = response.xpath('//table[2]/tr[5]/td[4]/text()').extract_first()
        items['house_num'] = response.xpath('//table[2]/tr[1]/td[2]/text()').extract_first()
        print items
        yield items
