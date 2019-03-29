# coding=utf-8
import requests
import time
import json
from lxml import etree
import pymysql
from sshtunnel import SSHTunnelForwarder
import csv

# fp = open('0322买号信息.txt', 'a+', encoding='utf8')

add_cookie = input('Cookie:')
add_TimeStamp = input('TimeStamp:')

def to_sql(li):
    # with SSHTunnelForwarder(
    #         ('120.132.65.133', 22),  # B机器的配置
    #         ssh_password=r'*:A8QDe(98KIJx07l\bRm5k/#/3a',
    #         ssh_username='root',
    #         remote_bind_address=('10.9.72.185', 3306)) as server:  # A机器的配置

    db_connect = pymysql.connect(host='10.9.72.185',  # 此处必须是是127.0.0.1
                                 port=3306,
                                 user='root',
                                 passwd='8jN5N8T5v4K5',
                                 db='data_third')

    cursor = db_connect.cursor()

    ww = li[0]

    # bid = li[1]

    base_info = li[1]

    tag = li[2]['标签']

    deep_info = li[3]

    add_time = li[4]

    # mjxy = base_info['买家信誉']
    # sjxy = base_info['商家信誉']
    # sex = base_info['性别']
    # sdhpl = base_info['收到好评率']
    # zcrq = base_info['注册日期']
    # tl = base_info['淘龄']
    # mjzzpj = base_info['买家总周平均']
    # cxsj = base_info['查询时间']
    # nameconform = base_info['是否实名']
    # vip_level = base_info['会员类型']
    # tbhy = base_info['淘宝会员']
    # tz = base_info['打标情况-兔子(拿完了商家的返款就恶意退款跑了！)']
    # mh = base_info['打标情况-蜜獾(用各种方式威胁你给钱！)']
    # hl = base_info['打标情况-狐狸(用各种方式骗你钱了！)']
    # eyu = base_info['打标情况-鳄鱼(用工商，发票，字体，商标，假货各种方式来坑你钱了！)']
    # jq = base_info['打标情况-降权处置']
    # black = base_info['云黑名单']

    # Average_number = deep_info['近一季度平均周成交次数:']
    # xfl = deep_info['消费力:']
    # yhdy = deep_info['用户地域:']
    # fchpl = deep_info['发出好评率:']
    # gmpl = deep_info['购买频率:']
    # yhtkl = deep_info['用户退款率:']
    # zdph = deep_info['终端偏好:']

    # 拼接sql语句
    sql = 'insert into shuangying_huoyingfu(ww,buyreputation,bussreputation,sex,favrate,regdate,amoyage,buyweeklyaver,querytime,real_name,vip_level,vip_info,tucao,tuzi,mihuan,huli,eyu,disposalsitus,blacklist,label,averagetimes,consumpower,userarea,sendrate,buyfrequency,userrefund,terminal,add_time) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d")' % (
        ww,
        base_info['买家信誉'], base_info['商家信誉'], base_info['性别'], base_info['收到好评率'], base_info['注册日期'], base_info['淘龄'], base_info['买家总周平均'], base_info['查询时间'], base_info['是否实名'], base_info['会员类型'], base_info['淘宝会员'],
        base_info['吐槽'],base_info['打标情况-兔子'], base_info['打标情况-蜜獾'], base_info['打标情况-狐狸'], base_info['打标情况-鳄鱼'], base_info['打标情况-降权处置'], base_info['云黑名单'],
        tag,deep_info['近一季度平均周成交次数'],deep_info['消费力'],deep_info['用户地域'],deep_info['发出好评率'],deep_info['购买频率'],deep_info['用户退款率'],deep_info['终端偏好'],add_time)
    # 执行sql语句
    try:
        cursor.execute(sql)
        db_connect.commit()
        print('插入成功')
    except Exception as e:
        print(e)
        db_connect.rollback()
    cursor.close()
    db_connect.close()

def get_tag(name):
    headers_tag = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '51',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': add_cookie,
        'Host': 'app.tk1788.com',
        'Origin': 'http://app.tk1788.com',
        'Referer': 'http://app.tk1788.com/app/superscan/searchAliim.jsp',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    tag_data = {
        'm': 'tagSearch',
        'aliim': name
    }

    content3 = requests.post('http://app.tk1788.com/app/superscan/op.jsp', data=tag_data, headers=headers_tag).text

    time.sleep(4)

    return content3

def get_sign(name):
    headers_getSign = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '76',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': add_cookie,
        'Host': 'app.tk1788.com',
        'Origin': 'http://app.tk1788.com',
        'Referer': 'http://app.tk1788.com/app/superscan/searchAliim.jsp',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data_getSign = {
        'm': 'getSign',
        'aliim': name,
        'timeStamp': add_TimeStamp,
    }

    content1 = requests.post(url='http://app.tk1788.com/app/superscan/op.jsp', headers=headers_getSign,
                             data=data_getSign).text

    sign_data = json.loads(content1)

    return sign_data

def Deep_Search(regist_day, sign, name):
    headers_DeepSearch = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '142',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': add_cookie,
        'Host': 'app.tk1788.com',
        'Origin': 'http://app.tk1788.com',
        'Referer': 'http://app.tk1788.com/app/superscan/searchAliim.jsp',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data_DeepSearch = {
        'm': 'deepSearchAliim',
        'aliim': name,
        'buyNum': '',
        'registDay': regist_day,
        'timeStamp': add_TimeStamp,
        'sign': sign,
    }

    content4 = requests.post(url='http://app.tk1788.com/app/superscan/op.jsp', headers=headers_DeepSearch,
                             data=data_DeepSearch).text

    time.sleep(2)

    data_Deep_Search = json.loads(content4)

    return data_Deep_Search

add_time = int(time.strftime('%Y%m%d', time.localtime(time.time())))

# huoying_url = 'http://plm.huoyingfu.com/comm_plat_shuangying/out_bind_info'
# content = requests.get(url=huoying_url).json()

