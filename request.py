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
    """get a random user agent in case agent not provided in fetch funca
    Keyword arguments:
        path -- path to useragent file"""
    with open(path, 'r') as userAgents:
        user_agents = userAgents.readlines()
    user_agents = map(str.strip, user_agents)
    return user_agents[randint(0, len(user_agents) - 1)]


def fetch(url, method='get', timeout=5, debuglevel=0,
          proxy=False, tor=False, agent=False, params={},
          headers=[]):
    """wrapper that provides easy use of urllib2
    and works with SOCKS4, SOCKS5, and HTTP proxy
    Keyword arguments:
        url -- main url to open
        method -- method when fetch the url (default get)
        params -- parameters when use POST as a method
        timeout -- socket timeout (default 5)
        debuglevel -- debug info (default false)
        proxy -- connect through a proxy server (http://127.0.0.1:8080)
        tor -- use TOR anonmity network
        agent -- spoof the useragent
        headers -- set a custom header (header=value)"""
    try:
        proxy_support = ProxyHandler({'http': proxy} if proxy else {})
        opener = build_opener(
            proxy_support,
            HTTPHandler(debuglevel=debuglevel)
        )

        opener = build_opener(
            SocksiPyHandler(debuglevel, PROXY_TYPE_SOCKS5, '127.0.0.1', 9050),
        ) if tor else opener

        #exit(opener.open('http://ifconfig.me/ip').read().strip())

        # Spoof the user-agent
        if agent:
            opener.addheaders = [('User-agent', agent)]
        else:
            opener.addheaders = [('User-agent', get_userAgent())]

        install_opener(opener)
        if method == 'post':
            data = urlencode(params)
            src = opener.open(url, data, timeout=timeout)
        else:
            src = opener.open(url, data=None, timeout=timeout)
        src = src.read()
        return src
    except socket.timeout:
        pass


if __name__ == '__main__':
    print "[+] Spoofing User-Agent:"
    print "[!!] (%s)" % fetch(
        "http://ifconfig.me/ip",
        agent="Spoofed-Agent",
        debuglevel=1
    ).strip()

    print "\n[+] Using TOR Network"
    print "[!!] (%s)" % fetch(
        "http://ifconfig.me/ip",
        tor=True,
        timeout=10
    ).strip()
