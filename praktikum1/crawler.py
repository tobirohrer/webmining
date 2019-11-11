import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess

class HeiseSpider(scrapy.Spider):
    name = 'heise_spider'
    allowed_domains = ['t3n.de']
    start_urls = ['https://t3n.de/news/expertenanhoerung-huawei-5g-1219846/']

    def parse(self, response):
        headings = response.xpath("//h2[@class='u-gap-medium u-text-extralarge']").extract()
        yield {'headings': headings}


def runCrawler(name):
    c = CrawlerProcess({
        'USER_AGENT': 'HochschuleDarmstadt-TextWebMining',
        'FEED_FORMAT': 'csv',
        'FEED_URI': name + '.csv',
        'DOWNLOAD_DELAY': 0.5,
        'ROBOTSTXT_OBEY': True,
        'HTTPCACHE_ENABLED': True
    })
    c.crawl(HeiseSpider)
    c.start()  # the script will block here until the crawling is finished

runCrawler('HeiseSpider')