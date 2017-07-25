# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import codecs
import json
import threading
lock = threading.Lock()
reload(sys)
sys.setdefaultencoding('utf-8')



def my_string_process(string):
    """
    对数据进行一个简单的处理，去除空字符
    :param string:
    :return:
    """
    if type(string) in [str, unicode]:
        return string.strip()
    else:
        return string


class NewhousePipeline(object):

    def open_result_file(self, file_name, item):
        """
        存储网页上面的内容，以json格式存储到文件中
        :param file_name:
        :param item:
        :return:
        """
        lock.acquire()
        f1 = codecs.open('./out_put/%s' % file_name, mode='a', encoding='utf-8')
        json_data = json.dumps(item, ensure_ascii=False)
        f1.write(json_data + '\r\n')
        f1.close()
        lock.release()

    def process_data(self, item):
        """
        对从网页上扒下来的数据进行初步判断是否满足要求，将空值设置为“na”
        :param item:
        :return:
        """
        for key in item:
            if not item[key] or item[key] == 'null':
                item[key] = 'na'
            else:
                processed_val = my_string_process(item[key])
                item[key] = processed_val
        return item

    def process_item(self, item, spider):
        item = dict(item)
        file_name = spider.name + '.json'
        item = self.process_data(item)
        self.open_result_file(file_name, item)
        return item
