#!usr/bin/env python
# coding:utf-8

import sys
import scrapy
import datetime
from newHouse.items import ShanghaiItem
from newHouse.log_package.log_file import logs
reload(sys)
sys.setdefaultencoding('utf-8')


class ShanghaiNewHouse(scrapy.Spider):
    name = 'ShanghaiSpider'
    start_urls = (
        'http://www.fangdi.com.cn/complexPro.asp',
    )

    def parse(self, response):
        all_district = response.xpath('//select[@name="districtID"]/option')
        for d in all_district:
            district = d.xpath('./text()').extract_first()
            value = d.xpath('./@value').extract_first()
            logs.debug('---------district---------%s' % district)

            yield scrapy.FormRequest(response.url,
                                     formdata={'districtID': value},
                                     callback=self.parse_district,
                                     dont_filter=True)

    def parse_district(self, response):
        all_project = response.xpath('//table[6]//tr[td[a]]')
        print len(all_project)

        for project in all_project[:-1]:
            project_name = project.xpath('./td[2]/a/text()').extract_first()
            project_url = response.urljoin(project.xpath('./td[2]/a/@href').extract_first())
            sale_status = project.xpath('./td[1]/text()').extract_first()

            project_total_house_num = project.xpath('./td[4]/text()').extract_first()
            total_area = project.xpath('./td[5]/text()').extract_first()
            district = project.xpath('./td[6]/text()').extract_first()
            # logs.debug('--------project_name-------%s' % project_name)
            # logs.debug('--------project_url--------%s' % project_url)

            yield scrapy.Request(project_url, callback=self.parse_project, meta={
                'project_name': project_name, 'sale_status': sale_status, 'project_total_house_num': project_total_house_num,
                'total_area': total_area, 'district': district
            })

        next_p = response.xpath('//table[6]//tr/td/table/tr/td/a')
        for n in next_p:
            if n.xpath('./text()').extract_first() == '[下一页]':
                next_page = response.urljoin(n.xpath('./@href').extract_first())
                logs.debug('--------------next_page: %s------------' % next_page)
                yield scrapy.Request(next_page, callback=self.parse_district)

    def parse_project(self, response):
        iframe = response.urljoin(response.xpath('//*[@id="SUList"]/@src').extract_first())
        logs.debug('----------iframe: ---------------%s' % iframe)
        yield scrapy.Request(iframe, callback=self.parse_iframe, meta=response.meta)

    def parse_iframe(self, response):
        all_xq = response.xpath('//tr[td[a]]')
        meta = response.meta
        # logs.debug('=========meta==iframe=======%s' % meta)
        for xq in all_xq:
            meta['permit_presale'] = \
                xq.xpath('./td[2]/a/span/text()').extract_first().encode('cp1252').decode('gb2312')
            xq_url = response.urljoin(xq.xpath('./td[2]/a/@href').extract_first())
            meta['opening_time'] = xq.xpath('./td[3]/text()').extract_first()
            meta['total_num'] = xq.xpath('./td[4]/text()').extract_first()
            meta['xq_house_num'] = xq.xpath('./td[5]/text()').extract_first()
            meta['all_house_area'] = xq.xpath('./td[6]/text()').extract_first()
            meta['building_all_area'] = xq.xpath('./td[7]/text()').extract_first()
            # meta['sale_sale_status'] = xq.xpath('./td[8]/text()').re_first('\S+')
            yield scrapy.Request(xq_url, callback=self.parse_xq, meta=meta)

    def parse_xq(self, response):
        buildings = response.xpath('//tr[td[a]]')
        meta = response.meta
        # logs.debug('--------meta--xq--------%s' % meta)
        for i in buildings:
            meta['building_name'] = i.xpath('./td[1]/a/text()').extract_first().encode('cp1252').decode('gb2312')
            building_url = response.urljoin(i.xpath('./td[1]/a/@href').extract_first())
            max_price = i.xpath('./td[2]/text()').re_first('(\d+)/\d+')
            min_price = i.xpath('./td[2]/text()').re_first('\d+/(\d+)')
            meta['max_price'] = max_price
            meta['min_price'] = min_price
            if not max_price and not min_price:
                meta['total_price'] = i.xpath('./td[2]/text()').re_first('\d+')

            logs.debug('------max_price: %s------ min_price: %s------total_price:%s----'
                       % (meta['max_price'], meta['min_price'], meta.get('total_price')))
            yield scrapy.Request(building_url, callback=self.parse_building, meta=meta)

    def parse_building(self, response):
        meta = response.meta
        # logs.debug('-----------meta---building---------%s' % meta)
        all_room_urls = response.xpath('//tr/td/a[b]/@href').extract()
        for url in all_room_urls:
            yield scrapy.Request(response.urljoin(url), callback=self.parse_detail, meta=meta)

    def parse_detail(self, response):
        item = ShanghaiItem()
        print '+++++++++++++6666666666666666+++++++++++++'

        item['province'] = '上海'
        item['city'] = '上海'
        # item['url'] = response.url
        item['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        item['project_name'] = response.meta['project_name']
        item['sale_status'] = response.meta['sale_status']
        item['project_total_house_num'] = response.meta['project_total_house_num']
        item['total_area'] = response.meta['total_area']
        item['district'] = response.meta['district']
        item['permit_presale'] = response.meta['permit_presale']
        item['opening_time'] = response.meta['opening_time']
        item['total_num'] = response.meta['total_num']
        item['xq_house_num'] = response.meta['xq_house_num']
        item['all_house_area'] = response.meta['all_house_area']
        item['building_all_area'] = response.meta['building_all_area']
        # item['sale_sale_status'] = response.meta['sale_sale_status']
        item['building_name'] = response.meta['building_name']
        item['max_price'] = response.meta.get('max_price')
        item['min_price'] = response.meta.get('min_price')
        item['total_price'] = response.meta.get('total_price')

        item['house_marking'] = response.xpath('//*[@id="Table1"]//table//tr[3]/td[2]/text()').extract_first()
        item['build_type'] = response.xpath('//*[@id="Table1"]//table//tr[4]/td[2]/text()').extract_first()
        item['floor'] = response.xpath('//*[@id="Table1"]//table//tr[2]/td[2]/text()').re_first('\d+')
        item['structure'] = response.xpath('//*[@id="Table1"]//table//tr[5]/td[2]/text()').extract_first()

        item['build_area'] = response.xpath('//*[@id="Table1"]//table//tr[10]/td[2]/text()').extract_first()
        item['build_in_area'] = response.xpath('//*[@id="Table1"]//table//tr[11]/td[2]/text()').extract_first()
        item['AVG_area'] = response.xpath('//*[@id="Table1"]//table//tr[12]/td[2]/text()').extract_first()

        yield item
