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
# re = requests.get(url=huoying_url).json()

re = [{'account_name': 'sbxktei0918'}, {'account_name': 's520901023'}, {'account_name': 'sunrise08121688'}, {'account_name': 'qiangtiancai'}, {'account_name': 'nl宝贝'}, {'account_name': 'o0约定之地0o'}, {'account_name': 'soung02'}, {'account_name': 'nok1013'}, {'account_name': 'shaiss188'}, {'account_name': 'tasha8888'}, {'account_name': 'speedrace66'}, {'account_name': 'singforyou24296346'}, {'account_name': 'q645185'}, {'account_name': 'tb09106084'}, {'account_name': 'tb07970435'}, {'account_name': 'shengming'}, {'account_name': 'qingqingyy66'}, {'account_name': 'sadlgkj'}, {'account_name': 'shunfengsumai'}, {'account_name': 'shy19790912hmy'}, {'account_name': 'pingu118'}, {'account_name': 'q5205620'}, {'account_name': 'sushuyang2006'}, {'account_name': 'tb11182928'}, {'account_name': 'nssqxj'}, {'account_name': 'qqww03'}, {'account_name': 'shaqima2011'}, {'account_name': 's2015雪雪'}, {'account_name': 'shtko02'}, {'account_name': 'pkrabyro343'}, {'account_name': 'q1164487267'}, {'account_name': 'qq60414090'}, {'account_name': 'ptpfdvll775'}, {'account_name': 'sky_790312'}, {'account_name': 'sdxluanchuanzfb'}, {'account_name': 'taotaobao0705'}, {'account_name': 'ocean_adam'}, {'account_name': 'ppjuiwh31069'}, {'account_name': 'q541837160'}, {'account_name': 'qqw8867060'}, {'account_name': 'qian牛花'}, {'account_name': 'sheaijss'}, {'account_name': 'sujian831229'}, {'account_name': 'paradiseiwai'}, {'account_name': 'q305021779'}, {'account_name': 'sunshine_wuxi'}, {'account_name': 'qq美丽新天地'}, {'account_name': 'pyx123456796'}, {'account_name': 'smzdqj68'}, {'account_name': 'sdkd156'}, {'account_name': 'selang_007'}, {'account_name': 'ruixili'}, {'account_name': 'mywater1020'}, {'account_name': 'samsonl1'}, {'account_name': 'sttk900714'}, {'account_name': 'qq3473563'}, {'account_name': 'ningmeng520_007'}, {'account_name': 'r先生哟'}, {'account_name': 'richiechen0108'}, {'account_name': 'qq531576600'}, {'account_name': 'songxiaoyan71'}, {'account_name': 'Sunnes阳'}, {'account_name': 'qq765026396qq'}, {'account_name': 'nevegiveup1004'}, {'account_name': 'sweetcc13'}, {'account_name': 'sweetchengn'}, {'account_name': 'rochietyl'}, {'account_name': 'songxizhe1'}, {'account_name': 'superhokhim'}, {'account_name': 'Q美丽99'}, {'account_name': 'prince522009'}, {'account_name': 'oxhfbsj06353'}, {'account_name': 'suen02071'}, {'account_name': 'ruanfeifei0804'}, {'account_name': 'ruanjingeng'}, {'account_name': 'qq520guom'}, {'account_name': 'sunshine87927'}, {'account_name': 'mymumlyl'}, {'account_name': 'openshy4'}, {'account_name': 'raomingbo'}, {'account_name': 'slimlala'}, {'account_name': 'scxffk'}, {'account_name': 'niuheyiff'}, {'account_name': 'okcandme'}, {'account_name': 'qq8380161'}, {'account_name': 'qwzx蔡小蔡'}, {'account_name': 'shiyali1989112718055587'}, {'account_name': 'penshine375753549'}, {'account_name': 'sm16588'}, {'account_name': 'nono接仔'}, {'account_name': 'seson'}, {'account_name': 'pinsum'}, {'account_name': 'nounou_baobei'}, {'account_name': 'tb08830455'}, {'account_name': 'syxx847'}, {'account_name': 'qcancer'}, {'account_name': 'samzhang11'}, {'account_name': 'tb06842133'}, {'account_name': 'songhao0114'}, {'account_name': 'rock20111021'}, {'account_name': 'oasis0117'}, {'account_name': 'ning214021'}, {'account_name': 'sdf23fsdfwe'}, {'account_name': 'tb073291973'}, {'account_name': 'pxyanyan'}, {'account_name': 'tangyuan20150115'}, {'account_name': 'nksv3040'}, {'account_name': 'tb058696254'}, {'account_name': 'tb06246026'}, {'account_name': 'tb03905944'}, {'account_name': 'shuaaivv'}, {'account_name': 'nicola513'}, {'account_name': 'pschen710'}, {'account_name': 'shanshanbb'}, {'account_name': 'qq99955201'}, {'account_name': 'q505089029'}, {'account_name': 'nana0619'}, {'account_name': 'tb108212289'}, {'account_name': 'tb02439049'}, {'account_name': 'tb08028522'}, {'account_name': 'raytang65'}, {'account_name': 'pengrui201110'}, {'account_name': 'ningzj'}, {'account_name': 'sum907'}, {'account_name': 'pyowdw'}, {'account_name': 'qin13321725804'}, {'account_name': 'tb0376592'}, {'account_name': 'raduke'}, {'account_name': 'shenqi'}, {'account_name': 'neversaynever4'}, {'account_name': 'qq970724588'}, {'account_name': 'rkrk1008'}, {'account_name': 'rainbow紫'}, {'account_name': 'syh感谢有的陪伴'}, {'account_name': 'tb10903705'}, {'account_name': 'tankeqingg'}, {'account_name': 't18137311795'}, {'account_name': 'nixiaoming119'}, {'account_name': 'shaoxu320261'}, {'account_name': 'qd390197298'}, {'account_name': 'show_vis'}, {'account_name': 'ooohqaqfi93'}, {'account_name': 'qinwenzhou'}, {'account_name': 'ping1169'}, {'account_name': 'tablezq'}, {'account_name': 'qq877680091'}, {'account_name': 'ruhaoxu2008'}, {'account_name': 'skater小皮蛋'}, {'account_name': 'tb003672477'}, {'account_name': 'qq812386786'}, {'account_name': 'skybey12'}, {'account_name': 'nxp730'}, {'account_name': 'tangtangyun71'}, {'account_name': 'shiqiujunzm'}, {'account_name': 'sex_black'}, {'account_name': 'Pangqdiongzhen'}, {'account_name': 'PMX满满'}, {'account_name': 'neilu999'}, {'account_name': 'nph3555'}, {'account_name': 'reuopec'}, {'account_name': 'tb02746838'}, {'account_name': 'tb103039684'}, {'account_name': 'qianxiuxiu671990'}, {'account_name': 'q1103507455'}, {'account_name': 'n2006hj'}, {'account_name': 'tb023867223'}, {'account_name': 'pch12345'}, {'account_name': 'tb07571922'}, {'account_name': 'qinran2010'}, {'account_name': 'shasha121416'}, {'account_name': 'renlei0039'}, {'account_name': 'rubic'}, {'account_name': 'rizwanam22'}, {'account_name': 'ss19880104'}, {'account_name': 'qianhao828'}, {'account_name': 'pjy18770162595'}, {'account_name': 'q5645778'}, {'account_name': 'sunnystudio24'}, {'account_name': 'sdfdfcvbn'}, {'account_name': 'sxd12345688'}, {'account_name': 'piaoyapiaode521'}, {'account_name': 'tb03107209'}, {'account_name': 'sinmez'}, {'account_name': 'tb055972679'}, {'account_name': 'qq343364627'}, {'account_name': 'niu8664911'}, {'account_name': 'tb065928353'}, {'account_name': 'tb03406816'}, {'account_name': 'shuyonge'}, {'account_name': 'q2856030131'}, {'account_name': 'qqwlf'}, {'account_name': 'pand_mai'}, {'account_name': 'rome_5'}, {'account_name': 'nqmmyyll'}, {'account_name': 'nzzzy55'}, {'account_name': 'oscorkid'}, {'account_name': 'nkj2103300'}, {'account_name': 'sunnylee_x'}, {'account_name': 'pan青晨'}, {'account_name': 'myf6622'}, {'account_name': 'qq15813488318'}, {'account_name': 'shanbb96'}, {'account_name': 'qq444087939'}, {'account_name': 'tb04642_44'}, {'account_name': 'tb00915768'}, {'account_name': 'q317707019'}, {'account_name': 'second230'}, {'account_name': 'shixu1996'}, {'account_name': 'tb034888518'}, {'account_name': 'pgy646468513'}, {'account_name': 'q330325032'}, {'account_name': 'qq11535399'}, {'account_name': 'samoye'}, {'account_name': 'renxin1110'}, {'account_name': 'tb04733910'}, {'account_name': 'purehj'}, {'account_name': 'taobaozhaoyi315'}, {'account_name': 'tb06031590'}, {'account_name': 'nageshabi17'}, {'account_name': 'tb108670698'}, {'account_name': 'tattathana'}, {'account_name': 'oto营销'}, {'account_name': 'sunny小懒123'}, {'account_name': 'sonona000'}, {'account_name': 'nihaomania7'}, {'account_name': 'ruwine'}, {'account_name': 'silentb'}, {'account_name': 'qiangyu735799491'}, {'account_name': 'tb089952592'}, {'account_name': 'qin168feng'}, {'account_name': 'pangxinrui335014891'}, {'account_name': 'somewhereintime73'}, {'account_name': 'qq305373998'}, {'account_name': 'tang糖11036444'}, {'account_name': 'tb110919229'}, {'account_name': 'tb006104'}, {'account_name': 'pullwly'}, {'account_name': 'penglu216913'}, {'account_name': 'superandsupper'}, {'account_name': 'tb041843561'}, {'account_name': 'tb0012233_00'}, {'account_name': 'qw我是天龙'}, {'account_name': 'stanleywong1026'}, {'account_name': 'sisiyz54761524'}, {'account_name': 'tb0954482_2013'}, {'account_name': 'szy梦醒时刻'}, {'account_name': 'shangchengwuye2011'}, {'account_name': 'qasim仇'}, {'account_name': 'samsung68'}, {'account_name': 'qq401731402'}, {'account_name': 'niu308311'}, {'account_name': 'sweetzhangxue'}, {'account_name': 'srhjwb'}, {'account_name': 'shjiaming'}, {'account_name': 'qinqin05783517'}, {'account_name': 'onzpo27'}, {'account_name': 'sxjiaosenxian'}, {'account_name': 'sunduoduo2008'}, {'account_name': 'tb076618424'}, {'account_name': 'one愤怒的小鸟1'}, {'account_name': 'qianf007'}, {'account_name': 'sen993062857'}, {'account_name': 'princess101619'}, {'account_name': 'shadows5257'}, {'account_name': 'pengruirui12'}, {'account_name': 'qixiangyu112'}, {'account_name': 'naka17mca'}, {'account_name': 'sqvvvvv'}, {'account_name': 'sunshowman'}, {'account_name': 'sunboom0324'}, {'account_name': 'saiji6815256'}, {'account_name': 'peipei313188'}, {'account_name': 'sakurarose'}, {'account_name': 'sjf0002014'}, {'account_name': 'rill_heaven'}, {'account_name': 'sang145511'}, {'account_name': 'stone邹'}, {'account_name': 'ses5213'}, {'account_name': 'q15899594031'}, {'account_name': 'smile701161080'}, {'account_name': 'si987642'}, {'account_name': 'shiqiangyan9'}, {'account_name': 'olive9922'}, {'account_name': 'songjingli99999'}, {'account_name': 'sambeng'}, {'account_name': 'q851517944'}, {'account_name': 'shangpent'}, {'account_name': 'sht平凡'}, {'account_name': 'qq289767375'}, {'account_name': 's951010sam'}, {'account_name': 'rainy2653'}, {'account_name': 'qwe3542011'}, {'account_name': 'qishiyinhe'}, {'account_name': 'pinganshifu369'}, {'account_name': 'qiuxiao856'}, {'account_name': 'sun980705535'}, {'account_name': 'songqiangnihao'}, {'account_name': 'qqrr526'}, {'account_name': 'rjaa1982'}, {'account_name': 'qixin19'}, {'account_name': 'tb078910757'}, {'account_name': 'tb027921735'}, {'account_name': 'only睿纹'}, {'account_name': 'sbidtf1314'}, {'account_name': 'shuiniao007'}, {'account_name': 'tb064763340'}, {'account_name': 'songye131445'}, {'account_name': 'shh5526423'}, {'account_name': 'tb023928444'}, {'account_name': 'qq1206428557'}, {'account_name': 'niahkndb'}, {'account_name': 'qq1050426594'}, {'account_name': 'my欧美站'}, {'account_name': 'nxp1101'}, {'account_name': 'mylove古力'}, {'account_name': 'neogodhoneyben'}, {'account_name': 'tb0155007_11'}, {'account_name': 'suxia89826964'}, {'account_name': 'takeyoufly510'}, {'account_name': 'o淡淡椰香o'}, {'account_name': 'snow慧93'}, {'account_name': 'qiujianlong2011'}, {'account_name': 'sam153153096352743'}, {'account_name': 'qjliuyon'}, {'account_name': 'rbk688'}, {'account_name': 'nectaire'}, {'account_name': 'panweijing1989'}, {'account_name': 'ss1641351292'}, {'account_name': 'sdq65b0p7'}, {'account_name': 'okk168'}, {'account_name': 'shuikongqi1'}, {'account_name': 'okman444'}, {'account_name': 'q610949606'}, {'account_name': 'tb06043159'}, {'account_name': 'tb029051301'}, {'account_name': 'sph8086'}, {'account_name': 'rgfgfgd123'}, {'account_name': 'puxia13140'}, {'account_name': 'puvyluosv'}, {'account_name': 'sjcgbhzl清清'}, {'account_name': 'tangqin5'}, {'account_name': 'sxmazl1976'}, {'account_name': 'onlyluyinini0142536'}, {'account_name': 'qq540766647qq88'}, {'account_name': 'tb0100459_2011'}, {'account_name': 'rammy19900721'}, {'account_name': 'ps装小娟'}, {'account_name': 'ruyanhuanlegou'}, {'account_name': 'qq1102949795'}, {'account_name': 'sunny_hsm'}, {'account_name': 'superman_s'}, {'account_name': 'southkeke'}, {'account_name': 'sandy_jia'}, {'account_name': 'talia1029'}, {'account_name': 'tangtangwaiting'}, {'account_name': 'snow静轩'}, {'account_name': 'sunshishi7285009'}, {'account_name': 'shixiaofeng16'}, {'account_name': 'qq892920755'}, {'account_name': 'o简简单单ooo'}, {'account_name': 'shin712712'}, {'account_name': 'osoon78'}, {'account_name': 'sy9901310651'}, {'account_name': 'shg_19840906'}, {'account_name': 'tb0979786_33'}, {'account_name': 'qinghuoyanyan2'}, {'account_name': 'qq371249858'}, {'account_name': 'srieverct'}, {'account_name': 'steveoption'}, {'account_name': 'panbo589'}, {'account_name': 'nana362712072'}, {'account_name': 'qq286182575'}, {'account_name': 'starwar1989'}, {'account_name': 'shshaishan'}, {'account_name': 'songdada1229'}, {'account_name': 'rainsummer0'}, {'account_name': 'q1515'}, {'account_name': 'shi史旺'}, {'account_name': 'quting1989'}, {'account_name': 'perar'}, {'account_name': 'qwopkd1023'}, {'account_name': 'ranchan2'}, {'account_name': 'qin3111028'}, {'account_name': 'shuangbaodai'}, {'account_name': 'nju67'}, {'account_name': 'shizhonglin19661'}, {'account_name': 'pwone_1982'}, {'account_name': 'renjianbo139993125'}, {'account_name': 'sindy553'}, {'account_name': 'qinlele0714'}, {'account_name': 'pengweiwei871223'}, {'account_name': 'tb041846504'}, {'account_name': 'sumerr0'}, {'account_name': 'sbear0520'}, {'account_name': 'sunyaohui77'}, {'account_name': 'shenghong8'}, {'account_name': 'qw416415590'}, {'account_name': 'shenjing2423973356'}, {'account_name': 'suhaiyan2441625516'}, {'account_name': 'shaboji33'}, {'account_name': 'rryy4333705'}, {'account_name': 'soloyoyo2008'}, {'account_name': 'tb056269817'}, {'account_name': 'tb052376044'}, {'account_name': 'shirley_runan'}, {'account_name': 'q826347844'}, {'account_name': 'oumylady0123'}, {'account_name': 'sun19900527'}, {'account_name': 'syh1568'}, {'account_name': 'sya4763248'}, {'account_name': 'seeyou5521chb'}, {'account_name': 'sqc5222'}, {'account_name': 'mzjlswatt'}, {'account_name': 'njny5897059'}, {'account_name': 'tb040022453'}, {'account_name': 'qianwenxia818'}, {'account_name': 'qqqwww023'}, {'account_name': 'qwerzxcvfdsa'}, {'account_name': 'summer密斯李'}, {'account_name': 'q334877370'}, {'account_name': 'tb00159358'}, {'account_name': 'shuqinfeng'}, {'account_name': 'ssccyy'}, {'account_name': 'oyyj00830'}, {'account_name': 'qiao8694'}, {'account_name': 'tb0062429_33'}, {'account_name': 'mzmamwe'}, {'account_name': 'songlili54247893'}, {'account_name': 'shgdu88837122'}, {'account_name': 'sunlight_0001'}, {'account_name': 't _1493438061854_0419'}, {'account_name': 'tangbm88'}, {'account_name': 'qym红叶飘飘'}, {'account_name': 'nitianbuwei'}, {'account_name': 'qyw13579'}, {'account_name': 'tb064606209'}, {'account_name': 'my_love_blue'}, {'account_name': 'stella3321'}, {'account_name': 'saintleander001'}, {'account_name': 'sq75688'}, {'account_name': 'peipeixt'}, {'account_name': 'nywangyong'}, {'account_name': 'qqqqq9846'}, {'account_name': 'nigning1225'}, {'account_name': 'rongfei_007'}, {'account_name': 'smm6060'}, {'account_name': 'paullukluk'}, {'account_name': 'tb1029594643'}, {'account_name': 'sally5amy'}, {'account_name': 'ns8771'}, {'account_name': 'santiao24'}, {'account_name': 'pengb514zq'}, {'account_name': 'somethinglikethis'}, {'account_name': 'rantiantian88508'}, {'account_name': 'tangding012345'}, {'account_name': 'mzkang520chy'}, {'account_name': 'Taowt_1999'}, {'account_name': 'plus小可爱'}, {'account_name': 'qq826064580'}, {'account_name': 'quna246800'}, {'account_name': 'psvita3000'}, {'account_name': 'qcwji974'}, {'account_name': 'tb031446236'}, {'account_name': 'qdcf冰琦'}, {'account_name': 'tb09691696'}, {'account_name': 'syn140310'}, {'account_name': 'super跳跳龙'}, {'account_name': 'rldrpnbr393'}, {'account_name': 'qq5595655'}, {'account_name': 'tb10919283'}, {'account_name': 'silviafmy'}, {'account_name': 'PMX霞霞'}, {'account_name': 'tb00651950'}, {'account_name': 'phlf1967'}, {'account_name': 'samyli1985'}, {'account_name': 'qq308871273'}, {'account_name': 'qazwsxer1234'}, {'account_name': 'sensen080210'}, {'account_name': 'tb102061973'}, {'account_name': 'sss夜猫子'}, {'account_name': 'qq704635305'}, {'account_name': 'qinyongxiang2008'}, {'account_name': 'ozgo6'}, {'account_name': 'sn_84'}, {'account_name': 'sjw76753934'}, {'account_name': 'smilezjp2'}, {'account_name': 'song3710'}, {'account_name': 'rongpeijie'}, {'account_name': 'shaoye00008'}, {'account_name': 'popkkingt8'}, {'account_name': 'penny_832'}, {'account_name': 'quheng987'}, {'account_name': 's15753760334'}, {'account_name': 'tb087382542'}, {'account_name': 'pipidan7456'}, {'account_name': 'show1986zai'}, {'account_name': 'qqyujiaqi'}, {'account_name': 'shuiwuzhou'}, {'account_name': 'szwsaf'}, {'account_name': 'tb015615612'}, {'account_name': 'tb100758412'}, {'account_name': 'poso4'}, {'account_name': 'qq12310a'}, {'account_name': 'q709218754'}, {'account_name': 'snoopy1377'}, {'account_name': 'sky2259244'}, {'account_name': 'pqm1005'}, {'account_name': 'sunlijun522'}, {'account_name': 'nikkily'}, {'account_name': 'tasty1234'}, {'account_name': 'rycdyy2011'}, {'account_name': 'qq345638594'}, {'account_name': 'shenyu520'}, {'account_name': 'niaodesi'}, {'account_name': 'sexy肖恩'}, {'account_name': 'shippergu'}, {'account_name': 'pengpanpan198602'}, {'account_name': 'qq769355311'}, {'account_name': 'q3294158'}, {'account_name': 'stay617'}, {'account_name': 'tb0234362_2012'}, {'account_name': 'qq914968782'}, {'account_name': 'ninhjing致远'}, {'account_name': 'tb01901767'}, {'account_name': 'tb08177761'}, {'account_name': 'starrystarr'}, {'account_name': 'tb05124404'}, {'account_name': 'rong桂桂'}, {'account_name': 'tb0403_2007'}, {'account_name': 'qq171109766'}, {'account_name': 'tb00543500'}, {'account_name': 'sj小鬼kid'}, {'account_name': 'sunjie0707a'}, {'account_name': 'tb06918471'}, {'account_name': 'stw95270'}, {'account_name': 'rongyan11'}, {'account_name': 'tb11432583'}, {'account_name': 'raimbo'}, {'account_name': 'nb_日天大哥'}, {'account_name': 'sherryzhang531'}, {'account_name': 'shanshan66885'}, {'account_name': 'peng853401928'}, {'account_name': 'nan22926069'}, {'account_name': 'shuyanbin1988'}, {'account_name': 'qqwwee14202301'}, {'account_name': 'syz901122'}, {'account_name': 'songtingting85'}, {'account_name': 'sun85117289'}, {'account_name': 'qingqing766635882'}, {'account_name': 'q妈妈171686'}, {'account_name': 'tb050436471'}, {'account_name': 'ss36031219'}, {'account_name': 'pengpengjun_303'}, {'account_name': 'ss552100'}, {'account_name': 'qing清lng'}, {'account_name': 'quan在路上'}, {'account_name': 'tb0289355_88'}, {'account_name': 'sdkjfsd'}, {'account_name': 'tao13655147640'}, {'account_name': 'ss1572770'}, {'account_name': 'need0001'}, {'account_name': 'm集美小屋m'}, {'account_name': 'shiwu1002'}, {'account_name': 'sxf521028'}, {'account_name': 'qazx1214'}, {'account_name': 'tb082331365'}, {'account_name': 'qizhi38218219'}, {'account_name': 'shangmingxun521'}, {'account_name': 'oowmjoo'}, {'account_name': 'taki8858715'}, {'account_name': 'nandehutu男人'}, {'account_name': 'nowsoon'}, {'account_name': 'rong15833010330'}, {'account_name': 'san435463875'}, {'account_name': 'rd雨霖00'}, {'account_name': 'robinkung63'}, {'account_name': 'qingshangao88'}, {'account_name': 'pinkfloyd1973'}, {'account_name': 's对不起我爱你'}, {'account_name': 'qq1499818728'}, {'account_name': 'nmd7410'}, {'account_name': 'papapa8856509984'}, {'account_name': 'sunsha0403'}, {'account_name': 'ronggou58'}, {'account_name': 'shen0414'}, {'account_name': 'shenwuquan2010'}, {'account_name': 'sophiafeng_2008'}, {'account_name': 'pmr深情似海真心一片'}, {'account_name': 'ss8081089'}, {'account_name': 'ningjing158'}, {'account_name': 'ps风雨无情'}, {'account_name': 'qiangyu2011'}, {'account_name': 'qq409719757'}, {'account_name': 'taotao9725'}, {'account_name': 'pangyuliang86'}, {'account_name': 'rainie5'}, {'account_name': 'shane方'}, {'account_name': 'tb0757357_2011'}, {'account_name': 'qll么么哒'}, {'account_name': 'tb07115205'}, {'account_name': 'shaka602'}, {'account_name': 'tb093606_99'}, {'account_name': 'nininihao啊'}, {'account_name': 'shen1240'}, {'account_name': 'tb093453171'}, {'account_name': 'tb10964698'}, {'account_name': 'shi860319'}, {'account_name': 'shuibian18349055'}, {'account_name': 'q582110722'}, {'account_name': 'tb018801611'}, {'account_name': 'qi6666'}, {'account_name': 'qq1102128063'}, {'account_name': 'oo7788cc'}, {'account_name': 'pingying181'}, {'account_name': 'slzs12345'}, {'account_name': 'soohyun大椒'}, {'account_name': 'qq8872224'}, {'account_name': 'smd860921'}, {'account_name': 'sky150000'}, {'account_name': 'osaka1984'}, {'account_name': 'tb089416616'}, {'account_name': 'sunjacob'}, {'account_name': 'sunny辰00'}, {'account_name': 'm故乡的云'}, {'account_name': 'tb03315009'}, {'account_name': 'syh13395469762'}, {'account_name': 'slq851222'}, {'account_name': 't b18056_2013'}, {'account_name': 'myqueen00'}, {'account_name': 'ninhao1231630'}, {'account_name': 'q1445925111'}, {'account_name': 'slnfq杨琴'}, {'account_name': 'tb0639086_33'}, {'account_name': 'suruixia8'}, {'account_name': 'sunchengai1'}, {'account_name': 'qqa69828182'}, {'account_name': 'qq1145896085'}, {'account_name': 'tb054820664'}, {'account_name': 'szh乌鸦129608493'}, {'account_name': 'songwenyan934'}, {'account_name': 'sunny梁宝贝'}, {'account_name': 'tailjqq'}, {'account_name': 'najiuzheyangla'}, {'account_name': 'quistis0830'}, {'account_name': 'naxitian242'}, {'account_name': 'onetime58'}, {'account_name': 'tb057986411'}, {'account_name': 'nihao2164809'}, {'account_name': 'rqqzzh'}, {'account_name': 'ryy11333'}, {'account_name': 'nangoulu779'}, {'account_name': 'tb1121615904'}, {'account_name': 'sks123545'}, {'account_name': 'sslzz118'}, {'account_name': 'pengwei986'}, {'account_name': 'sangxiusong'}, {'account_name': 'ntb_88'}, {'account_name': 'nnn10888'}, {'account_name': 'tb04783299'}, {'account_name': 'tb07099589'}, {'account_name': 'tb071285539'}, {'account_name': 'qwaszx8520061199833'}, {'account_name': 's59731228'}, {'account_name': 'sunjiwu926602'}, {'account_name': 'sng1985'}, {'account_name': 's9921200'}, {'account_name': 'shenbing731'}, {'account_name': 'sunyue950607'}, {'account_name': 'seuchenluphy'}, {'account_name': 'tb069660661'}, {'account_name': 'sunpeng82533103'}, {'account_name': 'retfrsatf'}, {'account_name': 'rlarns1010'}, {'account_name': 'qjh135790'}, {'account_name': 'ptczlz'}, {'account_name': 'songzi2030'}, {'account_name': 'silence527'}, {'account_name': 'qq57405465'}, {'account_name': 'sunny是我'}, {'account_name': 'pfyn123'}, {'account_name': 'tangqionglilong'}, {'account_name': 'quyufu'}, {'account_name': 'sskui1'}, {'account_name': 'siubo12160118'}, {'account_name': 'q54472489'}, {'account_name': 'seri0319'}, {'account_name': 'tb0297542_99'}, {'account_name': 'pasty_c'}, {'account_name': 'roe001124567'}, {'account_name': 'symi明'}, {'account_name': 'shuizhong_2009'}, {'account_name': 'sun20131211'}, {'account_name': 'ningkun0531'}, {'account_name': 'orange0869'}, {'account_name': 'sandy930'}, {'account_name': 'qiangshipeng'}, {'account_name': 'studioanecdote'}, {'account_name': 'ruyan0427'}, {'account_name': 'qqg我是王子'}, {'account_name': 'tb01331097'}, {'account_name': 'tb100436631'}, {'account_name': 'rap丶c'}, {'account_name': 'qianqian5754'}, {'account_name': 'spicykai'}, {'account_name': 'pinpin525'}, {'account_name': 'tb007132391'}, {'account_name': 'tamuxu'}, {'account_name': 'tao_baochen1'}, {'account_name': 'sa946478309'}, {'account_name': 'qq574784115w'}, {'account_name': 'sunbright880811'}, {'account_name': 'tb077455442'}, {'account_name': 'tb018254444'}, {'account_name': 'tb0284217_2011'}, {'account_name': 'ranran_521521'}, {'account_name': 'q10414200'}, {'account_name': 'tb09691052'}, {'account_name': 'sunjunhua_6688'}, {'account_name': 'tan易亚枚'}, {'account_name': 'rockrock1982'}, {'account_name': 'qq415377014'}, {'account_name': 'tb043915097'}, {'account_name': 'oooooofujb'}, {'account_name': 'slyxxckk521'}, {'account_name': 'szsdqwlkj'}, {'account_name': 'tailjq'}, {'account_name': 'nandao61'}, {'account_name': 'myl3014'}, {'account_name': 'shuitanke'}, {'account_name': 'tb07157362'}, {'account_name': 'qiuaichun123'}, {'account_name': 'qq20004604'}, {'account_name': 'taokezhe2010'}, {'account_name': 'phelpsnb'}, {'account_name': 'q追梦者'}, {'account_name': 'piggusll'}, {'account_name': 'ran5234270'}, {'account_name': 'tb10932427'}, {'account_name': 'pengbaorong1988'}, {'account_name': 'q714003718'}, {'account_name': 'shiyaobin0'}, {'account_name': 'tb067698377'}, {'account_name': 'onelove自白'}, {'account_name': 'rainzhao0202'}, {'account_name': 'ouyangle1994'}, {'account_name': 'tb100672048'}, {'account_name': 'q1215664310'}, {'account_name': 'simplelife好心情mu'}, {'account_name': 'smartrain3'}, {'account_name': 'sunpeixin'}, {'account_name': 'qq415631'}, {'account_name': 'qiusongailihua'}, {'account_name': 'nakajimahayate'}, {'account_name': 'qqq495111984'}, {'account_name': 'qqshiyiangel'}, {'account_name': 'sfy方园'}, {'account_name': 'newtonkuku'}, {'account_name': 'sean125037009'}, {'account_name': 'tb10343638'}, {'account_name': 'sunzeqi00'}, {'account_name': 'richshangwei'}, {'account_name': 'tb0169962_2012'}, {'account_name': 'tb08017045'}, {'account_name': 'shijialioyw'}, {'account_name': 'qianlanjuan'}, {'account_name': 'pg美人网210402164'}, {'account_name': 'sftzou'}, {'account_name': 'qu285675385'}, {'account_name': 'tb00599903'}, {'account_name': 'syf13933714329'}, {'account_name': 'solisa'}, {'account_name': 'netesh'}, {'account_name': 'roman090'}, {'account_name': 'taobao蓝蜗牛'}, {'account_name': 'penghaijing2014'}, {'account_name': 'tb0952945605'}, {'account_name': 'nuaacheny'}, {'account_name': 'szxharry'}, {'account_name': 'nrg300001'}, {'account_name': 'sfb03041021'}, {'account_name': 'prd_03'}, {'account_name': 'tb00614985'}, {'account_name': 'qq交友中心'}, {'account_name': 'sjclovelp'}, {'account_name': 'tb008524270'}, {'account_name': 'pangyixing'}, {'account_name': 'nthlty'}, {'account_name': 'san壹世繁华'}, {'account_name': 'qb5201314156'}, {'account_name': 'sl359908'}, {'account_name': 'taojie_7821'}, {'account_name': 'qustlm163'}, {'account_name': 'single0097'}, {'account_name': 'tb065240680'}, {'account_name': 's70899'}, {'account_name': 'nganleung'}, {'account_name': 'tb04751529'}, {'account_name': 'sishi153'}, {'account_name': 'qiuwenzeng3'}, {'account_name': 'pepsi0122'}, {'account_name': 'nancy11352'}, {'account_name': 'tang816925'}, {'account_name': 'sunjiuyang629'}, {'account_name': 'qiuxin_12'}, {'account_name': 'ran280236966'}, {'account_name': 'qq465315804'}, {'account_name': 'ridrkfk'}, {'account_name': 'ncfzz5138471'}, {'account_name': 'ninizhu14'}, {'account_name': 'orstar4819'}, {'account_name': 'tb0571346_11'}, {'account_name': 'tb01051636'}, {'account_name': 'suiyxin'}, {'account_name': 'shell舒心'}, {'account_name': 'niniq777'}, {'account_name': 'tb05710704'}, {'account_name': 'smine9'}, {'account_name': 'tb020678551'}, {'account_name': 'tb063279982'}, {'account_name': 'pingping7924'}, {'account_name': 'sffstt1332'}, {'account_name': 'qq929360868'}, {'account_name': 'nblvxians'}, {'account_name': 'nin885522'}, {'account_name': 'pwy20100825'}, {'account_name': 'rx10b'}, {'account_name': 'shimengkai123'}, {'account_name': 'nnllf86'}, {'account_name': 'qq594517417'}, {'account_name': 'shirely921'}, {'account_name': 'pangcaifeng12'}, {'account_name': 'sunxm651017'}, {'account_name': 'sisi963'}, {'account_name': 'tb081525_2012'}, {'account_name': 'qq443690207'}, {'account_name': 'tb066014143'}, {'account_name': 'qinglilaiwang'}, {'account_name': 'q838035118'}, {'account_name': '15914290308ie'}, {'account_name': 'tb081834691'}, {'account_name': 'nate1103'}, {'account_name': 'silver_ice'}, {'account_name': 'tb10986048'}, {'account_name': 'sujing9548'}, {'account_name': 'quduo121'}, {'account_name': 'qq421254181'}, {'account_name': 'o烧饼夹里脊o'}, {'account_name': 'mzr小芝'}, {'account_name': 'sisi_zhilian'}, {'account_name': 't19871028'}, {'account_name': 'nana351585997'}, {'account_name': 'qichunyan841121'}, {'account_name': 'qinbeer'}, {'account_name': 'pengpenghao1'}, {'account_name': 'hhhhhh琦'}, {'account_name': 'gao055221'}, {'account_name': 'l447055281'}, {'account_name': 'mystical周泽纯'}, {'account_name': 'cherry830721'}, {'account_name': 'hfsc038'}, {'account_name': 'gjh多姿多彩'}, {'account_name': 'jjss778'}, {'account_name': 't878218'}, {'account_name': 'jjt涛涛77'}, {'account_name': 'alicehuihui'}, {'account_name': '419285744吴小勇'}, {'account_name': 'chen13376555'}, {'account_name': 'haomeijia1221'}, {'account_name': '198724'}, {'account_name': 'jjrainy'}, {'account_name': 'frizensteve'}, {'account_name': 'tb025139984'}, {'account_name': 'laijin松'}, {'account_name': 'q790490748'}, {'account_name': '123席昌迎'}, {'account_name': '13466099072'}, {'account_name': 'hh1260842376'}, {'account_name': 'p的宝贝1'}, {'account_name': 'mei3214862438'}, {'account_name': '17776256600'}, {'account_name': 'a11111250250'}, {'account_name': 'tb064134'}, {'account_name': '1982胡杨树'}, {'account_name': 'L回忆过去时光'}, {'account_name': 'jurlyzhou'}, {'account_name': 'oliveolivelin'}, {'account_name': '17688454317'}, {'account_name': 'hl199387'}]

for i in re:
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