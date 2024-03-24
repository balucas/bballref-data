from pathlib import Path
from ..items import Gamelog

import scrapy

GAMELOG_TABLE_XP = "body/div[@id='wrap']/div[@id='content']//table[@id='pgl_basic']/tbody/tr[not(@class='thead')]"

class GamelogSpider(scrapy.Spider):
	name = "gamelog"
	start_urls = ["https://www.basketball-reference.com/players/"]

	def parse(self, response):
		letter_links = response.xpath("//ul[@class='page_index']//li/a[re:match(text(),'^.$')]")[:1]
		yield from response.follow_all(letter_links, self.parse_letter)

	def parse_letter(self, response):
		active_player_links = [href.get()[:-5] + '/gamelog/2024' for href in response.xpath("//table/tbody/tr/th/strong/a/@href")][:2]
		yield from response.follow_all(active_player_links, self.parse_player)

	def parse_player(self, response):
		## TODO: parse player season and career averages
		## TODO: split up logs and player info

		def get_stat(row, stat):
			datum = row.xpath(f"td[@data-stat='{stat}']")
			if not datum:
				return None

			if datum[0].xpath("a"):
				return datum[0].xpath("a/text()").get()

			return datum[0].xpath("text()").get()

		# gamelog meta
		url_split = response.url.split("/")

		# parse player info
		# name = response.xpath("body/div[@id='wrap']/div[@id='info']/div[@id='meta']/div/h1/span/text()").get()[:-17]

		# parse game log table
		gamelogs_rows = response.xpath("body/div[@id='wrap']/div[@id='content']//table[@id='pgl_basic']/tbody/tr[not(@class='thead')]")
		for row in gamelogs_rows:

			# gamelog player id and season
			gamelog = Gamelog()
			gamelog["player_id"] = url_split[5]
			gamelog["season"] = url_split[-1]

			# plain text
			gamelog["age"] = get_stat(row, "age")
			gamelog["status"] = "INACTIVE" if row.xpath(f"td[@data-stat='reason']") else "ACTIVE"
			gamelog["game_location"] = "AWAY" if row.xpath(f"td[@data-stat='game_location']") else "HOME"
			gamelog["game_result"] = get_stat(row, "game_result")
			gamelog["gs"] = get_stat(row, "gs")
			gamelog["mp"] = get_stat(row, "mp")
			gamelog["fg"] = get_stat(row, "fg")
			gamelog["fga"] = get_stat(row, "fga")
			gamelog["fg_pct"] = get_stat(row, "fg_pct")
			gamelog["fg3"] = get_stat(row, "fg3")
			gamelog["fg3a"] = get_stat(row, "fg3a")
			gamelog["fg3_pct"] = get_stat(row, "fg3_pct")
			gamelog["ft"] = get_stat(row, "ft")
			gamelog["fta"] = get_stat(row, "fta")
			gamelog["orb"] = get_stat(row, "orb")
			gamelog["drb"] = get_stat(row, "drb")
			gamelog["trb"] = get_stat(row, "trb")
			gamelog["ast"] = get_stat(row, "ast")
			gamelog["stl"] = get_stat(row, "stl")
			gamelog["blk"] = get_stat(row, "blk")
			gamelog["tov"] = get_stat(row, "tov")
			gamelog["pf"] = get_stat(row, "pf")
			gamelog["pts"] = get_stat(row, "pts")
			gamelog["game_score"] = get_stat(row, "game_score")
			gamelog["plus_minus"] = get_stat(row, "plus_minus")
			gamelog["date_game"] = get_stat(row, "date_game")
			gamelog["team_id"] = get_stat(row, "team_id")
			gamelog["opp_id"] = get_stat(row, "opp_id")

			# links
			link_stat = row.xpath("td[a]")
			for link in link_stat:
				gamelog[link.xpath("@data-stat").get()] = link.xpath("a/text()").get()
			
			yield gamelog
