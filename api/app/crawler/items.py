import scrapy


class MangaItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
