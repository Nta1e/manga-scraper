import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class PopularMangaSpider(scrapy.Spider):
    name = "popular_manga"

    start_urls = [
        "https://mangarock.com"
    ]
    BASE_URL = "https://www.mangareader.net"

    def __init__(self):
        self.option = Options()
        self.option.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.option)

    def parse(self, response):
        self.driver.get(response.url)
        selector = Selector(text=self.driver.page_source)
        lis = []
        popular_elements = selector.xpath("//*[@data-test='most_popular']/div[2]/div[contains(@class,'_1Ndy6 _1BkZ9')]")
        for element in popular_elements:
            lis.append(element)
        import pdb; pdb.set_trace()

    def parse_page(self, response):
        image = response.xpath('//*[@id="mangaimg"]/img/@src').extract()[0]
        description = response.xpath('//*[@id="readmangasum"]/p//text()').extract()[0]
        return
