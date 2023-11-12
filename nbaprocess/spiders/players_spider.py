from pathlib import Path

import scrapy

class PlayersSpider(scrapy.Spider):
	name = "players"

	def start_requests(self):
		urls = [
			"https://www.basketball-reference.com/players/a/"
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for row in response.xpath("//table//tbody//tr"):
			yield {
				"id": row.xpath("th/@data-append-csv").get(),
				"name": row.xpath("th//a/text()").get(),
				"path": row.xpath("th//a/@href").get(),
				"year_min": int(row.xpath("td[@data-stat = 'year_min']/text()").get()),
				"year_max": int(row.xpath("td[@data-stat = 'year_max']/text()").get()),
				"pos": row.xpath("td[@data-stat = 'pos']/text()").get(),
				"height": row.xpath("td[@data-stat = 'height']/text()").get(),
				"weight": int(row.xpath("td[@data-stat = 'weight']/text()").get()),
				"birth_date": row.xpath("td[@data-stat = 'year_max']/text()").get()
			}
		
