import urllib2

class GetUrls:
    def __init__(self, feed):    
        self.feed = feed
            
    def get_rss_list(self):
        txt = urllib2.urlopen(self.feed)
        txt = txt.read()
        urls = txt.split()
        return urls
    
class GetTerms:
    def __init__(self, feed):    
        self.feed = feed
        
    def get_rss_list(self):
        txt = urllib2.urlopen(self.feed)
        txt = txt.read()
        searchterms = unicode(txt, errors='replace')
        searchterms = searchterms.split('\n')
        return searchterms
