
# -*- coding: utf-8 -*-
import scrapy
import logging
import time

from newHouse.items import DongGuanItem

class DongGuanSpider(scrapy.Spider):
    name = 'DongGuan_data'
    # start_urls = ('http://www.bjjs.gov.cn')
    start_urls = ('http://dgfc.dg.gov.cn/dgwebsite_v2/Vendition/ProjectInfo.aspx?new=1',)

    def parse(self, response):
        tmp = response.xpath('//*[@id="resultTable"]/tr')
        resultCount = len(tmp) -1
        form_contend = {}
        view_state = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()
        logging.debug('---------------view_state:%s'%view_state[:20])
        event_validation = response.xpath('//*[@id="__EVENTVALIDATION"]/@value').extract_first()
        logging.debug('---------------event_validation:%s' % event_validation[:20])
        district_list = response.xpath('//*[@id="townName"]/option')
        logging.debug('---------------district_list[-1]:%s' % district_list[-1])
        if district_list:
            for elem in district_list:
                target_dustrict_code = elem.xpath('@value').extract_first()
                form_contend['__VIEWSTATE'] = view_state
                form_contend['__EVENTVALIDATION'] = event_validation
                form_contend['townName'] = str(target_dustrict_code)
                form_contend['usage'] = ''
                form_contend['projectName'] = ''
                form_contend['developer'] = ''
                form_contend['area1'] = ''
                form_contend['area2'] = ''
                form_contend['resultCount'] = str(resultCount)
                form_contend['pageIndex'] = '0'
                logging.debug("------- ----------url:%s"%response.url)
                yield scrapy.FormRequest.from_response(response, formdata=form_contend,callback=self.open_url_list)

    def open_url_list(self,response):
        logging.debug('------- ----------open formdata succeed!')
        url_list = response.xpath('//*[@id="resultTable"]/tr')
        for elem in url_list[1:]:
            relative_url = elem.xpath('td[2]/a/@href').extract_first()
            if relative_url:
                target_url = response.urljoin(relative_url)
                logging.debug("------- ----------target_url:%s"%target_url)
            yield scrapy.Request(target_url, callback=self.open_xiaoqu_url)

    def open_xiaoqu_url(self,response):
        xiaoqu_msg = {}
