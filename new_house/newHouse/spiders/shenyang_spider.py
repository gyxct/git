#!/usr/bin/env python
# coding=utf-8

import sys
import urllib
import scrapy
from ..items import SyNewhouseItem


class ShenyangSpider(scrapy.Spider):
    name = 'ShenyangSpider'
    start_urls = (
        'http://www.syfc.com.cn/work/xjlp/new_building.jsp?page=%s' % i for i in range(1, 109)
    )

    def __init__(self,):
        super(ShenyangSpider, self).__init__()
        self.item = SyNewhouseItem()

    def parse(self, response):
        info_all = response.xpath('/html/body/table[2]/tr/td[3]/table[3]/tr[2]/td/table/tr')
        for i in info_all:
            project_name = i.xpath('./td[1]/a/text()').extract_first()
            url_part = i.xpath('./td[1]/a/@href').extract_first()
            url_full = response.urljoin(url_part)
            district = i.xpath('./td[2]/text()').extract_first()
            develop_company = i.xpath('./td[4]/text()').extract_first()
            opening_time = i.xpath('./td[5]/text()').extract_first()
            # print district, develop_company, opening_time, url_full, '***********11111111111************'
            yield scrapy.Request(url_full, callback=lambda responses=response, district=district,project_name=project_name,
                                                           develop_company=develop_company, opening_time=opening_time:
            self.enter_houses_list(responses, district, develop_company, opening_time, project_name), dont_filter=True)

    def enter_houses_list(self, response, district, develop_company, opening_time, project_name):
        houses_list = response.xpath('/html/body/table[2]/tr/td[2]/table[2]/tr[3]/td/'
                                     'table/tr[1]/td/table/tr/td[1]/a')
        for h in houses_list:
            if h:
                url = response.urljoin(h.xpath('./@href').extract_first())
                # yield scrapy.Request(url, callback=self.enter_iframe)
                # print district, develop_company, opening_time, url, '************22222222222222***********'
                yield scrapy.Request(url, callback=lambda responses=response, district=district,
                                                               develop_company=develop_company, project_name=project_name,
                                                               opening_time=opening_time:
                self.enter_iframe(responses, district, develop_company, opening_time, project_name), dont_filter=True)

    def enter_iframe(self, response, district, develop_company, opening_time, project_name):
        url = response.xpath('//td[@align="center"]/iframe/@src').extract_first()
        # yield Request(url, callback=self.enter_every_house_list, )
        # print district, develop_company, opening_time, url, '************33333333333333***********'
        yield scrapy.Request(url, callback=lambda responses=response, district=district,
                                                  develop_company=develop_company,project_name=project_name,
                                                  opening_time=opening_time:
        self.enter_every_house_list(responses, district, develop_company, opening_time, project_name), dont_filter=True)

    def enter_every_house_list(self, response, district, develop_company, opening_time, project_name):
        all_house_list = response.xpath('/html/body/table/tr/td[2]/a')
        for a in all_house_list:
            if a:
                url = response.urljoin(a.xpath('./@href').extract_first())
                ch = a.xpath('./@href').re_first('&xszt=(\S+)')
                trans = urllib.quote(str(ch).decode(sys.stdin.encoding).encode('gbk'), safe='/')
                real_url = response.urljoin(a.xpath('./@href').re_first('(\S+&xszt=)\S+')) + trans
                # yield Request(real_url, callback=self.parse_detail, )
                # print district, develop_company, opening_time, real_url, '***********44444444444444***********'
                yield scrapy.Request(real_url, callback=lambda responses=response, district=district,
                                                               develop_company=develop_company, project_name=project_name,
                                                               opening_time=opening_time:
                self.parse_detail(responses, district, develop_company, opening_time, project_name), dont_filter=True)

    def parse_detail(self, response, district, develop_company, opening_time, project_name):
        self.item['houses_address'] = response.xpath('/html/body/table[2]/tr[2]/td/table/tr[1]/td/'
                                                     'table[2]/tr[2]/td[2]/text()').extract_first()
        self.item['house_marking'] = response.xpath('/html/body/table[2]/tr[2]/td/table/tr[1]/td/'
                                                'table[2]/tr[3]/td[2]/text()').extract_first()
        self.item['build_in_area'] = response.xpath('/html/body/table[2]/tr[2]/td/table/tr[1]/td/'
                                                   'table[2]/tr[4]/td[2]/text()').extract_first()
        self.item['AVG_area'] = response.xpath('/html/body/table[2]/tr[2]/td/table/tr[1]/td/'
                                                       'table[2]/tr[5]/td[2]/text()').extract_first()
        self.item['balcony_area'] = response.xpath('/html/body/table[2]/tr[2]/td/table/tr[1]/td/'
                                                   'table[2]/tr[6]/td[2]/text()').extract_first()
        self.item['saled_area'] = response.xpath('/html/body/table[2]/tr[2]/td/table/tr[1]/td/'
                                                'table[2]/tr[7]/td[2]/text()').extract_first()
        self.item['build_area'] = response.xpath('/html/body/table[2]/tr[2]/td/table/tr[1]/td/'
                                                     'table[2]/tr[8]/td[2]/text()').extract_first()
        self.item['build_type'] = response.xpath('/html/body/table[2]/tr[2]/td/table/tr[1]/td/'
                                                 'table[2]/tr[9]/td[2]/text()').extract_first()
        self.item['sale_status'] = response.xpath('/html/body/table[2]/tr[2]/td/table/tr[1]/td/'
                                             'table[2]/tr[10]/td[2]/text()').extract_first()
        self.item['district'] = district
        self.item['project_name'] = project_name
        self.item['develop_company'] = develop_company
        self.item['opening_time'] = opening_time
        self.item['url'] = response.url
        self.item['province'] = '辽宁'
        self.item['city'] = '沈阳'
        # print district, develop_company, opening_time, '************55555555555555***********'
        yield self.item
