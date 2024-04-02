# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class NbaprocessItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Gamelog(scrapy.Item):

    _id = Field()
    season = Field()
    # season_game = Field() # disabled
    # age = Field()         # disabled
    status = Field()
    game_result = Field()
    game_location = Field()
    gs = Field()
    mp = Field()
    fg = Field()
    fga = Field()
    fg_pct = Field()
    fg3 = Field()
    fg3a = Field()
    fg3_pct = Field()
    ft = Field()
    fta = Field()
    ft_pct = Field()
    orb = Field()
    drb = Field()
    trb = Field()
    ast = Field()
    stl = Field()
    blk = Field()
    tov = Field()
    pf = Field()
    pts = Field()
    # game_score = Field()      # disabled, not available on boxscore page
    plus_minus = Field()
    date_game = Field()
    team_id = Field()
    opp_id = Field()

    
