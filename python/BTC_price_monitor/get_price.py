#!/usr/bin/env python
#  -*- coding:utf-8 -*-
import urllib2
import json

def http_post():
 
    #server_ip='192.168.168.104'
    get_url='https://api.coinmarketcap.com/v1/ticker/bitcoin/'

    headers={'UserAgent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    request=urllib2.Request(get_url,headers=headers)
    #获得回送的数据
    response=urllib2.urlopen(request)#如果后台没有立即给返回值，则阻塞等待
    ret = response.read()
    return ret
'''
[
    {
        "id": "bitcoin", 
        "name": "Bitcoin", 
        "symbol": "BTC", 
        "rank": "1", 
        "price_usd": "8970.07", 
        "price_btc": "1.0", 
        "24h_volume_usd": "6135570000.0", 
        "market_cap_usd": "151919455678", 
        "available_supply": "16936262.0", 
        "total_supply": "16936262.0", 
        "max_supply": "21000000.0", 
        "percent_change_1h": "0.44", 
        "percent_change_24h": "6.13", 
        "percent_change_7d": "8.62", 
        "last_updated": "1521868767"
    }
]
'''
'''
[{u'market_cap_usd': u'151690138691', u'price_usd': u'8956.53', u'last_updated': \
u'1521869067', u'name': u'Bitcoin', u'24h_volume_usd': u'6132890000.0', u'percent_change_7d': u'8.48',\
 u'symbol': u'BTC', u'max_supply': u'21000000.0', u'rank': u'1', u'percent_change_1h': u'0.27',\
 u'total_supply': u'16936262.0', u'price_btc': u'1.0', u'available_supply': u'16936262.0', \
 u'percent_change_24h': u'5.98', u'id': u'bitcoin'}]
'''
if __name__ == '__main__':
    text = json.loads(http_post())
    print type(text),text
