# 使用pagerank算法进行链接分析
from igraph import *
import sqlite3

# 先对于数据库中link表内的父链接——子链接的关系建表，再调用igraph里的pagerank函数计算pagerank，存入数据库中rank表内
def pagerank(sqlpath):
    conn =sqlite3.connect(sqlpath)
    cur = conn.cursor()
    # 获取表中的链接关系
    cur.execute("SELECT DISTINCT parent_id,leaf_id FROM link")
    p2l_list =cur.fetchall()
    # 加入边，创建Graph对象，建立链表
    edges = []
    for parent_id,lead_id in p2l_list:
        edges.append((parent_id,lead_id))
    g = Graph.TupleList(edges, directed=False, vertex_name_attr='name')
    # 直接调用pagerank算法
    scores = g.pagerank()
    # 结果存入rank表中
    ranks = []
    r_id = 1
    for score in scores:
        ranks.append((score,r_id))
        r_id+=1
    cur.executemany("UPDATE rank SET score=? WHERE r_id==?", ranks)
    conn.commit()
    cur.close()

if __name__ == "__main__":
    pagerank("..\\nkuinfo\\nkuinfo\\spiders\\mysql.sqlite")