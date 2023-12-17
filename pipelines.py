# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


import json
from scrapy.exporters import CsvItemExporter

class LemondeScrapePipeline:
    def __init__(self):
        self.file = open("output.csv", "wb")
        self.exporter = CsvItemExporter(self.file, delimiter=';')
        self.exporter.fields_to_export = ["title", "author", "summary", "date", "link", "category"]
        self.exporter.start_exporting()
        self.formatted_data = []

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        with open("output.json", "w", encoding='utf-8') as f:
            json.dump(self.formatted_data, f, indent=4, ensure_ascii=False)

    def process_item(self, item, spider):
        self.formatted_data.append(item)
        self.exporter.export_item(item)
        return item








