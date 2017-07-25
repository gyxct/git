# -*- coding: utf-8 -*-
import scrapy
import logging
import time

from newHouse.items import JinHuaItem

class JinHuaSpider(scrapy.Spider):
    name = 'JinHua_data'
    start_urls = ("http://www.jhfc.gov.cn/Default.aspx",)

    def parse(self,response):
        data_form = {}
        data_form["__EVENTTARGET"] = "query"
        data_form["__EVENTARGUMENT"] = ""
        print "open page"
        yield scrapy.FormRequest.from_response(response, formdata=data_form, callback=self.open_url_page)

    def open_url_page(self,response):
        target_url = "http://www.jhfc.gov.cn/touming/itemSeach.aspx?Sql"
        yield scrapy.Request(target_url,callback=self.get_xiaoqu)

    def get_xiaoqu(self,response):
        '''
            init for_data
        '''
        item = {}
        next_href= response.xpath('//*[@id="lnkbtnNext"]/@href').extract_first()
        xiaoqu_url_list = response.xpath('//*[@class="conten_chage"]/div/table/tr')
        for elem in xiaoqu_url_list:
            sub_elem = elem.xpath('td/a/text()').extract()
            item["district"] = sub_elem[0].strip()
            item["plate"] = sub_elem[1].strip()
            item["license_key"] = sub_elem[2].strip()
            item["project_name"] = sub_elem[3].strip()
            item["develop_company"] = sub_elem[4].strip()
            item["opening_time"] = sub_elem[5].strip()
            for tmp in item.keys():
                print '--------------%s  :'%tmp,item[tmp]
            xiaoqu_url = response.urljoin(elem.xpath('td/a/@href').extract_first())
            yield scrapy.Request(xiaoqu_url,meta=item,callback=self.get_xiaoqu_detail)

        if next_href:
            form_data = {}
            form_data['__EVENTTARGET'] = 'lnkbtnNext'
            form_data['__EVENTARGUMENT'] = ''
            form_data['__VIEWSTATE'] = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()
            print "--- ------ %s"%form_data['__VIEWSTATE']
            yield scrapy.FormRequest.from_response(response,formdata=form_data,callback=self.get_xiaoqu)

    def get_xiaoqu_detail(self,response):
        next_href = response.xpath('//*[@class="conten_chage"]/div[3]/div[2]/a[3]/@href').extract()
        contend_list = response.xpath('//*[@class="conten_chage"]/div[1]/table/tr/td[2]/span/text()').extract()
        item = dict(response.meta)
        item['project_addr'] = contend_list[2]
        item['publish_place'] = contend_list[3]
        item['opening_price'] = contend_list[6]
        item['approve_time'] = response.xpath('//*[@class="conten_chage"]/div[1]/table/tr[7]/td[4]/span/text()').extract_first()
        item['completion_time'] = response.xpath('//*[@class="conten_chage"]/div[1]/table/tr[9]/td[4]/span/text()').extract_first()

        house_list = response.xpath("//*[@class='conten_chage']/div[3]/table[2]/tr")
        for elem in house_list:
            item['sale_building_num'] = elem.xpath('td[1]/a/text()').extract_first()
            item['structure'] = elem.xpath('td[2]/a/text()').extract_first()
            item['total_floor'] = elem.xpath('td[3]/a/text()').extract_first()
            item['building_area'] = elem.xpath('td[4]/a/text()').extract_first()
            item['avg_price'] = elem.xpath('td[5]/a/text()').extract_first()
            house_url = response.urljoin(elem.xpath('td[1]/a/@href').extract_first())
            yield scrapy.Request(house_url,meta=item,callback=self.get_house_detail)
        if next_href:
            form_data = {}
            form_data["__EVENTTARGET"] = "NextPage"
            form_data["__EVENTARGUMENT"] = ""
            yield scrapy.FormRequest.from_response(response,formdata=form_data,callback=self.get_xiaoqu_detail)

    def get_house_detail(self,response):
        m_item = JinHuaItem()
        m_item['district'] = response.meta['district']
        m_item['plate'] = response.meta['plate']
        m_item['license_key'] = response.meta['license_key']
        m_item['project_name'] = response.meta['project_name']
        m_item['develop_company'] = response.meta['develop_company']
        m_item['opening_time'] = response.meta['opening_time']
        m_item['project_addr'] = response.meta['project_addr']
        m_item['publish_place'] = response.meta['publish_place']
        m_item['opening_price'] = response.meta['opening_price']
        m_item['approve_time'] = response.meta['approve_time']
        m_item['completion_time'] = response.meta['completion_time']
        m_item['sale_building_num'] = response.meta['sale_building_num']
        m_item['structure'] = response.meta['structure']
        m_item['total_floor'] = response.meta['total_floor']
        m_item['building_area'] = response.meta['building_area']
        m_item['avg_price'] = response.meta['avg_price']
        m_item['use_for'] = response.xpath('//*[@class="conten_chage"]/div[2]/table/tr[5]/td[2]/span/text()').extract_first()
        m_item['total_house_num'] = response.xpath('//*[@class="conten_chage"]/div[2]/table/tbody/tr[6]/td[2]/span/text()').extract_first()
        m_item['total_floor'] = response.xpath('//*[@class="conten_chage"]/div[2]/table/tr[4]/td[4]/span/text()').extract_first()

        msg_litst = response.xpath('//*[@class="conten_chage"]/table/tr[1]/td[1]/table/tr/td[2]/span/text()').extract()
        m_item['internet_pre_sales_total_nums'] = msg_litst[0]
        m_item['internet_pre_sales_live_nums'] = msg_litst[1]
        m_item['internet_pre_sales_other_nums'] = msg_litst[2]

        m_item['internet_pre_sales_total_areas'] = msg_litst[3]
        m_item['internet_pre_sales_live_areas'] = msg_litst[4]
        m_item['internet_pre_sales_other_areas'] = msg_litst[5]

        m_item['pre_sales_total_nums'] = msg_litst[6]
        m_item['pre_sales_total_areas'] = msg_litst[7]
        m_item['house_num'] = msg_litst[8]
        m_item['can_sale_total_area'] = msg_litst[9]

        m_item['deal_num'] = msg_litst[10]
        m_item['deal_area'] = msg_litst[11]
        m_item['preOrder_or_saled_total_AVG_price'] = msg_litst[12]
        m_item['preOrdered_nums'] = msg_litst[13]
        m_item['preOrdered_areas'] = msg_litst[14]

        m_item['limited_nums'] = msg_litst[15]
        m_item['limited_areas'] = msg_litst[16]
        m_item['not_in_internet_sales_nums'] = msg_litst[17]
        m_item['not_in_internet_sales_areas'] = msg_litst[18]#url
        m_item['url'] = response.url
        m_item['crawl_time'] = time.ctime()
        m_item['city'] = u'金华'
        m_item['province'] = u'浙江'
        yield m_item




