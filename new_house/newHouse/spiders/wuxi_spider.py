#!usr/bin/env python
# coding:utf-8

import sys
import scrapy
from newHouse.items import WuxiItem
from newHouse.log_package.log_file import logs
reload(sys)
sys.setdefaultencoding('utf-8')


class SuzhouNewHouse(scrapy.Spider):
    name = 'WuxiSpider'
    start_urls = (
        'http://www.wxhouse.com/search/house.html?PageIndex=1&District=%B1%F5%BA%FE%C7%F8',
        'http://www.wxhouse.com/search/house.html?PageIndex=1&District=%B3%E7%B0%B2%C7%F8',
        'http://www.wxhouse.com/search/house.html?PageIndex=1&District=%C4%CF%B3%A4%C7%F8',
        'http://www.wxhouse.com/search/house.html?PageIndex=1&District=%D0%C2%A1%A1%C7%F8',
        'http://www.wxhouse.com/search/house.html?PageIndex=1&District=%B1%B1%CC%C1%C7%F8',
        'http://www.wxhouse.com/search/house.html?PageIndex=1&District=%BB%DD%C9%BD%C7%F8',
        'http://www.wxhouse.com/search/house.html?PageIndex=1&District=%CE%FD%C9%BD%C7%F8',
    )

    def parse(self, response):
        districts = response.xpath('/html/body/table/tr[td[div] and td[span]]')
        for d in districts:
            d_url = d.xpath('./td[2]/div[1]/a/@href').extract_first()
            project_name = d.xpath('./td[2]/div[1]/a/text()').extract_first()
            project_address = d.xpath('./td[2]/div[2]/text()').extract_first()
            develop_company = d.xpath('./td[2]/div[3]/text()').extract_first()
            avg_price = d.xpath('./td[3]/span/text()').extract_first()
            yield scrapy.Request(response.urljoin(d_url), callback=self.parse_detail,
                                 meta={'project_name': project_name, 'project_address': project_address,
                                       'develop_company': develop_company, 'avg_price': avg_price}
                                 )
        next_page = response.xpath('//div[@class="numList"]/a[last()]')
        if next_page.xpath('./text()') == '>':
            logs.debug('------------next page: %s------------' % next_page.xpath('./@href'))
            yield scrapy.Request(response.urljoin(next_page.xpath('./@href')), callback=self.parse)

    def parse_detail(self, response):
        item = WuxiItem()
        d = dict()

        all_info = response.xpath('/html/body/table[10]/tr/td[1]/table[2]/tr/td/table/tr/td')
        for i, j in zip(all_info[0:-1:2], all_info[1:-1:2]):
            d[''.join(i.xpath('./text()').extract_first().split())] = j.xpath('./text()').extract_first()
        logs.debug('----------- d: %s -----------' % d)

        item['district'] = response.xpath('//*[@id="divmenuinfo1"]/tr/td[3]/table[1]/tr/td[2]/text()').extract_first()
        item['opening_date'] = response.xpath('//*[@id="divmenuinfo1"]/tr/td[3]/table[2]/tr[2]/td[2]/text()'
                                              ).extract_first()
        item['house_type'] = response.xpath('//*[@id="divmenuinfo1"]/tr/td[3]/table[2]/tr[3]/td[2]/text()'
                                           ).extract_first()

        item['delivery_time'] = d.get(u'交付时间：')
        item['property_type'] = d.get(u'物业类型：')
        item['sale_house_num'] = d.get(u'可售套数：')
        item['green_rate'] = d.get(u'绿化率：')
        item['agent_company'] = d.get(u'代理公司：')
        item['property_fee'] = d.get(u'物管费用：')
        item['volume_rate'] = d.get(u'容积率：')
        item['total_num'] = d.get(u'总套数：')
        item['property_company'] = d.get(u'物管公司：')

        item['project_name'] = response.meta['project_name']
        item['project_address'] = response.meta['project_address']
        item['develop_company'] = response.meta['develop_company']
        item['avg_price'] = response.meta['avg_price']
        item['province'] = '江苏'
        item['city'] = '无锡'
        # logs.debug('------------ item: %s -------------' % item)

        yield item
