# -*- coding: utf-8 -*-
import scrapy
import logging
import re

from newHouse.items import shaoxingItem


class HuZhouSpider(scrapy.Spider):
    name = 'ShaoXing_data'
    start_urls = (
        'http://www.sxhouse.com.cn/loupan/list.aspx?t=&tm=&regioncode=&hk=&price=&page=1&odb=&k=&vid=&time=now',
    )

    def parse(self, response):
        all_page_num = response.xpath('//div[@class="page-info"]/text()').extract_first()
        all_num = re.findall(r'\d+', all_page_num)[-1]
        if all_num:
            for i in range(1, int(all_num) + 1):
                next_url = re.sub(r'page=\d*', r'page=%s' % i, response.url)
                print next_url
                yield scrapy.Request(next_url, self.get_loupan_url)

    def get_loupan_url(self, response):
        loupan_detail_url = response.xpath('//ul[@class="h-list h-list-full newhouse-list"]/li/div[1]/div[1]/a')
        for url in loupan_detail_url:
            next_url = response.urljoin(url.xpath('@href').extract_first())
            yield scrapy.Request(next_url, callback=self.get_key_word)

    def get_key_word(self, response):
        item = shaoxingItem()
        item['province'] = '浙江'
        item['city'] = '绍兴'
        item['house_url'] = response.url
        item['project_name'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[1]/td/text()').re_first('\S+')
        # 开发商
        item['company'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[2]/td/text()').re_first('\S+')
        # 所属区域
        item['district'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[3]/td/text()').re_first('\S+')
        # 面积范围
        item['area_range'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[4]/td/text()').re_first('\S+')
        # 占地面积
        item['use_area'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[5]/td/text()').re_first('\S+')
        # 建筑面积
        item['building_area'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[6]/td/text()').re_first('\S+')
        # 起价
        item['start_price'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[7]/td/text()').re_first('\S+')
        # 均价
        item['avg_price'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[8]/td[2]/text()').re_first('\S+')
        # 销售装态
        sale_states = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[9]/td[2]/img/@src').extract_first()
        if sale_states == "/content/images/icon_selling.gif":
            item['sale_states'] = '在售'
        else:
            item['sale_states'] = '待售'
        # 物业类型
        item['property_type'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[10]/td[2]/text()').extract_first()
        # 楼层状况
        item['floor_status'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[11]/td[2]/text()').extract_first()
        # 物业公司
        item['property_company'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[13]/td[2]/text()').extract_first()
        # 装修状态
        item['decorate_status'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[14]/td[2]/text()').extract_first()
        # 开盘时间
        item['start_sale_time'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[8]/td[1]/text()').re_first('\S+')
        # 绿化率
        item['green_rate'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[9]/td[1]/text()').re_first('\S+')
        # 容积率
        item['volume_rate'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[10]/td[1]/text()').re_first('\S+')
        # 停车位
        item['carport'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[11]/td[1]/text()').re_first('\S+')
        # 售楼地址
        item['sale_address'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[14]/td[1]/text()').re_first('\S+')
        # 详细地址
        item['project_address'] = response.xpath('//div[@class="wrap h-overview-wrap"]/table[1]/tr[16]/td[1]/text()').re_first('\S+')
        print item
        yield item
