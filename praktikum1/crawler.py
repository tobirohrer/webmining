import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess


class T3nSpider(scrapy.Spider):
    name = 't3n_spider'
    allowed_domains = ['t3n.de']
    start_urls = ['https://t3n.de/news']

    def parse(self, response):
        extractor = LinkExtractor(allow='news', allow_domains=self.allowed_domains)
        links = extractor.extract_links(response)

        for link in links:
            absolute_next_page_url = response.urljoin(link.url)
            yield {'from': response.url, 'url': link.url, 'text': link.text.strip()}
            yield scrapy.Request(absolute_next_page_url)

        heading = response.xpath("//h2[@class='u-gap-medium u-text-extralarge']/text()").extract()
        yield {'heading': heading, 'url': response.url}


def run_crawler(name):
    c = CrawlerProcess({
        'USER_AGENT': 'HochschuleDarmstadt-TextWebMining',
        'FEED_FORMAT': 'csv',
        'FEED_URI': name + '.csv',
        'DOWNLOAD_DELAY': 0.5,
        'ROBOTSTXT_OBEY': True,
        'HTTPCACHE_ENABLED': True
    })
    c.crawl(T3nSpider)
    c.start()  # the script will block here until the crawling is finished


run_crawler('t3nspider')