#        project_name = scrapy.Field()
#        saled_area = scrapy.Field()
#        project_addr = scrapy.Field()
        logging.debug('------- ----------xiaoqu_url:%s'%response.url)
        xiaoqu_msg['project_addr'] = response.xpath('//*[@id="houseTable_1"]/tr[2]/td[2]/a/text()').extract_first()
        logging.debug("------- ----------project_addr:%s"%xiaoqu_msg['project_addr'])
        xiaoqu_msg['project_name'] = response.xpath('//*[@id="content_1"]/div[3]/text()[3]').extract_first().split()[0]
        logging.debug("------- ----------project_name:%s" % xiaoqu_msg['project_name'])
        xiaoqu_msg['saled_area'] = response.xpath('//*[@id="houseTable_1"]/tr[2]/td[6]/a/text()').extract_first()
        logging.debug("------- ----------saled_area:%s"%xiaoqu_msg['saled_area'])

        relative_url = response.xpath('//*[@id="houseTable_1"]/tr[2]/td[2]/a/@href').extract_first()
        xiaoqu_url = response.urljoin(relative_url)
        logging.debug("------- ----------xiaoqu_detail:%s"%xiaoqu_url)
        if len(xiaoqu_msg) and xiaoqu_url:
            logging.debug("------- ----------start_house_request!")
            logging.debug("------- ----------house url request msg !")
            logging.debug("------- ----------xiaoqu_url:%s"%xiaoqu_url)
            logging.debug("------- ----------project_addr:%s"%xiaoqu_msg['project_addr'])
            logging.debug("------- ----------project_name:%s"%xiaoqu_msg['project_name'])
            logging.debug("------- ----------saled_area:%s"%xiaoqu_msg['saled_area'])

            yield scrapy.Request(xiaoqu_url,meta = xiaoqu_msg,callback=self.open_house_url)
        else:
            logging.warning('++++++++++ +++++++++not start_house_request!')

    def open_house_url(self,response):
        logging.debug('------- ----------response:%s'%response.url)
        try:
            floor_list = response.xpath('//*[@id="roomTable"]/tr')
            for elem in floor_list[1:]:
                logging.debug("elem --- --- ---%s"%elem)
                if elem:
                    house_line_list = elem.xpath('td[2]/table/tr')
                    for house_list in house_line_list:
                        house_list_tmp = house_list.xpath('td')
                        if not house_list_tmp:
                            logging.warning('------- ----------response house contend is empty: %s'%response.url)
                        else:
                            for house_elem in house_list_tmp:
                                relative_url_list = house_elem.xpath('a/@href').extract()
                                for tmp in relative_url_list:
                                    relative_url = tmp
                                    if relative_url:
                                        house_url = response.urljoin(relative_url)
                                        logging.debug('--------- --------relative_url: %s'%relative_url)
                                        yield scrapy.Request(house_url, meta=response.meta, callback=self.get_house_msg)
                                    else :
                                        logging.warning('--------- --------relative_url get error! host url is: %s'%response.url)
                else:
                    logging.warning("++++++++++++++++++ elem  get error")
        except:
            logging.error('############ ######   open url error%s'%response.url)

    def get_house_msg(self,response):
        # build_area = scrapy.Field()
        # build_in_area = scrapy.Field()
        # price = scrapy.Field()
        logging.debug('--------- --------house_url: %s'%response.url)
        items = DongGuanItem()
        items['project_addr'] = response.meta['project_addr']
        logging.debug('--------- --------project_addr: %s' % items['project_addr'])
        items['project_name'] = response.meta['project_name']
        logging.debug('--------- --------project_name: %s' % items['project_addr'])
        items['saled_area'] = response.meta['saled_area']
        logging.debug('--------- --------saled_area: %s' % items['project_addr'])

        tmp = response.xpath('//*[@class="content"]/table/tr[2]/td[4]/text()').extract_first()
        if tmp:
            items['build_area'] = tmp.split()[0]
            logging.debug('--------- --------%s'%items['build_area'])
        else:
            logging.debug('++++++ ++++++get_house_msg() build_area get fail: %s'%response.url)

        tmp = response.xpath('//*[@class="content"]/table/tr[3]/td[4]/text()').extract_first()
        if tmp:
            items['build_in_area'] = tmp.split()[0]
            logging.debug('--------- --------%s' % items['build_in_area'])
        else:
            logging.debug('++++++ ++++++get_house_msg() build_in_area get fail: %s' % response.url)

        tmp = response.xpath('//*[@class="content"]/table/tr[6]/td[4]/text()').extract_first()
        if tmp:
            items['price'] = tmp.split()[0]
            logging.debug('--------- --------%s' % items['price'])
        else:
            logging.debug('++++++ ++++++get_house_msg() price get fail: %s' % response.url)

        tmp = response.xpath('//*[@class="content"]/table/tr[1]/td[2]/text()').extract_first()
        if tmp:
            items['house_marking'] = tmp.split()[0]
            logging.debug('--------- --------%s' % items['price'])
        else:
            logging.debug('++++++ ++++++get_house_msg() house_marking get fail: %s' % response.url)

        tmp = response.xpath('//*[@class="content"]/table/tr[1]/td[4]/text()').extract_first()
        if tmp:
            items['floor'] = tmp.split()[0]
            logging.debug('--------- --------%s' % items['price'])
        else:
            logging.debug('++++++ ++++++get_house_msg() floor get fail: %s' % response.url)

        tmp = response.xpath('//*[@class="content"]/table/tr[2]/td[2]/text()').extract_first()
        if tmp:
            items['use_for'] = tmp.split()[0]
            logging.debug('--------- --------%s' % items['price'])
        else:
            logging.debug('++++++ ++++++get_house_msg() use_for get fail: %s' % response.url)

        tmp = response.xpath('//*[@class="content"]/table/tr[3]/td[2]/text()').extract_first()
        if tmp:
            items['sale_status'] = tmp.split()[0]
            logging.debug('--------- --------%s' % items['sale_status'])
        else:
            logging.debug('++++++ ++++++get_house_msg() sale_status get fail: %s' % response.url)

        tmp = response.xpath('//*[@class="content"]/table/tr[4]/td[4]/text()').extract_first()
        if tmp:
            items['AVG_area'] = tmp.split()[0]
            logging.debug('--------- --------%s' % items['AVG_area'])
        else:
            logging.debug('++++++ ++++++get_house_msg() AVG_area get fail: %s' % response.url)


        tmp = response.xpath('//*[@class="content"]/table/tr[5]/td[2]/text()').extract_first()
        if tmp:
            items['back_cast_status'] = tmp.split()[0]
            logging.debug('--------- --------%s' % items['back_cast_status'])
        else:
            logging.debug('++++++ ++++++get_house_msg() back_cast_status get fail: %s' % response.url)

        tmp = response.xpath('//*[@class="content"]/table/tr[5]/td[4]/text()').extract_first()
        if tmp:
            items['total_price'] = tmp.split()[0]
            logging.debug('--------- --------%s' % items['total_price'])
        else:
            logging.debug('++++++ ++++++get_house_msg() total_price get fail: %s' % response.url)

        tmp = response.xpath('//*[@class="content"]/table/tr[6]/td[2]/text()').extract_first()
        if tmp:
            items['close_status'] = tmp.split()[0]
            logging.debug('--------- --------%s' % items['close_status'])
        else:
            logging.debug('++++++ ++++++get_house_msg() close_status get fail: %s' % response.url)
        for i in items.keys():
            print i,'--- --- ================= -----',items[i],'----------------'

        items['house_url'] = response.url
        items['city'] = u'东莞'
        items['province']= u'广东'
        items['crawl_time'] = time.ctime()
        items['building_name'] = 'na'
        yield items
