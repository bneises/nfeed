import time
import redis

import tornado.httpserver
import tornado.ioloop
import tornado.web

class GenerateFeed(tornado.web.RequestHandler):
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
            
        if results:
            self.write("""<?xml version="1.0" encoding="UTF-8" ?>
                                       <rss version="2.0">
                                       <channel>
                                       <title>Notifeeder</title>
                                       <link>http://code.google.com/p/notifeed</link>
                                       <description>searching some stuff</description>
                                       <language>en-us</language>""")
      #self.write('<pubDate>%s</pubDate>' % thetime)
            self.write('<generator>Freaking Manual Labor 1.0</generator>') 
            self.write('<ttl>10</ttl>')
      
        for item in results:
            theterm = item['searchterm']
            thelink = item['link']
            thetitle = item['title']
            theid = item['id']
          
            self.write("<item>")
            self.write("<title><![CDATA[%s]]></title>" % thetitle)
            self.write("<link><![CDATA[%s]]></link>" % thelink)
            self.write("""<description xml:space='preserve'><br/>Your search 
                                       term was "<![CDATA[%s]]>" <br/><br/>
                                       You have been notified by <a href="http://code.google.com/p/notifeed">Notifeeder!</a></description>""" % theterm)
            self.write("<guid><![CDATA[%s]]></guid>" % theid)
            self.write("</item>")
            self.write('</channel></rss>')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/rss", GenerateFeed),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
