#!/usr/bin/env python
# coding=utf-8

import json
import random
import scrapy
from ..items import HfNewhouseItem


def nscaler(n):
    d = {'0': '0', '1': '2', '2': '5', '3': '8', '4': '6', '5': '1', '6': '3', '7': '4', '8': '9', '9': '7'}
    num = ''
    for i in str(n):
        num += d[i]
    return int(num)


class HefeiSpider(scrapy.Spider):
    name = 'HefeiSpider'
    start_urls = (
        'http://real.hffd.gov.cn/?re=&servicetype=%25E4%25BD%258F%25E5%25AE%2585',
    )

    def __init__(self,):
        super(HefeiSpider, self).__init__()
        self.item = HfNewhouseItem()

    def parse(self, response):
        district = response.xpath('//ul[@class="select"]/li[1]/dl[1]/dd/a/text()').extract()
        for dis in district[1:]:
            d_url = response.url.replace('?re=', '?re='+dis)
            yield scrapy.Request(d_url, callback=self.parse_xiaoqu, meta={'district': dis})

    def parse_xiaoqu(self, response):
        iptstamp = response.xpath('//input[@id="iptstamp"]/@value').extract_first()
        all_xq = response.xpath('//p[@class="pleft_1_1"]/span/a')
        for a in all_xq:
            xq_id = a.xpath('./@id').extract_first()
            xq_name = a.xpath('./text()').extract_first()
            value = nscaler(xq_id)  # 差值
            num1 = nscaler(xq_id)
            num3 = random.randrange(1000, 9999)
            num2 = num3 + value
            num4 = nscaler(iptstamp)
            real_url = 'http://real.hffd.gov.cn/item/{}-{}-{}-{}'.format(num1, num2, num3, num4)
            print 'real_url-----------', real_url, '2222222222222222'
            meta = response.meta
            meta['xq_name'] = xq_name
            yield scrapy.Request(real_url, callback=self.parse_xqinfo, meta=meta)

    def parse_xqinfo(self, response):

        houses_addr = response.xpath('//dl[@class="lbox"]/dd[10]/text()').extract_first()
        company = response.xpath('//dl[@class="lbox"]/dd[1]/text()').extract_first()
        all_houses_url = response.xpath('//table[@id="ContentPlaceHolder1_dlBuildingList"]/tbody/tr/td/div/a/@href').extract()
        print len(all_houses_url), '============3333333333333333==========='
        if all_houses_url:
            for url in all_houses_url:
                h_url = response.urljoin(url)
                print 'h_url   ', h_url, '--------------', '3333333333333333'
                meta = response.meta
                meta['houses_addr'] = houses_addr
                meta['company'] = company
                yield scrapy.Request(h_url, callback=self.parse_house, meta=meta)
        else:
            return

    def parse_house(self, response):
        house_marking = response.xpath('//div[@class="content_xiangx"]/ul[1]/li[5]/p[1]/span/text()').extract_first()
        opening_time = response.xpath('//div[@class="content_xiangx"]/ul[1]/li[5]/p[2]/span/text()').extract_first()
        completion_time = response.xpath('//div[@class="content_xiangx"]/ul[1]/li[7]/p[1]/span/text()').extract_first()
        delivery_time = response.xpath('//div[@class="content_xiangx"]/ul[1]/li[8]/p[1]/span/text()').extract_first()
        all_house = response.xpath('//table/tr/td[@style="width:70px; height:20px; background-color:#00ff00;'
                                   'text-wrap:none;text-align:center;color:#fff"]/@onclick').re('\d+')
        if all_house:
            for h_id in all_house:
                print h_id, '44444444444444444444444444'
                real_id = nscaler(h_id)
                detail_url = 'http://real.hffd.gov.cn/details/getrsa/{}'.format(real_id)
                meta = response.meta
                meta['house_marking'] = house_marking
                meta['opening_time'] = opening_time
                meta['completion_time'] = completion_time
                meta['delivery_time'] = delivery_time
                yield scrapy.Request(detail_url, callback=self.get_id, meta=meta)
        else:
            return

    def get_id(self, response):
        j = json.loads(response.body)
        print j
        h_id = j.get('id')
        if h_id:
            print '------------============-------------', h_id, '55555555555555555'
            url = 'http://real.hffd.gov.cn/details/house/{}'.format(h_id)
            yield scrapy.Request(url, callback=self.parse_house_info, meta=response.meta)
        else:
            print 'h_id is None  5555555555555555555555555'
            return

    def parse_house_info(self, response):
        data = json.loads(response.body)
        print
        data = data.get('data')
        if data:
            print response.meta, '666666666666666666'
            print data, '66666666666666666666'

            self.item['project_name'] = response.meta['xq_name']
            self.item['district'] = response.meta['district']
            self.item['company'] = response.meta['company']
            self.item['opening_time'] = response.meta['opening_time']
            self.item['address'] = data.get('lbLocation')
            self.item['project_addr'] = response.meta['houses_addr']
            self.item['house_marking'] = data.get('lbPartNO')
            self.item['house_marking'] = data.get('lbHouseUsefulness')
            self.item['build_in_area'] = data.get('lbInsideArea')
            self.item['AVG_area'] = data.get('lbJoinArea')
            self.item['build_area'] = data.get('lbBuildArea')
            self.item['sale_status'] = data.get('lbSellFlag')
            self.item['price'] = data.get('iPrice')
            self.item['city'] = '合肥'
            self.item['province'] = '安徽'
            self.item['completion_time'] = response.meta['completion_time']
            self.item['delivery_time'] = response.meta['delivery_time']
            yield self.item
        else:
            return

