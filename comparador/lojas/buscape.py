from .loja import  Loja
from lxml import html
import requests

class Buscape(Loja):
    origin = 'buscape'

    def str_to_search_url(self, s):
        return "https://www.buscape.com.br/search?q="+s

    def url_to_json(self, url):
        if "buscape" in url:
            site = "https://www.buscape.com.br"
        else:
            return False

        page = requests.get(url)
        tree = html.fromstring(page.content)
        ad_list_div = tree.xpath('//div[@id="pageSearchResultsBody"]/div/div/a[@class="cardImage"]')
        
        ads = []
        err = False
        for a in ad_list_div:
            try:
                link = a.xpath('@href')
                title = a.xpath('@title')
                image = a.xpath('img/@src')
                price_span = a.xpath('parent::*/div[@class="cardBody"]/div[@class="cardInfo"]/div[@class="priceArea"]/div[@class="priceWrapper"]/a[@class="price"]/span[@class="customValue"]') #or ('','')
                if len(price_span) > 0:
                    main = price_span[0].xpath('span[@class="mainValue"]/text()')[0]
                    cents = price_span[0].xpath('span[@class="centsValue"]/text()')[0]
                    price = float(int(main[3:].replace('.','')) + int(cents[1:])/100.0)
                else:
                    price = ''
                #print(link[0])
                #print(title[0])
                #print(image[0])
                #print(price)
                ads.append({'title': title[0], 'link': site+link[0], 'image': image[0], 'price':price})
            except:
                err = True

        return {'ads': ads, 'errors': err}