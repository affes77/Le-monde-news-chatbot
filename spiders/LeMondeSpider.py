import scrapy
from urllib.parse import urlparse
from datetime import datetime, timedelta

class LeMondeSpider(scrapy.Spider):
    name = 'lemonde'
    allowed_domains = ['lemonde.fr']
    start_urls = ['https://www.lemonde.fr/archives-du-monde/01-01-2010/1/']
    end_date = '31-12-2020'
    def __init__(self):
        self.scraped_links = set()
    def parse(self, response):
        # Check if current page has already been scraped
        if response.url in self.scraped_links:
            return
        else:
            self.scraped_links.add(response.url)
        for article in response.xpath('//section[@class="teaser teaser--inline-picture  "]'):
            item = {}
            item['title'] = article.xpath('.//a[@class="teaser__link"]/h3[@class="teaser__title"]/text()').get()
            item['link'] = article.xpath('.//a[@class="teaser__link"]/@href').get()
            try:
                item['category'] = urlparse(item['link']).path.split('/')[1]
            except IndexError:
              item['category'] = None
            item['author'] = article.xpath('.//p[@class="meta__publisher meta--page"]/span[2]/text()').get()
            item['date'] = article.xpath('.//p[@class="meta__publisher meta--page"]/span/text()').get()
            item['summary'] = article.xpath('.//a/p[@class="teaser__desc"]/text()').get()
            yield item
        # Check if there are more pages for the same date
        page_number = 2
        next_page_link = response.xpath(f'//a[@class="river__pagination river__pagination--page "][text()="{page_number}"]/@href')
        while next_page_link:
            yield scrapy.Request(response.urljoin(next_page_link.get()), callback=self.parse)
            page_number += 1
            next_page_link = response.xpath(f'//a[@class="river__pagination river__pagination--page "][text()="{page_number}"]/@href')
        # Check if there are more dates to scrape
        date_str = response.url.split('/')[-3]
        current_date = datetime.strptime(date_str, '%d-%m-%Y').date()
        end_date = datetime.strptime(self.end_date, '%d-%m-%Y').date()
        if current_date >= end_date:
            return
        next_date = current_date + timedelta(days=1)
        next_date_link = f'https://www.lemonde.fr/archives-du-monde/{next_date.strftime("%d-%m-%Y")}/1/'
        yield scrapy.Request(next_date_link, callback=self.parse)


## scrapy crawl lemonde -L INFO -o output2020.csv -t csv