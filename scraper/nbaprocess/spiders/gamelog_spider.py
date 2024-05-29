from pathlib import Path
from datetime import datetime
from ..items import Gamelog

import scrapy

class GamelogSpider(scrapy.Spider):
	name = "gamelog"
	start_urls = ["https://www.basketball-reference.com/players/"]

	def parse(self, response):
		letter_links = response.xpath("//ul[@class='page_index']//li/a[re:match(text(),'^.$')]")
		yield from response.follow_all(letter_links, self.parse_letter)

	def parse_letter(self, response):
		active_player_links = [href.get()[:-5] + '/gamelog/2024' for href in response.xpath("//table/tbody/tr/th/strong/a/@href")]
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
			game_result = get_stat(row, "game_result")
			game_id = row.xpath("td[@data-stat='date_game']/a/@href").get()[11:-5]
			date_game = datetime.strptime(game_id[:-4], "%Y%m%d")
			played = not row.xpath(f"td[@data-stat='reason']")

			# gamelog ids and season info
			gamelog = Gamelog()
			gamelog["_id"] = {
				"player_id": url_split[5],
				"game_id": game_id
			}
			gamelog["season"] = url_split[-1]

			# plain text stats
			gamelog["status"] = "ACTIVE" if played else "INACTIVE"
			gamelog["game_location"] = "AWAY" if row.xpath(f"td[@data-stat='game_location']") else "HOME"
			gamelog["game_result"] = int(game_result[game_result.find("(")+1:game_result.find(")")])
			gamelog["gs"] = get_stat(row, "gs") == "1"
			mp = get_stat(row, "mp").split(':') if played else None
			gamelog["mp"] = int(mp[0]) * 60 + int(mp[1]) if played else None
			gamelog["fg"] = int(get_stat(row, "fg")) if played else None
			gamelog["fga"] = int(get_stat(row, "fga")) if played else None
			gamelog["fg_pct"] = round(gamelog["fg"]/gamelog["fga"], 3) if gamelog["fg"] else None
			gamelog["fg3"] = int(get_stat(row, "fg3")) if played else None
			gamelog["fg3a"] = int(get_stat(row, "fg3a")) if played else None
			gamelog["fg3_pct"] = round(gamelog["fg3"]/gamelog["fg3a"], 3) if gamelog["fg3"] else None
			gamelog["ft"] = int(get_stat(row, "ft")) if played else None
			gamelog["fta"] = int(get_stat(row, "fta")) if played else None
			gamelog["ft_pct"] = round(gamelog["ft"]/gamelog["fta"], 3) if gamelog["ft"] else None
			gamelog["orb"] = int(get_stat(row, "orb")) if played else None
			gamelog["drb"] = int(get_stat(row, "drb")) if played else None
			gamelog["trb"] = int(get_stat(row, "trb")) if played else None
			gamelog["ast"] = int(get_stat(row, "ast")) if played else None
			gamelog["stl"] = int(get_stat(row, "stl")) if played else None
			gamelog["blk"] = int(get_stat(row, "blk")) if played else None
			gamelog["tov"] = int(get_stat(row, "tov")) if played else None
			gamelog["pf"] = int(get_stat(row, "pf")) if played else None
			gamelog["pts"] = int(get_stat(row, "pts")) if played else None
			# gamelog["game_score"] = get_stat(row, "game_score")
			gamelog["plus_minus"] = int(get_stat(row, "plus_minus")) if played else None
			gamelog["date_game"] = date_game 
			gamelog["team_id"] = get_stat(row, "team_id")
			gamelog["opp_id"] = get_stat(row, "opp_id")
			
			yield gamelog
