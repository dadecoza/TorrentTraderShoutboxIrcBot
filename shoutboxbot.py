#! /usr/bin/env python
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr
import urllib2
import json
import threading


shoutboxJsonUrl = 'http://torrents.ctwug.za.net/shoutbox_json.php'
nick = 'shoutbox'
channel = '#ctwug-lounge'
server = '172.26.16.1'
port = 6667


class TestBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)
        print "connected"


bot = None
done = []


def poll():
    global done
    current = []
    threading.Timer(10, poll).start()
    if (bot is not None):
        try:
            response = urllib2.urlopen(shoutboxJsonUrl)
            data = json.load(response)
            for i in data:
                if i['id'] not in done:
                    msg = "<%s> %s" % (i['user'], i['message'])
                    bot.connection.privmsg(bot.channel, msg)
                    print msg
                current.append(i['id'])
            done = current
        except Exception, e:
            print e


def init():
    global done
    response = urllib2.urlopen(shoutboxJsonUrl)
    data = json.load(response)
    for i in data:
        done.append(i['id'])


def main():
    import sys
    global bot
    init()
    bot = TestBot(channel, nick, server, port)
    poll()
    bot.start()

if __name__ == "__main__":
    main()
