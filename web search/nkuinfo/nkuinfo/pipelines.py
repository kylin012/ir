# 将爬取的数据存入数据库
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
import sqlite3
from bs4 import BeautifulSoup

class NkuinfoPipeline:
    # def process_item(self, item, spider):
    #     # print(item['links'][55].url)
    #     # print(BeautifulSoup(item['links'][55].text, 'lxml').get_text("\n", strip=True))
    #     print(item['url'])
    #     return item
    # 开始爬取数据，建立与数据库的连接
    def open_spider(self, spider):
        self.conn = sqlite3.connect("mysql.sqlite")
        self.cur =self.conn.cursor()

    # 结束爬取数据，提交数据并关闭与数据库的连接
    def close_spider(self, spider):
        self.conn.commit()
        self.cur.close()

    # 将爬取的数据放到数据库中
    def process_item(self, item, spider):
        # 总共三张表，第一张link表存储当前页面和该页面中的锚文本及其对应的页面——parent_id、leaf_id、mtext
        # 第二张rank表存储页面的url和其对应的分数，用于保存pagerank算法的结果——r_id、url、score
        # 第三张page表用于存储页面的标题、时间、文本、html代码等信息——p_id、p_title、p_time、p_text、p_restext
        sql_insert_link = "INSERT OR REPLACE INTO link (parent_id,leaf_id,mtext) SELECT ? ,r_id,? FROM rank WHERE url==?"
        sql_insert_rank = "INSERT OR IGNORE INTO rank(url) VALUES (?)"
        sql_insert_page = "INSERT OR REPLACE INTO page (p_id,p_title,p_time,p_text,p_restext) VALUES (?,?,?,?,?)"
        sql_select_rid = "SELECT r_id FROM rank WHERE url==?"
        # 通过sql语句实现对数据的插入和查找
        self.cur.execute(sql_insert_rank, (item['url'],))
        self.cur.execute(sql_select_rid, (item['url'],))
        # link表中会出现一个parent_id对多个leaf_id的情况
        parent_id = self.cur.fetchone()[0]
        # 如果不是首次插入，就更新数据
        pageinfo =(parent_id, item['title'], item['date'], item['text'], item['restext'],)
        self.cur.execute(sql_insert_page,pageinfo)
        linkinfos = []
        urls = []
        for link in item['links']:
            urls.append((link.url,))
            mtext = BeautifulSoup(link.text,'lxml').get_text(" ", strip=True)
            linkinfos.append((parent_id, mtext, link.url,))
        print('data save x1\n')
        self.cur.executemany(sql_insert_rank, urls)
        self.cur.executemany(sql_insert_link, linkinfos)

