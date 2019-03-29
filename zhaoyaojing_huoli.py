# coding=utf-8
import requests
import time
import json
from lxml import etree
import pymysql

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
    sql = 'insert into shuangying_huolifu(ww,buyreputation,bussreputation,sex,favrate,regdate,amoyage,buyweeklyaver,querytime,real_name,vip_level,vip_info,tucao,tuzi,mihuan,huli,eyu,disposalsitus,blacklist,label,averagetimes,consumpower,userarea,sendrate,buyfrequency,userrefund,terminal,add_time) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d")' % (
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

# huoli_url = 'http://plm.huolifu.com/comm_plat_huoli/out_bind_info'
# content = requests.get(url=huoli_url).json()
content = [{'account_name': 'windsboy0'}, {'account_name': 't_1482072513396_0678 '}, {'account_name': 'wangul123'}, {'account_name': 't_1490751425861_0921'}, {'account_name': 'wgjyf51314'}, {'account_name': 't_1498529621826_0336'}, {'account_name': 'tpf7594'}, {'account_name': 'wang诺诺0605'}, {'account_name': 'whirlpoolkitty'}, {'account_name': 'tt一生的呼召'}, {'account_name': 't_1504018734540_0383'}, {'account_name': 't_1480048986823_0674'}, {'account_name': 'tlaa73815'}, {'account_name': 'wn真帅'}, {'account_name': 't_1497407135572_0784'}, {'account_name': 'wuyanbo62'}, {'account_name': 't_1493422804453_0649'}, {'account_name': 'wk102633106'}, {'account_name': 't_1504190498561_0906'}, {'account_name': 'tb凌未风'}, {'account_name': 't_1486124276996_0799'}, {'account_name': 't_1507391903745_0253'}, {'account_name': 't_1491919956017_0333'}, {'account_name': 'tlppp1'}, {'account_name': 'wangyueyao917'}, {'account_name': 'tb_6995076'}, {'account_name': 'why5833217936'}, {'account_name': 't_1479742220666_0364'}, {'account_name': 'wylhsp'}, {'account_name': 'tutu4618212'}, {'account_name': 'wing010a'}, {'account_name': 't_1488847562252_0558'}, {'account_name': 'wenzhe092933'}, {'account_name': 't_1509018031316_0670'}, {'account_name': 'wanglin9330'}, {'account_name': 'wx好态度123'}, {'account_name': 'unclelee2012'}, {'account_name': 'wyl_bh'}, {'account_name': 'wumingru958'}, {'account_name': 'waynesjw'}, {'account_name': 'weng喵喵'}, {'account_name': 'ting1234_54'}, {'account_name': 't_1507454473692_0492'}, {'account_name': 'weishu燕'}, {'account_name': 'w19810304126com'}, {'account_name': 'tel小怪'}, {'account_name': 't_1502023719695_0379'}, {'account_name': 't_1502163348469_0589'}, {'account_name': 'tb可昕可菲'}, {'account_name': 't_1503637675817_0562'}, {'account_name': 't_1478357687291_0'}, {'account_name': 'vipcomlz'}, {'account_name': 'tb_5394127'}, {'account_name': 'vakegogo'}, {'account_name': 'tb_9043901'}, {'account_name': 'toy丶喃'}, {'account_name': 'wozilinbaba521'}, {'account_name': 'tb_5647631'}, {'account_name': 'wjm13638004751'}, {'account_name': 't_1478483778467_0'}, {'account_name': 't_1514518881342_0165'}, {'account_name': 't_1509922009165_0521'}, {'account_name': 't_1509154634616_0535'}, {'account_name': 't_1489410249152_073'}, {'account_name': 'ttzyzxjlqr'}, {'account_name': 'wq125718'}, {'account_name': 'wintersun50'}, {'account_name': 'thy阳光宝贝'}, {'account_name': 'wwfok3950231'}, {'account_name': 't_1506668034700_07'}, {'account_name': 't_1494048513632_0550'}, {'account_name': 'wo886688666'}, {'account_name': 'tb_李海珍'}, {'account_name': 'wsxp天王盖地虎'}, {'account_name': 'w281987650'}, {'account_name': 'wangnawei_0'}, {'account_name': 'wintersun5022'}, {'account_name': 'txp201328'}, {'account_name': 't_1481633414083_0286'}, {'account_name': 'tp0816ch'}, {'account_name': 'wenlovebobo'}, {'account_name': 'ttthj'}, {'account_name': 'whhs168'}, {'account_name': 'tb如花si玉'}, {'account_name': 'wang77615'}, {'account_name': 'v_vando_o'}, {'account_name': 'whklslu66735'}, {'account_name': 't_1479178681374_0'}, {'account_name': 't_1515982652764_075'}, {'account_name': 'wanghua201501'}, {'account_name': 't_1516072535851_0851'}, {'account_name': 't_1479600192384_0743'}, {'account_name': 'timkly'}, {'account_name': 'vcubic'}, {'account_name': 't_1486037165311_0239'}, {'account_name': 'woshi578770628'}, {'account_name': 'wwwtb2525'}, {'account_name': 't_1512135871177_0346'}, {'account_name': 'wly9899'}, {'account_name': 'tutu3162461'}, {'account_name': 'wangyimao111'}, {'account_name': 'wangyuegz'}, {'account_name': 'wang770614'}, {'account_name': 'wangyizi1223'}, {'account_name': 'wnugt4'}, {'account_name': 'wj901128'}, {'account_name': 't_1508128106019_0920'}, {'account_name': 'volcano198954'}, {'account_name': 'tb_8795221'}, {'account_name': 'tfdsdf'}, {'account_name': 't_1502601688357_0838'}, {'account_name': 'wmywkg'}, {'account_name': 'wu59987981'}, {'account_name': 'vbhtfs'}, {'account_name': 'wang20110729'}, {'account_name': 'w2226424814'}, {'account_name': 'tb_9633232'}, {'account_name': 't_1481514229518_0892'}, {'account_name': 't_1505561280733_0347'}, {'account_name': 'wyq18789565871'}, {'account_name': 'vnzpjr'}, {'account_name': 'wppdl'}, {'account_name': 'tb_8716728'}, {'account_name': 'tyz845570890'}, {'account_name': 'wilberlin'}, {'account_name': 'www787926397'}, {'account_name': 't_1483420742252_0810'}, {'account_name': 'timao_xiho'}, {'account_name': 'wmaiyh1314'}, {'account_name': 'wsadwsad37'}, {'account_name': 'ttqqyyttqqyy'}, {'account_name': 'vinc2nt'}, {'account_name': 'tzweys'}, {'account_name': 'whf天蓝蓝'}, {'account_name': 'vkiidow'}, {'account_name': 't_1504066518962_0897'}, {'account_name': 'wuhuahua600207'}, {'account_name': 'w162057168'}, {'account_name': 'weiailh'}, {'account_name': 'woaihailuo'}, {'account_name': 'woyaoshoping'}, {'account_name': 'wozai258236'}, {'account_name': 't_1514455675902_0169'}, {'account_name': 'vae许嵩2013'}, {'account_name': 't_1479015562053_0'}, {'account_name': 't_1484191137501_0903'}, {'account_name': 'wangjiangxia55555'}, {'account_name': 'wxl9966'}, {'account_name': 'wmy王梦瑶1996'}, {'account_name': 'tony_rar'}, {'account_name': 't_1478507595474_0'}, {'account_name': 'wx_2012'}, {'account_name': 'unicompany'}, {'account_name': 'wxy15820001005'}, {'account_name': 't_1478859642167_0'}, {'account_name': 'tc小半边天'}, {'account_name': 'winger19861212'}, {'account_name': 'windding1981'}, {'account_name': 'wlawx1314'}, {'account_name': 'tptp1991'}, {'account_name': 'wdghk3154'}, {'account_name': 'tkgg长风破浪'}, {'account_name': 'wlw0364'}, {'account_name': 'woyao355'}, {'account_name': 'www叶倾城'}, {'account_name': 't_1499391974046_0196'}, {'account_name': 't_1500957119114_0545'}, {'account_name': 'tiffanybb141201'}, {'account_name': 'wangtt01133'}, {'account_name': 'wangjunqf'}, {'account_name': 't_1507032739577_0780'}, {'account_name': 't_1509689070373_0415'}, {'account_name': 'wx米兰阳光'}, {'account_name': 't_1489378304002_0145'}, {'account_name': 't_1490370138589_0332'}, {'account_name': 'wuxqaihaohao'}, {'account_name': 't_1493348413288_0427'}, {'account_name': 't_1515245998721_0175'}, {'account_name': 'wenhonglin81'}, {'account_name': 't_1486006723175_0241'}, {'account_name': 't_1479470230964_0458'}, {'account_name': 't_1489148171596_0561'}, {'account_name': 'tcmelody0521'}, {'account_name': 't_1493284749004_0574'}, {'account_name': 't_1516191072702_0437'}, {'account_name': 't_1512738633124_0423'}, {'account_name': 't_1482287523158_089'}, {'account_name': 'tsaopuchun'}, {'account_name': 'w1102032061'}, {'account_name': 't_1504969547133_0206'}, {'account_name': 'tw9521'}, {'account_name': 'wudw1024'}, {'account_name': 't_1484623616005_0636'}, {'account_name': 't_1491216077594_0926'}, {'account_name': 'wwenmg'}, {'account_name': 't_1481099232790_0280'}, {'account_name': 'wangjieen'}, {'account_name': 't_1493294495030_0317'}, {'account_name': 'wdan0233'}, {'account_name': 'tmzhtb'}, {'account_name': 'tianzhiya04413675'}, {'account_name': 't_1493777888338_0408'}, {'account_name': 'wdd854943795'}, {'account_name': 't_1495625662471_0503'}, {'account_name': 'wfeather'}, {'account_name': 't_1502357315128_0710'}, {'account_name': 'wangqianming12'}, {'account_name': 't_1512040969877_023'}, {'account_name': 'woshiliuyj'}, {'account_name': 'wu飘飘98'}, {'account_name': 'wangyuchieh18949'}, {'account_name': 'tb王晓菲'}, {'account_name': 't_1507496041182_0456'}, {'account_name': 't_1498996538229_0849'}, {'account_name': 'wangshangfei70'}, {'account_name': 'th888126'}, {'account_name': 'w260261685'}, {'account_name': 't_1494428211682_0730'}, {'account_name': 'why353012592'}, {'account_name': 'wang911122'}, {'account_name': 't_1503924734180_0677'}, {'account_name': 'violet她的花'}, {'account_name': 'vincenfang'}, {'account_name': 'vbabeibei'}, {'account_name': 't_1494989860649_0429'}, {'account_name': 'tiantiantian阳阳'}, {'account_name': 'wangyong38289'}, {'account_name': 'weijuan1119'}, {'account_name': 'ting欣然'}, {'account_name': 't_1507366482646_0972'}, {'account_name': 't_1485016871397_074'}, {'account_name': 'wqxiangxuan2017'}, {'account_name': 'winds_0214'}, {'account_name': 'vicky萱妈'}, {'account_name': 'wqm139356'}, {'account_name': 't_1491992236347_0702'}, {'account_name': 't_1505635409221_0252'}, {'account_name': 't_1483600285849_0731'}, {'account_name': 'wujiezhu'}, {'account_name': 'tingting16156083'}, {'account_name': 'wgc20081209w'}, {'account_name': 't_1486867799196_0292'}, {'account_name': 'tp1159'}, {'account_name': 't_1509008857934_0827'}, {'account_name': 'vipzyh17'}, {'account_name': 't_1510050873088_0803'}, {'account_name': 't_1493023497739_0160'}, {'account_name': 'Wangyuede0122'}, {'account_name': 't_1503057361976_0320'}, {'account_name': 'wangying25881'}, {'account_name': 'wo5544388'}, {'account_name': 'wangzixuan851015'}, {'account_name': 'wenxin363'}, {'account_name': 'wojiazhuxiaoben'}, {'account_name': 'tongwingian'}, {'account_name': 't_1504847236562_0335'}, {'account_name': 't_1484326692211_0805'}, {'account_name': 'watslxl001'}, {'account_name': 'weijianan19881123'}, {'account_name': 'tianchengongyi'}, {'account_name': 't_1497267441159_0742'}, {'account_name': 'wukongdou'}, {'account_name': 't_1504568319058_0847'}, {'account_name': 'wuyue585'}, {'account_name': 'touming蓝鸟'}, {'account_name': 'w8116492'}, {'account_name': 'vintagesunflower'}, {'account_name': 't_1482231099994_0133'}, {'account_name': 't_1480509549638_0806'}, {'account_name': 'wanjianhua009'}, {'account_name': 't_1502088548803_0137'}, {'account_name': 'wangwei_8023'}, {'account_name': 't_1489653992122_0286'}, {'account_name': 'tb_9606292'}, {'account_name': 'wxf34'}, {'account_name': 't_1501382208869_0619'}, {'account_name': 'wuyun1037191496'}, {'account_name': 'tb_4525178'}, {'account_name': 't_1491555032791_067'}, {'account_name': 't_1510927830791_0226'}, {'account_name': 't_1513657029819_0798'}, {'account_name': 't_1511787868362_064'}, {'account_name': 't_1490962000889_0251'}, {'account_name': 'wjz402373372'}, {'account_name': 't_1513835060592_0170'}, {'account_name': 't_1482130790114_0211'}, {'account_name': 'wangtao19901122'}, {'account_name': 'wang占修'}, {'account_name': 'weiyizhe9'}, {'account_name': 'u9865973'}, {'account_name': 'tgpgtmjwtpwt'}, {'account_name': 't_1513259051325_0395'}, {'account_name': 'wj107288483'}, {'account_name': 't_1503815297893_045'}, {'account_name': 'wxr9152'}, {'account_name': 't_1514198648764_0577'}, {'account_name': 't_1478387482269_0'}, {'account_name': 't_1486715894152_0587'}, {'account_name': 't_1501756562165_0794'}, {'account_name': 't_1480913502591_0586'}, {'account_name': 'wowangxiao_119418'}, {'account_name': 'wh1519100876'}, {'account_name': 'w1394183572'}, {'account_name': 't_1496045810477_0570'}, {'account_name': 't_1499051084919_0236'}, {'account_name': 'tb小洋人'}, {'account_name': 'tb_3122702'}, {'account_name': 't_1491055544808_0384'}, {'account_name': 'waterboss0621'}, {'account_name': 't_1503313240295_0448'}, {'account_name': 'whl19881003'}, {'account_name': 'txf13926629152'}, {'account_name': 't_1491223647516_0929'}, {'account_name': 'wuzhihuaailiujie1117'}, {'account_name': 'thkley0'}, {'account_name': 'tian仅有的'}, {'account_name': 'weichensheng1'}, {'account_name': 't_1481526149862_0778'}, {'account_name': 't_1491987976416_0507'}, {'account_name': 'w2006y728'}, {'account_name': 'tommy211'}, {'account_name': 'wangguangsen1978'}, {'account_name': 'ting转身离开'}, {'account_name': 't_1493798517258_0184'}, {'account_name': 't_1487637830689_057'}, {'account_name': 't_1499596660418_0374'}, {'account_name': 't_1481169405314_0473'}, {'account_name': 't_1479278763764_0'}, {'account_name': 't_1510048300024_0971'}, {'account_name': 't_1505717862527_0435'}, {'account_name': 'tb_5014523'}, {'account_name': 'wwrr胡萝卜'}, {'account_name': 'tianxin890'}, {'account_name': 'ww929293743.'}, {'account_name': 't_1495662023947_0600'}, {'account_name': 'whereareyou我在这里等你'}, {'account_name': 'wudongchaolove'}, {'account_name': 'tb_9886238'}, {'account_name': 'wumengls'}, {'account_name': 'wfy877716336'}, {'account_name': 'vickyzx成'}, {'account_name': 'wangli1511585544848302505'}, {'account_name': 'wolzyj'}, {'account_name': 't_1482566783541_0289'}, {'account_name': 't_1492478298961_0898'}, {'account_name': 'ws86o8'}, {'account_name': 't_1515932514981_0501'}, {'account_name': 't_1527411443613_0171'}, {'account_name': 'wv0a102711'}, {'account_name': 'wang407ting'}, {'account_name': 'vivovivo梅'}, {'account_name': 'two1819'}, {'account_name': 't_1513401007786_0125'}, {'account_name': 'wangdonghongzhai'}, {'account_name': 'wj1602459366366'}, {'account_name': 'wulinlingai5'}, {'account_name': 'tutu88ooo'}, {'account_name': 'warm橘林'}, {'account_name': 't_1487763039950_0663'}, {'account_name': 'wjwsh0107'}, {'account_name': 't_1493991797141_0807'}, {'account_name': 'tm1111gouwu'}, {'account_name': 'tianfei5220080'}, {'account_name': 'tfpivp'}, {'account_name': 'wangdi159951'}, {'account_name': 'wwjthlwsq'}, {'account_name': 'w15853314162'}, {'account_name': 't_1494927731008_0969'}, {'account_name': 'wxz风雨彩虹'}, {'account_name': 't唐冬梅t'}, {'account_name': 'wawa1965_2009'}, {'account_name': 't_1493386809507_060'}, {'account_name': 't_1509428007502_0426'}, {'account_name': 't_1492608970409_0405'}, {'account_name': 't_1491783125019_0379'}, {'account_name': 'wxx779290733'}, {'account_name': 'wodetaobao199206'}, {'account_name': 'tsx318'}, {'account_name': 'tianyouxi1982'}, {'account_name': 'tgy941560419'}, {'account_name': 't_1505271244216_0378'}, {'account_name': 't_1509763666427_0824'}, {'account_name': 'tb_583549'}, {'account_name': 't_1490772502937_0498'}, {'account_name': 'tmmj001'}, {'account_name': 't_1480212281663_0895'}, {'account_name': 't_1501350971858_079'}, {'account_name': 't_1486374185357_0746'}, {'account_name': 't_1485315063701_046'}, {'account_name': 't_1499577184069_0347'}, {'account_name': 'tjhdhr001'}, {'account_name': 'wuyunli517'}, {'account_name': 'wjy785016'}, {'account_name': 't_1511883090832_0787'}, {'account_name': 't_1482556911923_035'}, {'account_name': 'tyn0114'}, {'account_name': 'wuziyao201209'}, {'account_name': 'wxf2399'}, {'account_name': 'wee_j'}, {'account_name': 't_1489390773930_0846'}, {'account_name': 't_1508211251803_0879'}, {'account_name': 't_1501425751240_0185'}, {'account_name': 't_1504169797217_0831'}, {'account_name': 'vothone'}, {'account_name': 't_1511764192471_0705'}, {'account_name': 't_1507868601219_0615'}, {'account_name': 'wh821211741'}, {'account_name': 'wt4117'}, {'account_name': 'wcm13876749097'}, {'account_name': 'tianyagang1'}, {'account_name': 'w082113'}, {'account_name': 'wbxyfl'}, {'account_name': 'weizhusuoxin86'}, {'account_name': 't_1480662176476_0417'}, {'account_name': 't_1510205447555_0782'}, {'account_name': 't_1511439272431_0697'}, {'account_name': 't_1485921461500_0231'}, {'account_name': 'vivenn'}, {'account_name': 't_1488518430621_0591'}, {'account_name': 'weixu0529'}, {'account_name': 't_1487990889410_0998'}, {'account_name': 't_1501914416996_0224'}, {'account_name': 'tcdog'}, {'account_name': 'vaierns一族'}, {'account_name': 'tb_98642'}, {'account_name': 'wttrwd'}, {'account_name': 'wu249254088'}, {'account_name': 'wyl2627278'}, {'account_name': 'vivi菇凉'}, {'account_name': 't_1514727811015_067'}, {'account_name': 'utem1026'}, {'account_name': 't_1482059804315_0343'}, {'account_name': 'ww929293743'}, {'account_name': 't_1496674896131_0830'}, {'account_name': 'wangyucui0108'}, {'account_name': 'wen123cc'}, {'account_name': 'wli118'}, {'account_name': 't_1482624854303_044'}, {'account_name': 'wang瞌睡宝宝'}, {'account_name': 'teddynier'}, {'account_name': 'wwj51907337'}, {'account_name': 'tyqayy'}, {'account_name': 'tb_6909381'}, {'account_name': 't_1512708330915_00'}, {'account_name': 'www23456'}, {'account_name': 'wangxiaoyong1988'}, {'account_name': 'viky0227'}, {'account_name': 'wenhuameng'}, {'account_name': 't_1507858092650_0423'}, {'account_name': 'w44584472'}, {'account_name': 'wuhenruf'}, {'account_name': 't_1507028505907_0535'}, {'account_name': 't_1498792586182_0194'}, {'account_name': 'wenguang_0518'}, {'account_name': 'U9941057'}, {'account_name': 't_1480794323992_0610'}, {'account_name': 't_1497622680135_039'}, {'account_name': 't_1483180017712_0434旺旺名禅心有机'}, {'account_name': 'tian_56'}, {'account_name': 'tianlanbeiji'}, {'account_name': 'wolovebaby1'}, {'account_name': 'wang52013682575'}, {'account_name': 'woaimeinv180'}, {'account_name': 't_1488437017186_0411'}, {'account_name': 'weilong58888'}, {'account_name': 't_1499421064727_0123'}, {'account_name': 'wuyou1897'}, {'account_name': 't_1481015184788_0999'}, {'account_name': 'wangbiao_7739'}, {'account_name': 't_1514343456377_0225'}, {'account_name': 'the小星星啦啦'}, {'account_name': 't_1499908624015_0354'}, {'account_name': 'wang13863231366'}, {'account_name': 't_1508075752478_0231'}, {'account_name': 't_1515282487166_0875'}, {'account_name': 'tb东方朔'}, {'account_name': 't_1485615834961_0942'}, {'account_name': 'u723497603'}, {'account_name': 't_1505017421586_0856'}, {'account_name': 't_1482333134472_076'}, {'account_name': 'T_1514363043735_0402'}, {'account_name': 't_1498115366795_0187'}, {'account_name': 'tfjfxbnh73739'}, {'account_name': 't_1510243799311_0220'}, {'account_name': 'wangjieqb'}, {'account_name': 'wjlwjx20072010'}, {'account_name': 't_1514278809025_0681'}, {'account_name': 'ty兰兰天空'}, {'account_name': 'vig_001'}, {'account_name': 't_1496588972411_0451'}, {'account_name': 'wanghkaituo30'}, {'account_name': 'wj1020315'}, {'account_name': 'tb_5534413'}, {'account_name': 'tb_19870317'}, {'account_name': 'www柠檬绿茶'}, {'account_name': 't_1498031198795_0663'}, {'account_name': 'tc冯俊光'}, {'account_name': 'wjp890416'}, {'account_name': 'tianping_1128'}, {'account_name': 'win_liu888666'}, {'account_name': 'why7525'}, {'account_name': 'warrq'}, {'account_name': 't_1486720177377_0424'}, {'account_name': 'weiyidehuamanlou'}, {'account_name': 'ww3242'}, {'account_name': 'thandlz'}, {'account_name': 'wq陈伟强'}, {'account_name': 't_1509985350200_0440'}, {'account_name': 'vudfguihottx'}, {'account_name': 'wjwjiuhuo'}, {'account_name': 'ttrb2838'}, {'account_name': 'tb_6189473'}, {'account_name': 't_1500692632979_0772'}, {'account_name': 'wangzai1066'}, {'account_name': 'tom888828'}, {'account_name': 't_1528082081206_0349'}, {'account_name': 'ted006'}, {'account_name': 'wa_jm_2005'}, {'account_name': 'wspxm123'}, {'account_name': 'wei445316342'}, {'account_name': 'wanxx519926'}, {'account_name': 't_1484749726437_017'}, {'account_name': 't_1485783850334_+0892'}, {'account_name': 't_1508486415153_0843'}, {'account_name': 't_1498903190741_0917'}, {'account_name': 't_1495538054963_0575'}, {'account_name': 'weiweigxz'}, {'account_name': 'tracy0093'}, {'account_name': 'wangxuan1266126'}, {'account_name': 'wuxiaola521'}, {'account_name': 't_1512969118980_0936'}, {'account_name': 'wanghuanrui66'}, {'account_name': 'woaiwojia344'}, {'account_name': 't_1480313565355_0914'}, {'account_name': 't_1487165682033_0281'}, {'account_name': 'wangshuai19860112'}, {'account_name': 'verylike504'}, {'account_name': 'wing5211314'}, {'account_name': 'w839969149'}, {'account_name': 't_1484282395001_0102'}, {'account_name': 'wujianbo0882'}, {'account_name': 'w18060616114'}, {'account_name': 'tb_4701727'}, {'account_name': 't_1487835401555_095'}, {'account_name': 't_1510639617352_018'}, {'account_name': 't_1478574551314_0'}, {'account_name': 't_1487669634686_0131'}, {'account_name': 'wangluosa002598387'}, {'account_name': 't_1508581796220_0959'}, {'account_name': 't_1489205780581_0489'}, {'account_name': 'wang770615'}, {'account_name': 'thinkingbing'}, {'account_name': 'wxd521214'}, {'account_name': 'wen文人'}, {'account_name': 'woai亚洲125'}, {'account_name': 't_14886608011640_779'}, {'account_name': 'W6023597'}, {'account_name': 'wl20041029'}, {'account_name': 'tb_6891463'}, {'account_name': 'tb_3108096'}, {'account_name': 't_1482071394164_0852'}, {'account_name': 'terrytmf'}, {'account_name': 'wangruang'}, {'account_name': 'tb两0131'}, {'account_name': 't_1507193682146_0189'}, {'account_name': 'tb_7064569'}, {'account_name': 'tsuki0000'}, {'account_name': 't_1488516873660_0703'}, {'account_name': 't_1494426571251_0945'}, {'account_name': 't_1496639354012_0605'}, {'account_name': 'wtohotnba'}, {'account_name': 't_1510964272985_022'}, {'account_name': 'wanggang520chong'}, {'account_name': 'wangliangbeibei'}, {'account_name': 't_1511614643238_0947'}, {'account_name': 't_1480945384260_0844'}, {'account_name': 'viavia温'}, {'account_name': 't_1480342303703_0250'}, {'account_name': 'weinisi008'}, {'account_name': 'tskb130'}, {'account_name': 't_1479191700309_0'}, {'account_name': 'wuwei52013140110'}, {'account_name': 't_1482160785935_0938'}, {'account_name': 'tb_5870924'}, {'account_name': 'wbzds握不住的沙'}, {'account_name': 't_1485650563351_0573'}, {'account_name': 't_1511084803417_0213'}, {'account_name': 't_1514285173882_086'}, {'account_name': 'wangxing200988'}, {'account_name': 'tttttttttttt2'}, {'account_name': 'w153997455'}, {'account_name': 't_1508737606273_0158'}, {'account_name': 't_1500203605626_0880'}, {'account_name': 'wangweidong220'}, {'account_name': 'Tkyer'}, {'account_name': 'tb_5897123'}, {'account_name': 'vaca1216'}, {'account_name': 'whphzp'}, {'account_name': 'ugv3jshop.'}, {'account_name': 'wuna8385'}, {'account_name': 'wl0501026'}, {'account_name': 'wanglu68'}, {'account_name': 'w13487707342'}, {'account_name': 'tyw280837444'}, {'account_name': 'wy1993yf'}, {'account_name': 'wangsanfu2'}, {'account_name': 'wo13998250208'}, {'account_name': 'wwy582261482'}, {'account_name': 't_1514463198295_0488'}, {'account_name': 't_1481109772144_0109'}, {'account_name': 't_1508304422420_0338'}, {'account_name': 'wuyi8888888888'}, {'account_name': 'wuting19880822'}, {'account_name': 'tianyanyanlovehui'}, {'account_name': 'weijiansuoxin'}, {'account_name': 't_1496057492963_0630'}, {'account_name': 'vifa277'}, {'account_name': 'wolf801129'}, {'account_name': 'wuyong6718'}, {'account_name': 'wingchiehpih'}, {'account_name': 'woaiwangwang永远'}, {'account_name': 'tootongs'}, {'account_name': 't_1504280701789_0588'}, {'account_name': 'tutu8901'}, {'account_name': 'tb张春'}, {'account_name': 't_1497782782586_0277'}, {'account_name': 't_1499469154573_0781'}, {'account_name': 'tb_7822597'}, {'account_name': 'veranj1988'}, {'account_name': 'wulinlin325'}, {'account_name': 't_1499867864319_0694'}, {'account_name': 't_1479420036328_0406'}, {'account_name': 't_1498421667412_0445'}, {'account_name': 'vampire620'}, {'account_name': 'tb_6223933'}, {'account_name': 'w443255696'}, {'account_name': 'wwj1241651589'}, {'account_name': 't_1514194602959_0925'}, {'account_name': 't_1483921181927_090'}, {'account_name': 'wym15347602742'}, {'account_name': 'V影子是时光的心'}, {'account_name': 't_1491547945295_0540'}, {'account_name': 'toborchen'}, {'account_name': 'wang4215708'}, {'account_name': 't_1496143332433_0703'}, {'account_name': 't_1516463984651_051'}, {'account_name': 't_1494092361771_0479'}, {'account_name': 'tmchen0728'}, {'account_name': 't_1494899344659_0927'}, {'account_name': 'v空间'}, {'account_name': 'tb_4114856'}, {'account_name': 'tianmao99022'}, {'account_name': 't_1509520136655_091'}, {'account_name': 'wangjing6199'}, {'account_name': 'tramywqm'}, {'account_name': 'whqjcd'}, {'account_name': 'tiaotiao0123'}, {'account_name': 'woshiwangziqian'}, {'account_name': 'theone1983'}, {'account_name': 'tb_6067172'}, {'account_name': 'tb_5020829'}, {'account_name': 't_1479221864165_0'}, {'account_name': 'wbh714'}, {'account_name': 't_1503887001450_0851'}, {'account_name': 'terence419'}, {'account_name': 'wtb20140730'}, {'account_name': 'woaitayishengys'}, {'account_name': 'tb_79310'}, {'account_name': 't_1488936586426_0246'}, {'account_name': 't_1514107259774_0584'}, {'account_name': 'tingting26zheng'}, {'account_name': 'welcomelibo'}, {'account_name': 't_1508504013054_0591'}, {'account_name': 'tear954'}, {'account_name': 't_1505098060808_0198'}, {'account_name': 'wcjian55'}, {'account_name': 't_1500962593367_0241'}, {'account_name': 'wy18037039696'}, {'account_name': 't_1502239954999_0227'}, {'account_name': 'tb_9870153'}, {'account_name': 'wjw660086'}, {'account_name': 't_1513769137047_0134'}, {'account_name': 't_1488717615253_0298'}, {'account_name': 'tb_1837422'}, {'account_name': 't_1504294702823_0642'}, {'account_name': 'wujinjing1'}, {'account_name': 't_1481183087718_059'}, {'account_name': 't_1507382072497_0120'}, {'account_name': 'ww换个'}, {'account_name': 'tyydabaobei521'}, {'account_name': 't_1481035808474_0350'}, {'account_name': 't_1486700020376_0823'}, {'account_name': 't_1493284655139_0378'}, {'account_name': 'wgd_bh'}, {'account_name': 'woaixiaofeifei2007'}, {'account_name': 't_1486089543827_0485'}, {'account_name': 't_1510453673778_0745'}, {'account_name': 'wx唯美筱瑄'}, {'account_name': 'vocationel'}, {'account_name': 'T_1507812341905_0991'}, {'account_name': 'walaoehtaoyan'}, {'account_name': 't_1503230686567_0236'}, {'account_name': 'wo135997710'}, {'account_name': 't_1508934399761_0607'}, {'account_name': 't_1490178768238_0738'}, {'account_name': 'wo小肥兔shi'}, {'account_name': 't_1483067589681_0841'}, {'account_name': 't_1486995738118_0793'}, {'account_name': 't_1515661190633_082'}, {'account_name': 't_1484841872865_0713'}, {'account_name': 'wunaiyou'}, {'account_name': 't_1505453588115_0344'}, {'account_name': 'wangliying553024'}, {'account_name': 'wghshch1'}, {'account_name': 'tjl谭锦龙'}, {'account_name': 't_1485956847414_0809'}, {'account_name': 't_1509883580094_0197'}, {'account_name': 't_1514032584072_0624'}, {'account_name': 'weodfg'}, {'account_name': 'thewhitelie'}, {'account_name': 't_1482021519211_0938'}, {'account_name': 'tzrzx1988'}, {'account_name': 'wanglei782141'}, {'account_name': 't_1478793941768_0'}, {'account_name': 't_1490173452046_062'}, {'account_name': 't_1510193665661_087'}, {'account_name': 'tujun133'}, {'account_name': 'tianqishen6'}, {'account_name': 'wymzj2588'}, {'account_name': 'whff1985'}, {'account_name': 'wskihc88'}, {'account_name': 't婷yu雨'}, {'account_name': 't_1484838803474_055'}, {'account_name': 't_1482225706031_0407'}, {'account_name': 'wm王萌萌55'}, {'account_name': 't_1482940648375_0585'}, {'account_name': 'tonywear929'}, {'account_name': 'tb76052493'}, {'account_name': 'tb_3771103'}, {'account_name': 'winner67880'}, {'account_name': 'wucx812'}, {'account_name': 't_1484992020934_0542'}, {'account_name': 't_1497428077490_0750'}, {'account_name': 'watb15825870005'}, {'account_name': 'wangdong 136157'}, {'account_name': 'woaini12310603246'}, {'account_name': 't_1499493269142_08'}, {'account_name': 'top小菲菲'}, {'account_name': 'tb_3098524'}, {'account_name': 't_1482298989246_0364'}, {'account_name': 't_1488325505962_0864'}, {'account_name': 'wsy1172128658'}, {'account_name': 'tcylxs'}, {'account_name': 'wo8300feng'}, {'account_name': 'wtt不是我太乖'}, {'account_name': 'wjcxhl'}, {'account_name': 'wang671105'}, {'account_name': 'wgx娃娃'}, {'account_name': 'wuhr1115'}, {'account_name': 't_1515809586656_0346'}, {'account_name': 'whyf126'}, {'account_name': 'w2474931730'}, {'account_name': 't_1497014105564_0378'}, {'account_name': 't_1489207369410_0123'}, {'account_name': 'uehzushbs'}, {'account_name': 'w1401738814'}, {'account_name': 't_1508371462689_0739'}, {'account_name': 'vus806588'}, {'account_name': 't_1502708971311_0525'}, {'account_name': 't_1483886836935_065'}, {'account_name': 'www王月如'}, {'account_name': 'wojiaomeng'}, {'account_name': 't_1488501111325_0667'}, {'account_name': 'wangdanrui2006'}, {'account_name': 't_1479369697722_0'}, {'account_name': 'woyingng'}, {'account_name': 't_1513928244847_0219'}, {'account_name': 'va3225'}, {'account_name': 'tb_8110257'}, {'account_name': 't_1484106901646_0740'}, {'account_name': 'tengyongning110'}, {'account_name': 'wangpenghui720614534'}, {'account_name': 'Why_19821013'}, {'account_name': 'vgsl736708'}, {'account_name': 't_1508769813232_0888'}, {'account_name': 't_1486738522274_0557'}, {'account_name': 't_1485948136945_0240'}, {'account_name': 't_1489225613209_0247'}, {'account_name': 'tb_6456391'}, {'account_name': 'wenisgod0513'}, {'account_name': 'wangshi888'}, {'account_name': 't_1506163963001_0184'}, {'account_name': 'wenfuchao'}, {'account_name': 'weihang598'}, {'account_name': 't_1498370793035_0271'}, {'account_name': 't_1510359928407_0161'}, {'account_name': 't_1513319685632_0487'}, {'account_name': 'wgheat_q'}, {'account_name': 'wwyyyuiiuui'}, {'account_name': 'woliu9'}, {'account_name': 't_1505022026964_0203'}, {'account_name': 'wodejiangxin'}, {'account_name': 'wd可爱宝贝03608266'}, {'account_name': 'ttzz20135'}, {'account_name': 'wjp12345699'}, {'account_name': 't_1497498314229_0145'}, {'account_name': 'woshihuazai888898'}, {'account_name': 'wujing15172252250'}, {'account_name': 'tonlin41788'}, {'account_name': 'tsangel贝贝'}, {'account_name': 'wangronggui99'}, {'account_name': 'wxyabc123_ji'}, {'account_name': 'V望尘莫及1'}, {'account_name': 'wang_shizhan'}, {'account_name': 'wmht2006'}, {'account_name': 't_1506515305080_0123'}, {'account_name': 'tiantianxiang1710'}, {'account_name': 'wxrbbx'}, {'account_name': 'tyb368'}, {'account_name': 'wang188160738'}, {'account_name': 't_1482481727525_0890'}, {'account_name': 't_1493712860350_0886'}, {'account_name': 'wuqun117'}, {'account_name': 't_1502367488118_0383'}, {'account_name': 't_1525877545947_0323'}, {'account_name': 'wdsa369'}, {'account_name': 'tlily0502'}, {'account_name': 'wuyahan20141203'}, {'account_name': 'vickyaya99'}, {'account_name': 'wangweichengxu'}, {'account_name': 't_1503325464446_0150'}, {'account_name': 't_1495162685740_037'}, {'account_name': 'trlan'}, {'account_name': 't_1502620387668_0672'}, {'account_name': 'tb_3967515'}, {'account_name': 'wujing8710081688'}, {'account_name': 'wsyqx于清鑫'}, {'account_name': 'umin_yang'}, {'account_name': 'tgt1972'}, {'account_name': 'tttttop888'}, {'account_name': 'thr62698038'}, {'account_name': 't_1478410539662_0'}, {'account_name': 'wyb125426'}, {'account_name': 'www13963826921'}, {'account_name': 't_1505226372907_0723'}, {'account_name': 'wb_chen2005'}, {'account_name': 'wdh315675514'}, {'account_name': 't_1515850118904_0374'}, {'account_name': 'Wangyali0514'}, {'account_name': 'wdsr159'}, {'account_name': 't_1493475187807_0243'}, {'account_name': 't_1496737487001_019'}, {'account_name': 't_14886626058822_0884'}, {'account_name': 't_1487508418909_0545'}, {'account_name': 'ting51246230'}, {'account_name': 'wcxmissyou'}, {'account_name': 'wxq20131227'}, {'account_name': 'wendy490825'}, {'account_name': 'tom1993415'}, {'account_name': 'wupeixuan601'}, {'account_name': 'why200209'}, {'account_name': 'ws992954'}, {'account_name': 'ulayay527'}, {'account_name': 't_1504064324281_0624'}, {'account_name': 't_1481636097155_0511'}, {'account_name': 'wodegehai'}, {'account_name': 't_1496741556103_0145'}, {'account_name': 't_1495121942663_0988'}, {'account_name': 'topming2008'}, {'account_name': 'tianyongan168'}, {'account_name': 'wanwan313'}, {'account_name': 't_1497003856813_0791'}, {'account_name': 't_1492934660017_0678'}, {'account_name': 'thj1045'}, {'account_name': 't_1495087088874_0372'}, {'account_name': 't_1495818727784_0599'}, {'account_name': 'wenxiang50201664'}, {'account_name': 't_1491918404038_021'}, {'account_name': 'wenyiwenmei'}, {'account_name': 'h13832648598'}, {'account_name': 't_1494679401559_0565'}, {'account_name': 'wangyueya19'}, {'account_name': 't_1513148901108_0746'}, {'account_name': 'tt暧昧1991'}, {'account_name': 't_1512786291325_0820'}, {'account_name': 'titikaka0311'}, {'account_name': 'u9hko3xylje'}, {'account_name': 'wangchuanyun2012'}, {'account_name': 'wushunlove'}, {'account_name': 'woodz75'}, {'account_name': 't_1499949356923_0800'}, {'account_name': 'wvvwuuuuu'}, {'account_name': 'tt_eddie'}, {'account_name': 't_t大爱罗志祥'}, {'account_name': 'uegoudongj'}, {'account_name': 't_1479612170904_0814'}, {'account_name': 'weihuilim2009'}, {'account_name': 'tb572448710'}, {'account_name': 'wangtianyu1989915'}, {'account_name': 'wjq1304701669'}, {'account_name': 'chenyao950802'}, {'account_name': 'tb261425140'}, {'account_name': 'lsj112398'}, {'account_name': 'cqb706212'}, {'account_name': 'tb81169642'}, {'account_name': '15914290308ie'}, {'account_name': 'tb56637487'}, {'account_name': 'tb709074643'}, {'account_name': 'ke18867787882'}, {'account_name': 'tlh960622'}, {'account_name': 't_1488327888748_0539'}, {'account_name': 'tb285833725'}, {'account_name': 'wang446072047'}, {'account_name': 'anzhizi_58'}, {'account_name': 'orclver'}, {'account_name': 'tb28602843'}, {'account_name': '168豆浆油条'}, {'account_name': 'lili215583193'}, {'account_name': 'tb513211808'}, {'account_name': 'lumeng1225'}, {'account_name': 'louisgeyh'}, {'account_name': 'shiluo19920812'}, {'account_name': 'bosaywan'}, {'account_name': 'tb262848068'}, {'account_name': 'tb324644125'}, {'account_name': 'dxjcom'}, {'account_name': 'chongchong892x'}, {'account_name': 'lujunfeng91'}, {'account_name': '15838783880'}, {'account_name': 'baby俪人'}, {'account_name': 'hm520cc'}, {'account_name': 'a416511101'}, {'account_name': 't_1515365633788_0843'}, {'account_name': 't_1507904996956_0852'}, {'account_name': 'aimer_qian'}, {'account_name': 'tb464471342'}, {'account_name': 'tb148149565'}, {'account_name': '15956173087a'}, {'account_name': 'lolicon丶萝莉控'}, {'account_name': 'tb714924_2013'}, {'account_name': 'liji5589'}, {'account_name': 'na@520pw.pw'}, {'account_name': 'pkandnn'}, {'account_name': 'n一半一伴'}, {'account_name': 'tb89401616'}, {'account_name': 'lingli0220'}, {'account_name': 'patricktsang123'}, {'account_name': 'chenchenaiqiqi'}, {'account_name': 'mojicxin'}, {'account_name': 'tb455719958'}, {'account_name': 'tb59911435'}, {'account_name': 'esmove'}, {'account_name': 'ennen'}, {'account_name': 'elfdingdingdandan'}, {'account_name': 'tb76535411'}, {'account_name': 'tb475818321'}, {'account_name': 'h15251907618'}, {'account_name': 'shuaishuai_001'}, {'account_name': 'hl1944553119'}, {'account_name': 'hlyj宁静致远'}, {'account_name': 'tb39662937'}, {'account_name': '13670523141'}, {'account_name': '299wzyj'}, {'account_name': 't_1494853710952_0387'}, {'account_name': 'kaisershy1'}, {'account_name': 'wangfadong1207'}, {'account_name': 'tb13784668'}, {'account_name': '0221zxh'}, {'account_name': 't_1503711781944_0846'}, {'account_name': 'shanlangchuanshuo'}, {'account_name': 'liushili9960'}, {'account_name': 'ergouzi123'}, {'account_name': 'tb150597926'}, {'account_name': 'wangqiangyinfang'}, {'account_name': 'mingchaonaxie2'}, {'account_name': 'psyxff'}, {'account_name': '13522272561'}, {'account_name': 'tb840190958'}, {'account_name': 'jiaju1213'}, {'account_name': 'linpeiwa'}, {'account_name': 'h艳辉'}, {'account_name': 'gcf_001'}, {'account_name': 'tb882202551'}, {'account_name': 'tdh181'}, {'account_name': 'freedom自由之翼'}, {'account_name': 'sunjiang14'}, {'account_name': 'tb959927519'}, {'account_name': 'tb0778176_2011'}, {'account_name': 'jiandeyeya'}, {'account_name': 'tb677540009'}, {'account_name': 'tb03245574'}, {'account_name': 'bingyumuyue'}, {'account_name': 'wanghaiping11111'}, {'account_name': 'q309006132'}, {'account_name': 'tb83366139'}, {'account_name': 'hxscg'}, {'account_name': '308667315@qq.com'}, {'account_name': 'hqw13925442395'}, {'account_name': 'tb236622957'}, {'account_name': 'agudong'}]


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