# -*- coding: utf-8 -*-
import csv
from itertools import islice

import scrapy


class DgrhSpider(scrapy.Spider):
    name = "dgrh"
    allowed_domains = ["siarh.unicamp.br"]
    search_url = ('http://www.siarh.unicamp.br/'
                  'consultaFuncionario/action/ConsultaFuncionario'
                  '?nome=&local=&matricula={matricula}')
    name_xpath = ('//table[@width="750"]/tr[./td[contains(., "{matricula}")]]'
                  '/td[1]/text()')

    def start_requests(self):
        with open('./remuneracao-por-bruto.csv') as datafile:
            for line in islice(csv.reader(datafile), 1, 101):
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
