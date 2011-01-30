import time
import redis


class GenerateFeed():
    def __init__(self):
        self.get()

    def get(self):
   # thetime = time.strftime("%d%b%Y", time.localtime())
        #q = db.GqlQuery("SELECT * FROM Entry")
        #results = q.fetch(25)
        r = redis.Redis("localhost")
        keys = r.lrange('itemindex','0','20')
        results = []
        for key in keys:
            value = r.hgetall('item:%s' % key)
            results.append(value)
            
        print results
        if results:
            print("""<?xml version="1.0" encoding="UTF-8" ?>
                                       <rss version="2.0">
                                       <channel>
                                       <title>Notifeeder</title>
                                       <link>http://code.google.com/p/notifeed</link>
                                       <description>searching some stuff</description>
                                       <language>en-us</language>""")
      #print('<pubDate>%s</pubDate>' % thetime)
            print('<generator>Freaking Manual Labor 1.0</generator>') 
            print('<ttl>10</ttl>')
      
        for item in results:
            theterm = item['searchterm']
            thelink = item['link']
            thetitle = item['title']
            theid = item['id']
          
            print("<item>")
            print("<title><![CDATA[%s]]></title>" % thetitle)
            print("<link><![CDATA[%s]]></link>" % thelink)
            print("""<description xml:space='preserve'><br/>Your search 
                                       term was "<![CDATA[%s]]>" <br/><br/>
                                       You have been notified by <a href="http://code.google.com/p/notifeed">Notifeeder!</a></description>""" % theterm)
            print("<guid><![CDATA[%s]]></guid>" % theid)
            print("</item>")
            print('</channel></rss>')



def main():
    GenerateFeed()

if __name__ == '__main__':
    main()
