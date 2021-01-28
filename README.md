# cafebazar-crawler
Crawl strategy games from cafe bazar and save informations of each game in mongodb and json file.
## How to use?
First of all, install the required Python packages:
```
pip install requirements.txt
```
And then run the Python program with this command:
```
scrapy crawl games
```
If you want to run scheduled crawling use schedule_crawl.py file:
```
python schedule_crawl.py
```
> this file crawl games every 2 hour
