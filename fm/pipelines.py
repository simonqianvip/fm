# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import logging
from scrapy import signals
from twisted.enterprise import adbapi
from datetime import datetime
import MySQLdb
import MySQLdb.cursors

logger = logging.getLogger(__name__)


class FmPipeline(object):
    def __init__(self):
        try:
            self.file = codecs.open('C:\Users\simon\Desktop\\fm086.json', 'wb', encoding='utf-8')
        except IOError, msg:
            print(msg)
            raise

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode("unicode_escape"))
        # self.file.close()
        return item


class MySQLStoreFmPipeline(object):
    """
    数据存储到mysql
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''
        从settings文件加载属性
        :param settings:
        :return:
        '''
        dbargs = dict(
                host=settings['MYSQL_HOST'],
                db=settings['MYSQL_DBNAME'],
                user=settings['MYSQL_USER'],
                passwd=settings['MYSQL_PASSWD'],
                charset='utf8',
                cursorclass=MySQLdb.cursors.DictCursor,
                use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    # pipeline默认调用
    def process_item(self, item, spider):
        deferred = self.dbpool.runInteraction(self._do_upinsert, item, spider)
        deferred.addErrback(self._handle_error)
        # d.addBoth(lambda _: item)
        return deferred

    # 将每行更新或写入数据库中
    """
    id            char(32)  utf8_general_ci  NO      PRI     (NULL)           select,insert,update,references  主键
    url           text      utf8_general_ci  YES             (NULL)           select,insert,update,references  url链接
    cr            text      utf8_general_ci  YES             (NULL)           select,insert,update,references  法人
    reg_no        text      utf8_general_ci  YES             (NULL)           select,insert,update,references  公司注册号
    company_name  text      utf8_general_ci  YES             (NULL)           select,insert,update,references  公司名称
    money         text      utf8_general_ci  YES             (NULL)           select,insert,update,references  注册资金
    sale          text      utf8_general_ci  YES             (NULL)           select,insert,update,references  年营业额
    """

    def _do_upinsert(self, conn, item, spider):

        if item['url']:
            url = item['url'][0]
        else:
            url = '不详'

        if item['cr']:
            cr = item['cr'][0]
        else:
            cr = '不详'

        if item['reg_no']:
            reg_no = item['reg_no'][0]
        else:
            reg_no = '不详'

        if item['company_name']:
            company_name = item['company_name'][0]
        else:
            company_name = '不详'

        if item['money']:
            money = item['money'][0]
        else:
            money = '不详'

        if item['sale']:
            sale = item['sale'][0]
        else:
            sale = '不详'

        print(url + "," +cr+","+reg_no+","+company_name+","+money+","+sale)

        conn.execute("""
                insert into fm(url, cr, reg_no, company_name, money,sale)
                values(%s, %s, %s, %s, %s, %s)
        """, (url, cr, reg_no, company_name, money, sale))

        # print """
        #         insert into fm(url, cr, reg_no, company_name, money,sale)
        #         values(%s, %s, %s, %s, %s, %s)
        # """, (url.decode("unicode_escape"), cr.decode("unicode_escape"), reg_no.decode("unicode_escape"), company_name.decode("unicode_escape"), money.decode("unicode_escape"), sale.decode("unicode_escape"))

    def _handle_error(self, failue):
        logger.error(failue)

        # linkmd5id = self._get_linkmd5id(item)
        # print linkmd5id
        # now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        # conn.execute("""
        #         select 1 from fm where id = %s
        # """, (linkmd5id, ))
        # ret = conn.fetchone()

        # if ret:
        #     conn.execute("""
        #         update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
        #     """, (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id))
        # print """
        #    update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
        # """, (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id)
        # else:
        #     conn.execute("""
        #         insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated)
        #         values(%s, %s, %s, %s, %s, %s)
        #     """, (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now))
        # print """
        #    insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated)
        #    values(%s, %s, %s, %s, %s, %s)
        # """, (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now)
        # 获取url的md5编码
        # def _get_linkmd5id(self, item):
        #     #url进行md5处理，为避免重复采集设计
        #     return md5(item['link']).hexdigest()
        # 异常处理
