from external import feedparser
import urllib2, re


class ItemFinder:
    '''Pass a list of feeds and searchterms, returns tuple: list of dicts, list of badfeeds''' 
    def __init__(self, feeds, searchterms):
        self.feeds = feeds
        self.searchterms = searchterms
        self.quickResult = []
        self.quick_match()
        
    def quick_match(self):     ## returns a list of tuples ('xml1, url1, term1' , 'xml2', 'url2, term2')

        for feed in self.feeds:
            xml = feed['xml']
            url = feed['url']
            for term in self.searchterms:
                if re.search(term, xml, re.I):
                    matchDict  = {'xml': xml,'term': term,'url': url}
                    self.quickResult.append(matchDict)
                    #print self.urlterm
        return self.quickResult
    
    def entry_popper(self):     ## returns snippet(search term, rss entry title, and rss entry link) and broken feeds(feeds that feedparser doesnt like)
        self.items = []
        self.brokenfeeds = []
        for feed in self.quickResult:     
            xml = feed['xml']
            searchterm = feed['term']
            url = feed['url']
            
            d = feedparser.parse(xml)
            feedentries = d.entries
            
            for entry in feedentries:
                contents = []
                if entry.has_key('title'):
                    contents.append(entry.title)
                if entry.has_key('summary'):
                    contents.append(entry.summary)
                if not entry.has_key('id'):
                    entry.id = entry.title
                
                if contents and searchterm:   
                    for c in contents:                                    
                        if re.search(searchterm, c, re.X):
                            item = {'title': entry.title, 'link': entry.link, 'id': entry.id, 'feed' : url, 'searchterm': searchterm}
                            self.items.append(item)
                            break                     
                        else:
                            continue
                else:
                    self.brokenfeeds.append(url)
                    break

        return {'items':self.items, 'brokenfeeds': self.brokenfeeds}
    
    
    