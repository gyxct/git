# coding:utf-8

import re
import scrapy
from newHouse.log_package.log_file import logs
from newHouse.items import HuzhouItem


class HuzhouSoider(scrapy.Spider):
    name = 'HuzhouSpider'
    start_urls = (
        'http://www.hufdc.com/presell.jspx?pageno=%s' % i for i in range(1, 35)
    )

    def parse(self, response):
        all_xq = response.xpath('//div[@class="lbox"]/table/tr')
        print len(all_xq)
        for xq in all_xq[1:]:
            project_name = xq.xpath('./td[2]/a/@title').extract_first()
            develop_company = xq.xpath('./td[3]/a/@title').extract_first()

            certificate_date = xq.xpath('./td[4]/a/text()').extract_first()
            detail_url = response.urljoin(xq.xpath('./td[1]/a/@href').extract_first())
            logs.debug('------111111111--------detail_url-----%s' % detail_url)
            yield scrapy.Request(detail_url, callback=self.parse_xq,
                                 meta={'project_name': project_name, 'develop_company': develop_company,
                                       'certificate_date': certificate_date})

    def parse_xq(self, response):
        info = response.xpath('//div[@class="contentfj"]//table/tbody')
        project_addr = info.xpath('./tr[3]/td[2]/span/text()').extract_first()
        district = info.xpath('./tr[5]/td[2]/span/text()').extract_first()
        approve_time = info.xpath('./tr[6]/td[4]/span/text()').extract_first()
        opening_time = info.xpath('./tr[7]/td[4]/span/text()').extract_first()
        completion_time = info.xpath('./tr[8]/td[4]/span/text()').extract_first()
        xq_total_area = info.xpath('./tr[8]/td[2]/span/text()').extract_first()

        meta = response.meta
        logs.debug('--------222222--------meta---------------%s' % meta)

        meta['project_addr'] = project_addr
        meta['district'] = district
        meta['approve_time'] = approve_time
        meta['opening_time'] = opening_time
        meta['completion_time'] = completion_time
        meta['xq_total_area'] = xq_total_area

        all_building = response.xpath('//div[@class="lptypebarin"]/a')
        for i in all_building:
            building_name = i.xpath('./text()').extract_first()
            meta['building_name'] = building_name
            href = i.xpath('./@href').re_first('\d+,\d+')
            houseid = href.split(',')[0]
            itemid = href.split(',')[1]
            url = 'http://www.hufdc.com/presellinfo.jspx?itemid=%s&houseid=%s' % (itemid, houseid)
            logs.debug('----------url-------222222222222222----------------%s' % url)
            logs.debug('----------------meta--------2222222-------%s' % meta)
            yield scrapy.Request(url, callback=self.parse_building, meta=meta)

    def parse_building(self, response):
        info = response.xpath('//div[@class="housezinfo"]/table/tbody')
        structure = info.xpath('./tr[2]/td[1]/text()').extract_first()
        total_floor = info.xpath('./tr[2]/td[2]/text()').extract_first()
        building_all_area = info.xpath('./tr[2]/td[3]/text()').extract_first()
        all_house_area = info.xpath('./tr[2]/td[3]/text()').extract_first()
        all_sale_area = info.xpath('./tr[2]/td[3]/text()').extract_first()
        total_num = info.xpath('./tr[4]/td[1]/text()').extract_first()
        house_num = info.xpath('./tr[4]/td[2]/text()').extract_first()
        sale_house_num = info.xpath('./tr[4]/td[3]/text()').extract_first()
        logs.debug('------------meta--------33333---------%s' % response.meta)

        house_list = response.xpath('//div[@class="fangjia"]/div[2]/table/tbody/tr')
        for i in house_list:
            item = HuzhouItem()
            item['province'] = '浙江'
            item['city'] = '湖州'

            item['floor'] = i.xpath('./td[2]/text()').extract_first()
            item['house_marking'] = i.xpath('./td[3]/text()').extract_first()
            item['build_area'] = i.xpath('./td[4]/span/text()').extract_first()
            item['build_in_area'] = i.xpath('./td[5]/span/text()').extract_first()
            item['AVG_area'] = i.xpath('./td[6]/span/text()').extract_first()
            item['use_for'] = i.xpath('./td[7]/text()').extract_first()
            item['total_price'] = i.xpath('./td[8]/span/text()').extract_first()

            item['project_addr'] = response.meta['project_addr']
            item['district'] = response.meta['district']
            item['approve_time'] = response.meta['approve_time']
            item['opening_time'] = response.meta['opening_time']
            item['completion_time'] = response.meta['completion_time']
            item['xq_total_area'] = response.meta['xq_total_area']
            item['structure'] = structure
            item['total_floor'] = total_floor
            item['building_all_area'] = building_all_area
            item['all_house_area'] = all_house_area
            item['all_sale_area'] = all_sale_area
            item['total_num'] = total_num
            item['house_num'] = house_num
            item['sale_house_num'] = sale_house_num
            item['project_name'] = response.meta['project_name']

            item['url'] = response.url

            yield item

        next_page = response.xpath('//div[@class="pagenext"]/a[last()]')
        if next_page.xpath('./text()').extract_first() == u'下一页':
            next_page_num = next_page.xpath('./@onclick').re_first('\d+')
            if '&pageno=' not in response.url:
                next_url = response.url + '&pageno=' + next_page_num
            else:
                # next_url = response.url.replace('&pageno='+str(int(next_page_num)-1), '&pageno='+next_page_num)
                next_url = re.sub('&pageno=\d+', '&pageno='+next_page_num, response.url)

            logs.debug('next_url----------%s---------------' % next_url)
            yield scrapy.Request(next_url, callback=self.parse_building, meta=response.meta)






