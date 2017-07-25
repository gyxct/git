# coding:utf-8

import scrapy
from newHouse.items import FuzhouItem


class FuzhouSoider(scrapy.Spider):
    name = 'FuzhouSpider'
    start_urls = (
        'http://222.77.178.63:7002/result_new.asp?page2=%s' % i for i in range(1, 116)
    )

    def parse(self, response):
        all_xq = response.xpath('//body/table[1]/tr[2]//table//tr[@height="25"]')
        for xq in all_xq:
            permission_area = xq.xpath('./td[3]/text()').extract_first()
            sale_building_num = xq.xpath('./td[4]/text()').extract_first()

            completion_time = xq.xpath('./td[6]/text()').extract_first()
            detail_url = response.urljoin(xq.xpath('./td[2]/a/@href').extract_first())
            print detail_url, '-----------11111111111111'
            yield scrapy.Request(detail_url, callback=self.parse_xq,
                                 meta={'permission_area': permission_area, 'sale_building_num': sale_building_num,
                                       'completion_time': completion_time})

    def parse_xq(self, response):
        project_name = response.xpath('//body/table[2]/tr[1]//table/tr[1]/table/tr/td[2]/table/tr[2]/td[1]'
                                      '/table/tr[1]/td[2]/text()').extract_first()
        district = response.xpath('//body/table[2]/tr[1]//table/tr[1]/table/tr/td[2]/table/tr[2]/td[1]'
                                  '/table/tr[1]/td[4]/text()').extract_first()
        project_addr = response.xpath('//body/table[2]/tr[1]//table/tr[1]/table/tr/td[2]/table/tr[2]/td[1]'
                                      '/table/tr[2]/td[2]/text()').extract_first()
        company = response.xpath('//body/table[2]/tr[1]//table/tr[1]/table/tr/td[2]/table/tr[2]/td[1]'
                                 '/table/tr[3]/td[2]//text()').extract_first()
        meta = response.meta
        meta['project_name'] = project_name
        meta['district'] = district
        meta['project_addr'] = project_addr
        meta['company'] = company

        iframe_url = response.urljoin(response.xpath('//*[@id="SUList"]/@src').extract_first())
        print response.xpath('//*[@id="SUList"]/@src').extract_first(), '222__------------'
        print iframe_url, '----------22222222222222'
        yield scrapy.Request(iframe_url, callback=self.parse_iframe, meta=meta)

    def parse_iframe(self, response):
        all_project = response.xpath('//table/tr')
        for p in all_project[1:]:
            project_url = response.urljoin(p.xpath('./td[1]/a/@href').extract_first())
            approve_time = p.xpath('./td[4]/text()').extract_first()
            meta = response.meta
            meta['approve_time'] = approve_time
            print project_url, '--------333333333333333'
            yield scrapy.Request(project_url, callback=self.parse_project, meta=meta)

    def parse_project(self, response):
        all_building = response.xpath('//table//table//table/tr/td[1]/a')
        for i in all_building:
            url = response.urljoin(i.xpath('./@href').extract_first())
            building_name = i.xpath('./text()').extract_first()
            meta = response.meta
            meta['building_name'] = building_name
            print url, '----------44444444444444444444'
            yield scrapy.Request(url, callback=self.parse_building, meta=meta)

    def parse_building(self, response):
        all_room = response.xpath('//*[@id="Table1"]/tr/td/table[2]/tr/td[@bgcolor="#00FF00"]/a')
        for r in all_room:
            url = response.urljoin(r.xpath('./@href').extract_first())
            meta = response.meta
            print url, '---------555555555555555'
            yield scrapy.Request(url, meta=meta, callback=self.parse_room)

    def parse_room(self, response):
        item = FuzhouItem()
        data = response.xpath('//body/table[2]//table/tbody')
        item['house_marking'] = data.xpath('./tr[3]/td[2]/text()').extract_first()
        item['build_type'] = data.xpath('./tr[4]/td[2]/text()').extract_first()
        item['build_area'] = data.xpath('./tr[6]/td[2]/text()').extract_first()
        item['build_in_area'] = data.xpath('./tr[7]/td[2]/text()').extract_first()
        item['AVG_area'] = data.xpath('./tr[8]/td[2]/text()').extract_first()
        item['sale_status'] = data.xpath('./tr[14]/td[2]/text()').extract_first()
        item['price'] = data.xpath('./tr[15]/td[2]/text()').extract_first()
        item['total_price'] = data.xpath('./tr[16]/td[2]/text()').extract_first()

        item['permission_area'] = response.meta['permission_area']
        item['sale_building_num'] = response.meta['sale_building_num']
        item['completion_time'] = response.meta['completion_time']
        item['project_name'] = response.meta['project_name']
        item['district'] = response.meta['district']
        item['project_addr'] = response.meta['project_addr']
        item['company'] = response.meta['company']
        item['approve_time'] = response.meta['approve_time']
        item['building_name'] = response.meta['building_name']
        item['city'] = '福州'
        print item
        yield item





