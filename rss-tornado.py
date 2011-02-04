import time
import redis
from optparse import OptionParser

import tornado.httpserver
import tornado.ioloop
import tornado.web


def get_args():
    parser = OptionParser(description='Example: python rss-tornade.py -u /foo -p 80')
    parser.add_option('-u', '--url', dest='url', default='/rss',
                         help='Url to serve RSS page')
    parser.add_option('-p', '--port', dest='port', default=80,
                         help='Port for http server to listen on')
    args = parser.parse_args()
    return args


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
                                       <title>nFeed</title>
                                       <link>http://github.com/petekalo/nfeed</link>
                                       <description>searching some stuff</description>
                                       <language>en-us</language>""")
      #self.write('<pubDate>%s</pubDate>' % thetime)
            self.write('<generator>various and sundry</generator>') 
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
                                       You have been notified by <a
href="http://github.com/petekalo/nfeed">nFeed!</a></description>""" % theterm)
            self.write("<guid><![CDATA[%s]]></guid>" % theid)
            self.write("</item>")
        self.write('</channel></rss>')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

#application = tornado.web.Application([
#    (r"%s" % url, GenerateFeed),
#])

if __name__ == "__main__":
    args = get_args()[0]
    port = args.port
    url = args.url
    application = tornado.web.Application([
                (r"%s" % url, GenerateFeed),])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(int(port))
    tornado.ioloop.IOLoop.instance().start()
