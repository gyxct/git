#!usr/bin/env python
# coding:utf-8


import scrapy
from newHouse.items import XmNewhouseItem
from newHouse.log_package.log_file import logs


class XiamenNewHouse(scrapy.Spider):
    name = 'xiamen_new_house'
    start_urls = (
        'http://www.xmjydj.com/search/Project?idx=1',
    )

    def parse(self, response):
        all_page_num = response.xpath('//input[@id="RowCount"]/@value').extract_first()
        page_num = int(all_page_num) / 13 + 1
        for i in range(1, page_num+1):
            next_page_url = response.url + '&page=' + str(i)
            yield scrapy.Request(next_page_url, callback=self.parse_first_url)

    def parse_first_url(self, response):
        project_url = response.xpath('//td[@class="xmmc"]/a/@href').extract()
        for i in project_url:
            yield scrapy.Request(response.urljoin(i), callback=self.parse_basic_detail)

    def parse_basic_detail(self, response):
        basic_info = {}
        basic_info['project_name'] = response.xpath('//span[@class="logo1"]/text()').re_first('\S+')
        basic_info['permit_presale'] = response.xpath('//table[@style="margin-top:10px"]/tr[1]/td[2]/text()').re_first('\d+')
        basic_info['district'] = response.xpath('//table[@style="margin-top:10px"]/tr[2]/td[2]/text()').re_first('\S+')
        basic_info['project_addr'] = response.xpath('//table[@style="margin-top:10px"]/tr[3]/td[2]/text()').re_first('\S+')
        basic_info['company'] = response.xpath('//table[@style="margin-top:10px"]/tr[4]/td[2]//text()').re_first('\S+')
        basic_info['start_time'] = response.xpath('//div[@id="ProjectDetail"]/table[3]/tr[1]/td[2]//text()').re_first('\S+')
        basic_info['end_time'] = response.xpath('//div[@id="ProjectDetail"]/table[3]/tr[2]/td[2]//text()').re_first('\S+')
        basic_info['approve_time'] = response.xpath('//div[@id="ProjectDetail"]/table[3]/tr[7]/td[2]//text()').re_first('\S+')

        house_list_url = response.xpath('//span[@id="zslpDetail"]/a/@href').extract_first()
        if house_list_url:
            yield scrapy.Request(response.urljoin(house_list_url), callback=self.parse_detail, meta={'basic_info': basic_info})

    def parse_detail(self, response):
        logs.debug("*************%s*************" % response.url)
        url = 'http://www.xmjydj.com/Lp/LPPartial/'
        all_panel_form = response.xpath('//ul[@id="browser"]/li/ul/li')
        for i in all_panel_form:
            sale_building_num = i.xpath('span[@class="folder"]/text()').extract_first()
            for j in i.xpath('ul/li'):
                panel_form = j.xpath('a/@href').re(r'\d+')
                house_cate = j.xpath('a/span/text()').extract_first()
                formdata = {'BuildID': panel_form[0] if panel_form else '',
                            'NAID': panel_form[1] if panel_form else '',
                            'lotid': panel_form[2] if panel_form else '',
                            't': '1493705977437'}
                yield scrapy.FormRequest(url, formdata=formdata, callback=self.parse_final_info,
                                         meta={'basic_info': response.meta['basic_info'], 'house_cate': house_cate, 'sale_building_num':sale_building_num})

    def parse_final_info(self, response):
        info = response.xpath('//table[@id="Table1"]/tr')
        zt = 1
        for i in info:
            logs.debug("$$$$$$$$$$$$$$$$%s$$$$$$$$$$$$$$$$" % i)
            floor = i.xpath('//td[1]/text()').re_first('\S+')
            for j in i.xpath('td')[2:]:
                house_number = j.xpath('text()').re_first('\d+')
                id = j.xpath('@id').extract_first()
                tip = j.xpath('@tipmsg').extract_first()
                zs = j.xpath('@hzsstate').extract_first()
                house_marking = j.xpath('text()').extract_first()
                url = '/House/Fwztxx?HouseId=' + id+ '&yyxx=' + tip + '&zs=' + zs + '&zt=' + str(zt)
                logs.debug("---------------%s----------------" % url)
                yield scrapy.Request(response.urljoin(url), callback=self.parse_final_detail,
                                     meta={'basic_info': response.meta['basic_info'], 'house_cate': response.meta['house_cate'],
                                           'sale_building_num': response.meta['sale_building_num'], 'house_number':house_number, 'floor': floor, 'house_marking':house_marking})

    def parse_final_detail(self, response):
        item = XmNewhouseItem()
        logs.debug("---------------%s----------------" % response.url)
        item['project_name'] = response.meta['basic_info'].get('project_name', '')
        item['permit_presale'] = response.meta['basic_info'].get('permit_presale', '')
        item['district'] = response.meta['basic_info'].get('district', '')
        item['project_addr'] = response.meta['basic_info'].get('project_addr', '')
        item['company'] = response.meta['basic_info'].get('company', '')
        item['start_time'] = response.meta['basic_info'].get('start_time', '')
        item['end_time'] = response.meta['basic_info'].get('end_time', '')
        item['approve_time'] = response.meta['basic_info'].get('approve_time', '')
        item['sale_building_num'] = response.meta['sale_building_num']
        item['house_cate'] = response.meta['house_cate']
        item['floor'] = response.meta['floor']
        item['house_number'] = response.meta['house_number']
        item['build_type'] = response.xpath('//div//text()').re_first(u'性质:(\S+)')
        item['use_for'] = response.xpath('//div//text()').re_first(u'用途:(\S+)')
        item['build_area'] = response.xpath('//div//text()').re_first(u'面积:(\S+)')
        item['price'] = response.xpath('//div//text()').re_first(u'拟售单价:(\S+)')
        item['ownership_restriction'] = response.xpath('//div//text()').re_first(u'权属限制:(\S+)')
        item['house_marking'] = response.meta['house_marking']
        item['city'] = '厦门'
        yield item













