# -*- coding: utf-8 -*-
import scrapy
import logging
import time

from newHouse.items import GzNewhouseItem



class GuangZhouSpider(scrapy.Spider):
    name = 'Guangzhou_data'
    start_urls = (
        "http://www.gzcc.gov.cn/laho/ProjectSearch.aspx/ProjectSearch.aspx?page=" + str(i)
        for i in range(1,400))
    def parse(self, response):
        tmp = response.xpath('//*[@class="resultTableC"]/tbody/tr')
        base_url = 'http://www.gzcc.gov.cn//laho/project.aspx?'
        for elem in tmp[1:]:
            item = {}
            item['project_name'] = elem.xpath('td')[1].xpath('a/text()').extract_first()
            item['develop_company'] = elem.xpath('td')[2].xpath('a/text()').extract_first()
            item['project_address'] = elem.xpath('td')[4].xpath('a/text()').extract_first()
            xiaoqu_url = elem.xpath('td')[2].xpath('a/@href').extract_first()
            PID = xiaoqu_url[xiaoqu_url.find('pjID='):xiaoqu_url.find('&name')]
            target_xiaoqu_url = base_url + PID
            # logging.debug('project_name:%s',elem.xpath('td')[1].xpath('a/text()').extract_first())
            # logging.debug('developr:%s', elem.xpath('td')[2].xpath('a/text()').extract_first())
            # logging.debug('local_place:%s', elem.xpath('td')[4].xpath('a/text()').extract_first())
            # logging.debug('target_xiaoqu_url:%s', target_xiaoqu_url)
            yield scrapy.Request(target_xiaoqu_url,meta = item,callback=self.parse_detail)

    def parse_detail(self,response):
        '''
        saledHouse_num = scrapy.Field()
        unsaledHouse_num = scrapy.Field()
        area = scrapy.Field()
        saled_area = scrapy.Field()
        unsaled_area = scrapy.Field()
        price = scrapy.Field()
        '''
        item = GzNewhouseItem()
        item['project_name'] = response.meta['project_name']
        item['develop_company'] = response.meta['develop_company']
        item['project_address'] = response.meta['project_address']
        item['use_area'] = response.xpath('//*[@class="content"]/table[1]/tr[4]/td[2]/text()').extract_first()
        item['saled_House_num'] = response.xpath('//*[@class="content"]/table[2]/tr[3]/td[5]/text()').extract_first()
        item['deal_area'] = response.xpath('//*[@class="content"]/table[2]/tr[3]/td[6]/text()').extract_first()
        item['unsaledHouse_num'] = response.xpath('//*[@class="content"]/table[2]/tr[3]/td[8]/text()').extract_first()
        item['unsaled_area'] = response.xpath('//*[@class="content"]/table[2]/tr[3]/td[9]/text()').extract_first()
        item['avg_price'] = response.xpath('//*[@class="content"]/table[2]/tr[3]/td[7]/text()').extract_first()
        item['url'] = response.url
        item['city'] = u'广州'
        item['province'] = u'广东'
        item['crawl_time'] = time.ctime()
        # logging.debug('area:%s', item['area'])
        # logging.debug('saledHouse_num:%s', item['saledHouse_num'])
        # logging.debug('saled_area:%s', item['saled_area'])
        # logging.debug('unsaledHouse_num:%s', item['unsaledHouse_num'])
        # logging.debug('unsaled_area:%s', item['unsaled_area'])
        # logging.debug('price:%s', item['price'])
        yield item




