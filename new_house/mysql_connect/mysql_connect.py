#!/usr/bin/env python
# coding=utf-8

import MySQLdb
import time


class MySQLConn(object):

    def __init__(self):
        i = 1
        while True:
            try:
                self.db = MySQLdb.connect(
                    host='116.62.8.44',
                    user='cnfsdata1',
                    passwd='cnfsdata123',
                    db='cnfsdata',
                    charset='utf8',
                )
            except MySQLdb.Error as e:
                print ("The %s times connect to mysql~~" % i)
                i += 1
                time.sleep(60)
                continue
            break
        self.cursor = self.db.cursor()

    def inser_data(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.db.close()
        except Exception as e:
            print ("Some thing is wrong~: %s" % e)
            return False
        return True

    def select_data(self, sql):
        data = ''
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            self.db.close()
        except Exception as e:
            print e
            # logs.debug("select failed : %s" % e)
        return data

    def update_to_table(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.db.close()
        except Exception as e:
            print e
            # logs.debug('update failed : %s' % e)
            return False
        return True

    def delete_useless_url(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.db.close()
        except Exception as e:
            print e
            # logs.debug('delete failed : %s' % e)

#
# sql = """
#     delete from ip_t where ip="113.234.108.225"
# """
# mysql = MySQLConn()
# mysql.delete_useless_url(sql)
# # time.sleep(30)
# # print data


