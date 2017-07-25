#! /usr/bin/env python
# coding=utf-8

import json
import hashlib
import utils
import datetime
import os
from mysql_connect.mysql_connect import MySQLConn
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def transformd5(data):
    """
    进行简单的字符串转换为MD5编码，确保得到的数据的唯一性，避免重复
    :param data:
    :return:
    """
    if data:
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()
    else:
        return ' '


file_names = os.listdir('./out_put')
for file_name in file_names:
    if file_name.startswith('.'):
        pass
    print file_name
    f = file('./out_put/'+file_name)
    print file_name
    for line in f.xreadlines():
        dict_line = {}
        print line
        try:
            dict_line = json.loads(line)
        except Exception as e:
            print e

        project_name = dict_line.get('project_name', '')
        project_address = dict_line.get('project_address', '')
        develop_company = dict_line.get('develop_company', '')
        use_area = dict_line.get('use_area', '')
        use_area = utils.pro_float(use_area)

        building_area = dict_line.get('building_area', '')
        building_area = utils.pro_float(building_area)

        plan_area = dict_line.get('plan_area', '')
        plan_area = utils.pro_float(plan_area)

        url = dict_line.get('url', '')
        disposal_date = dict_line.get('disposal_date', '')
        city = dict_line.get('city', '')
        property_company = dict_line.get('property_company', '')
        district = dict_line.get('district', '')
        province = dict_line.get('province', '')
        crawl_time = dict_line.get('crawl_time', '')
        house_type = dict_line.get('house_type', '')
        use_for = dict_line.get('use_for', '')
        loupan_type = dict_line.get('loupan_type', '')
        property_fee = dict_line.get('property_fee', '')
        green_rate = dict_line.get('green_rate', '')
        volume_rate = dict_line.get('volume_rate', '')
        decorate_status = dict_line.get('decorate_status', '')
        agent_company = dict_line.get('agent_company', '')

        building_num = dict_line.get('building_num', '')
        house_num = dict_line.get('house_num', '')
        saled_House_num = dict_line.get('saled_House_num', '')
        unsaledHouse_num = dict_line.get('unsaledHouse_num', '')
        deal_num = dict_line.get('deal_num', '')

        unsaled_area = dict_line.get('unsaled_area', '')
        unsaled_area = utils.pro_float(unsaled_area)

        property_type = dict_line.get('property_type', '')
        deal_area = dict_line.get('deal_area', '')
        deal_area = utils.pro_float(deal_area)

        can_sale_total_area = dict_line.get('can_sale_total_area', '')
        can_sale_total_area = utils.pro_float(can_sale_total_area)

        avg_price = dict_line.get('avg_price', '')
        avg_price = utils.pro_digital(avg_price)
        uniq_id = transformd5(city+project_name)
        items = {
            'project_name': project_name, 'project_address': project_address,
            'develop_company': develop_company, 'use_area': use_area, 'building_area': building_area, 'plan_area': plan_area,
            'url': url, 'disposal_date': disposal_date, 'city': city, 'district': district, 'province': province,
            'crawl_time': datetime.datetime.now().strftime('%Y-%m-%d'),
            'house_type': house_type, 'use_for': use_for, 'loupan_type': loupan_type, 'property_fee': property_fee, 'green_rate': green_rate,
            'volume_rate': volume_rate, 'decorate_status': decorate_status, 'agent_company': agent_company, 'building_num': building_num,
            'house_num': house_num, 'saled_House_num': saled_House_num, 'unsaledHouse_num': unsaledHouse_num, 'deal_num': deal_num,
            'unsaled_area': unsaled_area, 'deal_area': deal_area, 'can_sale_total_area': can_sale_total_area, 'property_type': property_type,
            'property_company': property_company, 'uniq_id': uniq_id, 'avg_price': avg_price
        }
        stable_keys = ['project_name', 'project_address', 'develop_company', 'use_area', 'building_area', 'plan_area', 'url',
                'disposal_date', 'city', 'province', 'district', 'house_type', 'loupan_type', 'use_for',
                'property_fee', 'green_rate', 'volume_rate', 'decorate_status', 'property_type', 'property_company',
                'agent_company', 'building_num', 'uniq_id', 'avg_price'
                ]
        unstable_keys = ['house_num', 'saled_House_num', 'unsaledHouse_num', 'deal_num', 'can_sale_total_area',
                         'xq_id', 'unsaled_area', 'deal_area', 'crawl_time']

        select_sql = """
        select count(id) from new_house_xq WHERE uniq_id = '%s'
        """ % uniq_id
        sql_conn = MySQLConn()
        counts = sql_conn.select_data(select_sql)
        if counts[0][0] != 0:
            unstable_str = '`, `'.join(unstable_keys)
            unstable_vals = []
            for i in unstable_keys:
                if i == 'xq_id':
                    i = 'uniq_id'
                unstable_vals.append(items[i])
            unstable_val_str = '", "'.join(unstable_vals)
            sql = """
                insert into new_house_xq_unstable (`%s`) VALUES ("%s")
                """ % (unstable_str, unstable_val_str)
            print sql
            sql_conn = MySQLConn()
            sql_conn.inser_data(sql)
        else:
            keys_str = '`, `'.join(stable_keys)
            vals = []
            for i in stable_keys:
                vals.append(items[i])
            val_str = '", "'.join(vals)
            sql = """
            insert into new_house_xq (`%s`) VALUES ("%s")
            """ % (keys_str, val_str)
            print sql
            sql_conn = MySQLConn()
            flag = sql_conn.inser_data(sql)
            if flag:
                unstable_str = '`, `'.join(unstable_keys)
                unstable_vals = []
                for i in unstable_keys:
                    if i == 'xq_id':
                        i = 'uniq_id'
                    unstable_vals.append(items[i])
                unstable_val_str = '", "'.join(unstable_vals)
                sql = """
                    insert into new_house_xq_unstable (`%s`) VALUES ("%s")
                    """ % (unstable_str, unstable_val_str)
                print sql
                sql_conn = MySQLConn()
                sql_conn.inser_data(sql)