content = [{'account_name': 'christgirl88'}, {'account_name': 'dayaojia1122'}, {'account_name': 'cly世界'}, {'account_name': 'd880303'}, {'account_name': 'clocky1234'}, {'account_name': 'daibogui'}, {'account_name': 'cwf612612'}, {'account_name': 'dcl273470641'}, {'account_name': 'cyl201702'}, {'account_name': 'cruel_2008'}, {'account_name': 'cxxjcst'}, {'account_name': 'dai976472098'}, {'account_name': 'dd0414艳'}, {'account_name': 'cuidazhaowg123'}, {'account_name': 'c惟爱你c'}, {'account_name': 'cyp么么哒83520'}, {'account_name': 'cssmcgrady'}, {'account_name': 'czylrr'}, {'account_name': 'cs200991'}, {'account_name': 'cyh15875177143'}, {'account_name': 'cl0123'}, {'account_name': 'cowboybaby'}, {'account_name': 'czh华仔哥cxh'}, {'account_name': 'cwq888vip'}, {'account_name': 'cwqqwe'}, {'account_name': 'cuisite579'}, {'account_name': 'coolei0114'}, {'account_name': 'cxm3166'}, {'account_name': 'circe3'}, {'account_name': 'crise80523'}, {'account_name': 'damihaoran'}, {'account_name': 'cx876278707'}, {'account_name': 'ck1988qx'}, {'account_name': 'dcy7389'}, {'account_name': 'cjf1049467806'}, {'account_name': 'cucczxw'}, {'account_name': 'cycmay2003'}, {'account_name': 'cpo蛋'}, {'account_name': 'cooeells'}, {'account_name': 'cljljljl'}, {'account_name': 'cx915150085'}, {'account_name': 'clover1517056'}, {'account_name': 'cjj8776419'}, {'account_name': 'dalushuhua2015'}, {'account_name': 'cjl5201982526'}, {'account_name': 'coder2005'}, {'account_name': 'clx2561184'}, {'account_name': 'cjacz1314'}, {'account_name': 'daisy881108'}, {'account_name': 'cyycxt'}, {'account_name': 'chusong1010'}, {'account_name': 'cx承旭'}, {'account_name': 'chm73901642'}, {'account_name': 'dan13702147'}, {'account_name': 'd1060934096'}, {'account_name': 'crowslovecn'}, {'account_name': 'cz前街小子'}, {'account_name': 'cwq4312'}, {'account_name': 'dan0114dan'}, {'account_name': 'daniellytian'}, {'account_name': 'clp358386136'}, {'account_name': 'cyjzjh325'}, {'account_name': 'cyjnihao99'}, {'account_name': 'chuniuniu822'}, {'account_name': 'congcong19890202'}, {'account_name': 'coco婷婷7'}, {'account_name': 'danteng殇'}, {'account_name': 'darkyu2006'}, {'account_name': 'cqdjzgp'}, {'account_name': 'cyh0001202'}, {'account_name': 'dc月色朦胧'}, {'account_name': 'cuirensheng'}, {'account_name': 'cjw880905'}, {'account_name': 'dalushuhua1'}, {'account_name': 'cxy陈650993'}, {'account_name': 'cxlli11'}, {'account_name': 'cjl一帘幽梦'}, {'account_name': 'cw9622668'}, {'account_name': 'cytheria格格8023'}, {'account_name': 'clgwdhao'}, {'account_name': 'ckc199109'}, {'account_name': 'cyf106飞飞'}, {'account_name': 'clr112飘影伊人'}, {'account_name': 'cocoey6'}, {'account_name': 'coolyzx'}, {'account_name': 'cszn10086'}, {'account_name': 'cuizicen'}, {'account_name': 'cy18017383250'}, {'account_name': 'cui64085109'}, {'account_name': 'chuchun07'}, {'account_name': 'cjm2sz'}, {'account_name': 'dashu52121'}, {'account_name': 'cy13368187193'}, {'account_name': 'crystalzongzi'}, {'account_name': 'daiqian123410'}, {'account_name': 'dan32158'}, {'account_name': 'cy15068822673'}, {'account_name': 'cleolla'}, {'account_name': 'cong135987'}, {'account_name': 'dc雨荷'}, {'account_name': 'cyq820110'}, {'account_name': 'cq第6个'}, {'account_name': 'daiboaijiao520'}, {'account_name': 'cx1984525894000'}, {'account_name': 'Cj叶良辰'}, {'account_name': 'cyj85152333'}, {'account_name': 'cong995'}, {'account_name': 'day大大'}, {'account_name': 'cmc520dxf1'}, {'account_name': 'cjh6243857'}, {'account_name': 'danfight'}, {'account_name': 'dajiadajidj'}, {'account_name': 'cx红玫瑰9'}, {'account_name': 'cjx13626090802'}, {'account_name': 'cui002356916'}, {'account_name': 'dcba延勇'}, {'account_name': 'chiuchiu814'}, {'account_name': 'd88421152'}, {'account_name': 'ctubox'}, {'account_name': 'crs518815'}, {'account_name': 'clonechen_taobao'}, {'account_name': 'darkkite'}, {'account_name': 'cowbrotherboy2012'}, {'account_name': 'cyy1099267409'}, {'account_name': 'dangdang198666'}, {'account_name': 'cyj211314'}, {'account_name': 'curve曲线'}, {'account_name': 'cinderella林168'}, {'account_name': 'daney790405'}, {'account_name': 'csldw'}, {'account_name': 'daimeian221'}, {'account_name': 'ch梓诺墨'}, {'account_name': 'cqbgn4600'}, {'account_name': 'da大饼14'}, {'account_name': 'daijingna'}, {'account_name': 'dahai303792962'}, {'account_name': 'cyndyyang'}, {'account_name': 'dahan_99'}, {'account_name': 'davidsonyu'}, {'account_name': 'd1343109596'}, {'account_name': 'cmt17826255513'}, {'account_name': 'daidai901023'}, {'account_name': 'chunheise1314'}, {'account_name': 'chs就是我'}, {'account_name': 'dalmd'}, {'account_name': 'dabaitu奶糖11'}, {'account_name': 'ckz297355524'}, {'account_name': 'danyang_lh'}, {'account_name': 'cool_1314521'}, {'account_name': 'cyqrjy'}, {'account_name': 'cj1987161'}, {'account_name': 'cwy快乐人生'}, {'account_name': 'dangshen07'}, {'account_name': 'chungspring'}, {'account_name': 'dcfswana'}, {'account_name': 'cxq19810107'}, {'account_name': 'chlpe3'}, {'account_name': 'clf11920'}, {'account_name': 'chl望天'}, {'account_name': 'crp离陌'}, {'account_name': 'congyin0312'}, {'account_name': 'colf01016'}, {'account_name': 'crskyzx'}, {'account_name': 'dan青春万岁'}, {'account_name': 'cuffsdouglas'}, {'account_name': 'chunhuawei58'}, {'account_name': 'clock钟1'}, {'account_name': 'cong20161003'}, {'account_name': 'db13736595095'}, {'account_name': 'chxl8095'}, {'account_name': 'cuna80636'}, {'account_name': 'cxw7668120'}, {'account_name': 'cx2009sdb'}, {'account_name': 'cyy877490396'}, {'account_name': 'cy_蓝枫叶'}, {'account_name': 'chy新星'}, {'account_name': 'cyn小娜娜'}, {'account_name': 'cong5288'}, {'account_name': 'csymrtguyan'}, {'account_name': 'cyazy丫头'}, {'account_name': 'cyzxn12373325234'}, {'account_name': 'Combiil'}, {'account_name': 'cn167linyun'}, {'account_name': 'cuichunting'}, {'account_name': 'dan时光若止'}, {'account_name': 'crooked狂风'}, {'account_name': 'claireeee111'}, {'account_name': 'ctycat'}, {'account_name': 'cuiyeye'}, {'account_name': 'cjy羽羽'}, {'account_name': 'conbry'}, {'account_name': 'cong169'}, {'account_name': 'cxl134139'}, {'account_name': 'daliqi718'}, {'account_name': 'coco来哪'}, {'account_name': 'clarklee2'}, {'account_name': 'chywt0'}, {'account_name': 'daimeian'}, {'account_name': 'chr15889'}, {'account_name': 'clf陈霖烽'}, {'account_name': 'chonglai12014'}, {'account_name': 'cyf_wc521'}, {'account_name': 'dcgfd么'}, {'account_name': 'dasenyien'}, {'account_name': 'cz陈展'}, {'account_name': 'chris蜻蜓仔'}, {'account_name': 'dd83569'}, {'account_name': 'chunxiaqiudong'}, {'account_name': 'cuizhihua11'}, {'account_name': 'csl0980'}, {'account_name': 'cuijiansheng99'}, {'account_name': 'cm19902880'}, {'account_name': 'daisy15297239'}, {'account_name': 'chrisleecornchris'}, {'account_name': 'CJC762726'}, {'account_name': 'cnnbry'}, {'account_name': 'cissywong2014'}, {'account_name': 'cls珊宝'}, {'account_name': 'dang_xx'}, {'account_name': 'chx1234565'}, {'account_name': 'cmm5666870'}, {'account_name': 'css19820728'}, {'account_name': 'dalin对自己好点'}, {'account_name': 'cy9559'}, {'account_name': 'cyt807127919'}, {'account_name': 'comfortable23168948'}, {'account_name': 'cs2236'}, {'account_name': 'congshibo'}, {'account_name': 'cindywoaiwojia'}, {'account_name': 'cxjcoolboy'}, {'account_name': 'chxchl123456789'}, {'account_name': 'dadang258'}, {'account_name': 'consider256'}, {'account_name': 'dandycoco'}, {'account_name': 'cq第三个'}, {'account_name': 'daxxx7821'}, {'account_name': 'ckjjha'}, {'account_name': 'czwxpc'}, {'account_name': 'cypcftx'}, {'account_name': 'db528927'}, {'account_name': 'congsiyu2'}, {'account_name': 'daixiaoyu123321'}, {'account_name': 'clw19891111'}, {'account_name': 'coneja1228'}, {'account_name': 'ct陈涛66'}, {'account_name': 'd32325656'}, {'account_name': 'cr982096529'}, {'account_name': 'dancing_kitty23'}, {'account_name': 'dalushuhua2018'}, {'account_name': 'cui_vampire'}, {'account_name': 'cola7796'}, {'account_name': 'c_henyingbo'}, {'account_name': 'coong1hao'}, {'account_name': 'chy8893'}, {'account_name': 'davidluisea'}, {'account_name': 'cyp南城旧梦'}, {'account_name': 'dc今生有缘'}, {'account_name': 'cryangel198725184'}, {'account_name': 'cndwaugvwufgfd'}, {'account_name': 'cyp1538'}, {'account_name': 'dc相思豆'}, {'account_name': 'cl019'}, {'account_name': 'consider253'}, {'account_name': 'cxx765808837'}, {'account_name': 'cuijianghong888'}, {'account_name': 'dashuai9898'}, {'account_name': 'dafufeifei'}, {'account_name': 'chongzi20143'}, {'account_name': 'dagangshenqi'}, {'account_name': 'csd12399999'}, {'account_name': 'cndtbh'}, {'account_name': 'colorful2008'}, {'account_name': 'chuyunierburande'}, {'account_name': 'danaewd'}, {'account_name': 'connie7125'}, {'account_name': 'chylyl2013'}, {'account_name': 'cindy20004'}, {'account_name': 'dadada12345623923241'}, {'account_name': 'cui02407226'}, {'account_name': 'cookielttt'}, {'account_name': 'ct12322'}, {'account_name': 'cucu1234_2008'}, {'account_name': 'chixiuluo'}, {'account_name': 'cxj9279'}, {'account_name': 'dabao12375'}, {'account_name': 'dangdaa'}, {'account_name': 'CT幸福821377930'}, {'account_name': 'dashuai0912'}, {'account_name': 'chplus'}, {'account_name': 'cnng96'}, {'account_name': 'cws似水'}, {'account_name': 'cibmooo'}, {'account_name': 'daijiaxing5188'}, {'account_name': 'cuiliting001'}, {'account_name': 'czs18219141387'}, {'account_name': 'cyh72300'}, {'account_name': 'dailijun1988'}, {'account_name': 'dakan2830'}, {'account_name': 'cpk4zj3f'}, {'account_name': 'cxy199955小白'}, {'account_name': 'daijiangbo1919'}, {'account_name': 'coo7891'}, {'account_name': 'cz铭di'}, {'account_name': 'cyn宝贝yn'}, {'account_name': 'cookieltt'}, {'account_name': 'clwhappy8168'}, {'account_name': 'crazy灬万万'}, {'account_name': 'chois汽香伊'}, {'account_name': 'conine005'}, {'account_name': 'danhui0109'}, {'account_name': 'cui5843719'}, {'account_name': 'daa26905'}, {'account_name': 'cyf820610'}, {'account_name': 'chunxiaoali'}, {'account_name': 'czhen0720'}, {'account_name': 'cuijianqiang_1991'}, {'account_name': 'cxiu秀'}, {'account_name': 'csxhaha1'}, {'account_name': 'chp114160'}, {'account_name': 'cxl15844315001'}, {'account_name': 'ctwrc520'}, {'account_name': 'cy0452060409'}, {'account_name': 'd2535382861'}, {'account_name': 'cuikexin981'}, {'account_name': 'chwshr'}, {'account_name': 'ch洪基'}, {'account_name': 'cxwxf23'}, {'account_name': 'cqchccjw5569617'}, {'account_name': 'cucnyinan'}, {'account_name': 'cream198852'}, {'account_name': 'dazhangwai'}, {'account_name': 'cuigui99'}, {'account_name': 'clz168'}, {'account_name': 'cyc140821'}, {'account_name': 'dawangyi1'}, {'account_name': 'dalinxl'}, {'account_name': 'cjjabc19851113'}, {'account_name': 'db850323'}, {'account_name': 'cuixiaona2'}, {'account_name': 'dashan996'}, {'account_name': 'cuirongqin'}, {'account_name': 'c龙龙a'}, {'account_name': 'cly18068156506'}, {'account_name': 'clay陈'}, {'account_name': 'dajidalilalala'}, {'account_name': 'dan111_33dan'}, {'account_name': 'chong6187'}, {'account_name': 'cindys'}, {'account_name': 'colacokeke'}, {'account_name': 'cqx201488'}, {'account_name': 'dandan022995105488'}, {'account_name': 'chong3230'}, {'account_name': 'cz苏炜基'}, {'account_name': 'cykzlh'}, {'account_name': 'cjwzcr幸福'}, {'account_name': 'constantin1985'}, {'account_name': 'csboy88'}, {'account_name': 'dandan92938590'}, {'account_name': 'cjccyjcrg'}, {'account_name': 'cpucc123'}, {'account_name': 'cmzcwx'}, {'account_name': 'dayashabi'}, {'account_name': 'czza2288'}, {'account_name': 'cqs83163942'}, {'account_name': 'david_zhangyuan'}, {'account_name': 'cmzooobgnsd'}, {'account_name': 'colourkuang'}, {'account_name': 'cn小资女人2'}, {'account_name': 'david8788888'}, {'account_name': 'cy1285'}, {'account_name': 'cle131452000'}, {'account_name': 'ctlsj'}, {'account_name': 'cnq6789'}, {'account_name': 'c饭泡粥'}, {'account_name': 'cx704743125'}, {'account_name': 'csp4053'}, {'account_name': 'cmw崔明旺'}, {'account_name': 'cyq13145208'}, {'account_name': 'chl480527'}, {'account_name': 'dawdlefish'}, {'account_name': 'dawen19880423'}, {'account_name': 'cjdcj曾经的曾经'}, {'account_name': 'crlbinbin'}, {'account_name': 'cjy109356854'}, {'account_name': 'czx简简单单'}, {'account_name': 'chuntian8_2009'}, {'account_name': 'daixixue33'}, {'account_name': 'dawnsun88'}, {'account_name': 'cntanghuacn'}, {'account_name': 'chungkayo'}, {'account_name': 'damiano_cn'}, {'account_name': 'cr扑克脸'}, {'account_name': 'daodaoqqz'}, {'account_name': 'csol菜鸟bt'}, {'account_name': 'chsi7835'}, {'account_name': 'cly2978038151'}, {'account_name': 'danceoffirefiles'}, {'account_name': 'ckz813388540'}, {'account_name': 'chiuchiu18'}, {'account_name': 'chj8401'}, {'account_name': 'daisy79889507618'}, {'account_name': 'c心向未来'}, {'account_name': 'crazychenkaishan'}, {'account_name': 'dcyang129'}, {'account_name': 'crisas'}, {'account_name': 'dachanli'}, {'account_name': 'cly901226'}, {'account_name': 'daya914'}, {'account_name': 'dadwwww'}, {'account_name': 'cqhb17'}, {'account_name': 'crysis丶'}, {'account_name': 'ckj00000'}, {'account_name': 'dafang345085617'}, {'account_name': 'cyp12105'}, {'account_name': 'dc34350'}, {'account_name': 'cwxaihhh'}, {'account_name': 'cwdhml'}, {'account_name': 'chowhiuwun'}, {'account_name': 'chunjie369'}, {'account_name': 'chrislee117'}, {'account_name': 'ctwrc120'}, {'account_name': 'ch快乐go'}, {'account_name': 'cuandojoven'}, {'account_name': 'chunheise8585706'}, {'account_name': 'd811067612'}, {'account_name': 'da伟伟7750450'}, {'account_name': 'CN淘物乐'}, {'account_name': 'czm472670736'}, {'account_name': 'cjbcyq65'}, {'account_name': 'daiyanguo199262'}, {'account_name': 'congzai1424'}, {'account_name': 'cuidian2017'}, {'account_name': 'cyggenmcl86030'}, {'account_name': 'crazyc杨'}, {'account_name': 'dasoup'}, {'account_name': 'cy851027'}, {'account_name': 'CY浩纯'}, {'account_name': 'chinhnan'}, {'account_name': 'csyljy222'}, {'account_name': 'cl0846'}, {'account_name': 'cshcshcshcshcshcsh'}, {'account_name': 'cxl212'}, {'account_name': 'daisy5934'}, {'account_name': 'CL风味茄子'}, {'account_name': 'csyljy111'}, {'account_name': 'cyrcjlc'}, {'account_name': 'chinikuo1020'}, {'account_name': 'cyx821026'}, {'account_name': 'cwkwx'}, {'account_name': 'cidy23'}, {'account_name': 'cnyg90'}, {'account_name': 'clq888886'}, {'account_name': 'cjj9309061'}, {'account_name': 'chuxing12345654692209'}, {'account_name': 'csc13960311995'}, {'account_name': 'CXY4481'}, {'account_name': 'connielin1972'}, {'account_name': 'dazhuang1209'}, {'account_name': 'cocl82'}, {'account_name': 'cxh18254698861'}, {'account_name': 'comatday'}, {'account_name': 'cqmjxf'}, {'account_name': 'd402396'}, {'account_name': 'cjh890416'}, {'account_name': 'davysmo'}, {'account_name': 'chushi130533'}, {'account_name': 'dazexiaoze'}, {'account_name': 'cxy949672624'}, {'account_name': 'cky890412'}, {'account_name': 'chrison1106'}, {'account_name': 'dasesong'}, {'account_name': 'czh041205'}, {'account_name': 'cxp313875153'}, {'account_name': 'ciy1017'}, {'account_name': 'cora_wenwen'}, {'account_name': 'chirsjem'}, {'account_name': 'cvjcdoc'}, {'account_name': 'cpu276'}, {'account_name': 'cltf'}, {'account_name': 'cyl_0753'}, {'account_name': 'dddqdkp24813'}, {'account_name': 'daijie1987'}, {'account_name': 'dd20461'}, {'account_name': 'dangkaiyu111'}, {'account_name': 'congcong846391950'}, {'account_name': 'cludy'}, {'account_name': 'cuihangrui641700'}, {'account_name': 'chiouyuyuan'}, {'account_name': 'chocolate78817'}, {'account_name': 'cic3da'}, {'account_name': 'citic_zmj'}, {'account_name': 'ckckws'}, {'account_name': 'choubao925317'}, {'account_name': 'cj394401925'}, {'account_name': 'daiyuben69'}, {'account_name': 'cz啷个哩个啷'}, {'account_name': 'czw陈梓炜'}, {'account_name': 'czx08041'}, {'account_name': 'd8825801'}, {'account_name': 'chy133800020'}, {'account_name': 'dd18818'}, {'account_name': 'cocong1'}, {'account_name': 'cxy秀英88'}, {'account_name': 'chintclf'}, {'account_name': 'cholatescream'}, {'account_name': 'cvghy'}, {'account_name': 'chixiong31'}, {'account_name': 'c幸福四叶草c'}, {'account_name': 'coco154'}, {'account_name': 'chuhung68'}, {'account_name': 'coast413'}, {'account_name': 'cy258164403'}, {'account_name': 'cxh平凡人'}, {'account_name': 'chun05790579'}, {'account_name': 'czgrjj馨颖'}, {'account_name': 'cpu634'}, {'account_name': 'chuyanlingwy'}, {'account_name': 'ct2846'}, {'account_name': 'crystal5004'}, {'account_name': 'cxt筱婷'}, {'account_name': 'c周g荷zk3sc6'}, {'account_name': 'coco丽1338'}, {'account_name': 'chuxingyou521'}, {'account_name': 'daiyusong511901'}, {'account_name': 'cyj861017'}, {'account_name': 'cml15222991002'}, {'account_name': 'ct893906001'}, {'account_name': 'closedcjt'}, {'account_name': 'daodan2583'}, {'account_name': 'daisy楚人美'}, {'account_name': 'columbia1314'}, {'account_name': 'cmr129'}, {'account_name': 'ddddddd899519665'}, {'account_name': 'cjh890316'}, {'account_name': 'cyc0817'}, {'account_name': 'corinnelyon'}, {'account_name': 'dawaciren73869125'}, {'account_name': 'cjy95270'}, {'account_name': 'cz976077791'}, {'account_name': 'cuiping890617'}, {'account_name': 'cym12345cym'}, {'account_name': 'cyh393867221'}, {'account_name': 'ch_x_l'}, {'account_name': 'dabai同学'}, {'account_name': 'CZC1004'}, {'account_name': 'dckdqk'}, {'account_name': 'cuihehe'}, {'account_name': 'daleilei88'}, {'account_name': 'cuweimao776'}, {'account_name': 'crs5651'}, {'account_name': 'dahuwuqu'}, {'account_name': 'cmp681899'}, {'account_name': 'chiouchieh'}, {'account_name': 'cxzyw1'}, {'account_name': 'cjclxj1128'}, {'account_name': 'compoq76766'}, {'account_name': 'config789'}, {'account_name': 'dai13764'}, {'account_name': 'cui725000'}, {'account_name': 'cympn'}, {'account_name': 'colerfean_2005'}, {'account_name': 'ctockne77313'}, {'account_name': 'cswsunny'}, {'account_name': 'cqweixiaoli'}, {'account_name': 'clr543'}, {'account_name': 'coffcoff123'}, {'account_name': 'chunyan19880225'}, {'account_name': 'c枫o沈2wux'}, {'account_name': 'cncj025'}, {'account_name': 'dcjlayhxx11533'}, {'account_name': 'c梓彬'}, {'account_name': 'dandanchun003'}, {'account_name': 'dahai2008hebei'}, {'account_name': 'cxm891111'}, {'account_name': 'd1023190284'}, {'account_name': 'cool小迷弟'}, {'account_name': 'cyb开拓者'}, {'account_name': 'chu8701'}, {'account_name': 'cnzyn'}, {'account_name': 'czhczh2171'}, {'account_name': 'cuiyongqian0515'}, {'account_name': 'dapangpan'}, {'account_name': 'danielwellington_space'}, {'account_name': 'chuanqi0017'}, {'account_name': 'd6484'}, {'account_name': 'cmbc_95568'}, {'account_name': 'cyj嘉'}, {'account_name': 'cui123455'}, {'account_name': 'cwl593312849'}, {'account_name': 'daisy19851986'}, {'account_name': 'crdj574916554'}, {'account_name': 'CL15852735202'}, {'account_name': 'chuhongmei333'}, {'account_name': 'chunqingezu'}, {'account_name': 'chuntaoi22'}, {'account_name': 'cj5674122'}, {'account_name': 'cx最佳了'}, {'account_name': 'cui13723177018'}, {'account_name': 'dannymt'}, {'account_name': 'dai244814137'}, {'account_name': 'cream_815'}, {'account_name': 'cxcsmile'}, {'account_name': 'cycumonk'}, {'account_name': 'd6zdz17'}, {'account_name': 'chuanle512'}, {'account_name': 'cle2009'}, {'account_name': 'ddbb6199566'}, {'account_name': 'dashan499533929'}, {'account_name': 'cknygg888'}, {'account_name': 'c忆笙'}, {'account_name': 'clm19810728'}, {'account_name': 'ddaixuwei'}, {'account_name': 'cyw3060377'}, {'account_name': 'cwyzmhrr660'}, {'account_name': 'daoren76113772'}, {'account_name': 'datouwoaini5211314'}, {'account_name': 'cws19951226'}, {'account_name': 'czkhcj'}, {'account_name': 'cyjwdy'}, {'account_name': 'dad2007'}, {'account_name': 'cynthiaks'}, {'account_name': 'cuiwensheng19870911'}, {'account_name': 'cjw118378'}, {'account_name': 'danney9987'}, {'account_name': 'cs2861'}, {'account_name': 'danyuananhao'}, {'account_name': 'cloudy147'}, {'account_name': 'dd15894853939'}, {'account_name': 'cqy7895'}, {'account_name': 'cjy嗳慌恋'}, {'account_name': 'cq2i8oau6'}, {'account_name': 'daisy丶恩'}, {'account_name': 'cj1185824326'}, {'account_name': 'cjichao123'}, {'account_name': 'chongwu1002'}, {'account_name': 'daichunyu1230'}, {'account_name': 'daynjwynjh8866'}, {'account_name': 'chunlin331688'}, {'account_name': 'csp11111'}, {'account_name': 'cqx19880806'}, {'account_name': 'choushen'}, {'account_name': 'coco_1997'}, {'account_name': 'darkstar4k'}, {'account_name': 'cing0501'}, {'account_name': 'dd851230'}, {'account_name': 'cqdtxorc808'}, {'account_name': 'cyn12900'}, {'account_name': 'contilenasqt'}, {'account_name': 'congbode'}, {'account_name': 'dantat'}, {'account_name': 'cs1988928'}, {'account_name': 'cslmm'}, {'account_name': 'ctrl花舞街'}, {'account_name': 'cuiying冰心'}, {'account_name': 'coco_19860305'}, {'account_name': 'clist917'}, {'account_name': 'cz891124'}, {'account_name': 'congtoukaishi1980'}, {'account_name': 'cp250171222'}, {'account_name': 'concert00'}, {'account_name': 'dayu2000'}, {'account_name': 'cristina_meow'}, {'account_name': 'crest2001'}, {'account_name': 'cynthiayv'}, {'account_name': 'cxz19850912'}, {'account_name': 'darkcat0815'}, {'account_name': 'cxl286136773'}, {'account_name': 'chunfen58888'}, {'account_name': 'cpu048'}, {'account_name': 'crazycir'}, {'account_name': 'd57452'}, {'account_name': 'dawn明'}, {'account_name': 'cp920626'}, {'account_name': 'c好男人不止曾小贤'}, {'account_name': 'cw131011'}, {'account_name': 'cqp20111'}, {'account_name': 'czl618452'}, {'account_name': 'c蔡18788558855'}, {'account_name': 'cly1176937192'}, {'account_name': 'dagelin123321'}, {'account_name': 'czk23881018'}, {'account_name': 'cz112898469'}, {'account_name': 'daiyun10'}, {'account_name': 'cltxx55'}, {'account_name': 'danni415109'}, {'account_name': 'd405075787'}, {'account_name': 'cici2vivi'}, {'account_name': 'da113143605'}, {'account_name': 'daimai915'}, {'account_name': 'clz真逸'}, {'account_name': 'chkiki33'}, {'account_name': 'chqing34'}, {'account_name': 'ch大队长'}, {'account_name': 'daisy木木子'}, {'account_name': 'cici_赵'}, {'account_name': 'daisycausten'}, {'account_name': 'cydbx'}, {'account_name': 'cp988204'}, {'account_name': 'chupbb'}, {'account_name': 'daxinbag'}, {'account_name': 'damo93'}, {'account_name': 'ck16819018'}, {'account_name': 'cywznq'}, {'account_name': 'choubaozhouss'}, {'account_name': 'copyly爱情'}, {'account_name': 'cmj123459'}, {'account_name': 'dat99'}, {'account_name': 'cyp平'}, {'account_name': 'c快乐宠吧'}, {'account_name': 'cuicui627'}, {'account_name': 'daxiangbna'}, {'account_name': 'cjj502490506'}, {'account_name': 'cyghxqcyf'}, {'account_name': 'cuiyunya820913'}, {'account_name': 'cookie906'}, {'account_name': 'cys7417'}, {'account_name': 'chlin20130408'}, {'account_name': 'cuiqiang1982'}, {'account_name': 'cyh2688fg'}, {'account_name': 'coffeebean2009'}, {'account_name': 'cxj请稍后'}, {'account_name': 'cui123476'}, {'account_name': 'cqbltb'}, {'account_name': 'cloud赟'}, {'account_name': 'cqb0603'}, {'account_name': 'csskb123'}, {'account_name': 'czjhbs'}, {'account_name': 'crs20051220'}, {'account_name': 'cjwcjw240'}, {'account_name': 'coldtea82'}, {'account_name': 'dangdang599'}, {'account_name': 'davidlu1992'}, {'account_name': 'cynthiajyj'}, {'account_name': 'daidingdaiding'}, {'account_name': 'daiguofenga'}, {'account_name': 'crazyjolie'}, {'account_name': 'cl梦雨的乐乐'}, {'account_name': 'danxiangsi111'}, {'account_name': 'datou2003090018'}, {'account_name': 'cty87512'}, {'account_name': 'clnljj'}, {'account_name': 'daf827'}, {'account_name': 'dawdg1'}, {'account_name': 'cs_shuo'}, {'account_name': 'ct115703'}, {'account_name': 'cn19113'}, {'account_name': 'cindyzuojia'}, {'account_name': 'cuiwei_728'}, {'account_name': 'danjiaong'}, {'account_name': 'cpp_008_2008'}, {'account_name': 'cloudsingza'}, {'account_name': 'davedenglee'}, {'account_name': 'ckwhrq'}, {'account_name': 'cwx3668'}, {'account_name': 'colorful_dye'}, {'account_name': 'danhong1108'}, {'account_name': 'clear4179'}, {'account_name': 'csuczj'}, {'account_name': 'cx450989695'}, {'account_name': 'christina疯癫喃'}, {'account_name': 'cjx236'}, {'account_name': 'dark辉space'}, {'account_name': 'danjuju'}, {'account_name': 'cx13678677860'}, {'account_name': 'czhen126'}, {'account_name': 'chuyang94609'}, {'account_name': 'cicly女王荟'}, {'account_name': 'colourmm1'}, {'account_name': 'danidexing1'}, {'account_name': 'clflj'}, {'account_name': 'cpr1983'}, {'account_name': 'chongbaba_tl'}, {'account_name': 'crb13960862754'}, {'account_name': 'dayday电玩批发'}, {'account_name': 'cwy陈小妞'}, {'account_name': 'collora'}, {'account_name': 'chsh0310'}, {'account_name': 'crazy苗宝0822'}, {'account_name': 'd15253080825'}, {'account_name': 'cqy213'}, {'account_name': 'corso0399'}, {'account_name': 'cy12340'}, {'account_name': 'cp198988'}, {'account_name': 'csr20120818'}, {'account_name': 'cyp870923'}, {'account_name': 'czdawei996'}, {'account_name': 'cl565619945'}, {'account_name': 'Daemon1998'}, {'account_name': 'dbl18827511705'}, {'account_name': 'conglin5200'}, {'account_name': 'darcy007'}, {'account_name': 'cl07051213'}, {'account_name': 'darling路0509'}, {'account_name': 'cjxyru'}, {'account_name': 'coto800727'}, {'account_name': 'cxf025'}, {'account_name': 'cp1187476972'}, {'account_name': 'cisco_f1sh'}, {'account_name': 'dc102888'}, {'account_name': 'cs点点点'}, {'account_name': 'cxn19821015'}, {'account_name': 'cjkileko'}, {'account_name': 'clr08'}, {'account_name': 'cr15696550402'}, {'account_name': 'dangguoning123456'}, {'account_name': 'cys83120'}, {'account_name': 'dailei002'}, {'account_name': 'come亮仔on'}, {'account_name': 'chiwa1015'}, {'account_name': 'clee41'}, {'account_name': 'c陈鹏飞f'}, {'account_name': 'cnywwjx88'}, {'account_name': 'cjf1972329'}, {'account_name': 'cqfy70fyx'}, {'account_name': 'da大饼'}, {'account_name': 'cplove538'}, {'account_name': 'csli2012'}, {'account_name': 'cyjt2008'}, {'account_name': 'cythcg'}, {'account_name': 'cjhxyx'}, {'account_name': 'czbgff110'}, {'account_name': 'clx198799'}, {'account_name': 'cqh12593'}, {'account_name': 'cxz8877999'}, {'account_name': 'daijing跳跳'}, {'account_name': 'closergirl09'}, {'account_name': 'coralineluo'}, {'account_name': 'crazy哞哞'}, {'account_name': 'cwkhgib'}, {'account_name': 'crybuaaron'}, {'account_name': 'chunaidongailiang'}, {'account_name': 'dan默念幸福'}, {'account_name': 'cl90999'}, {'account_name': 'coco桃子3529'}, {'account_name': 'cx左耳'}, {'account_name': 'cyn893383'}, {'account_name': 'dandancall88'}, {'account_name': 'chl88888888'}, {'account_name': 'daobeiyuan'}, {'account_name': 'czhen09'}, {'account_name': 'chunyu258369'}, {'account_name': 'cyhzone'}, {'account_name': 'cuijiale99'}, {'account_name': 'coco李婷8976'}, {'account_name': 'chuazhen92'}, {'account_name': 'czh881021'}, {'account_name': 'daihaichen'}, {'account_name': 'ck154198116'}, {'account_name': 'cxgj1985'}, {'account_name': 'csz355407'}, {'account_name': 'csohmygod'}, {'account_name': 'czy月下静海'}, {'account_name': 'cy2009_love'}, {'account_name': 'czz_624'}, {'account_name': 'cinderella美美美'}, {'account_name': 'cindy_994'}, {'account_name': 'cric1069'}, {'account_name': 'cyh52110'}, {'account_name': 'cmf1261639461'}, {'account_name': 'cwl1010857185'}, {'account_name': 'cxy陈1218'}, {'account_name': 'd360472902'}, {'account_name': 'cmd520'}, {'account_name': 'd95399'}, {'account_name': 'c\u200613991052739'}, {'account_name': 'cxie2'}, {'account_name': 'co小静'}, {'account_name': 'dandan103219'}, {'account_name': 'colorfull木糖醇'}, {'account_name': 'dd1127586004'}, {'account_name': 'cuixisunny'}, {'account_name': 'cyc13087035601'}, {'account_name': 'cuttogether'}, {'account_name': 'chzafar85'}, {'account_name': 'clot811074'}, {'account_name': 'ctr男'}, {'account_name': 'cq13164614342'}, {'account_name': 'crylllian恋'}, {'account_name': 'dd254425599'}, {'account_name': 'cjiaying819'}, {'account_name': 'chuangparker'}, {'account_name': 'cq_2020'}, {'account_name': 'clm810'}, {'account_name': 'cuiganglu22'}, {'account_name': 'dcmwqdx'}, {'account_name': 'crong_95'}, {'account_name': 'dadajiangyou123'}, {'account_name': 'cmq19930625'}, {'account_name': 'chrisshine0128'}, {'account_name': 'clq1121'}, {'account_name': 'czg1974'}, {'account_name': 'conyao2222'}, {'account_name': 'dai8600740'}, {'account_name': 'cui151007'}, {'account_name': 'churros2'}, {'account_name': 'chunlai97'}, {'account_name': 'cimcuidu123'}, {'account_name': 'cs00637'}, {'account_name': 'csw320927'}, {'account_name': 'ddaroll'}, {'account_name': 'chuz520'}, {'account_name': 'danielchau080935'}, {'account_name': 'czs2858647875'}, {'account_name': 'cqb70615'}, {'account_name': 'csgq0602'}, {'account_name': 'cool19830720'}, {'account_name': 'cxf99475199'}, {'account_name': 'cjf1788'}, {'account_name': 'cs55916945'}, {'account_name': 'cym958611'}, {'account_name': 'daochun234'}, {'account_name': 'czkt爱你们'}, {'account_name': 'crans'}, {'account_name': 'coyizk'}, {'account_name': 'cundiange215698'}, {'account_name': 'colliniimk'}, {'account_name': 'cy9158sl'}, {'account_name': 'clive小牛'}, {'account_name': 'cuirunsheng168'}, {'account_name': 'crystal020888'}, {'account_name': 'ckc璇姐姐'}, {'account_name': 'dcduxar23206'}, {'account_name': 'czx_2010'}, {'account_name': 'cxm656811813'}, {'account_name': 'dahuagua2010'}, {'account_name': 'chuanshuoxiaona'}, {'account_name': 'daisy286427883'}, {'account_name': 'davidleung728'}, {'account_name': 'dan1993'}, {'account_name': 'cielo0302'}, {'account_name': 'cococatt123'}, {'account_name': 'crazy411455825'}, {'account_name': 'd1u2l3i4n5'}, {'account_name': 'dahai199503'}, {'account_name': 'cuteninibear1986'}, {'account_name': 'dayaoyaowang'}, {'account_name': 'cijincha123'}, {'account_name': 'cindy3387'}, {'account_name': 'congming3589'}, {'account_name': 'cw程丽云'}, {'account_name': 'chuanwenxiayun'}, {'account_name': 'd3897'}, {'account_name': 'cj1019583984'}, {'account_name': 'dcheng925'}, {'account_name': 'dafu54321'}, {'account_name': 'dabao87770058'}, {'account_name': 'cowlywang1015'}, {'account_name': 'd363407397'}, {'account_name': 'cranberry。'}, {'account_name': 'ckx1879'}, {'account_name': 'ctk2008'}, {'account_name': 'chun1'}, {'account_name': 'dayong198'}, {'account_name': 'chunedmund312'}, {'account_name': 'cuifei15866349925'}, {'account_name': 'dabaobei198547'}, {'account_name': 'cyf07101'}, {'account_name': 'cth5165'}, {'account_name': 'chulian73'}, {'account_name': 'dangling1225'}, {'account_name': 'daixrffg'}, {'account_name': 'cxmlchlmh'}, {'account_name': 'cpdw3'}, {'account_name': 'cosmopolitan19'}, {'account_name': 'dckdcj1976'}, {'account_name': 'dangdangcute'}, {'account_name': 'churi1'}, {'account_name': 'cjb13636600787'}, {'account_name': 'cxb_24008'}, {'account_name': 'colorful丶胖子'}, {'account_name': 'cxq13555076111'}, {'account_name': 'cuicui503824'}, {'account_name': 'chengan60'}, {'account_name': '888小弟弟'}, {'account_name': '520ljf009'}, {'account_name': 'a649335895'}, {'account_name': '1786574婷'}, {'account_name': '17773478979'}, {'account_name': '155wyl'}, {'account_name': 'ai13737565573'}, {'account_name': '13030327550'}, {'account_name': 'bightf08437'}, {'account_name': 'danfang060917'}, {'account_name': 'baoshuangcom'}, {'account_name': '667gangdo'}, {'account_name': 'aa26336060'}, {'account_name': 'bby424'}, {'account_name': 'crazykru'}, {'account_name': 'anna081887'}, {'account_name': '2015小小大'}, {'account_name': '15166376625'}, {'account_name': '12丹丹563049002'}, {'account_name': '0359利'}, {'account_name': 'chengji201585257795'}, {'account_name': 'chen529127466.'}, {'account_name': '98放开'}, {'account_name': 'chenmianli33'}, {'account_name': '17071411184'}, {'account_name': 'a1731688042'}, {'account_name': '437743487许'}]


