import scrapy
import re
import requests


class GamesSpider(scrapy.Spider):
    name = "games"
    start_urls = ["http://cafebazaar.ir"]

    def parse(self, response):
        get_page_pathes = [
            'dynamic?slug=ml-strategy-editors-choice-best-new-games',
            'dynamic?slug=all-time-great-strategy-games',
            'dynamic?slug=ml-defense-games-gc',
            'dynamic?slug=ml-battle-arena-games-gc',
            'dynamic?slug=al-king-games-gc',
            'dynamic?slug=ml-mmo-strategy-games-gc',
            'dynamic?slug=new-strategy-games'
        ]
        app_details_url = "https://api.cafebazaar.ir/rest-v1/process/AppDetailsRequest"
        get_page_url = "https://api.cafebazaar.ir/rest-v1/process/GetPageRequest"
        app_details_ploads = {
            "properties": {
                "language": 2, 
                "clientID": "q6ad7dfhvi10wwxha0njokewxtzxppyu", 
                "deviceID": "q6ad7dfhvi10wwxha0njokewxtzxppyu",
                "clientVersion": "web"
            }, 
            "singleRequest": {
                "appDetailsRequest": {
                    "language": "fa", 
                    # "packageName": "com.rattagames.meow_war"
                }
            }
        }
        get_page_ploads = {
            "properties": {
                "language": 2, 
                "clientID": "q6ad7dfhvi10wwxha0njokewxtzxppyu", 
                "deviceID": "q6ad7dfhvi10wwxha0njokewxtzxppyu",
                "clientVersion": "web"
            }, 
            "singleRequest": {
                "getPageRequest": {
                    # "path": "dynamic?slug=ml-best-new-strategy-games", 
                    # "offset": 0, 
                    "language": "fa"
                }
            }
        }
        header = {
            'authority': 'api.cafebazaar.ir',
            'method': 'POST',
            'path': '/rest-v1/process/GetPageRequest', #TODO
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en, fa; q = 0.9, en-US ;q = 0.8',
            'content-length': '256',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https: // cafebazaar.ir',
            'referer': 'https: // cafebazaar.ir /',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        }
        package_names = []
        for path in get_page_pathes:
            get_page_ploads['singleRequest']['getPageRequest']['path'] = path
            i = 0
            while True:
                get_page_ploads['singleRequest']['getPageRequest']['offset'] = 0 if i == 0 else i*24+1
                response = requests.post(get_page_url, headers=header, json=get_page_ploads).json()
                contentList = response['singleReply']['getPageReply']['contentList']
                if len(contentList) == 0:
                    break
                i += 1
                for content in contentList:
                    if content['layoutApp']['packageName'] not in package_names:
                        package_names.append(content['layoutApp']['packageName'])
        # print(package_names)
        print(len(package_names), 'packages founded')
        print('crawling details for each game ...')
        header['path'] = '/rest-v1/process/AppDetailsRequest'
        tag_regex = re.compile('<.*?>')
        for package in package_names:
            app_details_ploads['singleRequest']['appDetailsRequest']['packageName'] = package
            response = requests.post(app_details_url, headers=header, json=app_details_ploads).json()
            response = response['singleReply']['appDetailsReply']
            data = {
                'packageName': package,
                'name': response['name'],
                'authorName': response['authorName'],
                'description': tag_regex.sub('', response['description']),
                'versionName': response['package']['versionName'],
                'size': {
                    'size': response['package']['packageSize'],
                    'verboseSize': response['package']['verboseSize'],
                    'verboseSizeLabel': response['package']['verboseSizeLabel']
                },
                'price': {
                    'price': response['price']['price'],
                    'priceString': response['price']['priceString'],
                    'hasInAppPurchase': response['hasInAppPurchase'],
                },
                'installCountRange': response['installCountRange'],
                'rate': response['rate'],
            }
            yield data