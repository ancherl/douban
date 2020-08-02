# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# import pymysql as mysql
from pymongo import MongoClient

class DoubanPipeline:

    # 实例化mongodb client and database
    def open_spider(self, spider):
        self.mongo_client = MongoClient(host='localhost', port=27017)
        self.db = self.mongo_client.spider

    def process_item(self, item, spider):
        print(item)
        # 从传过来的item中获取数据
        # movie_id = item.get('id')
        # movie_name = item.get('movie_name')
        # image = item.get('image', 'N/A')
        # average = item.get('average')
        # director = item.get('director', 'N/A')
        # duration = item.get('duration')
        # publish_date = item.get('publish_date', 'N/A')
        # movie_type = item.get('type', 'N/A')

        self.db.douban_movies.insert(dict(item))

        # MySQL语句执行
        # sql_query = "insert into moivestop250_douban(id, title, image_url, average, director, duration, publish_date, type) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        # self.cur.execute(sql_query, (movie_id, movie_name, image, average, director, duration, publish_date, movie_type))
        # self.conn.commit()

    def close_spider(self, spider):
       #  关闭mongo_client 连接
       self.mongo_client.close()