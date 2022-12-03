# 查询，包括站内查询、文档查询。短语查询、通配查询
import sqlite3
from elasticsearch import Elasticsearch

class searchtype:
    def __init__(self):
        # 初始化网址前缀、时间范围、查询方法、查询域、查询关键词、学院等。实际使用时这些变量由用户设置
        self.url = ''
        self.st_date = '2000-01-01'
        self.method = 'match'
        self.fields = ['title', 'text', 'mtext']
        self.query = ''
        self.college = ''
        self.from1 = 0
        self.size1 = 10

    # 根据网址前缀和时间范围进行过滤
    def filter_search(self):
        res = []
        if self.url:
            res.append({
                "prefix": {
                    "url": self.url
                }
            })
        if self.st_date:
            res.append({
                "range": {
                    "date": {
                        "gte": self.st_date
                    }
                }
            })
        return res

    # 在多个字段（域）上反复执行相同查询
    def multi_search(self):
        multi_fields = [f"{field}^10" for field in self.fields]
        # 默认使用best_fields最佳字段查询
        return [{
            "multi_match": {
                "query": self.query,
                "fields": multi_fields,
                # tie_breaker：除了最佳匹配语句之外，一定程度上考虑其他语句的评分
                "tie_breaker": 0.3,
                # minimum_should_match：精度控制，必须有25%以上的词项匹配才能说明文档是相关的
                "minimum_should_match": "25%",
            }
        }]

    # 为页面赋予权重
    def pgrank_search(self):
        return [{
            "rank_feature": {
                "field": "pgrank_score",
                # boost表示相当于权重，非线性
                "boost": 10,
                "log": {
                    "scaling_factor": 10
                },
            }
        }]

    # 短语查询
    def phrase_search(self):
        res = []
        for field in self.fields:
            res.append({
                # match_phrase，要求词项的位置关系必须固定
                "match_phrase": {
                    field: {
                        "query": self.query,
                        "boost": 10,
                    }
                }
            })
        return res

    # 通配查询
    def wildcard_search(self):
        res = []
        for field in self.fields:
            res.append(
                {
                    # 要求至少有一个符合条件
                    "wildcard": {
                        field: {
                            "value": self.query,
                            "boost": 10,
                        }
                    },
                })
        return res

    # 个性化查询，返回偏向本学院的信息
    def indiv_search(self):
        res = []
        for field in self.fields:
            res.append({
                "match":
                {
                    field: {
                        "query": self.college,
                        "boost": 2,
                    }
                },
            })
        return res

    # 统筹管理所有的查询方式，根据method选择一种方式进行查询
    def search_ma(self):
        sea = {
            "bool": {
                "must": [],
                "should": [],
                'filter': [],
            }
        }
        sea['bool']['filter']+=self.filter_search()
        if self.method == "match":
            sea['bool']['must'] +=self.multi_search()
        if self.method == "phrase":
            sea['bool']['should'] += self.phrase_search()
        if self.method == "wildcard":
            sea['bool']['should'] += self.wildcard_search()
        if self.college:
            sea['bool']['should'] += self.indiv_search()
        sea['bool']['must']+= self.pgrank_search()

        return sea

# 搜索结果高亮
class hlsearch:
    def __init__(self):
        self.es = Elasticsearch()
        # 索引名和数据库与index.py中保持一致
        self.idname = "pageinfoindex"
        self.conn = sqlite3.connect("nkuinfo\\nkuinfo\\spiders\\mysql.sqlite")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    # 执行高亮功能
    def highlight(self, sea:searchtype):
        hlbody = {
            "boundary_scanner_locale": "zh_CN",
            # 前后都添加strong的tag
            "pre_tags": ["<strong>"],
            "post_tags": ["</strong>"],
            "fields": {
                "title": {
                    "fragment_size": 20,
                    "no_match_size": 20,
                },
                "text": {
                    "fragment_size": 50,
                    "no_match_size": 50,
                },
                "mtext": {
                    "fragment_size": 20,
                    "no_match_size": 20,
                }
            },
        }

        res = self.es.search(
            index=self.idname,
            query=sea.search_ma(),
            highlight=hlbody,
            from_=sea.from1,
            size=sea.size1,
        )

        return {
            "pages": [{
                "url": restext['_source']['url'],
                "date": restext['_source']['date'],
                "title": restext['highlight']['title'],
                "text": restext['highlight']['text'],
                "mtext": restext['highlight']['mtext'] if 'mtext' in restext['highlight'] else '',
                "rawtitle": restext['_source']['title'],
                "rawmtext": restext['_source']['mtexts'],
            }for restext in res['hits']['hits']],
        }





