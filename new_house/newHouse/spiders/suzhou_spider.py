#!usr/bin/env python
# coding:utf-8


import scrapy
# import json
from newHouse.items import SzNewhouseItem
from newHouse.log_package.log_file import logs


class SuzhouNewHouse(scrapy.Spider):
    name = 'suzhou_new_house'
    start_urls = (
        'http://www.szfcweb.com/',
    )

    def parse(self, response):
        fang_url = response.xpath('//table/tr[3]/td[2]/a/@href').extract_first()
        if fang_url:
            yield scrapy.Request(response.urljoin(fang_url), callback=self.parse_search)

    def parse_search(self, response):
        district = ['RD001', 'RD002', 'RD003', 'RD004', 'RD005', 'RD008']
        # EVENTTARGET = response.xpath('//input[@name="__EVENTTARGET"]/@value').extract_first()
        # EVENTARGUMENT = response.xpath('//input[@name="__EVENTARGUMENT"]/@value').extract_first()
        # LASTFOCUS = response.xpath('//input[@name="__LASTFOCUS"]/@value').extract_first()
        VIEWSTATE = response.xpath('//input[@name="__VIEWSTATE"]/@value').extract_first()
        EVENTVALIDATION = response.xpath('//input[@name="__EVENTVALIDATION"]/@value').extract_first()
        VIEWSTATEGENERATOR = response.xpath('//input[@name="__VIEWSTATEGENERATOR"]/@value').extract_first()
        #'__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR if VIEWSTATEGENERATOR else '',
        for i in district:
            start = 0
            end = 80
            while start < 300:
                formdata = {
                    # '__EVENTTARGET': EVENTTARGET if EVENTTARGET else '',
                    # '__EVENTARGUMENT': EVENTARGUMENT if EVENTARGUMENT else '',
                    # '__LASTFOCUS': LASTFOCUS if LASTFOCUS else '',
                    '__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR if VIEWSTATEGENERATOR else '',
                    '__EVENTVALIDATION': EVENTVALIDATION if EVENTVALIDATION else '',
                    '__VIEWSTATE': VIEWSTATE if VIEWSTATE else '',
                    'ctl00$MainContent$txt_Pro': '',
                    'ctl00$MainContent$ddl_qy': i,
                    'ctl00$MainContent$txt_Com': '',
                    'ctl00$MainContent$rb_HF_CODE': '-1',
                    'ctl00$MainContent$txt_Price1': '',
                    'ctl00$MainContent$txt_Price2': '',
                    'ctl00$MainContent$txt_Area1': str(start),
                    'ctl00$MainContent$txt_Area2': str(end),
                    'ctl00$MainContent$ddl_houseclass': '1',
                    'ctl00$MainContent$bt_select': '查询'
                    # 'ctl00$MainContent$PageGridView1$ctl22$PageList': '0'
                }
                yield scrapy.FormRequest(response.url, formdata=formdata,
                                         callback=lambda responses, district=i, start=start, end=end:
                                         self.make_url(responses, district, start, end), meta={'final': end})
                logs.debug('***********%s--%s--%s--%s--%s**************' % (formdata.get('ctl00$MainContent$ddl_qy'),
                                                                    formdata.get('__EVENTTARGET'),
                                                                    formdata.get('__EVENTARGUMENT'),
                                                                    formdata.get('ctl00$MainContent$txt_Area1'),
                                                                    formdata.get('ctl00$MainContent$txt_Area2')))
                start =end
                end += 20
            start = 300
            end = 1500
            formdata = {
                # '__EVENTTARGET': EVENTTARGET if EVENTTARGET else '',
                # '__EVENTARGUMENT': EVENTARGUMENT if EVENTARGUMENT else '',
                # '__LASTFOCUS': LASTFOCUS if LASTFOCUS else '',
                '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR if VIEWSTATEGENERATOR else '',
                '__EVENTVALIDATION': EVENTVALIDATION if EVENTVALIDATION else '',
                '__VIEWSTATE': VIEWSTATE if VIEWSTATE else '',
                'ctl00$MainContent$txt_Pro': '',
                'ctl00$MainContent$ddl_qy': i,
                'ctl00$MainContent$txt_Com': '',
                'ctl00$MainContent$rb_HF_CODE': '-1',
                'ctl00$MainContent$txt_Price1': '',
                'ctl00$MainContent$txt_Price2': '',
                'ctl00$MainContent$txt_Area1': str(start),
                'ctl00$MainContent$txt_Area2': str(end),
                'ctl00$MainContent$ddl_houseclass': '1',
                'ctl00$MainContent$bt_select': '查询'
                # 'ctl00$MainContent$PageGridView1$ctl22$PageList': '0'
            }
            yield scrapy.FormRequest(response.url, formdata=formdata,
                                     callback=lambda responses, district=i, start=start, end=end:
                                     self.make_url(responses, district, start, end))
            logs.debug('***********%s--%s--%s--%s--%s**************' % (formdata.get('ctl00$MainContent$ddl_qy'),
                                                                        formdata.get('__EVENTTARGET'),
                                                                        formdata.get('__EVENTARGUMENT'),
                                                                        formdata.get(
                                                                            'ctl00$MainContent$txt_Area1'),
                                                                        formdata.get(
                                                                            'ctl00$MainContent$txt_Area2')))

    def make_url(self, response, district, start, end):
        # 如果len的长度是1说明请求的数据量超过1000条,在页面中不显示,需要重新定义请求量
        if len(response.xpath('//table[@id="ctl00_MainContent_PageGridView1"]/tr')) == 1:
            end = (end - start) / 2 + start
            # EVENTTARGET = response.xpath('//input[@name="__EVENTTARGET"]/@value').extract_first()
            # EVENTARGUMENT = response.xpath('//input[@name="__EVENTARGUMENT"]/@value').extract_first()
            # LASTFOCUS = response.xpath('//input[@name="__LASTFOCUS"]/@value').extract_first()
            VIEWSTATE = response.xpath('//input[@name="__VIEWSTATE"]/@value').extract_first()
            EVENTVALIDATION = response.xpath('//input[@name="__EVENTVALIDATION"]/@value').extract_first()
            VIEWSTATEGENERATOR = response.xpath('//input[@name="__VIEWSTATEGENERATOR"]/@value').extract_first()
            #__VIEWSTATEGENERATOR
            formdata = {
                # '__EVENTTARGET': EVENTTARGET if EVENTTARGET else '',
                # '__EVENTARGUMENT': EVENTARGUMENT if EVENTARGUMENT else '',
                # '__LASTFOCUS': LASTFOCUS if LASTFOCUS else '',
                '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR if VIEWSTATEGENERATOR else '',
                '__EVENTVALIDATION': EVENTVALIDATION if EVENTVALIDATION else '',
                '__VIEWSTATE': VIEWSTATE if VIEWSTATE else '',
                'ctl00$MainContent$txt_Pro': '',
                'ctl00$MainContent$ddl_qy': district,
                'ctl00$MainContent$txt_Com': '',
                'ctl00$MainContent$rb_HF_CODE': '-1',
                'ctl00$MainContent$txt_Price1': '',
                'ctl00$MainContent$txt_Price2': '',
                'ctl00$MainContent$txt_Area1': str(start),
                'ctl00$MainContent$txt_Area2': str(end),
                'ctl00$MainContent$ddl_houseclass': '1',
                'ctl00$MainContent$bt_select': '查询'
                # 'ctl00$MainContent$PageGridView1$ctl22$PageList': '0'
            }
            yield scrapy.FormRequest(response.url, formdata=formdata,
                                     callback=lambda responses, district=district, start=start, end=end:
                                     self.make_url(responses, district, start, end), meta={'final': response.meta['final']})
            logs.debug('***********%s--%s--%s--%s--%s**************' % (formdata.get('ctl00$MainContent$ddl_qy'),
                                                                        formdata.get('__EVENTTARGET'),
                                                                        formdata.get('__EVENTARGUMENT'),
                                                                        formdata.get('ctl00$MainContent$txt_Area1'),
                                                                        formdata.get('ctl00$MainContent$txt_Area2')))
            return
        item = SzNewhouseItem()
        res_xpath = response.xpath('//td[@align="left" and @colspan="4" and @style="text-align: center"]/div/table/tr')
        for i in res_xpath[1:]:
            item['project_name'] = i.xpath('td[1]/text()').extract_first()
            item['project_addr'] = i.xpath('td[1]/text()').extract_first()
            item['company'] = i.xpath('td[2]/text()').extract_first()
            item['build_type'] = i.xpath('td[4]/text()').extract_first()
            item['build_area'] = i.xpath('td[5]/text()').extract_first()
            item['price'] = i.xpath('td[6]/text()').extract_first()
            item['district'] = district
            yield item
        all_page_num = response.xpath('//td[@colspan="7"]/table/tr/td[1]/text()').re_first('\d+')

        page_num = int(all_page_num) / 20 + 1
        logs.debug('page_num: %s' % page_num)
        for num in range(0, page_num-1):
            # EVENTTARGET = response.xpath('//input[@name="__EVENTTARGET"]/@value').extract_first()
            # EVENTARGUMENT = response.xpath('//input[@name="__EVENTARGUMENT"]/@value').extract_first()
            # LASTFOCUS = response.xpath('//input[@name="__LASTFOCUS"]/@value').extract_first()
            VIEWSTATE = response.xpath('//input[@name="__VIEWSTATE"]/@value').extract_first()
            EVENTVALIDATION = response.xpath('//input[@name="__EVENTVALIDATION"]/@value').extract_first()
            VIEWSTATEGENERATOR = response.xpath('//input[@name="__VIEWSTATEGENERATOR"]/@value').extract_first()
            formdata = {
                # '__EVENTTARGET': 'ctl00$MainContent$PageGridView1$ctl22$Next',
                # '__EVENTARGUMENT': EVENTARGUMENT if EVENTARGUMENT else '',
                # '__LASTFOCUS': LASTFOCUS if LASTFOCUS else '',
                '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR if VIEWSTATEGENERATOR else '',
                '__EVENTVALIDATION': EVENTVALIDATION if EVENTVALIDATION else '',
                '__VIEWSTATE': VIEWSTATE if VIEWSTATE else '',
                'ctl00$MainContent$txt_Pro': '',
                'ctl00$MainContent$ddl_qy': district,
                'ctl00$MainContent$txt_Com': '',
                'ctl00$MainContent$rb_HF_CODE': '-1',
                'ctl00$MainContent$txt_Price1': '',
                'ctl00$MainContent$txt_Price2': '',
                'ctl00$MainContent$txt_Area1': str(start),
                'ctl00$MainContent$txt_Area2': str(end),
                'ctl00$MainContent$ddl_houseclass': '1',
                # 'ctl00$MainContent$PageGridView1$ctl22$PageList': str(num)
            }
            yield scrapy.FormRequest(response.url, formdata=formdata,
                                     callback=lambda responses, district=district:
                                     self.parse_detail(responses, district))
            logs.debug('***********%s--%s--%s--%s--%s--%s**************' % (formdata.get('ctl00$MainContent$ddl_qy'),
                                                                            formdata.get('__EVENTTARGET'),
                                                                            formdata.get('__EVENTARGUMENT'),
                                                                            formdata.get('ctl00$MainContent$txt_Area1'),
                                                                            formdata.get('ctl00$MainContent$txt_Area2'),
                                                                            formdata.get(
                                                                                'ctl00$MainContent$PageGridView1$ctl22$PageList')))

        if response.meta.get('final'):
            while end < response.meta['final']:
                # EVENTTARGET = response.xpath('//input[@name="__EVENTTARGET"]/@value').extract_first()
                # EVENTARGUMENT = response.xpath('//input[@name="__EVENTARGUMENT"]/@value').extract_first()
                # LASTFOCUS = response.xpath('//input[@name="__LASTFOCUS"]/@value').extract_first()
                VIEWSTATE = response.xpath('//input[@name="__VIEWSTATE"]/@value').extract_first()
                EVENTVALIDATION = response.xpath('//input[@name="__EVENTVALIDATION"]/@value').extract_first()
                VIEWSTATEGENERATOR = response.xpath('//input[@name="__VIEWSTATEGENERATOR"]/@value').extract_first()
                start = end
                end = response.meta['final']
                formdata = {
                    # '__EVENTTARGET': EVENTTARGET if EVENTTARGET else '',
                    # '__EVENTARGUMENT': EVENTARGUMENT if EVENTARGUMENT else '',
                    # '__LASTFOCUS': LASTFOCUS if LASTFOCUS else '',
                    '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR if VIEWSTATEGENERATOR else '',
                    '__EVENTVALIDATION': EVENTVALIDATION if EVENTVALIDATION else '',
                    '__VIEWSTATE': VIEWSTATE if VIEWSTATE else '',
                    'ctl00$MainContent$txt_Pro': '',
                    'ctl00$MainContent$ddl_qy': district,
                    'ctl00$MainContent$txt_Com': '',
                    'ctl00$MainContent$rb_HF_CODE': '-1',
                    'ctl00$MainContent$txt_Price1': '',
                    'ctl00$MainContent$txt_Price2': '',
                    'ctl00$MainContent$txt_Area1': str(start),
                    'ctl00$MainContent$txt_Area2': str(end),
                    'ctl00$MainContent$ddl_houseclass': '1',
                    'ctl00$MainContent$bt_select': '查询'
                    # 'ctl00$MainContent$PageGridView1$ctl22$PageList': '0'
                }
                yield scrapy.FormRequest(response.url, formdata=formdata,
                                         callback=lambda responses, district=district, start=start, end=end:
                                         self.make_url(responses, district, start, end), meta={'final': response.meta['final']})
                logs.debug('***********%s--%s--%s--%s--%s**************' % (formdata.get('ctl00$MainContent$ddl_qy'),
                                                                            formdata.get('__EVENTTARGET'),
                                                                            formdata.get('__EVENTARGUMENT'),
                                                                            formdata.get('ctl00$MainContent$txt_Area1'),
                                                                            formdata.get(
                                                                                'ctl00$MainContent$txt_Area2')))

    def parse_detail(self, response, district):
        item = SzNewhouseItem()
        res_xpath = response.xpath('//td[@align="left" and @colspan="4" and @style="text-align: center"]/div/table/tr')
        for i in res_xpath[1:]:
            item['project_name'] = i.xpath('td[1]/text()').extract_first()
            item['project_addr'] = i.xpath('td[1]/text()').extract_first()
            item['company'] = i.xpath('td[2]/text()').extract_first()
            item['build_type'] = i.xpath('td[4]/text()').extract_first()
            item['build_area'] = i.xpath('td[5]/text()').extract_first()
            item['price'] = i.xpath('td[6]/text()').extract_first()
            item['district'] = district
            yield item