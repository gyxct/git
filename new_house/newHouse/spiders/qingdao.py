#!usr/bin/env python
# coding:utf-8


import scrapy
from newHouse.items import QingdaoNewhouseItem
from newHouse.log_package.log_file import logs

class QingdaoNewHouse(scrapy.Spider):
    name = 'qingdao_new_house'
    start_urls = (
        'http://www.qdfd.com.cn/qdweb/realweb/fh/FhProjectQuery.jsp?',
    )

    def parse(self, response):
        page_num = response.xpath('//table')[2].xpath('tr/td/text()').re_first(u'共(\d+)页')
        for i in range(1, int(page_num)+1):
            next_page_url = 'http://www.qdfd.com.cn/qdweb/realweb/fh/FhProjectQuery.jsp?page=%s&rows=20&okey=&order=' % str(i)
            logs.debug("---------first--------: %s" % next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse_xiaoqu_url)

    def parse_xiaoqu_url(self, response):
        xiaoqu_url = response.xpath('//table')[1].xpath('tr')
        for i in xiaoqu_url:
            if i.xpath('td[1]/text()').extract_first() == '在售':
                projectID = i.xpath('td[2]/a/@href').re_first('\d+')
                url = 'http://www.qdfd.com.cn/qdweb/realweb/fh/FhProjectInfo.jsp'
                logs.debug("---------second--------: %s" % url)
                yield scrapy.FormRequest(url, callback=self.parse_building_url, formdata={'projectID': projectID})

    def parse_building_url(self, response):
        project_name = response.xpath('//td[@class="bszn_title"]/text()').re_first('\S+')
        company = response.xpath('//td[@class="xxxx_list1"]')[2].xpath('span[2]/a/text()').re_first('\S+')
        project_addr = response.xpath('//td[@class="xxxx_list1"]')[1].xpath('span[2]/text()').re_first('\S+')
        district = response.xpath('//td[@class="xxxx_list1"]')[0].xpath('span[2]/text()').re_first('\S+')
        permit_presale = response.xpath('//span[@id="preName"]/text()').re_first('\S+')
        iframe = response.xpath('//iframe[@id="buildShow"]/@src').extract_first()
        url = 'http://www.qdfd.com.cn/qdweb/realweb/fh/' + iframe
        logs.debug("---------third--------: %s" % url)
        yield scrapy.Request(url, callback=self.parse_iframe_url, meta={'project_name': project_name,
                                                                        'company': company,
                                                                        'project_addr': project_addr,
                                                                        'district': district,
                                'permit_presale':permit_presale})
    def parse_iframe_url(self, response):
        building_info = response.xpath('//ul[@class="xsb_bg"]//table')[1].xpath('tr')
        for i in building_info[1:]:
            sale_building_num = i.xpath('td[1]/a/text()').extract_first()
            total_price = i.xpath('td[2]/text()').extract_first()
            floating_range = i.xpath('td[3]/text()').extract_first()
            sale_house_num = i.xpath('td[4]/text()').extract_first()
            total_num = i.xpath('td[5]/text()').extract_first()
            total_number = i.xpath('td[6]/text()').extract_first()
            buildid = i.xpath('td[1]/a/@href').re('\d+')[0]
            startid = i.xpath('td[1]/a/@href').re('\d+')[1]
            proid = i.xpath('td[1]/a/@href').re('\d+')[2]
            url = 'http://www.qdfd.com.cn/qdweb/realweb/fh/' + 'FhHouseStatus.jsp?buildingID='+buildid+'&startID='+startid+'&projectID='+proid
            logs.debug("---------fourth--------: %s" % url)
            yield scrapy.Request(url, callback=self.parse_detail_url, meta={'project_name': response.meta['project_name'],
                                                                            'company': response.meta['company'],
                                                                            'project_addr': response.meta['project_addr'],
                                                                            'district': response.meta['district'],
                                                                            'permit_presale': response.meta['permit_presale'],
                                                                            'sale_building_num': sale_building_num,
                                                                            'total_price': total_price,
                                                                            'floating_range': floating_range,
                                                                            'sale_house_num': sale_house_num,
                                                                            'total_num': total_num,
                                                                            'total_number': total_number})

    def parse_detail_url(self, response):
        unit_info = response.xpath('//td[@bgcolor="#00C200"]')
        for i in unit_info:
            house_marking = i.xpath('a/text').extract_first()
            houseid = i.xpath('a/@href').re_first('\d+')
            url = 'http://www.qdfd.com.cn/qdweb/realweb/fh/' + 'FhHouseDetail.jsp?houseID='+houseid
            logs.debug("---------fifth--------: %s" % url)
            yield scrapy.Request(url, callback=self.parse_detail, meta={'project_name': response.meta['project_name'],
                                                                            'company': response.meta['company'],
                                                                            'project_addr': response.meta['project_addr'],
                                                                            'district': response.meta['district'],
                                                                            'permit_presale': response.meta['permit_presale'],
                                                                            'sale_building_num': response.meta['sale_building_num'],
                                                                            'total_price': response.meta['total_price'],
                                                                            'floating_range': response.meta['floating_range'],
                                                                            'sale_house_num': response.meta['sale_house_num'],
                                                                            'total_num': response.meta['total_num'],
                                                                            'total_number': response.meta['total_number'],
                                                                            'house_marking': house_marking})

    def parse_detail(self, response):
        item = QingdaoNewhouseItem()
        item['project_name'] = response.meta['project_name']
        item['company'] = response.meta['company']
        item['project_addr'] = response.meta['project_addr']
        item['permit_presale'] = response.meta['permit_presale']
        item['sale_building_num'] = response.meta['sale_building_num']
        item['total_price'] = response.meta['total_price']
        item['floating_range'] = response.meta['floating_range']
        item['sale_house_num'] =  response.meta['sale_house_num']
        item['total_num'] = response.meta['total_num']
        item['total_number'] = response.meta['total_number']
        item['house_marking'] = response.meta['house_marking']
        item['district'] = response.meta['district']
        item['province'] = '山东'
        item['city'] = '青岛'

        item['floor'] = response.xpath('//table')[1].xpath('tr[1]/td[2]/text()').re_first('\S+')
        item['build_type'] = response.xpath('//table')[1].xpath('tr[2]/td[2]/text()').re_first('\S+')
        item['structure'] = response.xpath('//table')[1].xpath('tr[2]/td[4]/text()').re_first('\S+')
        item['predicted_floor_area'] = response.xpath('//table')[1].xpath('tr[3]/td[2]/text()').re_first('\S+')
        item['build_area'] = response.xpath('//table')[1].xpath('tr[3]/td[4]/text()').re_first('\S+')
        item['predicted_inner_area'] = response.xpath('//table')[1].xpath('tr[4]/td[2]/text()').re_first('\S+')
        item['build_in_area'] = response.xpath('//table')[1].xpath('tr[4]/td[4]/text()').re_first('\S+')
        item['predicted_area'] = response.xpath('//table')[1].xpath('tr[5]/td[2]/text()').re_first('\S+')
        item['AVG_area'] = response.xpath('//table')[1].xpath('tr[5]/td[4]/text()').re_first('\S+')
        item['predicted_underground_area'] = response.xpath('//table')[1].xpath('tr[6]/td[2]/text()').re_first('\S+')
        item['measured_underground_area'] = response.xpath('//table')[1].xpath('tr[6]/td[4]/text()').re_first('\S+')
        item['house_marking'] = response.xpath('//table')[1].xpath('tr[1]/td[4]/text()').re_first('\S+')
        yield item






