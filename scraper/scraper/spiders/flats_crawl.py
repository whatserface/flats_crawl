import scrapy
from scrapy.http import JsonRequest

from scraper.items import FlatItem

class FlatsCrawlSpider(scrapy.Spider):
    name = 'flats_crawl'
    allowed_domains = ['sreality.cz']
    number_of_flats = '500'
    headers = {
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': None,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
            'accept-encoding': 'gzip, deflate, br',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        } # in order to get correct data we pretend to be human

    def __init__(self, number_of_flats=number_of_flats, *args, **kwargs):
        assert number_of_flats.isdigit() and number_of_flats != '0', "number_of_flats must be a natural number"
        FlatsCrawlSpider.number_of_flats = number_of_flats
        super(FlatsCrawlSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        urls = [
            # ('https://www.sreality.cz/api/cs/v2/filters', self.parse_filters), 
            (f'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&page=1&per_page={self.number_of_flats}',
            self.parse)
        ]
        for url, callback in urls:
            yield JsonRequest(url=url, callback=callback, headers=self.headers)

    # def parse_filters(self, response):
    #     '''Method to get names of values corresponding to "category_sub_cb", e.g.: 16: "Atypický"'''
    #     self.filters = {int(i['value']): i['name'].replace(' ', '-') for i in response.json()['filters']['3']['1'][2]['values']}

    def parse(self, response):
        '''Main method to parse information of flats'''
        for flat in response.json()['_embedded']['estates']:
            item = FlatItem()
            item['location'] = flat["locality"]
            category = flat['seo']['category_sub_cb']
            item['title'] = flat["name"]
            item['url'] = f'https://www.sreality.cz/detail/prodej/byt/{category}/{flat["seo"]["locality"]}/{flat["hash_id"]}'
            yield response.follow(f'https://www.sreality.cz/api/cs/v2/estates/{flat["hash_id"]}', callback=self.parse_flat, cb_kwargs={'item': item}, headers=self.headers)

    def parse_flat(self, response, item):
        '''Method to get links of full-sized images of flat'''
        r_json = response.json()
        item['image_urls'] = [i['_links']['self']['href'] for i in r_json['_embedded']['images']]
        # area = None
        # for i in r_json['items']:
        #     if 'plocha' in i['name']:
        #         area = i
        #         break
        # item['title'] += f'{area["value"]} {area["unit"]}'
        yield item

