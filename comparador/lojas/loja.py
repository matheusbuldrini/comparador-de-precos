from abc import ABC, abstractmethod
 
class Loja(ABC):
 
    @property
    def origin(self):
        raise NotImplementedError
 
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def str_to_search_url(self, s):
        raise NotImplementedError

    @abstractmethod
    def url_to_json(self, url):
        raise NotImplementedError

    def search(self, s):
        return self.url_to_json(self.str_to_search_url(s))