# -*- coding: utf-8 -*-
import scrapy
from anjvke.custom_settings import custom_settings
from anjvke.items import AnjvkeItem


class RentingSpider(scrapy.Spider):
    name = 'renting'
    custom_settings = custom_settings
    start_urls = []
    for i in range(1, 51):
        url = f'https://hz.zu.anjuke.com/fangyuan/p{i}/'
        start_urls.append(url)

    def parse(self, response):
        item = AnjvkeItem()
        div_list = response.xpath('//*[@id="list-content"]/div[@class="zu-itemmod"]')
        for i in div_list:
            title = i.xpath('.//div[@class="zu-info"]/h3/a/b/text()').extract()[0]
            href = i.xpath('.//div[@class="zu-info"]/h3/a/@href').extract()[0]
            meter = i.xpath('.//div[@class="zu-info"]/p[1]/b[3]/text()').extract()[0]
            room = i.xpath('.//div[@class="zu-info"]/p[1]/b[1]/text()').extract()[0]
            hall = i.xpath('.//div[@class="zu-info"]/p[1]/b[2]/text()').extract()[0]
            housing_estate = i.xpath('.//div[@class="zu-info"]/address/a/text()').extract()[0]
            detail_address = i.xpath('.//div[@class="zu-info"]/address/text()').extract()[1].strip()
            message = i.xpath('.//div[@class="zu-info"]/p[2]/span/text()').extract()
            money = i.xpath('.//div[@class="zu-side"]/p//text()').extract()[0] + i.xpath('.//div[@class="zu-side"]/p//text()').extract()[1]
            item['title'] = title
            item['href'] = href
            item['meter'] = meter
            item['room'] = room
            item['hall'] = hall
            item['money'] = money
            item['housing_estate'] = housing_estate
            item['detail_address'] = detail_address
            item['message'] = message
            yield item