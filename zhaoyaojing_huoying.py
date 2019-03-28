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

content = [{'account_name': 'cc19920318'}, {'account_name': 'cbxrkj'}, {'account_name': 'cbchong'}, {'account_name': 'cdx1006'}, {'account_name': 'chankki'}, {'account_name': 'cailang973'}, {'account_name': 'bynbym'}, {'account_name': 'charm鬼君'}, {'account_name': 'cbkor92976'}, {'account_name': 'c17701758782'}, {'account_name': 'chenmin6619'}, {'account_name': 'cb02051'}, {'account_name': 'c13558290210'}, {'account_name': 'Caipin65'}, {'account_name': 'caixia19830728'}, {'account_name': 'caicai561889'}, {'account_name': 'chaorenqiang8'}, {'account_name': 'c1113300124'}, {'account_name': 'chenyinyying'}, {'account_name': 'cc雨晨1314'}, {'account_name': 'caidongmeic'}, {'account_name': 'caisiyang01'}, {'account_name': 'Chen少煌'}, {'account_name': 'chenliangcd'}, {'account_name': 'ceozgy'}, {'account_name': 'cb438361486'}, {'account_name': 'chengzi1922'}, {'account_name': 'chenguo51889'}, {'account_name': 'cat2595'}, {'account_name': 'chen20163121990'}, {'account_name': 'c944303088'}, {'account_name': 'caienyu4'}, {'account_name': 'chenan165'}, {'account_name': 'cdwjlyl'}, {'account_name': 'ccc么哒哒'}, {'account_name': 'caipeixin555'}, {'account_name': 'caolili380153391'}, {'account_name': 'caoli19860226'}, {'account_name': 'changli6622656'}, {'account_name': 'chenjie36193333'}, {'account_name': 'cao15958318750'}, {'account_name': 'caoleik'}, {'account_name': 'chenxiwz'}, {'account_name': 'cangyedao'}, {'account_name': 'c67056'}, {'account_name': 'byq525781'}, {'account_name': 'catcattt'}, {'account_name': 'bx11x0'}, {'account_name': 'bxyjnl'}, {'account_name': 'chengwei760320'}, {'account_name': 'chenshi15875655965'}, {'account_name': 'caishujin423'}, {'account_name': 'chen767092108'}, {'account_name': 'cc你珍贵'}, {'account_name': 'chen琼婷'}, {'account_name': 'cbica09'}, {'account_name': 'chenhui6265'}, {'account_name': 'c407152911'}, {'account_name': 'byl月月'}, {'account_name': 'cc15893800476'}, {'account_name': 'chenzhaobaba'}, {'account_name': 'chenguijietaobao1234'}, {'account_name': 'chenyungao'}, {'account_name': 'c540387582'}, {'account_name': 'casilda'}, {'account_name': 'chenxing1141426763'}, {'account_name': 'ceshw'}, {'account_name': 'chen14486231'}, {'account_name': 'ccm1925458'}, {'account_name': 'carriony'}, {'account_name': 'C927053981'}, {'account_name': 'chenlihua317'}, {'account_name': 'candyzhu6898'}, {'account_name': 'chenzhongpei123'}, {'account_name': 'chen_晓娜'}, {'account_name': 'caolongyue01'}, {'account_name': 'chenfang_43'}, {'account_name': 'canbaby2'}, {'account_name': 'Chen759015704'}, {'account_name': 'cb我太善良'}, {'account_name': 'cb下雨天'}, {'account_name': 'chenchao8006'}, {'account_name': 'chencheng刘影666'}, {'account_name': 'caixiu01'}, {'account_name': 'cgw18249738992'}, {'account_name': 'cbu-abcde201211'}, {'account_name': 'cenjinyang0'}, {'account_name': 'chenzisj'}, {'account_name': 'bychum'}, {'account_name': 'cdewsx58'}, {'account_name': 'byj7510'}, {'account_name': 'chenxu5461182'}, {'account_name': 'c13806980349'}, {'account_name': 'by恋99'}, {'account_name': 'chenqiuxia28'}, {'account_name': 'cckz11'}, {'account_name': 'chaseyouqq'}, {'account_name': 'chenhua1996121'}, {'account_name': 'cheng牛牛'}, {'account_name': 'cdmagpstt'}, {'account_name': 'chen66103'}, {'account_name': 'chenan0917'}, {'account_name': 'chenxia987654'}, {'account_name': 'changshengli623'}, {'account_name': 'castrl'}, {'account_name': 'burgundy_lyz'}, {'account_name': 'chen小燕2'}, {'account_name': 'ceo辛铭轩'}, {'account_name': 'can1239187'}, {'account_name': 'cdgj55'}, {'account_name': 'chch宝'}, {'account_name': 'caiguihong0101'}, {'account_name': 'by之语录'}, {'account_name': 'chenfen198812'}, {'account_name': 'ccx1538772314'}, {'account_name': 'cheese芝士11'}, {'account_name': 'changchang0302'}, {'account_name': 'chenqi20110316'}, {'account_name': 'chao870723'}, {'account_name': 'chencuixia1113'}, {'account_name': 'chendan198958'}, {'account_name': 'chenkaixuan6'}, {'account_name': 'chanel猫格格'}, {'account_name': 'chen327202724'}, {'account_name': 'chen4992'}, {'account_name': 'cao5832'}, {'account_name': 'ch41646182'}, {'account_name': 'chen20090524'}, {'account_name': 'c15824356418'}, {'account_name': 'cao1385201424'}, {'account_name': 'changyueyue1005'}, {'account_name': 'chenyuyao2010125'}, {'account_name': 'chenwenhui8686'}, {'account_name': 'cf魂飞胆散小云'}, {'account_name': 'ch820427'}, {'account_name': 'chenanlvlijun'}, {'account_name': 'chengyanjing123'}, {'account_name': 'caihaibin5207873'}, {'account_name': 'chang3115304'}, {'account_name': 'chenqiajjin0305'}, {'account_name': 'ccy15605985783'}, {'account_name': 'Chenwei772009'}, {'account_name': 'cao158329'}, {'account_name': 'ch201514'}, {'account_name': 'caosujuan316'}, {'account_name': 'chenyuyu8888888'}, {'account_name': 'chenling101510'}, {'account_name': 'cengmengqi2008'}, {'account_name': 'cbu-qq594098177'}, {'account_name': 'caiyunyun19850607'}, {'account_name': 'chenkeke1989'}, {'account_name': 'cai羽翔'}, {'account_name': 'ccx15913999379'}, {'account_name': 'chengyan7451321'}, {'account_name': 'chenjinlan878'}, {'account_name': 'c1047484292'}, {'account_name': 'chinaxianyanglei'}, {'account_name': 'chen960215'}, {'account_name': 'caiyan888sex'}, {'account_name': 'chian232323'}, {'account_name': 'chengu1130'}, {'account_name': 'chengruixi520521'}, {'account_name': 'chenjinpeng123'}, {'account_name': 'carry丨全场丶'}, {'account_name': 'cece1989hua'}, {'account_name': 'bylisen'}, {'account_name': 'chenmy_19930428'}, {'account_name': 'chengbin3261'}, {'account_name': 'camilla0514雪'}, {'account_name': 'chinesemiao'}, {'account_name': 'changjun910121'}, {'account_name': 'bxl7000'}, {'account_name': 'c1122400'}, {'account_name': 'chenxindeyouxiang'}, {'account_name': 'c18060455191'}, {'account_name': 'caiwenya859426'}, {'account_name': 'cdb人在旅途'}, {'account_name': 'bustlingworld'}, {'account_name': 'chengkui心怀梦想meng'}, {'account_name': 'chenyou18516197870'}, {'account_name': 'cctv520380'}, {'account_name': 'c315245258'}, {'account_name': 'bzc200888'}, {'account_name': 'chendongabc2009'}, {'account_name': 'caf一切如初'}, {'account_name': 'chenxiao8909'}, {'account_name': 'candy201142'}, {'account_name': 'chenglifei6'}, {'account_name': 'byd10'}, {'account_name': 'carolmiao2'}, {'account_name': 'chaolingyan'}, {'account_name': 'ccjjhkvzj'}, {'account_name': 'ccxxyu'}, {'account_name': 'cherylyip88'}, {'account_name': 'caogui0535'}, {'account_name': 'chenxiaozhen1966'}, {'account_name': 'chh0355'}, {'account_name': 'chenqin810214810214'}, {'account_name': 'cg760813'}, {'account_name': 'chenbao辰宝辰宝'}, {'account_name': 'cfshenry'}, {'account_name': 'caobph83'}, {'account_name': 'cbsbpgq哥只是个传说'}, {'account_name': 'chenpeisheng1193'}, {'account_name': 'chenyu81a'}, {'account_name': 'caishibin2610'}, {'account_name': 'cbb兰若团队创始'}, {'account_name': 'chao198934'}, {'account_name': 'cdc18094041319'}, {'account_name': 'Chenxue12101210'}, {'account_name': 'ch823952013'}, {'account_name': 'cheng_19941125'}, {'account_name': 'chenbin3478'}, {'account_name': 'caoyihang123456'}, {'account_name': 'chengggg1122'}, {'account_name': 'cc429277769'}, {'account_name': 'chenjieqiong96'}, {'account_name': 'can861782732'}, {'account_name': 'c976392366'}, {'account_name': 'cdkeller01'}, {'account_name': 'chenchao159'}, {'account_name': 'chezaiyzzl2009'}, {'account_name': 'chaelen'}, {'account_name': 'cathychenchen'}, {'account_name': 'chen5qcong'}, {'account_name': 'c2007112'}, {'account_name': 'cd123458'}, {'account_name': 'chenyuehua112233'}, {'account_name': 'by7780227'}, {'account_name': 'chens920'}, {'account_name': 'ccc666c'}, {'account_name': 'cfa学霸'}, {'account_name': 'chengwenchong109211'}, {'account_name': 'cang503'}, {'account_name': 'chengmin654958'}, {'account_name': 'byby188'}, {'account_name': 'cainingrui520'}, {'account_name': 'chendan1224'}, {'account_name': 'caoxingxing887'}, {'account_name': 'caoyan886563'}, {'account_name': 'cdm13922768486'}, {'account_name': 'caozijian2010'}, {'account_name': 'chenzhun依'}, {'account_name': 'chenguo520998'}, {'account_name': 'bu要太在意'}, {'account_name': 'c272951441'}, {'account_name': 'carey1214'}, {'account_name': 'cailgx'}, {'account_name': 'cc我是你大爷'}, {'account_name': 'chenrouxinlin'}, {'account_name': 'cenken岑恒'}, {'account_name': 'chenxiaoli618216'}, {'account_name': 'bz3415775'}, {'account_name': 'cgz08290415'}, {'account_name': 'chenchunling1990'}, {'account_name': 'chenhouhui'}, {'account_name': 'chenshaowe'}, {'account_name': 'cehuanjir'}, {'account_name': 'chengqun10086a'}, {'account_name': 'cf君莫笑'}, {'account_name': 'caohuan211314'}, {'account_name': 'caojiao100200300'}, {'account_name': 'chen7860'}, {'account_name': 'ccpp1126'}, {'account_name': 'chenyingxin633'}, {'account_name': 'buzhipiang'}, {'account_name': 'chenhuirangdid'}, {'account_name': 'care我的床'}, {'account_name': 'chenfengyun0734'}, {'account_name': 'chenyang19851229'}, {'account_name': 'changliang1103'}, {'account_name': 'caiyishan199173'}, {'account_name': 'Cheng0823517014'}, {'account_name': 'cherry25叶'}, {'account_name': 'b忘情水'}, {'account_name': 'caijinping520'}, {'account_name': 'chenyazhou0525'}, {'account_name': 'caihongmei710'}, {'account_name': 'chenhong19870617'}, {'account_name': 'ch15035617484'}, {'account_name': 'chenhuijiaoqing'}, {'account_name': 'canye1314'}, {'account_name': 'cbx希希060409'}, {'account_name': 'chenyimo1129'}, {'account_name': 'chenshiya2011'}, {'account_name': 'cchhxxling'}, {'account_name': 'caihuaihai'}, {'account_name': 'cglovejt'}, {'account_name': 'caohailing7'}, {'account_name': 'caoyanjie_1314'}, {'account_name': 'chen1587825567'}, {'account_name': 'cdzminmin'}, {'account_name': 'chentao19881028'}, {'account_name': 'chengzi689811'}, {'account_name': 'chekang3'}, {'account_name': 'ccazfq'}, {'account_name': 'canlanzhixia'}, {'account_name': 'chenxiaoqing201112'}, {'account_name': 'cc1234a55'}, {'account_name': 'chao424308638'}, {'account_name': 'caojinlian98'}, {'account_name': 'caochao18873725625'}, {'account_name': 'cheng_19944'}, {'account_name': 'chenbo15006471387'}, {'account_name': 'byteda'}, {'account_name': 'chen504615502'}, {'account_name': 'chh花花花'}, {'account_name': 'chenxiaoquan8'}, {'account_name': 'cc巫娜儿'}, {'account_name': 'byf607'}, {'account_name': 'cchh255'}, {'account_name': 'cc湾湾'}, {'account_name': 'chao767218181'}, {'account_name': 'cai90445546'}, {'account_name': 'caofeifei882012'}, {'account_name': 'byiya1'}, {'account_name': 'chan5203'}, {'account_name': 'cangwei188'}, {'account_name': 'cgyxtdjt'}, {'account_name': 'car1960908923'}, {'account_name': 'chengzhijia02'}, {'account_name': 'chengqianjin906'}, {'account_name': 'cats我的'}, {'account_name': 'chang9725'}, {'account_name': 'cfh1529830'}, {'account_name': 'c1395813530'}, {'account_name': 'chen1ch1en'}, {'account_name': 'changeknow'}, {'account_name': 'chikelinsad'}, {'account_name': 'bnbnbn1218'}, {'account_name': 'buquexinyanzi'}, {'account_name': 'chenchenliujing'}, {'account_name': 'chendhong2004'}, {'account_name': 'chengw0804'}, {'account_name': 'chenyu831113'}, {'account_name': 'cccck19980526'}, {'account_name': 'caixiuyue11'}, {'account_name': 'chenbinghua0'}, {'account_name': 'chenge621'}, {'account_name': 'chenyan19871203'}, {'account_name': 'C080810'}, {'account_name': 'cb123079'}, {'account_name': 'chinazoe00'}, {'account_name': 'cc1459754423'}, {'account_name': 'cc1831800'}, {'account_name': 'candy170922'}, {'account_name': 'caiyunzheiyue'}, {'account_name': 'changlovemei'}, {'account_name': 'chf陈晨'}, {'account_name': 'chenyan52021'}, {'account_name': 'changjingtao0'}, {'account_name': 'cbu-tommy7895123'}, {'account_name': 'cfydfj'}, {'account_name': 'chenqi661770'}, {'account_name': 'chenyasi26'}, {'account_name': 'chenmuzhiguang1234'}, {'account_name': 'cherry0216888'}, {'account_name': 'chenyin080813'}, {'account_name': 'bxs1990'}, {'account_name': 'cbu-bing121720'}, {'account_name': 'cbb6622691'}, {'account_name': 'caifei_2008'}, {'account_name': 'changyihua'}, {'account_name': 'chaxiang135'}, {'account_name': 'caohui1981920'}, {'account_name': 'cgx5788'}, {'account_name': 'caifei560'}, {'account_name': 'chenhuafeng19840923'}, {'account_name': 'bxj5020'}, {'account_name': 'caiy冰'}, {'account_name': 'b豆豆哥'}, {'account_name': 'chang鹅'}, {'account_name': 'caiyuejing1'}, {'account_name': 'chijuanjuantb'}, {'account_name': 'chen陈馨馨'}, {'account_name': 'changma1121234035'}, {'account_name': 'chengnuo69114321'}, {'account_name': 'Cherry莉小成'}, {'account_name': 'capegirardeau'}, {'account_name': 'chenshufen陈'}, {'account_name': 'cdr1959'}, {'account_name': 'cheng溪舟'}, {'account_name': 'chentao9678'}, {'account_name': 'caiping547540'}, {'account_name': 'chenrui'}, {'account_name': 'chenxiangyu071253'}, {'account_name': 'cchhda'}, {'account_name': 'chenlu9233'}, {'account_name': 'chenmanquan5'}, {'account_name': 'cassy洛洛'}, {'account_name': 'cherry_103722'}, {'account_name': 'butterfly_527'}, {'account_name': 'caiwb1984'}, {'account_name': 'chenna18896524689'}, {'account_name': 'carsontian2014'}, {'account_name': 'cai111017'}, {'account_name': 'chenxin3379047'}, {'account_name': 'cgm19621016'}, {'account_name': 'candy43219'}, {'account_name': 'chenweidong2011'}, {'account_name': 'chenluluyaoyao'}, {'account_name': 'chenwei8476'}, {'account_name': 'chenqiuyue520520'}, {'account_name': 'cassidy_y'}, {'account_name': 'chenyp46'}, {'account_name': 'butty104'}, {'account_name': 'cemeb'}, {'account_name': 'chen6221886'}, {'account_name': 'cdd1122110'}, {'account_name': 'chengmeiyin_88'}, {'account_name': 'b詹粱yy'}, {'account_name': 'cckkd'}, {'account_name': 'can捻'}, {'account_name': 'cellyhuang'}, {'account_name': 'carrie_012'}, {'account_name': 'chang199707'}, {'account_name': 'chenjuan628628'}, {'account_name': 'c13303769129'}, {'account_name': 'cgh笛声'}, {'account_name': 'bxl909909'}, {'account_name': 'ccrtnnua'}, {'account_name': 'caiyundang520'}, {'account_name': 'chengeng0416'}, {'account_name': 'bzpmcl'}, {'account_name': 'ccssqq3333'}, {'account_name': 'chao67421749'}, {'account_name': 'chenchu1220'}, {'account_name': 'chenxi19791001'}, {'account_name': 'chenxiuyev'}, {'account_name': 'cas君小逸'}, {'account_name': 'chenxuejiao201211'}, {'account_name': 'cfh20140905'}, {'account_name': 'chenlilin371428'}, {'account_name': 'cc24681'}, {'account_name': 'carrie091'}, {'account_name': 'ccy45059220'}, {'account_name': 'chichipoppy'}, {'account_name': 'chenxiaoning620921'}, {'account_name': 'byebye8818'}, {'account_name': 'chen1014234893'}, {'account_name': 'chenyujie525'}, {'account_name': 'chenlihuixin'}, {'account_name': 'chengchong1992418'}, {'account_name': 'certylcf'}, {'account_name': 'changlipu'}, {'account_name': 'chenfwjj'}, {'account_name': 'chenxiaoman011'}, {'account_name': 'c620357'}, {'account_name': 'cbwzwazztmf'}, {'account_name': 'bxcbbb9'}, {'account_name': 'c1158803436'}, {'account_name': 'chenlijuan20131981'}, {'account_name': 'chengzi567899'}, {'account_name': 'c3gloen3rqz'}, {'account_name': 'chanjava'}, {'account_name': 'cd流年思绪'}, {'account_name': 'ccy_cai'}, {'account_name': 'cathyhoward'}, {'account_name': 'caonaizhong11'}, {'account_name': 'chengxiaolong2003'}, {'account_name': 'casper啊国'}, {'account_name': 'chenchen56320'}, {'account_name': 'chenlingyu141111'}, {'account_name': 'cc3234898'}, {'account_name': 'careamanda'}, {'account_name': 'chenyujong'}, {'account_name': 'changlinai131'}, {'account_name': 'chh19861116'}, {'account_name': 'candiline1102'}, {'account_name': 'chengzhihui2008'}, {'account_name': 'chenyumin88899'}, {'account_name': 'cao363636aa'}, {'account_name': 'chenyaot2'}, {'account_name': 'cc陈陈陈10086'}, {'account_name': 'cced0001'}, {'account_name': 'c9235009'}, {'account_name': 'chenglei352'}, {'account_name': 'b不忘初心x'}, {'account_name': 'cathylin1019'}, {'account_name': 'cheefy'}, {'account_name': 'caijiaming86'}, {'account_name': 'cdgsoaa37818'}, {'account_name': 'cancan199131'}, {'account_name': 'cby19990410'}, {'account_name': 'chenpengfei_2001'}, {'account_name': 'chenmengying0109'}, {'account_name': 'bzhbo1002'}, {'account_name': 'chenxi199085'}, {'account_name': 'CCJCXC5201314'}, {'account_name': 'CC17878751415'}, {'account_name': 'chenyang77889'}, {'account_name': 'celi10871688'}, {'account_name': 'buyneil'}, {'account_name': 'c378776887'}, {'account_name': 'cheesecake26'}, {'account_name': 'caixia19901230'}, {'account_name': 'chenglong120382782'}, {'account_name': 'chenzicz'}, {'account_name': 'by15295458998'}, {'account_name': 'caiwuyan12'}, {'account_name': 'chengshiqiang'}, {'account_name': 'cgrong'}, {'account_name': 'caiyigu'}, {'account_name': 'cctv99922'}, {'account_name': 'cfy0606'}, {'account_name': 'chen2hao32007'}, {'account_name': 'cheercora'}, {'account_name': 'bustera'}, {'account_name': 'Ccdd123皖'}, {'account_name': 'cgy789456123'}, {'account_name': 'caoxin110'}, {'account_name': 'cha6813'}, {'account_name': 'chengenwu520'}, {'account_name': 'chinghsiao0215'}, {'account_name': 'chenxi121'}, {'account_name': 'chenmei802320'}, {'account_name': 'bylb35'}, {'account_name': 'catty1217'}, {'account_name': 'celina889905153023'}, {'account_name': 'caohongbode'}, {'account_name': 'cc2590'}, {'account_name': 'cctv婷儿'}, {'account_name': 'carrylol'}, {'account_name': 'ccy7758521'}, {'account_name': 'cbu-andrew1945'}, {'account_name': 'chenweijj'}, {'account_name': 'c372669139'}, {'account_name': 'cblhaoren'}, {'account_name': 'ch147'}, {'account_name': 'chengsmalllove'}, {'account_name': 'chenzhenying123'}, {'account_name': 'chenglm47520'}, {'account_name': 'cc大白菜123'}, {'account_name': 'chinadeng555'}, {'account_name': 'cenxue666'}, {'account_name': 'charm_tomato'}, {'account_name': 'cc玉苗'}, {'account_name': 'caoyu7582'}, {'account_name': 'c4982921'}, {'account_name': 'cc大山里的孩子'}, {'account_name': 'chi2132089'}, {'account_name': 'chenteming'}, {'account_name': 'chenyingrui2012'}, {'account_name': 'C781912'}, {'account_name': 'cadgcwd'}, {'account_name': 'bzg761018'}, {'account_name': 'chengzfqq'}, {'account_name': 'chen甜心'}, {'account_name': 'chenzhenbo1993'}, {'account_name': 'chahckh3'}, {'account_name': 'chen娜娜d'}, {'account_name': 'chenyuan9009'}, {'account_name': 'chengmuhao201452'}, {'account_name': 'chenqian2805954447'}, {'account_name': 'chenyanm259'}, {'account_name': 'cheng981130188'}, {'account_name': 'cdq66609'}, {'account_name': 'caiqingpo22'}, {'account_name': 'cf9450'}, {'account_name': 'chengmin11'}, {'account_name': 'chensi我爱你'}, {'account_name': 'cbu-chy4159'}, {'account_name': 'cgg_0001'}, {'account_name': 'ceciletw'}, {'account_name': 'cf8586'}, {'account_name': 'chentingting8812'}, {'account_name': 'cc40777'}, {'account_name': 'chaochao3'}, {'account_name': 'celia彩虹1'}, {'account_name': 'cch19910607'}, {'account_name': 'caohueixin2010'}, {'account_name': 'chaopn5'}, {'account_name': 'c354964192'}, {'account_name': 'bxygrnu07120'}, {'account_name': 'chhiloveyout'}, {'account_name': 'cgp9322'}, {'account_name': 'chenyuehua29'}, {'account_name': 'chen18678487880'}, {'account_name': 'buziyi1234'}, {'account_name': 'buziyi1'}, {'account_name': 'cansado0104'}, {'account_name': 'chaomm0805'}, {'account_name': 'ch040404'}, {'account_name': 'challenge111'}, {'account_name': 'carrie_chm'}, {'account_name': 'cc9813888'}, {'account_name': 'candystim'}, {'account_name': 'byc2269'}, {'account_name': 'cexgjqxgo752513'}, {'account_name': 'bxxgdxjye553253'}, {'account_name': 'cancan250'}, {'account_name': 'chasty0212'}, {'account_name': 'chan彤彤彤'}, {'account_name': 'charlest710'}, {'account_name': 'chenmei_9300'}, {'account_name': 'cbu-zhangxiaoyu002'}, {'account_name': 'cbu-su060888'}, {'account_name': 'chaochaoyi'}, {'account_name': 'ch8601'}, {'account_name': 'caokaori12345'}, {'account_name': 'caiyerhappy'}, {'account_name': 'changmerson'}, {'account_name': 'chenmeimei5201'}, {'account_name': 'chenmeng831107'}, {'account_name': 'chenchen红利'}, {'account_name': 'ceng4567'}, {'account_name': 'cao85206'}, {'account_name': 'chengxingyuhdjdjsh'}, {'account_name': 'chaojifangfang'}, {'account_name': 'cch121005'}, {'account_name': 'cai克芳'}, {'account_name': 'c466658910'}, {'account_name': 'cao可口可乐77'}, {'account_name': 'chensisi19890826'}, {'account_name': 'cbu-taoba52'}, {'account_name': 'Chenyuebin54'}, {'account_name': 'chenliang6214195'}, {'account_name': 'cavijxgn'}, {'account_name': 'cdjinhao1988'}, {'account_name': 'chencheng624726'}, {'account_name': 'cheng289430309'}, {'account_name': 'cccc春明'}, {'account_name': 'chenxiaozhang01'}, {'account_name': 'carol_liu8288'}, {'account_name': 'chenggeas'}, {'account_name': 'cencen_5213344风'}, {'account_name': 'caiyishui1991'}, {'account_name': 'chenyawenc'}, {'account_name': 'chanfay默默'}, {'account_name': 'celinee31'}, {'account_name': 'chen393627697'}, {'account_name': 'caiyiyi0927'}, {'account_name': 'chensworden.m'}, {'account_name': 'c13935701872'}, {'account_name': 'cff3456'}, {'account_name': 'caffyli'}, {'account_name': 'calvin_hoo'}, {'account_name': 'cbu-x297987414'}, {'account_name': 'bvfhfhk'}, {'account_name': 'cherryaiyi'}, {'account_name': 'bxtser1028'}, {'account_name': 'caiyungw'}, {'account_name': 'chenxiyq'}, {'account_name': 'chen20070912'}, {'account_name': 'butoo'}, {'account_name': 'chenxinyi女儿'}, {'account_name': 'chenchuanfangabc'}, {'account_name': 'chengda616'}, {'account_name': 'caunse'}, {'account_name': 'chennig'}, {'account_name': 'catty0026'}, {'account_name': 'cherry丶anicca'}, {'account_name': 'cbu-wu584520'}, {'account_name': 'caicai04010825'}, {'account_name': 'c2991540s'}, {'account_name': 'bu筱鹏'}, {'account_name': 'chennianmiao'}, {'account_name': 'chenwanzheng_2007'}, {'account_name': 'chenxilucky99'}, {'account_name': 'chenyixia23'}, {'account_name': 'chenchao226'}, {'account_name': 'candy895525788'}, {'account_name': 'chenhui_1988211'}, {'account_name': 'CC5908'}, {'account_name': 'bururururababongbarabong'}, {'account_name': 'calarity'}, {'account_name': 'cheng5105'}, {'account_name': 'chang71082525'}, {'account_name': 'cchun646578632'}, {'account_name': 'c799328867'}, {'account_name': 'cancan11'}, {'account_name': 'chen耳朵10'}, {'account_name': 'chenlibang8899'}, {'account_name': 'cheng_380349342'}, {'account_name': 'caijieli1'}, {'account_name': 'cher1012'}, {'account_name': 'bywzxbz'}, {'account_name': 'caozewen2004'}, {'account_name': 'chenhua12368'}, {'account_name': 'chenayumi'}, {'account_name': 'chenliu904'}, {'account_name': 'ch4163319'}, {'account_name': 'chenpulin133'}, {'account_name': 'chatilion'}, {'account_name': 'capescott'}, {'account_name': 'chen_yi_88'}, {'account_name': 'bychhwoi'}, {'account_name': 'chen120995033'}, {'account_name': 'carson引'}, {'account_name': 'chenghui666888'}, {'account_name': 'chen小叮当123456'}, {'account_name': 'cghhys'}, {'account_name': 'chengwenwen13141'}, {'account_name': 'chen痴'}, {'account_name': 'chenmyth8'}, {'account_name': 'cbu-ma555888'}, {'account_name': 'cdy18777506770'}, {'account_name': 'chao1449748246'}, {'account_name': 'callmeegg'}, {'account_name': 'cbu-meteorfeifei'}, {'account_name': 'ch810099'}, {'account_name': 'ccc不懂裝懂'}, {'account_name': 'cc2小思'}, {'account_name': 'cashdev'}, {'account_name': 'chinayanzhou'}, {'account_name': 'ccs斯斯'}, {'account_name': 'chenzhenghangmama'}, {'account_name': 'Chhr520'}, {'account_name': 'chen_qiong_yu'}, {'account_name': 'caihaifei15211616251'}, {'account_name': 'chenguangzhou2012'}, {'account_name': 'caiqingdie'}, {'account_name': 'cassiopeiax1226'}, {'account_name': 'cheny2012i0630'}, {'account_name': 'chao767585740'}, {'account_name': 'cenchengzhong76'}, {'account_name': 'chenfuzhen9'}, {'account_name': 'ccmoveccmove'}, {'account_name': 'ccccccccccc_007'}, {'account_name': 'chenboshi2020'}, {'account_name': 'chen13078449'}, {'account_name': 'chenweijian2006'}, {'account_name': 'chenzhiyun1989'}, {'account_name': 'chen51612625'}, {'account_name': 'chengzhiyan9184'}, {'account_name': 'chengxiaomadebaobei'}, {'account_name': 'chenjun198109'}, {'account_name': 'chenskred1'}, {'account_name': 'chenwz2010'}, {'account_name': 'cgownhhk81'}, {'account_name': 'caodan0001'}, {'account_name': 'cbu-nvhai2012'}, {'account_name': 'changshast'}, {'account_name': 'chenchayu0317'}, {'account_name': 'chenwenjie2008_2008'}, {'account_name': 'chenling0419'}, {'account_name': 'cherycofe'}, {'account_name': 'chg1203'}, {'account_name': 'candy_caojia'}, {'account_name': 'bxf1026'}, {'account_name': 'chenshaorui122'}, {'account_name': 'chenbin7623519'}, {'account_name': 'ccc0578公公'}, {'account_name': 'chen81989'}, {'account_name': 'che7122140'}, {'account_name': 'canseqiqi7'}, {'account_name': 'chance34'}, {'account_name': 'cailu5210'}, {'account_name': 'chenya715831'}, {'account_name': 'cdl1275983933'}, {'account_name': 'chbmork'}, {'account_name': 'cbu-jjoker'}, {'account_name': 'cfwuxiaobing'}, {'account_name': 'carllx'}, {'account_name': 'chenjunxi'}, {'account_name': 'chendan99107'}, {'account_name': 'cbu-f8533666'}, {'account_name': 'chenjingweii'}, {'account_name': 'carina5250'}, {'account_name': 'cbu-clairesu41'}, {'account_name': 'chenmin861122'}, {'account_name': 'chenye19990502'}, {'account_name': 'caishujing0808'}, {'account_name': 'chenyan15691569'}, {'account_name': 'bu忘初心888'}, {'account_name': 'BZ任性淘'}, {'account_name': 'cherry_liu1188'}, {'account_name': 'ccjj3321015'}, {'account_name': 'chenweilong20011221'}, {'account_name': 'cancan851015'}, {'account_name': 'caiqiucheng'}, {'account_name': 'bx094'}, {'account_name': 'caotong1006'}, {'account_name': 'cbu-xiao20110816'}, {'account_name': 'cherry2006_tb'}, {'account_name': 'cataw4y'}, {'account_name': 'caocong926'}, {'account_name': 'cencen123_2009'}, {'account_name': 'ccippyongyuan'}, {'account_name': 'cecelia0112'}, {'account_name': 'cghhvdgnh'}, {'account_name': 'chenchenwoaini201119'}, {'account_name': 'chengjingyuan555'}, {'account_name': 'caicheng201388'}, {'account_name': 'cbu-aaron0923'}, {'account_name': 'ccyang2012'}, {'account_name': 'caojing0712w'}, {'account_name': 'cenbaowei'}, {'account_name': 'caifeng333333'}, {'account_name': 'chinapax'}, {'account_name': 'ccxx6301'}, {'account_name': 'chenbaoxia19900101'}, {'account_name': 'caojian443012894'}, {'account_name': 'bx柒猫猫'}, {'account_name': 'chenyonghua78'}, {'account_name': 'chen000562587'}, {'account_name': 'chendan8533'}, {'account_name': 'cbu-dandan307'}, {'account_name': 'cheungyy0622'}, {'account_name': 'chaochao211026'}, {'account_name': 'by2晓俊'}, {'account_name': 'chenwen91'}, {'account_name': 'chang_music'}, {'account_name': 'chenrongrong93'}, {'account_name': 'chenuwang'}, {'account_name': 'CCB陈长彪'}, {'account_name': 'chenliqiong1986'}, {'account_name': 'cbh13562011465'}, {'account_name': 'chenbolai88'}, {'account_name': 'chiangwill'}, {'account_name': 'chenshaohua18hao'}, {'account_name': 'chengnuotiajiale'}, {'account_name': 'cc的被子'}, {'account_name': 'cbu-gs414580'}, {'account_name': 'cassiopeia985711'}, {'account_name': 'c123xiongwei'}, {'account_name': 'cheng776279'}, {'account_name': 'changeabl_e'}, {'account_name': 'c11yingxiong'}, {'account_name': 'c843839103'}, {'account_name': 'changleletaobao'}, {'account_name': 'buy8899'}, {'account_name': 'chengtongwei'}, {'account_name': 'caixiaona_2007'}, {'account_name': 'chen13383842470'}, {'account_name': 'changwei530308'}, {'account_name': 'caiqing0813'}, {'account_name': 'bxb18389175029'}, {'account_name': 'chengzhengneng'}, {'account_name': 'chengcheng461'}, {'account_name': 'caohong英18551091366'}, {'account_name': 'cfcfc2005'}, {'account_name': 'chenpeng4500'}, {'account_name': 'chang会1989'}, {'account_name': 'cgwe135'}, {'account_name': 'chen_依酷'}, {'account_name': 'chen_1912'}, {'account_name': 'cctv168_007'}, {'account_name': 'catava_tan'}, {'account_name': 'chentianjie921126'}, {'account_name': 'chencanmh'}, {'account_name': 'ccs小鹿'}, {'account_name': 'chd1115'}, {'account_name': 'caozhenyu'}, {'account_name': 'caofang15093008122'}, {'account_name': 'chenjia891210'}, {'account_name': 'canyun901109'}, {'account_name': 'bxs8614711'}, {'account_name': 'chenjinliang11'}, {'account_name': 'chenyuqiao26'}, {'account_name': 'b丨boy阿德'}, {'account_name': 'chenjingcheng低调0620'}, {'account_name': 'chinaboyzq'}, {'account_name': 'butterflye'}, {'account_name': 'caiwuzhuguan'}, {'account_name': 'chen1330014200'}, {'account_name': 'chengoushi123'}, {'account_name': 'cathy851117'}, {'account_name': 'calvin_qi'}, {'account_name': 'chenzheng1320'}, {'account_name': 'candyxien'}, {'account_name': 'changgui1262107047'}, {'account_name': 'chenyan1983408'}, {'account_name': 'chanbass'}, {'account_name': 'caidingtian123'}, {'account_name': 'caoqishu19851127'}, {'account_name': 'charleslena'}, {'account_name': 'chenzhanyong1992'}, {'account_name': 'cherie潴'}, {'account_name': 'cdncxc'}, {'account_name': 'cao志霞'}, {'account_name': 'cfz15135977600'}, {'account_name': 'chengshuoyan521'}, {'account_name': 'c15163747057'}, {'account_name': 'cccczk'}, {'account_name': 'chenzezxm'}, {'account_name': 'caryy灬on'}, {'account_name': 'chenjinglin_8023'}, {'account_name': 'china徐祥'}, {'account_name': 'calpeace'}, {'account_name': 'chilijin85'}, {'account_name': 'ceryszjx'}, {'account_name': 'caiy萍'}, {'account_name': 'cdd00oo'}, {'account_name': 'cgf33061678'}, {'account_name': 'chengkuan07'}, {'account_name': 'chen斌仔o'}, {'account_name': 'chenlichun丽纯'}, {'account_name': 'chenzhaojin2011'}, {'account_name': 'chenxi365511099'}, {'account_name': 'chen_minglan'}, {'account_name': 'cch_0301'}, {'account_name': 'chimneyouyangchao'}, {'account_name': 'chen13237239110'}, {'account_name': 'chao470503'}, {'account_name': 'chao8783'}, {'account_name': 'chenpanpan1008'}, {'account_name': 'chenyuguoguo_2009'}, {'account_name': 'cbu-mayoutao'}, {'account_name': 'chen5714581'}, {'account_name': 'c445347327'}, {'account_name': 'chenzhi9561'}, {'account_name': 'chengzheyan265'}, {'account_name': 'ccc陈泽集'}, {'account_name': 'chen柏汛'}, {'account_name': 'chen13140000'}, {'account_name': 'chenjun627'}, {'account_name': 'ccc51ss'}, {'account_name': 'caoliang_777'}, {'account_name': 'c571540535'}, {'account_name': 'cavrain'}, {'account_name': 'chentangqiuqiu'}, {'account_name': 'chao13935828228'}, {'account_name': 'chengchaommsina'}, {'account_name': 'cdwoaini9'}, {'account_name': 'chen792202215'}, {'account_name': 'chenhua3024'}, {'account_name': 'changchang1984'}, {'account_name': 'call_yan11da'}, {'account_name': 'c778093993'}, {'account_name': 'cc_胖胖'}, {'account_name': 'carolgbq'}, {'account_name': 'cdpub'}, {'account_name': 'cenganson111'}, {'account_name': 'cfkeeet553'}, {'account_name': 'cece_20'}, {'account_name': 'cansijin114'}, {'account_name': 'cao626810332'}, {'account_name': 'cenhuini'}, {'account_name': 'cangtry'}, {'account_name': 'cathyzhang0918'}, {'account_name': 'can770722'}, {'account_name': 'candy_阳儿'}, {'account_name': 'cdm87438607'}, {'account_name': 'chen林海'}, {'account_name': 'chen_weixiao'}, {'account_name': 'c386043960'}, {'account_name': 'ccl713'}, {'account_name': 'cauhqzhang'}, {'account_name': 'buzhidao呢'}, {'account_name': 'chenzeping198885'}, {'account_name': 'chenli9942'}, {'account_name': 'chenxue79'}, {'account_name': 'cc112014'}, {'account_name': 'cad45nm5'}, {'account_name': 'caohaonan0621'}, {'account_name': 'cai香'}, {'account_name': 'carze55'}, {'account_name': 'bxl880725'}, {'account_name': 'caijk8978'}, {'account_name': 'chenleicl5'}, {'account_name': 'chengqi08729'}, {'account_name': 'cd548'}, {'account_name': 'chen清新'}, {'account_name': 'ce121635595'}, {'account_name': 'cheng小黄人'}, {'account_name': 'ccq阳光失意'}, {'account_name': 'cbgnd161843'}, {'account_name': 'chenbaiming88888'}, {'account_name': 'c1731954157f'}, {'account_name': 'chen群873967158'}, {'account_name': 'cacasea'}, {'account_name': 'buxiangnai'}, {'account_name': 'cafuc111111'}, {'account_name': 'chen小敏a'}, {'account_name': 'carlosxinxin'}, {'account_name': 'chenleichl'}, {'account_name': 'cherrychen10'}, {'account_name': 'chenfangli82'}, {'account_name': 'chenchen319123'}, {'account_name': 'champaign1992'}, {'account_name': 'chao18093452182'}, {'account_name': 'cain_lx'}, {'account_name': 'chaiwei12345'}, {'account_name': 'ch120748787'}, {'account_name': 'caicai114104'}, {'account_name': 'chengzhongmei20122013'}, {'account_name': 'baoshuangcom'}, {'account_name': '1024286736ma'}, {'account_name': '8伟大的梦想8'}, {'account_name': '18014565365'}, {'account_name': '87715408啊'}, {'account_name': 'chenxiuqun9098'}, {'account_name': 'angel昊2013'}, {'account_name': '1017_huangting'}, {'account_name': 'ai344979552'}, {'account_name': '1537567402@qq.com'}, {'account_name': '15777822811'}, {'account_name': 'aiganyanqing'}, {'account_name': '2675wen'}, {'account_name': 'casnapa'}, {'account_name': '13176957359'}, {'account_name': '18281855990'}, {'account_name': 'cdplaycd'}, {'account_name': 'can灿宝贝79159184'}, {'account_name': 'cbb12312312'}, {'account_name': '2015姚家人'}, {'account_name': 'chaoge861210'}, {'account_name': 'aronggu'}, {'account_name': '17072742894'}]


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