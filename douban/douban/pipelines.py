"""
    钩子函数(方法) -->回调函数(方法) -->callback
    数据批处理：将数据放到容器里。数据量达到多少提交一次。最后关爬虫判断是否有数据，有则再提交
"""
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import openpyxl
import pymysql


class PymysqlPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',
                                    user='root',
                                    password='123456',
                                    database='douban',
                                    charset='utf8mb4',
                                    port=3306)  # 连接数据库
        self.cursor = self.conn.cursor()  # 创建游标
        self.data = []

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        if len(self.data) > 0:
            self._write()
        self.conn.close()

    def process_item(self, item, spider):
        title = item.get('title') or '没有电影标题数据'
        time = item.get('time') or 0  # 没有数据则执行后面
        comments = item.get('comments') or '没有影片评语数据'
        self.data.append((title, time, comments))
        # 判断是否有该数据表，没有则创建
        self.cursor.execute("show tables like 'douban_top250_one'")
        table = self.cursor.fetchone()
        if table is None:
            print('没有该数据表，正在创建.........')
            sql = '''
                        CREATE TABLE douban_top250_one (
                        id INT(10) NOT NULL AUTO_INCREMENT  ,
                        title VARCHAR(40) NOT NULL,
                        times INT(8) NOT NULL,
                        comments VARCHAR(100) NOT NULL,
                        PRIMARY KEY (id)
                        )
                        '''
            self.cursor.execute(sql)
            print('成功创建数据表')
        try:
            if len(self.data) == 100:
                self._write()
                self.data.clear()
        except Exception as e:
            print('第一个数据表报错:', e)
        return item

    def _write(self):
        self.cursor.executemany(
            'insert into douban_top250_one(title,times,comments) values (%s,%s,%s)',
            self.data
        )
        self.conn.commit()


class Pymysql_Two_Pipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',
                                    user='root',
                                    password='123456',
                                    database='douban',
                                    charset='utf8mb4',
                                    port=3306)  # 连接数据库
        self.cursor = self.conn.cursor()  # 创建游标
        self.datas = []
        print(self.datas)

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):

        self.conn.close()

    def process_item(self, item, spider):
        two_title = item.get('two_title') or '没有电影标题数据'
        two_introduce = item.get('two_introduce') or '没有电影介绍'

        # 判断是否有该数据表，没有则创建
        self.cursor.execute("show tables like 'douban_top250_two'")
        table = self.cursor.fetchone()
        if table is None:
            print('没有该数据表，正在创建.........')
            sql = '''
                        CREATE TABLE douban_top250_two (
                        id INT(10) NOT NULL AUTO_INCREMENT  ,
                        two_title VARCHAR(40) NOT NULL,
                        two_introduce TEXT NOT NULL,
                        PRIMARY KEY (id)
                        )
                        '''
            self.cursor.execute(sql)
            print('成功创建数据表')
        try:
            self.cursor.execute(
                'insert into douban_top250_two(two_title,two_introduce) values (%s,%s)',
                (two_title,two_introduce)
            )
            self.conn.commit()
        except Exception as e:
            print('第二个数据表报错:', e)
        return item





class ExcelPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()  # 创建工作簿
        self.ws = self.wb.active  # 获取当前工作簿中的工作表
        self.ws.title = 'Top250'  # 工作表名字
        self.ws.append(('电影标题', '发布时间', '电影评语', '二级页面标题', '二级页面电影介绍'))  # 表头

    def close_spider(self, spider):
        """爬虫关闭时自动执行"""
        self.wb.save('豆瓣Top250.xlsx')

    def process_item(self, item, spider):  # 每次都会调用，250条数据就执行250次。
        title = item.get('title') or '没有电影标题数据'
        time = item.get('time') or '没有发布时间数据'  # 没有数据则执行后面
        comments = item.get('comments') or '没有影片评语数据'
        two_title = item.get('two_title') or '没有标题数据'
        two_introduce = item.get('two_introduce') or '没有电影介绍'
        self.ws.append((time,title , comments, two_title, two_introduce))
        return item
