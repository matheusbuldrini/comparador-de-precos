from .loja import  Loja
from lxml import html
import requests

class Olx(Loja):
    origin = 'olx'

    def str_to_search_url(self, s):
        return "https://www.olx.com.br/brasil?q="+s

    def url_to_json(self, url):
        if "olx" not in url:
            return False

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        page = requests.get(url, headers=headers)

        tree = html.fromstring(page.content)

        ad_list_div = tree.xpath('//ul[@id="ad-list"]')

        ads_list = ad_list_div[0].xpath('//li//a[@data-lurker-detail="list_id"]')

        ads = []
        err = False
        for a in ads_list:
            try:
                link = a.xpath('@href')
                title = a.xpath('@title')
                image = a.xpath('div/div/div/noscript/img/@src | div/div/div//img[not(@data-src)]/@src')
                price = a.xpath('div/div/div/div//p[@class="fnmrjs-16 jqSHIm"]/text()') or ['']
                #print(link[0])
                #print(title[0])
                #print(image[0])
                #print(price[0])
                ads.append({'title': title[0], 'link': link[0], 'image': image[0], 'price':price[0][3:] })
            except:
                err = True

        return {'ads': ads, 'errors': err}