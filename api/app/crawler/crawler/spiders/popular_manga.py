import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# from api.app.models import Manga


class PopularMangaSpider(scrapy.Spider):
    name = "popular_manga"

    start_urls = [
        "https://mangarock.com"
    ]

    BASE_URL = "https://mangarock.com"

    def __init__(self):
        self.option = Options()
        self.option.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.option)

    def parse(self, response):
        self.driver.get(response.url)
        selector = Selector(text=self.driver.page_source)
        popular_elements = selector.xpath("//*[@data-test='most_popular']/div[2]/div[contains(@class,'_1Ndy6 _1BkZ9')]")

        for element in popular_elements:
            url = element.xpath("a/@href").extract()[0]
            rank = element.css('._1O4WK::text').extract()[0]
            yield scrapy.Request(url=self.BASE_URL+url, callback=self.parse_page, meta={"rank": int(rank)})


    def parse_page(self, response):
        self.driver.get(response.url)
        selector = Selector(text=self.driver.page_source)
        manga_name = selector.xpath("//*[@itemprop='name headline']//text()").extract()[0]
        description = ''.join(map(str, selector.xpath("//*[@itemprop='articleBody']//text()").extract()))
        rank = response.meta["rank"]
        self.driver.implicitly_wait(3)
        image = self.driver.find_element_by_xpath("//*[@class='_1-8M9 _2tEoY']/img").get_attribute('src')
        import pdb; pdb.set_trace()

