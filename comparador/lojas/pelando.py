from .loja import  Loja
from lxml import html
import requests

class Pelando(Loja):
    origin = 'pelando'

    def str_to_search_url(self, s):
        return "https://www.pelando.com.br/search?q="+s

    def url_to_json(self, url):
        if "pelando" not in url:
            return False

        page = requests.get(url)
        tree = html.fromstring(page.content)
        ad_list_div = tree.xpath('//section[contains(@class,"cept-listing--card")]')
        ads_list = ad_list_div[0].xpath('//div[@class="gridLayout-item threadCardLayout--card"]/article')
        ads = []
        err = False
        for a in ads_list:
            try:
                link = a.xpath('div/strong/a/@href')
                title = a.xpath('div/strong/a/@title')
                image = a.xpath('div/a/img/@src')
                price = a.xpath('div/span/span/text()') or ['']
                #print(link[0])
                #print(title[0])
                #print(image[0])
                #print(price[0])
                ads.append({'title': title[0], 'link': link[0], 'image': image[0], 'price':price[0][2:].replace(".","") })
            except:
                err = True

        return {'ads': ads, 'errors': err}