from pathlib import Path

import scrapy

GAMELOG_TABLE_XP = "body/div[@id='wrap']/div[@id='content']//table[@id='pgl_basic']/tbody/tr[not(@class='thead')]"

class PlayersSpider(scrapy.Spider):
	name = "players"
	start_urls = ["https://www.basketball-reference.com/players/"]

	def parse(self, response):
		letter_links = response.xpath("//ul[@class='page_index']//li/a[re:match(text(),'^.$')]")[:1]
		yield from response.follow_all(letter_links, self.parse_letter)

	def parse_letter(self, response):
		active_player_links = [href[:-5] + '/gamelog/2024' for href in response.xpath("//table/tbody/tr/th/strong/a/@href")][:3]
		yield from response.follow_all(active_player_links, self.parse_player)

	def parse_player(self, response):
		# parse game log table
		gamelogs_rows = response.xpath("body/div[@id='wrap']/div[@id='content']//table[@id='pgl_basic']/tbody/tr[not(@class='thead')]")
		gamelogs = []
		for row in gamelogs_rows:
			gamelog = {}
			# plain text
			text_stat = row.xpath("td[./text()]")
			for stat in text_stat:
				gamelog[stat.xpath("@data-stat").get()] = stat.xpath("text()").get()

			# links
			link_stat = row.xpath("td[a]")
			for link in link_stat:
				gamelog[link.xpath("@data-stat").get()] = link.xpath("a/text()").get()

			gamelogs.append(gamelog)

		yield 

