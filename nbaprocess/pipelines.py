# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NbaprocessPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Convert data
        adapter["year_min"] = int(adapter["year_min"] or -1)
        adapter["year_max"] = int(adapter["year_max"] or -1)
        adapter["weight"] = int(adapter["weight"] or -1)
        
        return item
