import sys
import os
import base64
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from django.core.wsgi import get_wsgi_application

sys.path.append(os.path.dirname(os.path.normpath(sys.path[-1])))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manga_backend.settings.development")
get_wsgi_application()

from app.models import Manga


class PopularMangaSpider(scrapy.Spider):
    name = "popular_manga"

    start_urls = [
        "https://mangarock.com"
    ]

    BASE_URL = "https://mangarock.com"

    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options)

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
        chapters = selector.xpath("//*[@data-test='chapter-table']/tr/td/a/@href").extract()
        chapter_details = selector.xpath("//*[@data-test='chapter-table']/tr/td/a//text()").extract()
        chapters.reverse()
        chapter_details.reverse()
        for detail, chapter in zip(chapter_details[:10], chapters[:10]):
            yield scrapy.Request(url=self.BASE_URL+chapter, callback=self.parse_chapter, meta={"detail": detail.split(":")[0][-9:], "name": manga_name})

    def parse_chapters(self, response):
        self.driver.get(response.url)
        selector = Selector(text=self.driver.page_source)
        i = 1
        idx = 0
        action = ActionChains(self.driver)
        self.configure_page(action, self.driver)
        while True:
            self.driver.implicitly_wait(5)
            if selector.xpath('//*[@id="page-content"]/div/div[1]/div[2]/a[2]/span//text()').extract() == 'Next Chapter':
                break
            try:
                canvases = self.driver.find_elements_by_tag_name('canvas')
                base_64 = self.driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvases[idx])
            except IndexError:
                break
            filename = f"image_{i}.png"
            i+=1
            idx+=1
            image = open(filename, "wb")
            image.write(base64.b64decode(base_64))
            image.close()
            self.driver.implicitly_wait(10)
            next_btn = self.driver.find_element_by_xpath('//*[@id="page-content"]/div/div[1]/div[2]/a[2]')
            ActionChains(self.driver).move_to_element(next_btn).perform()
            next_btn.click()

    def configure_page(self, action, driver):
        elements = driver.find_elements_by_xpath('//*[@data-upgraded=",MaterialButton,MaterialRipple"]')
        btn = elements[7]
        action.move_to_element(btn)
        action.perform()
        btn.click()
        driver.implicitly_wait(5)
        driver.find_elements_by_class_name('Select-multi-value-wrapper')[0].click()
        element = driver.find_elements_by_class_name('_1elXr')
        driver.execute_script('arguments[0].click()', element[0])
        values = driver.find_elements_by_class_name('Select-value')
        driver.execute_script('arguments[0].click()', values[1])
        options = driver.find_elements_by_class_name('_1elXr')
        driver.execute_script('arguments[0].click()', options[0])
        btn2 = driver.find_elements_by_class_name('_34znY')
        driver.implicitly_wait(5)
        action.move_to_element(btn2[1]).click(btn2[1]).perform()
