# -*- coding: utf-8 -*-
import csv
from itertools import islice

import scrapy


class DgrhSpider(scrapy.Spider):
    name = "dgrh"
    allowed_domains = ["siarh.unicamp.br"]
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 6
    }

    search_url = ('http://www.siarh.unicamp.br/'
                  'consultaFuncionario/action/ConsultaFuncionario'
                  '?nome=&local=&matricula={matricula}')
    name_xpath = ('//table[@width="750"]/tr[./td[contains(., "{matricula}")]]'
                  '/td[1]/text()')

    def __init__(self, volume=100, *args, **kwargs):
        super(DgrhSpider, self).__init__(*args, **kwargs)
        self.volume = int(volume)

    def start_requests(self):
        with open('./remuneracao-por-bruto.csv') as datafile:
            for line in islice(csv.reader(datafile), 1, self.volume+1):
                yield scrapy.Request(
                    self.search_url.format(matricula=line[0]),
                    meta={'item': {'matricula': line[0],
                                   'salario_bruto': line[1],
                                   'salario_liquido': line[5]}})

    def parse(self, response):
        item = response.meta['item']
        text_data = response.xpath(self.name_xpath.format(**item))

        if text_data:
            item['nome'] = text_data.extract_first().strip()
            return item
