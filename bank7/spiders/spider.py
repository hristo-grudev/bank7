import scrapy

from scrapy.loader import ItemLoader

from ..items import Bank7Item
from itemloaders.processors import TakeFirst


class Bank7Spider(scrapy.Spider):
	name = 'bank7'
	start_urls = ['https://www.bank7.com/news/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="mk-blog-meta"]')
		for post in post_links:
			title = post.xpath('.//h3[@class="the-title"]/text()').get()
			description = post.xpath('.//div[@class="the-excerpt"]//text()[normalize-space() and not(ancestor::a)]').getall()
			description = [p.strip() for p in description if '{' not in p]
			description = ' '.join(description).strip()
			date = post.xpath('.//time/strong/text()').get()

			item = ItemLoader(item=Bank7Item(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()