"""
`house_num` VARCHAR(30) COMMENT '房屋套数',
`saled_House_num` VARCHAR(30) COMMENT '已售房屋套数',
`unsaledHouse_num` VARCHAR(30) COMMENT '未售房屋套数',
`deal_num` VARCHAR(30) COMMENT '成交套数',
`can_sale_total_area` VARCHAR(30) COMMENT '可售总面积',
`unsaled_area` VARCHAR(30) COMMENT '未销售面积',
`deal_area` VARCHAR(30) COMMENT '成交面积'

`loupan_type` VARCHAR(100) COMMENT '楼盘类型',
`use_for` VARCHAR(100) COMMENT '用途',
`property_fee` VARCHAR(50) COMMENT '物业费',
`green_rate` VARCHAR(30) COMMENT '绿化率',
`volume_rate` VARCHAR(30) COMMENT '容积率',
`decorate_status` VARCHAR(30) COMMENT '装修状态',
`property_type` VARCHAR(30) COMMENT '物业类型',
`property_company` VARCHAR(30) COMMENT '物业公司',
`agent_company` VARCHAR(30) COMMENT '代理公司',
`building_num` VARCHAR(30) COMMENT '楼幢数'
`id` MEDIUMINT KEY AUTO_INCREMENT COMMENT '自增id',
`uniq_id` varchar(32) NOT NULL COMMENT '新房小区唯一ID--省市小区名称',
`project_name` varchar(50) NOT NULL COMMENT '小区名称 ',
`project_address` varchar(100) COMMENT '小区所在地址',
`develop_company` VARCHAR(30) COMMENT '开发商',
`use_area` decimal(10,2)  COMMENT '小区占地面积',
`building_area` decimal(10,2) COMMENT '建筑面积',
`plan_area` decimal(10,2) COMMENT '规划面积',
`url` VARCHAR(100) COMMENT '链接地址',
`disposal_date` VARCHAR(30) COMMENT '批售日期',
`city` VARCHAR(30) COMMENT '城市',
`province` VARCHAR(30) COMMENT '省份',
`district` VARCHAR(30) COMMENT '行政区',
`crawl_time` VARCHAR(30) COMMENT '抓取时间',
`house_type` VARCHAR(100) COMMENT '房屋类型',
"""