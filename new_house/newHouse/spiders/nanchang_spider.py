#!usr/bin/env python
# coding:utf-8


import scrapy
from newHouse.items import NcNewhouseItem
from newHouse.log_package.log_file import logs

class XiamenNewHouse(scrapy.Spider):
    name = 'nanchang_new_house'
    start_urls = (
        'http://house.ncfdc.com.cn/default.aspx?tname=60/ProjectInfoList',
    )

    def parse(self, response):
        page_num = response.xpath('//span[@id="ctl09_lblPage_"]/text()').re_first(u'共(\d+)页')
        for i in range(1, int(page_num)+1):
            next_page_url = 'http://house.ncfdc.com.cn/default.aspx?tname=60/ProjectInfoList&page=' + str(i)
            logs.debug("---------first--------: %s" % next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse_xiaoqu_url)

    def parse_xiaoqu_url(self, response):
        xiaoqu_url = response.xpath('//p[@class="build_list_dl_company"]/span[1]/a/@href').extract()
        for i in xiaoqu_url:
            logs.debug("---------second--------: %s" % i)
            yield scrapy.Request(response.urljoin(i), callback=self.parse_iframe_url)

    def parse_iframe_url(self, response, times=1):
        iframe_url = response.xpath('//iframe/@src').extract_first()
        logs.debug("---------third--------: %s" % iframe_url)
        if iframe_url:
            yield scrapy.Request(iframe_url, callback=self.parse_detail_url)
        else:
            if times == 1:
                yield scrapy.Request(response.url, callback=lambda response, times=times+1: self.parse_iframe_url(response, times))

    def parse_detail_url(self, response):
        project_addr = response.xpath('//span[@id="ctl20_project_addr"]/text()').extract_first()
        url = response.xpath('//a[@id="ctl13_LnkLP_LD"]/@href').re_first("href='(\S+)'")
        if url:
            url = '/'.join(url.split('\\\\'))
            logs.debug("---------fourth--------: %s" % url)
            yield scrapy.Request(url, callback=self.parse_iframe_url2, meta={'project_addr': project_addr})

    def parse_iframe_url2(self, response):
        iframe_url = '/'.join(response.xpath('/html').re_first("SetUrl\('(\S+)'\)").split('\\\\')) + "&hrefID=" + response.url.split('=')[-1]
        logs.debug("---------fifth--------: %s" % iframe_url)
        yield scrapy.Request(iframe_url, callback=self.parse_check_detail, meta={'project_addr': response.meta['project_addr']})

    def parse_check_detail(self, response):
        page_num = response.xpath('//div[@class="page"]/span[2]/text()').extract_first()
        logs.debug("---------page_num--------: %s" % page_num)
        if page_num:
            house_list = response.xpath('//table/tr')[3:-1]
            for i in house_list:
                permit_presale = i.xpath('td[2]/a/text()').re_first('\S+')
                approve_time = i.xpath('td[3]/text()').re_first('\S+')
                url = i.xpath('td[last()]/a/@href').extract_first()
                url = '/?'.join(url.split('?'))
                yield scrapy.Request(url, callback=self.parse_detail,
                                     meta={'permit_presale': permit_presale, 'approve_time': approve_time,
                                           'project_addr': response.meta['project_addr']})
            next_page = response.xpath('//a[@id="ctl14_grdSeatList_ctl23_cmdNext"]/@href')
            if next_page:
                VIEWSTATE = response.xpath('//input[@name="__VIEWSTATE"]/@value').extract_first()
                EVENTVALIDATION = response.xpath('//input[@name="__EVENTVALIDATION"]/@value').extract_first()
                formdata = {
                    '__EVENTTARGET': 'ctl14$grdSeatList$ctl23$cmdNext',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': VIEWSTATE if VIEWSTATE else '',
                    '__VIEWSTATEENCRYPTED': '',
                    '__EVENTVALIDATION': EVENTVALIDATION if EVENTVALIDATION else '',
                    'ctl14$txtSearch': '请输入要查找的楼栋名'
                }
                yield scrapy.FormRequest(response.url, formdata=formdata, callback=self.parse_check_detail, meta={'project_addr': response.meta['project_addr']})
        else:
            house_list = response.xpath('//table/tr')[3:]
            for i in house_list:
                permit_presale = i.xpath('td[2]/a/text()').re_first('\S+')
                approve_time = i.xpath('td[3]/text()').re_first('\S+')
                url = i.xpath('td[last()]/a/@href').extract_first()
                url = '/?'.join(url.split('?'))
                yield scrapy.Request(url, callback=self.parse_detail, meta={'permit_presale': permit_presale, 'approve_time': approve_time, 'project_addr':response.meta['project_addr']})

    def parse_detail(self, response):
        item = NcNewhouseItem()
        for i in response.xpath('//tr[@align="center"]'):
            item['project_name'] = response.xpath('//div[@class="warp"]/table[1]/tr[3]/td/text()').re_first('\S+')
            item['company'] = response.xpath('//div[@class="warp"]/table[1]/tr[2]/td/text()').re_first('\S+')
            item['sale_building_num'] = response.xpath('//div[@class="warp"]/table[1]/tr[3]/td/text()').re(r'\S+')[1]
            item['house_number'] = i.xpath('td[2]/text()').re_first('\S+')
            item['build_type'] = i.xpath('td[3]/text()').re_first('\S+')
            item['build_area'] = i.xpath('td[4]/text()').re_first('\S+')
            item['sale_status'] = i.xpath('td[7]/text()').re_first('\S+')
            item['house_orientation'] = i.xpath('td[8]/text()').re_first('\S+')
            item['total_price'] = i.xpath('td[9]/text()').re_first('\S+')
            item['permit_presale'] = response.meta['permit_presale']
            item['approve_time'] = response.meta['approve_time']
            item['project_addr'] = response.meta['project_addr']
            yield item







