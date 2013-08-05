#!/usr/bin/env python

import socket
import os
from random import randint
from urllib import urlencode
from urllib2 import (ProxyHandler, build_opener,
                     HTTPHandler, install_opener)
from socks.socks import PROXY_TYPE_SOCKS5
from socks.socksipyhandler import SocksiPyHandler

dir = os.path.dirname(__file__)


def get_userAgent(path=os.path.join(dir, 'useragents.txt')):
    with open(path, 'r') as userAgents:
        user_agents = userAgents.readlines()
    user_agents = map(str.strip, user_agents)
    return user_agents[randint(0, len(user_agents) - 1)]


def fetch(url, timeout=5, verbos=True, method='get', level=0,
          proxy=False, tor=False, agent=False, params={},
          headers=[]):
    try:
        proxy_support = ProxyHandler({'http': proxy} if proxy else {})
        opener = build_opener(proxy_support, HTTPHandler(debuglevel=level))

        opener = build_opener(
            #HTTPHandler(debuglevel=level),
            SocksiPyHandler(level, PROXY_TYPE_SOCKS5, '127.0.0.1', 9050),
        ) if tor else opener

        #exit(opener.open('http://ifconfig.me/ip').read().strip())

        # Spoof the user-agent
        if agent:
            opener.addheaders = [('User-agent', agent)]
        else:
            opener.addheaders = [('User-agent', get_userAgent())]

        install_opener(opener)
        #url = 'http://%s' % url if not url.startswith('http://') else url
        if method == 'post':
            data = urlencode(params)
            src = opener.open(url, data, timeout=timeout)
        else:
            src = opener.open(url, timeout=timeout)
        src = src.read()
        return src
    except socket.timeout:
        if verbos:
            print "[!] Connection lost to host: %s" % url
        pass
