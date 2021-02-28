from datetime import datetime
from itemadapter import ItemAdapter
from datetime import datetime as dt
class JsonPipeline(object):
    def __init__(self):
        dt_string = dt.now().strftime("%Y/%m/%d-%H:%M:%S")
        self.file = open("games" + dt_string + ".json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
