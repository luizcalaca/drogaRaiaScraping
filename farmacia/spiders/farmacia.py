# -*- coding: utf-8 -*-
import scrapy


class FarmaciaSpider(scrapy.Spider):
    name = "farmacia"
    allowed_domains = ["drogaraia.com.br"]
    start_urls = (
        'http://www.drogaraia.com.br/saude/medicamentos/todos-de-a-z.html?p=5',
    )

    def parse(self, response):
        medicamentos = response.xpath('//div[@class="product-info"]')
        for medicamento in medicamentos:
        	nome_medicamento = medicamento.xpath('div[@class="product-name"]/a/@title').extract_first().encode('utf-8')
        	if nome_medicamento is not None:
        		print "Nome do medicamento: " +nome_medicamento
                detalhes_medicamento = medicamento.xpath('div[@class="product-attributes"]')
                marca = detalhes_medicamento.xpath('.//li[contains(@class, "marca")]/text()').extract_first().encode('utf-8')
                print "Marca: " +marca
                quantidade = detalhes_medicamento.xpath('.//li[contains(@class, "quantidade show")]/text()').extract_first().encode('utf-8')
                print "Quantidade: " +quantidade
                principio_ativo = detalhes_medicamento.xpath('.//li[contains(@class, "principioativo show")]/text()').extract_first(default='not-found').encode('utf-8')
                print "Princípio ativo: " +principio_ativo

                preco_atual = medicamento.xpath('.//span[@property="price"]/text()').extract_first(default='not-found').encode('utf-8')
                print "Preço atual: R$ " +preco_atual

        #next_page = response.xpath('//li[contains(@class, "current inline")]/text()').extract_first()
        next_page_url = response.xpath('//a[contains(@class, "next i-next btn-more")]/@href').extract_first()
        if next_page_url:
            #next_page = int(next_page) + 1
            #next_page_url = 'http://www.drogaraia.com.br/saude/medicamentos/todos-de-a-z.html?p=' +str(next_page)
            print 'Next Page: {0}'.format(next_page_url)
            cookie = response.headers
            print cookie
            request = scrapy.Request(url=next_page_url, headers={'Cookie': cookie}, callback=self.parse)
            yield request
