import scrapy

from spider.crawler.items import MangaItem


class PopularMangaSpider(scrapy.Spider):
    name = "popular_manga"

    start_urls = [
        "https://www.mangareader.net"
    ]
    BASE_URL = "https://www.mangareader.net"

    def parse(self, response):
        name_set = set(response.css('.popularitemcaption::text').extract())
        for name in name_set:
            MangaItem(title=name)
        links = response.xpath('//*[@id="popularlist"]/ol/li/div/b/a/@href').extract()
        for link in links:
            url = self.BASE_URL + link
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        image = response.xpath('//*[@id="mangaimg"]/img/@src').extract()[0]
        description = response.xpath('//*[@id="readmangasum"]/p//text()').extract()[0]
        import pdb; pdb.set_trace()