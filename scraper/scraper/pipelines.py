# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
from os import getenv
# from dotenv import load_dotenv

# load_dotenv()
class ScraperPipeline:
    def open_spider(self, spider):
        '''Open connection to database'''
        self.conn = psycopg2.connect(
            host='postgres',
            database=getenv('DATABASE'),
            user=getenv('USER'),
            password=getenv('PASSWORD'),
            port=getenv('PORT'),
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        # self.cursor.execute("DROP TABLE IF EXISTS public.flats;") # in case anything gets wrong there's a possibility that the table
        # is already created, although it's created with wrong parameters
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS public.flats (
                             id BIGSERIAL,
                             title varchar(35),
                             location varchar(100),
                             images text[],
                             url text
                            );''')

    def process_item(self, item, spider):
        '''Insert in database new flat'''
        self.cursor.execute('''INSERT INTO sreality.public.flats (title, "location", url, images) VALUES (\
         %s, %s, %s, %s);''', (item['title'], item['location'], item['url'], item['image_urls']))
        return item

    def close_spider(self, spider):
        '''Close connection to database'''
        self.cursor.execute('SELECT id, title, "location" FROM public.flats LIMIT 3;')
        print('Added to db:', self.cursor.fetchall())
        self.conn.close()
        