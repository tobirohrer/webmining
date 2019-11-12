import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess


class HeiseSpider(scrapy.Spider):
    name = 'heise_spider'
    allowed_domains = ['t3n.de']
    start_urls = ['https://t3n.de/news']

    def parse(self, response):
        extractor = LinkExtractor(allow='news', allow_domains=self.allowed_domains)
        links = extractor.extract_links(response)

        for link in links:
            absolute_next_page_url = response.urljoin(link.url)
            yield scrapy.Request(absolute_next_page_url)

        headings = response.xpath("//h2[@class='u-gap-medium u-text-extralarge']").extract()
        yield {'headings': headings}


def run_crawler(name):
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


run_crawler('HeiseSpider')
