from lib.httpgetfeednterms import *
from lib.itemfinder import *
import threading

from optparse import OptionParser

def get_args():
    parser = OptionParser(description='Example: python nfeed-cli.py -u http://foo -t http://bar')
    parser.add_option('-t', '--terms', dest='termlist', default=None,
                         help='search term list, via http URL')
    parser.add_option('-u', '--urls', dest='urllist', default=None,
                         help='rss feed list, via http URL')
    args = parser.parse_args()
    return args


class FeedFetch(threading.Thread):
    ' Appends a dictionary to a global variable feedfetchresult '
    def __init__(self, url):
        self.results = []
        self.url = url
#        print "DEBUG ", self.urls
        threading.Thread.__init__(self)
        
    
    def run(self):
        ' Returns dictionary of results ' 
        try:
            response = urllib2.urlopen(self.url)
        except urllib2.HTTPError, e:
            print 'Error %s from %s' % (e.code, self.url)  
        
        xml = response.read()
        
        fetchResult = {'url':self.url,'xml': xml}
        
        feedfetchresult.append(fetchResult)

def feed_fetch(urls):
    for url in urls:
        getcontent = FeedFetch(url)
        getcontent.start()

    getcontent.join()


if __name__ == '__main__':
    args = get_args()[0]
    urllist = args.urllist
    termlist = args.termlist
    urls = GetUrls(urllist).get_rss_list()
    searchterms = GetTerms(termlist).get_rss_list()
    
    feedfetchresult = []
    feed_fetch(urls)
    
    x = ItemFinder(feedfetchresult, searchterms)
    results = x.entry_popper()
    if results:
        total_items = len(results['items'])
        broken_feed_total = len(results['brokenfeeds'])
        for item in results['items']:
            print 'hits: %s %s %s %s \n' % (item['searchterm'], item['title'], item['link'], item['id'])
        for broken in results['brokenfeeds']:
            print 'brokenfeeds: ' + broken
        print 'total items: %s' % total_items
        print 'total brokenfeeds: %s' % broken_feed_total
    else:
        print 'no data'
    
    
    
    