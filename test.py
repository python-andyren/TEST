import hashlib
import time
import requests
import json
from lxml import etree
import re
import pymysql
from sshtunnel import SSHTunnelForwarder

huoli_url = 'http://plm.huolifu.com/comm_plat_huoli/out_bind_info'
content1 = requests.get(url=huoli_url).json()

print(content1)

huoying_url = 'http://plm.huoyingfu.com/comm_plat_shuangying/out_bind_info'
content2 = requests.get(url=huoying_url).json()

print(content2)