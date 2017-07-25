# -*- coding: utf-8 -*-
import scrapy
import logging
import time

from newHouse.items import BjNewhouseItem


g_dict = {}
g_dict[u'项目名称'] = "project_name"
g_dict[u'坐落位置'] = "project_addr"
g_dict[u'发证日期'] = "publish_date"
g_dict[u'房屋所有权人名称'] = "house_owner_name"
g_dict[u'房屋所有权证号'] = "house_owner_number"
g_dict[u'转移登记办理部门'] = "publish_place"
g_dict[u'土地使用权证号'] = "land_use_number"
g_dict[u'规划设计用途'] = "use_for"
g_dict[u'户　　型'] = "build_type"
g_dict[u'建筑面积'] = "build_area"
g_dict[u'套内面积'] = "build_in_area"
g_dict[u'按建筑面积拟售单价'] = "sale_for_build"
g_dict[u'按套内面积拟售单价'] = "sale_for_build_in"


class BeiJingSpider(scrapy.Spider):
    name = 'Beijing_data'
    start_urls = (
    'http://www.bjjs.gov.cn/eportal/ui?pageId=308452&ddlQX=-1&ddlQW=-1&isTure=ture&rblFWType1=x&currentPage=' + str(i)
    for i in range(1, 230))


    def parse(self, response):
        tmp = response.xpath('//*[@id="FDCJYFORM"]/table[2]/tr[2]/td/table/tr')
        for i in tmp:
            # 获得每个小区详情的URL
            tmp1 = i.xpath('td[2]/a/@href').extract_first()
            if tmp1 and len(tmp1):
                print '---', tmp1
                detail_url = response.urljoin(tmp1)
                # 打开小区的详情页，解析出小区的详情
                yield scrapy.Request(detail_url, callback=self.parse_XiaoQu_detail)

    def parse_XiaoQu_detail(self, response):
        # 获取小区详情
        xiaoqu_meta = {}
        tmp = response.xpath("//*[@id='XMmanage']/table[2]/tr/td[2]")
        id_list = tmp.xpath('@id').extract()
        span_contend = tmp.xpath('span/text()').extract()
        for i in range(len(tmp)-1):
            a = g_dict[id_list[i]]
            xiaoqu_meta[a] = span_contend[i]

        # 获得楼盘表里，查看信息的URl
        louhao_list = response.xpath('//*[@id="table_floorTray"]/tr')
        for lou_detail in louhao_list[2:]:
            lou_detail_list = lou_detail.xpath('td')
            xiaoqu_meta['building_name'] = lou_detail_list[0].xpath('text()').extract_first()
            lou_detail_msg_url = response.urljoin(lou_detail_list[-1].xpath('a/@href').extract_first())
            if lou_detail_msg_url:
                logging.debug("xiaoqu response.url: %s", response.url)
                logging.debug("loufnag lou_detail_msg_url: %s", lou_detail_msg_url)
                yield scrapy.Request(lou_detail_msg_url,
                                     meta=xiaoqu_meta,
                                     callback=self.make_house_url)

    def make_house_url(self, response):
        tmp = response.xpath('//*[@id="table_Buileing"]/tbody/tr')
        for elem in tmp[1:]:
            for sub_elem in elem.xpath('td')[-1].xpath('div'):
                # 获得房屋的url
                house_url = sub_elem.xpath('a/@href').extract_first()
                if house_url != u'#':
                    target_house_url = response.urljoin(house_url)
                    # 采集房屋信息
                    yield scrapy.Request(target_house_url,
                                         meta=response.meta,
                                         callback=self.get_house_detail)

    def get_house_detail(self, response):
        HouseItem = BjNewhouseItem()
        list_tmp = response.xpath('//*[@id="showDiv"]/table/tr')
        try:
            print '-----------------------------\n',len(response.meta),'\n-------------------------\nresponse.meta:\n'
            for elem in dict(response.meta).keys():
                print elem, ' | :', response.meta[elem]
            print '------------------------\n'
            meta_dict = dict(response.meta)
            HouseItem['house_url'] = response.url
            HouseItem['project_name'] = meta_dict.get('project_name')
            HouseItem['project_addr'] = meta_dict.get('project_addr')
            HouseItem['publish_date'] = meta_dict.get('publish_date')
            HouseItem['building_name'] = meta_dict.get('building_name')
            HouseItem["house_owner_name"] = meta_dict.get('house_owner_name')
            HouseItem["house_owner_number"] = meta_dict.get('house_owner_number')
            HouseItem["publish_place"] = meta_dict.get('publish_place')
            HouseItem["land_use_number"] = meta_dict.get('land_use_number')
            for elem in list_tmp[1:]:
                colum_name = g_dict.get(elem.xpath("td[1]/text()").extract_first())
                if colum_name:
                    HouseItem[colum_name] = elem.xpath("td[2]/text()").extract_first().split(' ')[0]
            HouseItem['city'] = u'北京'
            HouseItem['province'] = u'北京'
            HouseItem['crawl_time'] = time.ctime()
            HouseItem['house_marking'] = response.xpath('//*[@style="text-align: center; width: 730px"]/span/text()').extract_first()
        except Exception as e:
            print e,'----------\n'
            logging.error('''get contend error''')
        finally:
            error_msg = ''
            for key in HouseItem.keys():
                error_msg += HouseItem[key]
            logging.debug('get houseItem msg: %s', error_msg)
            logging.debug('house_url:%s', response.url)
            yield HouseItem