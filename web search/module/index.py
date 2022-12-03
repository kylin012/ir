# 构造索引
import sqlite3
from elasticsearch import Elasticsearch, helpers
from datetime import datetime

class getdata:
    def __init__(self, sqlpath):
        self.sqlpath = sqlpath
    # 从数据库中获取所需信息
    def __enter__(self):
        sql_get_data ="""
            SELECT url, p_time, p_title, p_text, score,
            (SELECT GROUP_CONCAT(DISTINCT mtext) FROM link WHERE leaf_id == r_id) as mtext,
            (SELECT GROUP_CONCAT(DISTINCT mtext) FROM link WHERE parent_id == r_id) as mtexts
            FROM rank INNER JOIN page ON r_id == p_id
        """
        self.conn = sqlite3.connect(self.sqlpath)
        self.cur = self.conn.execute(sql_get_data)
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
    # 每次获取100行数据
    def get100data(self):
        while 1:
            datas = self.cur.fetchmany(100)
            if not datas:
                break
            for url, p_time, p_title, p_text, score, mtext, mtexts in datas:
                yield{
                    "url": url,
                    "date": datetime.fromtimestamp(p_time).isoformat(),
                    "title": p_title,
                    "text": p_text,
                    "pgrank_score": score if score else 0.00001,
                    "mtext": mtext,
                    "mtexts": mtexts,
                }

if __name__ == '__main__':
    mymap ={
        "properties": {
            "url": {"type": "keyword", },
            "date": {"type": "date", "format": "strict_date_optional_time", },
            "title": {"type": "text", "analyzer": "ik_max_word", },
            "text": {"type": "text", "analyzer": "ik_smart", },
            "pgrank_score": {"type": "rank_feature", },
            "mtext": {"type": "text", "analyzer": "ik_max_word", },
            "mtexts": {"type": "text", "analyzer": "ik_max_word", },
        }
    }
    idname = "pageinfoindex"
    sqlpath = "..\\nkuinfo\\nkuinfo\\spiders\\mysql.sqlite"
    es = Elasticsearch()
    # 建立索引。如果已有索引，先删除再插入
    if es.indices.exists(index=idname):
        es.indices.delete(index=idname)
    es.indices.create(index=idname, mappings=mymap)
    print(es.search(index=idname))
    # 将数据放入索引中，使用helpers.bulk，一次放100行
    datas =[]
    with getdata(sqlpath) as g:
        for data in g.get100data():
            datas.append(data)
            if len(datas)>100:
                helpers.bulk(es, datas, index=idname)
                datas = []
            # 别忘了尾处理
        helpers.bulk(es, datas, index=idname)
