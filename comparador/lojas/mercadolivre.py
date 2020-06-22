from .loja import  Loja
import requests
import json

class Mercadolivre(Loja):
    origin = 'mercadolivre'
    
    def str_to_search_url(self, s):
        return "https://api.mercadolibre.com/sites/MLB/search?q="+s

    def url_to_json(self, url):
        if "api.mercadolibre.com/sites/MLB" not in url:
            return False

        j = requests.get(url).text
        ads_list = json.loads(j)['results']

        ads = []
        err = False
        for a in ads_list:
            try:
                ads.append({'title': a['title'], 'link': a['permalink'], 'image': a['thumbnail'][:-5]+"O.jpg", 'price':a['price'] })
            except:
                err = True

        return {'ads': ads, 'errors': err}