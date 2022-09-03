# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlatItem(scrapy.Item):
    title = scrapy.Field()
    location = scrapy.Field() # location is needed to distinguish flats with the same living area
    image_urls = scrapy.Field()
    url = scrapy.Field()
