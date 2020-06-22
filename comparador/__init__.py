from .lojas.aliexpress import Aliexpress
from .lojas.zoom import Zoom
from .lojas.buscape import Buscape
from .lojas.mercadolivre import Mercadolivre
from .lojas.olx import Olx
from .lojas.pelando import Pelando

Aliexpress = Aliexpress()
Zoom = Zoom()
Buscape = Buscape()
Mercadolivre = Mercadolivre()
Olx = Olx()
Pelando = Pelando()

lojas = [Zoom, Pelando, Olx, Mercadolivre, Aliexpress, Buscape]
retries_limit = 3

def search_all(param):
    results = []
    errors = False
    for loja in lojas:
        r = loja.search(param)
        retries = 0
        while r['errors'] and retries <= retries_limit:
            print("retrying...")
            r = loja.search(param)
            retries += 1
        if not r['errors']:
            results.append({'origin':loja.origin, 'ads':r['ads'], 'errors':r['errors']})
        else:
            errors = True
    
    return {'results': results, 'errors':errors}

def search_all_interleave(s):
    r = search_all(s)
    results = r['results']

    iterators = []
    final = []
    res_count = 0

    for result in results:
        iterators.append(iter(result['ads']))
        res_count += len(result['ads'])

    count = 0
    while count < res_count:

        for it in iterators:
            try:
                final.append(next(it))
                count +=1
            except StopIteration :
                iterators.remove(it)
        
    return {'ads': final}