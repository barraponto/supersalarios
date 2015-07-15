# -*- coding: utf-8 -*-
import scrapy


class DgrhSpider(scrapy.Spider):
    name = "dgrh"
    allowed_domains = ["siarh.unicamp.br"]
    start_urls = (
        'http://www.siarh.unicamp.br/',
    )

    def parse(self, response):
        pass
