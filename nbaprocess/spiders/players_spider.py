from pathlib import Path

import scrapy

class PlayersSpider(scrapy.Spider):
	name = "players"
	
	start_urls = ["https://www.basketball-reference.com/players/"]

	def parse(self, response):
		letter_links = response.xpath("//ul[@class='page_index']//li/a[re:match(text(),'^.$')]")
		yield from response.follow_all(letter_links, self.parse_letter)

	def parse_letter(self, response):
		for row in response.xpath("//table//tbody//tr"):
			yield {
				"id": row.xpath("th/@data-append-csv").get(),
				"name": row.xpath("th//a/text()").get(),
				"path": row.xpath("th//a/@href").get(),
				"year_min": row.xpath("td[@data-stat = 'year_min']/text()").get(),
				"year_max": row.xpath("td[@data-stat = 'year_max']/text()").get(),
				"pos": row.xpath("td[@data-stat = 'pos']/text()").get(),
				"height": row.xpath("td[@data-stat = 'height']/text()").get(),
				"weight": row.xpath("td[@data-stat = 'weight']/text()").get(),
				"birth_date": row.xpath("td[@data-stat = 'year_max']/text()").get()
			}
		
