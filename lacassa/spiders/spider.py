import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import LacassaItem
from itemloaders.processors import TakeFirst


class LacassaSpider(scrapy.Spider):
	name = 'lacassa'
	start_urls = ['https://www.lacassa.com/ita/News/Notizie-Cassa']

	def parse(self, response):
		year_links = response.xpath('//ul[@class="left-menu list-unstyled"]/li/ul/li/a/@href').getall()
		for link in year_links:
			yield response.follow(link, self.parse_year)

	def parse_year(self, response):
		article_links = response.xpath('//div[@class="testo"]/a/@href')
		yield from response.follow_all(article_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//article/h2/text()').get()
		description = response.xpath('//article//text()[normalize-space() and not(ancestor::h2 | ancestor::p[@class="date"] | ancestor::a)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//article/p[@class="date"]/text()').get()

		item = ItemLoader(item=LacassaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', re.findall(r"(\d{2}.\d{2}.\d{4})", date)[0])

		return item.load_item()
