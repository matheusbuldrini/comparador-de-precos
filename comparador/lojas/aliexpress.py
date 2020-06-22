from .loja import  Loja
from lxml import html
import requests
import json
import re

class Aliexpress(Loja):
    origin = 'aliexpress'

    def str_to_search_url(self, s):
        return "https://pt.aliexpress.com/wholesale?SearchText="+s

    def url_to_json(self, url):
        if "aliexpress" not in url:
            return False

        page = requests.get(url)
        tree = html.fromstring(page.content)

        script_list = tree.xpath('//script[@type="text/javascript"]/text()')
        j = ''
        for tag in script_list:
            if 'window.runParams = {"resultCount"' in tag:
                for line in str(tag).split('\n',3):
                    if 'window.runParams = {"resultCount"' in line:
                        j += line[:-1].split("window.runParams = ",1)[1] 
                        break
                break
        if not j:
            return {'ads': [], 'errors': True}
        ads_list = json.loads(j)['items']

        ads = []
        err = False
        for a in ads_list:
            try:
                ads.append({'title': a['title'], 'link': "http://"+a['productDetailUrl'][2:], 'image': "http://"+a['imageUrl'][2:], 'price':a['price'] })
            except:
                err = True

        return {'ads': ads, 'errors': err}