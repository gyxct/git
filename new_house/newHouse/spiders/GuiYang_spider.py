# -*- coding: utf-8 -*-
import scrapy
import logging
import time

from newHouse.items import GuiYangItem



class GuiYangSpider(scrapy.Spider):
    name = 'GuiYang_data'
    start_urls = (
        "http://www.gyfc.net.cn/2_proInfo/index.aspx?page=" + str(i)
        for i in range(1,50))

    def parse(self, response):
        div_list = response.xpath('//*[@id="right"]/table/tr/td/div')
        logging.debug(div_list)
        for elem in div_list[:-1]:
            xiaoqu_msg = {}
            target_href = elem.xpath('table/tr/td[1]/table/tr[1]/td[1]/a/@href').extract_first()
            logging.debug('------------- ------------target_href:%s' % target_href)
            if not target_href:
                logging.warning("+++++ ++++++++++++ ++++++++++++ ++++++++++++ +++++++ href empty: %s"%response.url)
            else:
                xiaoqu_msg['name'] = elem.xpath('table/tr/td[1]/table/tr[1]/td[3]/text()').extract_first()
                xiaoqu_msg['local_place'] = elem.xpath('table/tr/td[1]/table/tr[2]/td[2]/text()').extract_first()
                logging.debug('------------- --------name: %s'%xiaoqu_msg['name'])
                logging.debug('------------- --------local_place: %s' %xiaoqu_msg['local_place'])
                yield scrapy.Request(target_href,meta = xiaoqu_msg,callback = self.openXiaoqu)

    def openXiaoqu(self,response):
        logging.debug('------------- ------------open xiaoqu url: response_url: %s'%response.url)
        loupan_list = response.xpath('//*[@id="proInfodetail_panResult"]/table/tr/td/div')
        logging.debug(loupan_list)
        for elem in  loupan_list[:-1]:
            target_url = elem.xpath('table/tr/td[3]/a/@href').extract_first()
            if not target_url:
                logging.warning('+++++ ++++++++++++ ++++++++++++ ++++++++++++ +++++++ href empty: : %s' % target_url)
                logging.warning('+++++ ++++++++++++ ++++++++++++ ++++++++++++ +++++++ url:%s'%response.url)
            else:
                logging.debug('------------- --------------------open xiaoqu target_url : %s'%target_url)
                yield scrapy.Request(target_url,meta = response.meta,callback=self.parse_detail)

    def parse_detail(self,response):
        item = GuiYangItem()
        logging.debug('----------- -----------open detail success!:  %s'%response.url)
        td_label = response.xpath('//*[@id="ContentPlaceHolder1_sell_info1_DG_sale_info"]/tr[2]/td')
        item['project_name'] = response.meta['name']
        item['project_address'] = response.meta['local_place']
        item['house_type'] = td_label[0].xpath('text()').extract_first()
        logging.debug('------------- -------------type:%s'%item['house_type'])
        item['house_num'] = td_label[1].xpath('text()').extract_first()
        logging.debug('------------- -------------house_num:%s'%item['house_num'])
        item['can_sale_house'] = td_label[4].xpath('string(.)').extract_first()
        logging.debug('------------- -------------can_dale_house:%s'%item['can_sale_house'])
        item['avg_price'] = td_label[7].xpath('string(.)').extract_first()
        logging.debug('------------- -------------AVG_price:%s'%item['avg_price'])
        item['can_sale_total_area'] = response.xpath('//*[@id="ContentPlaceHolder1_sell_info1_DG_jd_info"]/tr[2]/td[3]/text()').extract_first()
        logging.debug('------------- -------------can_sale_total_area:%s' % item['can_sale_total_area'])

        dict_item = dict(item)
        for elem in dict_item:
            if not dict_item[elem] or dict_item[elem] == 'NULL':
                item[elem] = 'na'
        item['url'] = response.url
        item['crawl_time'] = time.ctime()
        item['city'] =  u'贵阳'
        item['province'] = u'贵州'

        yield item