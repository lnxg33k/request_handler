request_handler  
-------------------
request_handler is a urllib2 wrapper that works with **SOCKS4, SOCKS5** and **HTTP Proxy**.  
#####It consists of two main functions#####
---
1. get_userAgent():  
  `This function provides a random user agent when fetch a new URL`
  * path -- it indicates the path the userAgent file.  

2. fetch():  
  
    It provides an easy use of urllib2 with some new features like,  
      spoofing user-agent, working with some types of proxy networks  
      and using the TOR anonymity network without vidalia or privoxy.  

    `It takes 8 params, only one of them is a positional one 'url'`
      - url     --  main url to open  
      - method  --  method when fetch the url **(Default:  get)**
      - params -- parameters to use when method is **POST**
      - timeout -- socket timeout **(Default 5)**
      - debuglevel -- debugging info **(Default false)**
      - proxy -- connect through a proxy server **(http://127.0.0.1:8080)**
      - tor -- use TOR anonmity network **(Default '127.0.0.1', 9050)**
      - agent -- spoof the useragent **(Default random agent from get_userAgent())**
      
#####How To: 
___
~~~
>>> from request import fetch
>>>
>>> # normal GET request
>>> fetch("http://ifconfig.me/ip")
'X.X.X.X\n'
>>>
>>> # enable TOR and increase debug
>>> 'Congratulations.' in fetch("http://check.torproject.org/", tor=1, debuglevel=1)
send: 'GET / HTTP/1.1\r\nAccept-Encoding: identity\r\nHost: check.torproject.org\r\nConnection: close\r\nUser-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205\r\n\r\n'
reply: 'HTTP/1.1 200 OK\r\n'
header: Date: Mon, 05 Aug 2013 10:15:08 GMT
header: Server: Apache
header: Vary: Accept-Encoding
header: Connection: close
header: Transfer-Encoding: chunked
header: Content-Type: text/html; charset=utf-8
True
>>> 
>>> # POST request
>>> import re
>>> hash = "21232f297a57a5a743894a0e4a801fc3"
>>> url = "https://hashcracking.ru/index.php"
>>> src = fetch(url, method='post', params={'hash': hash})
>>> re.findall("<span class='green'>(?P<hash>.+)</span>'", src)
['admin']
>>> 
~~~

#####Screenshoot while intercepting a request_handler's connection using burpsuite:
---
![Alt text](http://s2.postimg.org/ms0etm7d5/handler_proxy.png "burpsuite_requestHandler")
