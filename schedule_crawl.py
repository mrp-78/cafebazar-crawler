from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from spiders.games_spider import GamesSpider
import time
from datetime import datetime


def crawl_job():
    """
    Job to start spiders.
    Return Deferred, which will execute after crawl has completed.
    """
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    return runner.crawl(GamesSpider)

def schedule_next_crawl(null, sleep_time):
    # Schedule the next crawl
    reactor.callLater(sleep_time, crawl)

def crawl():
    # A "recursive" function that schedules a crawl every 2 hours.
    # crawl_job() returns a Deferred
    start_time = time.time()
    print('crawl started at ', datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    d = crawl_job()
    # call schedule_next_crawl(<scrapy response>, n) after crawl job is complete
    d.addCallback(schedule_next_crawl, 2*60*60)
    d.addErrback(catch_error)
    print('next crawl after 2 hours')

def catch_error(failure):
    print(failure.value)


crawl()
reactor.run()