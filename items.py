# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html



import scrapy


class LemondeScrapeItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    summary = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    content = scrapy.Field()