for i in content:
    name = i['account_name']

    sign = get_sign(name)['sign']

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '193',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': add_cookie,
        'Host': 'app.tk1788.com',
        'Origin': 'http://app.tk1788.com',
        'Referer': 'http://app.tk1788.com/app/superscan/searchAliim.jsp',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    form_data = {
        'm': 'sAliim',
        'aliim': name,
        'costType': 'Type4Click',
        'timeStamp': add_TimeStamp,
        'sign': sign,
        'ifQBase': 'true',
        'ifQReport': 'true',
        'ifQDownB': 'true',
        'judgeAnother': 'true',
    }

    try:
        content = requests.post(url='http://app.tk1788.com/app/superscan/op.jsp', headers=headers, data=form_data).text

        time.sleep(2)

        content2 = json.loads(content)

        GetTag = json.loads(get_tag(name))['msg']

        tree = etree.HTML(GetTag)

        tag = tree.xpath('//span/text()')[0]

        regist_day = content2['registDay']

        DeepData = Deep_Search(regist_day, sign, name)

        msg = DeepData['msg']

        tree = etree.HTML(msg)

        questions = tree.xpath('//td/text()')

        result = tree.xpath('//span/text()')

        if len(result) == 8:
            a = result[0]
            b = result[1]
            c = result[2]
            d = result[3]
            e = result[4]
            f = result[5]
            g = result[6]
            h = result[7]
        elif len(result) == 7:
            a = result[0]
            b = result[1]
            c = result[2]
            d = result[3]
            e = '暂无数据'
            f = result[4]
            g = result[5]
            h = result[6]
        else:
            a = '暂无数据'
            b = '暂无数据'
            c = '暂无数据'
            d = '暂无数据'
            e = '暂无数据'
            f = '暂无数据'
            g = '暂无数据'
            h = '暂无数据'

        three_data = {
            '近一季度平均周成交次数': a,
            '消费力': b,
            '用户地域': c,
            '发出好评率': d,
            '购买频率': e,
            '用户退款率': f,
            '收到好评率:': g,
            '终端偏好': h,
        }

        one_data = {
            '买家信誉': content2['buyerCre'],
            '商家信誉': content2['sellerCredit'],
            '性别': content2['sex'],
            '收到好评率': content2['received_rate'],
            '注册日期': content2['created'],
            '淘龄': content2['registDay'],
            '买家总周平均': content2['buyerAvg'],
            '查询时间': content2['queryTime'],
            '是否实名': content2['nameconform'],
            '会员类型': content2['vip_level'],
            '淘宝会员': content2['vip_info'],
            '吐槽': content2['aliimComplaintsNum'],
            '打标情况-兔子': content2['type1'],
            '打标情况-蜜獾': content2['type2'],
            '打标情况-狐狸': content2['type3'],
            '打标情况-鳄鱼': content2['type4'],
            '打标情况-降权处置': content2['downNum'],
            '云黑名单': content2['yunBlack']
        }

        biaoqian = {
            '标签': tag
        }

        li = []
        li.append(name)
        li.append(one_data)
        li.append(biaoqian)
        li.append(three_data)
        li.append(add_time)
        print(li)

        to_sql(li)

        time.sleep(5)
    except:
        print('账号存在异常')
        time.sleep(3)

    time.sleep(2)

# fp.close()