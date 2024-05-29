from pathlib import Path
from datetime import datetime
from ..items import Gamelog

import scrapy

BOXSCORE_TABLES = "//table[contains(@id, 'game-basic')]"

class BoxscoreSpider(scrapy.Spider):
	name = "boxscore"
	start_urls = ["https://www.basketball-reference.com/boxscores/"]

	def parse(self, response):
		boxscore_links = response.xpath("//td[contains(@class, 'gamelink')]/a")[:1]
		yield from response.follow_all(boxscore_links, self.parse_boxscores)

	def parse_boxscores(self, response):
		teams = response.xpath("//div[@class='scorebox']//strong/a/@href")
		tables = response.xpath("//table[contains(@id, 'game-basic')]")
		game_id = response.url.split("/")[-1][0:-5]
		date_game = datetime.strptime(game_id[:-4], "%Y%m%d")
		season = response.xpath("//div[@id='bottom_nav']//a[contains(@href, '/leagues/NBA')]/@href").get().split("_")[1]
		scores = response.xpath("//div[@class='score']/text()")

		def get_stat(row, stat):
			datum = row.xpath(f"td[@data-stat='{stat}']")
			if not datum:
				return None

			if datum[0].xpath("a"):
				return datum[0].xpath("a/text()").get()

			return datum[0].xpath("text()").get()

		
		for i in range(2):
			team_id = teams[i].get()[7:10]
			opp_id = teams[(i + 1) % 2].get()[7:10]
			result = int(scores[i].get()) - int(scores[(i + 1) % 2].get())
			table = tables[i]
			gamelog_rows = table.xpath("tbody/tr[not(contains(@class, 'thead'))]")

			for idx, row in enumerate(gamelog_rows):
				played = False
				if len(row.xpath("td")) > 1:
					played = True
				gamelog = Gamelog()
				gamelog["_id"] = {
					"player_id": row.xpath("th/@data-append-csv").get(),
					"game_id": game_id
				}
				gamelog["season"] = season

				# plain text stats
				gamelog["status"] = "INACTIVE" if not played else "ACTIVE"
				gamelog["game_location"] = "AWAY" if row.xpath(f"td[@data-stat='game_location']") else "HOME"
				gamelog["game_result"] = result
				gamelog["gs"] = idx <= 4 	
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
				gamelog["team_id"] = team_id
				gamelog["opp_id"] = opp_id
				
				yield gamelog
