# coding:utf-8

import scrapy
from newHouse.items import NNItem


class NanningSoider(scrapy.Spider):
    """
    南宁现在无法爬去内容
    """
    name = 'NanningSpider'
    start_urls = (
        'http://www.nnfcj.gov.cn/tradedataProjectList_%s.jspx?ctg=0' % i for i in range(1, 440)
    )

    def parse(self, response):
        all_xq = response.xpath('//div[@class="article"]/div[1]/table/tr')
        for xq in all_xq[1:]:
            company = xq.xpath('./td[1]/text()').extract_first()
            xq_name = xq.xpath('./td[2]/text()').extract_first()
            xq_addr = xq.xpath('./td[3]/text()').extract_first()
            sale_area = xq.xpath('./td[5]/text()').extract_first()
            approve_time = xq.xpath('./td[6]/text()').extract_first()
            link = xq.xpath('@onclick').re_first("window.open\('(\S+)'")
            xq_url = response.urljoin(link)
            # print xq_url, '11111111111111111111111111'
            yield scrapy.Request(xq_url, callback=self.parse_xq,
                                 meta={'company': company, 'xq_name': xq_name, 'xq_addr': xq_addr,
                                       'sale_area': sale_area, 'approve_time': approve_time})

    def parse_xq(self, response):
        building_num = response.xpath('//div[@class="article"]/table[2]/tr')
        for n in building_num:
            link = n.xpath('@onclick').re_first("window\.location\.href=\'(\S+)\'")
            building_url = response.urljoin(link)
            # print building_url, '22222222222222222222222'
            yield scrapy.Request(building_url, callback=self.parse_building, meta=response.meta)

    def parse_building(self, response):
        layer = response.xpath('//div[@class="article mt10"]/table[2]/tr')
        for l in layer[1:]:
            all_room = l.xpath('./td/div/ul/li[@class="tjCor4"]')
            for room in all_room:
                item = NNItem()
                d_dict = dict()
                room_data = room.xpath('@title').extract_first()
                doorplate = room.xpath('./text()').re_first('\S+')
                # print '------333333333333', doorplate, '=========', response.meta
                data = map(lambda x: x.strip(), room_data.split('<br />'))
                for d in data:
                    d_data = d.split(u'：')
                    d_dict[d_data[0]] = d_data[1]
                # for i in d_dict:
                #     print i, d_dict.get(i), '33333===='

                item['develop_company'] = response.meta['company']
                item['project_name'] = response.meta['xq_name']
                item['project_address'] = response.meta['xq_addr']
                item['total_area'] = response.meta['sale_area']
                item['approve_time'] = response.meta['approve_time']
                item['doorplate'] = doorplate
                item['price'] = d_dict.get(u'预售价格')
                item['area'] = d_dict.get(u'建筑面积')
                item['use_for'] = d_dict.get(u'用途')
                item['house_structure'] = d_dict.get(u'户型')
                print item
                yield item
