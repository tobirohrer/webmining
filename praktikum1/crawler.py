import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess


class T3nUrlSpider(scrapy.Spider):
    name = 't3n_url_spider'
    allowed_domains = ['t3n.de']
    start_urls = ['https://t3n.de/news']

    def parse(self, response):
        extractor = LinkExtractor(allow='news', allow_domains=self.allowed_domains)
        links = extractor.extract_links(response)

        for link in links:
            absolute_next_page_url = response.urljoin(link.url)
            yield {'from': response.url, 'url': link.url, 'text': link.text.strip()}
            yield scrapy.Request(absolute_next_page_url)


class T3nDataSpider(scrapy.Spider):
    name = 't3n_data_spider'
    allowed_domains = ['t3n.de']
    start_urls = ['https://t3n.de/news']

    def parse(self, response):

        heading = response.xpath("//h2[@class='u-gap-medium u-text-extralarge']/text()").extract()
        yield {'heading': heading, 'url': response.url}

        extractor = LinkExtractor(allow='news', allow_domains=self.allowed_domains)
        links = extractor.extract_links(response)

        for link in links:
            absolute_next_page_url = response.urljoin(link.url)
            yield scrapy.Request(absolute_next_page_url)


def run_crawler(spider):
    c = CrawlerProcess({
        'CLOSESPIDER_PAGECOUNT': 50,
        'USER_AGENT': 'HochschuleDarmstadt-TextWebMining',
        'FEED_FORMAT': 'csv',
        'FEED_URI': spider.name + '.csv',
        'DOWNLOAD_DELAY': 0.5,
        'ROBOTSTXT_OBEY': True,
        'HTTPCACHE_ENABLED': True
    })
    c.crawl(spider)
    c.start()  # the script will block here until the crawling is finished
    

run_crawler(T3nDataSpider)
