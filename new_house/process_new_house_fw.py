# -*- coding: utf-8 -*-
import sys
import codecs
import json
import threading
import hashlib
import os
import re
import logging as logs
from mysql_connect.mysql_connect import MySQLConn
logs.basicConfig(level=logs.WARNING,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='new_house.log',
                filemode='w')


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

def build_sql(item):
    logs.debug(item)
    if not item.get('building_name'):
        item['building_name'] = 'na'
    # 枚举精确到房屋表里的所有字段以及数据类型
    type_dict = {"project_addr": "varchar(256)", "sale_for_build_in": "decimal(12,2)",
                 "total_floor": "decimal(12,2)",
                 "xq_total_area": "decimal(12,2)", "all_sale_area": "decimal(12,2)",
                 "completion_time": "varchar(32)",
                 "md5_mark": "varchar(32)", "approve_time": "varchar(32)", "house_num": "decimal(12,2)",
                 "building_name": "varchar(32)", "city": "varchar(32)", "house_orientation": "varchar(32)",
                 "start_time": "varchar(32)", "district": "varchar(32)", "floor": "decimal(12,2)",
                 "house_number": "decimal(12,2)", "sale_status": "varchar(32)", "unit_id": "varchar(64)",
                 "all_house_area": "decimal(12,2)", "structure": "varchar(32)", "opening_time": "varchar(32)",
                 "AVG_area": "decimal(12,2)", "saled_area": "decimal(12,2)", "sale_building_num": "varchar(64)",
                 "company": "varchar(128)", "use_for": "varchar(32)", "province": "varchar(32)",
                 "project_name": "varchar(128)", "price": "decimal(12,2)", "sale_house_num": "decimal(12,2)",
                 "build_in_area": "decimal(12,2)", "balcony_area": "decimal(12,2)", "house_marking": "varchar(32)",
                 "crawl_time": "varchar(32)", "address": "varchar(256)", "build_type": "varchar(32)",
                 "build_area": "decimal(12,2)", "house_url": "varchar(512)", "delivery_time": "varchar(32)",
                 "total_price": "decimal(12,2)", "total_num": "decimal(12,2)", "sale_for_build": "decimal(12,2)",
                 "publish_date": "varchar(32)", "end_time": "varchar(32)", "building_all_area": "decimal(12,2)"}
    print '''item.get("city"): %s,item.get('project_name'): %s,item.get('building_name'): %s, item.get('house_marking'): %s)''' % (
        item.get("city"), item.get('project_name'), 'building_name', item.get('house_marking'))
    # 生成md5_mark,确定房屋唯一标识
    try:
        city,project_name, building_name,house_marking= item.get("city"),item.get("project_name"),item.get("building_name"),item.get("house_marking")
        if not city:
              raise Exception('city is empty')
        if not project_name:
              raise Exception('project_name is empty')
        if not building_name:
              raise Exception('building_name is empty')
        if not house_marking:
              raise Exception('house_marking is empty')
        md5_mark = transformd5(city + project_name + building_name + house_marking)
    except  Exception as e:
        logs.error(e)
        logs.error('md5_mark build error')
        return -1
    # 查询该条信息是否存在
    sql_content = 'select count(*) from new_house_fw where md5_mark = \'%s\'' % (md5_mark)
    obj_mysql = MySQLConn()
    result = obj_mysql.select_data(sql_content)
    print sql_content, '--- --- -', result, '\n', type(result)
    if result[0][0] > 0:
        logs.debug('这条数据已经存在')
        logs.debug(sql_content)
        return -1
    # build sql
    exist_colume_list = item.keys()
    sql_contend = "insert into new_house_fw  ("
    for elem in exist_colume_list:
        if elem in type_dict:
            sql_contend += elem + ','
    sql_contend += 'md5_mark,'
    sql_contend = sql_contend[:-1] + ') values ('
    for elem in exist_colume_list:
        elem_type = type_dict.get(elem) if elem in type_dict else False
        if elem_type and elem_type.find('varchar') == -1:
            if item.get(elem) == 'na':
                sql_contend += '0.0,'
            else:
                if elem == 'AVG_area':
                    print '----------------', elem, item.get(elem) + ','
                value = re.findall('\d+\.?\d+|\d+', item.get(elem))
                if value and len(value) > 0:
                    sql_contend += value[0] + ','
        elif elem_type and elem_type.find('varchar') != -1:
            sql_contend += '\'' + item.get(elem) + '\','
    sql_contend += "\'" + md5_mark + '\')'
    return sql_contend



def run_file(div,target_file):
  target_file = os.path.join(div,target_file)
  print target_file
  if not os.path.exists(target_file):
      return 
  with open(target_file)as fd:
      for line in fd:
          try:
              item = eval(line)
              sql_contend = build_sql(item)
              if -1 != sql_contend:
                  obj_mysql = MySQLConn()
                  obj_mysql.inser_data(sql_contend)
          except Exception as e:
              logs.error(e)
              logs.warn(line)
      fd.close()



m_path = 'out_put'
fw_list = ['Beijing_data', 'DongGuan_data', 'FuzhouSpider','HefeiSpider', 'HuzhouSpider', 'ShanghaiSpider', 'ShenyangSpider', 'nanchang_new_house','qingdao_new_house', 'suzhou_new_house', 'xiamen_new_house']
for root,divs,files in os.walk(m_path):
    for file_elem in files:
        if file_elem[:file_elem.find('.')] in fw_list:
            t = threading.Thread(target=run_file,args=(m_path,file_elem))
            t.start()

