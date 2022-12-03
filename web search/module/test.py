from bs4 import BeautifulSoup
import requests
# url = "https://www.baidu.com"
# r1 = requests.get(url,'lxml')
# r1.encoding='utf-8'
# bs_1=BeautifulSoup(r1.text,'lxml').get_text(separator="\n",strip=True)
# print(bs_1)
#
# from tqdm import tqdm
# for i in tqdm(range(10000000)):
#     i

# import sys
# sys.path.append("E:\\1教材\\2022大三上\\信息检索导论\\作业\\hw5\\web search")
# import os
# os.remove("..\\nkuinfo\\nkuinfo\\1.txt")

# from igraph import Graph as IGraph
# edges = [('1', '2'), ('1', '3'), ('2', '3'), ('3', '7'), ('4', '5'), ('4', '6'), ('5', '6'),
# ('6', '7'), ('7', '8'), ('8', '9'), ('9', '10'), ('9', '11'),
# ('10', '11'), ('8', '12'), ('12', '13'), ('12', '14'), ('13', '14')]
# g = IGraph.TupleList(edges, directed=False, vertex_name_attr='name') #加入边，创建IGraph对象。
#
# pg = g.pagerank() #直接调用g里面的pagerank算法
# print(pg)
# print(len(edges))
# print(len(pg))

# from elasticsearch import Elasticsearch,helpers
# import jieba
# import time
# from datetime import datetime
# ts=time.time()
# mappings = {
#         "properties": {
#             "url": {"type": "text",},
#             "date": {"type": "date", "format": "strict_date_optional_time",},
#             "title":{"type": "text","analyzer": "ik_max_word",},
#             "text":{"type": "text","analyzer":"ik_smart",},
#             "pagerank":{"type": "text",},
#             "anchor":{"type": "text","analyzer": "ik_max_word",},
#         }
#     }
#
# # Create the client instance
# es = Elasticsearch([{"host":"localhost","port":9200}])
# # result = es.indices.create(index="ne",mappings=mappings)
# batch = []
# batch.append({"_index":"ne",
#               "_source":{
#                     "url": "1",
#                     "date": datetime.fromtimestamp(ts).isoformat(),
#                     "title":"000",
#                     "text":"abc",
#                     "pagerank": "11",
#                     "anchor":"no no",
#               }
#                 })
# dsl = {
#     'query': {
#         'match': {
#             'title': '000'
#         }
#     }
# }
# es.indices.delete(index="ne")
# es.indices.create(index="ne",mappings=mappings)
# helpers.bulk(es,batch)
# from elasticsearch import Elasticsearch
# es = Elasticsearch([{"host":"localhost","port":9200}])
# es.indices.create(index="pageinfoindex")
# res =es.search(index="pageinfoindex")
# print(res)

# def fetchOnlyOnce(self):
#         for i in range:
#             yield {
#                 "url": 1,
#                 "date": datetime.fromtimestamp(ts).isoformat(),
#                 "title": title,
#                 "text": text,
#                 "pagerank": score if score else 0.0000001,
#                 "anchor": anchor,
#             }
# WEIGHT = {
#         'title': 10,
#         'text': 10,
#         'anchor': 10,
#         'pagerank': 10,
#     }
# fields = ['title', 'text', 'anchor']
# wfields = [f"{field}^{WEIGHT[field]}" for field in fields]
#
# print(wfields)
# users={"计算机":{"password":"jsj","xueyuan":"计算机"}}
# history={"计算机":[]}
# with open('1.txt', 'w') as f:
#     f.write(users)
# with open('1.txt', 'w') as f:
#     f.write(history)
# users={"计算机":{"password":"jsj","xueyuan":"计算机"},'':{"111":"111"}}
# if '' in users:
#     print(1)
# else:
#     print(0)

# hist = {"计算机":[]}
# hist['计算机'].insert(0,{"password":1,"query":"2"})
# hist['计算机'].insert(0,{"password":3,"query":"4"})
# hist['计算机'].insert(0,{"password":5,"query":"6"})
# for h in hist['计算机'][:2]:
#     h = h['password']
#     print(h)
# re = ",首页,关于我们,工作动态,涉外会议,出国出境,海外学习,外国专家,外专发布,新闻,通知,预告,聘请指南,专爱南开,外专风采,剪影留声,一"
#
# print(re.split(',')[1])
a= 1
for i in a:

