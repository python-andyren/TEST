import hashlib
import time
import requests
import json
from lxml import etree
import re
import pymysql
from sshtunnel import SSHTunnelForwarder



good_url = 'http://www.wuliy.com/#/details?activityId={}'


def get_img(good_id):
    url = good_url.format(good_id)

    get_img_headers = {
        'Referer': 'http://www.wuliy.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',

    }

    content3 = requests.get(url=url, headers=get_img_headers).content.decode('utf8')

    print(content3)
    #
    # tree1 = etree.HTML(content3)
    #
    # img_list = tree1.xpath('//div[@class="tabCon"]/ul/li/div[2]/p/img/@src')
    #
    # return img_list

get_img(1107124878173011968)