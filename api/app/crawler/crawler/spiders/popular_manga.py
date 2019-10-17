import scrapy

from ....models import Manga


class PopularMangaSpider(scrapy.Spider):
    name = "popular_manga"

    start_urls = [
        "https://www.mangareader.net"
    ]
    BASE_URL = "https://www.mangareader.net"

    def parse(self, response):
        names = response.css('.popularitemcaption::text').extract()
        links = response.xpath('//*[@id="popularlist"]/ol/li/div/b/a/@href').extract()
        for link in links:
            url = self.BASE_URL + link
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        image = response.xpath('//*[@id="mangaimg"]/img/@src').extract()[0]
        description = response.xpath('//*[@id="readmangasum"]/p//text()').extract()[0]
        return
