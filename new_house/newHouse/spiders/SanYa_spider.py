# coding:utf-8

import scrapy
from newHouse.items import SanyaItem


class SanyaSoider(scrapy.Spider):
    name = 'SanyaSpider'
    start_urls = (
        'http://www.fcxx0898.com/syfdc/House/Search.aspx?keyword=&page=%s' % i for i in range(42)
    )

    def parse(self, response):
        all_houses = response.xpath('//table')
        print '--------------------------------', len(all_houses), '-----------------'
        for a in all_houses:
            houses_name = a.xpath('./tr[1]/td[2]/div/text()').re_first('\S+.*')
            houses_addr = ''.join(a.xpath('./tr[2]/td[1]/div/text()').extract_first().split()).split(u'：')[1]
            part_district = a.xpath('./tr[3]/td[1]/div/text()').extract_first().strip().split(u'：')[1]
            develop_company = a.xpath('./tr[4]/td[1]/div/text()').extract_first().strip().split(u'：')[1]
            fid = a.xpath('./tr[4]/td[2]/input/@fid').extract_first()
            # print fid, '-1--', develop_company, '-2--', part_district, '-3--', houses_addr, '-4--', houses_name
            detail_url = 'http://www.fcxx0898.com/syfdc/House/Details.aspx?fid=%s&type=1' % fid
            print 'fid', fid, '---', detail_url,  '---response.url-----', response.url
            yield scrapy.Request(detail_url, callback=self.parse_houses,
                                 meta={'houses_name': houses_name, 'houses_addr': houses_addr,
                                       'part_district': part_district, 'develop_company': develop_company})

    def parse_houses(self, response):
        item = SanyaItem()
        item['avg_price'] = response.xpath('//div[@class="house_content"]//table/tr[2]/th/span/strong/text()').extract_first()
        item['opening_date'] = response.xpath('//div[@class="house_content"]//table/tr[3]/th/text()').extract_first()
        item['loupan_type'] = response.xpath('//div[@class="house_content"]//table/tr[4]/th/text()').extract_first()
        item['house_type'] = response.xpath('//div[@id="wrap"]/div[3]/div[2]//table/tr[2]/th[1]/text()').extract_first()
        item['district'] = response.xpath('//div[@id="wrap"]/div[3]/div[2]//table/tr[3]/th[1]/text()').extract_first()
        item['plan_area'] = response.xpath('//div[@id="wrap"]/div[3]/div[2]//table/tr[4]/th[1]/text()').extract_first()
        item['building_area'] = response.xpath('//div[@id="wrap"]/div[3]/div[2]//table/tr[5]/th[1]/text()').extract_first()
        item['building_num'] = response.xpath('//div[@id="wrap"]/div[3]/div[2]//table/tr[6]/th[1]/text()').extract_first()
        item['house_num'] = response.xpath('//div[@id="wrap"]/div[3]/div[2]//table/tr[7]/th[1]/text()').extract_first()
        item['property_fee'] = response.xpath('//div[@id="wrap"]/div[3]/div[2]//table/tr[8]/th[1]/text()').extract_first()
        item['green_rate'] = response.xpath('//div[@id="wrap"]/div[3]/div[2]//table/tr[10]/th[1]/text()').extract_first()
        item['volume_rate'] = response.xpath('//div[@id="wrap"]/div[3]/div[2]//table/tr[9]/th[1]/text()').extract_first()
        item['decorate_status'] = response.xpath('//div[@id="wrap"]/div[3]/div[2]//table/tr[11]/th[1]/text()').extract_first()
        item['project_name'] = response.meta['houses_name']
        item['project_address'] = response.meta['houses_addr']
        item['part_district'] = response.meta['part_district']
        item['develop_company'] = response.meta['develop_company']
        item['url'] = response.url
        yield item
