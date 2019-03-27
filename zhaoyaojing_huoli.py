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
content = [{'account_name': 'tb188699662'}, {'account_name': 'tb38052137'}, {'account_name': 'tb33816'}, {'account_name': 'tb_1080865'}, {'account_name': 'tb1970427281'}, {'account_name': 'tb4091211_2011'}, {'account_name': 'tb54770344'}, {'account_name': 'tb4364417-2011'}, {'account_name': 'tb984158_00'}, {'account_name': 'tb4078525_99'}, {'account_name': 'tb5059844'}, {'account_name': 'tb32553487'}, {'account_name': 'tb717838_2011'}, {'account_name': 'tb20579683'}, {'account_name': 'tb6767147_2013'}, {'account_name': 'tb7167_1978'}, {'account_name': 'tb536391'}, {'account_name': 'tb390498787'}, {'account_name': 'tb19579190'}, {'account_name': 'tb364027_33'}, {'account_name': 'tb62401997'}, {'account_name': 'tb600502533'}, {'account_name': 'tb201200_77'}, {'account_name': 'tb13071654'}, {'account_name': 'tb44307307'}, {'account_name': 'tb20707604'}, {'account_name': 'tb983022840'}, {'account_name': 'tb1312554_11'}, {'account_name': 'tb92057273'}, {'account_name': 'tb60842931'}, {'account_name': 'tb94316788'}, {'account_name': 'tb517538013'}, {'account_name': 'tb41046572'}, {'account_name': 'tb25293244'}, {'account_name': 'tb24833892'}, {'account_name': 'tb4528952_00'}, {'account_name': 'tb7523459_88'}, {'account_name': 'tb911708305'}, {'account_name': 'tb7026711'}, {'account_name': 'tb96027535'}, {'account_name': 'tb262044_22'}, {'account_name': 'tb34993'}, {'account_name': 'tb40737361'}, {'account_name': 'tb70729614'}, {'account_name': 'tb400305701'}, {'account_name': 'tb469370560'}, {'account_name': 'tb19024199'}, {'account_name': 'tb80448454'}, {'account_name': 'tb246269291'}, {'account_name': 'tb167057701'}, {'account_name': 'tb73344115'}, {'account_name': 'tb759828870'}, {'account_name': 'tb861894649'}, {'account_name': 'tb465308741'}, {'account_name': 'tb6736817_2011'}, {'account_name': 'tb185661_2011'}, {'account_name': 'tb6024468-2012'}, {'account_name': 'tb14871336'}, {'account_name': 'tb6939469_88'}, {'account_name': 'tb51159092'}, {'account_name': 'tb312579986'}, {'account_name': 'tb5902600_2013'}, {'account_name': 'tb68766829'}, {'account_name': 'tb4516723_2012'}, {'account_name': 'tb449438203'}, {'account_name': 'tb2942676_2012'}, {'account_name': 'tb45354556'}, {'account_name': 'tb740832888'}, {'account_name': 'tb9732537_00'}, {'account_name': 'tb2771272_2012'}, {'account_name': 'tb8743850_2011'}, {'account_name': 'tb551450951'}, {'account_name': 'tb944809381'}, {'account_name': 'tb663907_77'}, {'account_name': 'tb9800004_2011'}, {'account_name': 'tb463534712'}, {'account_name': 'tb96816265'}, {'account_name': 'tb26325094'}, {'account_name': 'tb3953560_2013'}, {'account_name': 'tb41598156'}, {'account_name': 'tb72316498'}, {'account_name': 'tb6119063_2013'}, {'account_name': 'tb348068804'}, {'account_name': 'tb99664169'}, {'account_name': 'tb825890008'}, {'account_name': 'tb256141348'}, {'account_name': 'tbgukejun123123'}, {'account_name': 'tb91300308'}, {'account_name': 'tb69635063'}, {'account_name': 'tb49606995'}, {'account_name': 'tbb158'}, {'account_name': 'tb903122771'}, {'account_name': 'tb84210266'}, {'account_name': 'tb33150116'}, {'account_name': 'tb669004554'}, {'account_name': 'tb49309486'}, {'account_name': 'tb870097050'}, {'account_name': 'tb966160406'}, {'account_name': 'tb32591043'}, {'account_name': 'tb896692148'}, {'account_name': 'tb362895_22'}, {'account_name': 'tb893880478'}, {'account_name': 'tb881353175'}, {'account_name': 'tbguoyunshe'}, {'account_name': 'tb17623545'}, {'account_name': 'tb86026914'}, {'account_name': 'tb157256196'}, {'account_name': 'tb41935434'}, {'account_name': 'tb495276644'}, {'account_name': 'tb44691314'}, {'account_name': 'tb478964904'}, {'account_name': 'tb83494764'}, {'account_name': 'tb97200920'}, {'account_name': 'tb2757_42'}, {'account_name': 'tb2833166_2012'}, {'account_name': 'tb35916_00'}, {'account_name': 'tb262914310'}, {'account_name': 'tb843471864'}, {'account_name': 'tb220436262'}, {'account_name': 'tb43191427'}, {'account_name': 'tb2860151_2011'}, {'account_name': 'tb96284285'}, {'account_name': 'tb879669492'}, {'account_name': 'tb63471074'}, {'account_name': 'tb55540390'}, {'account_name': 'tb5119506'}, {'account_name': 'tb64618495'}, {'account_name': 'tb651870_99'}, {'account_name': 'tb335705381'}, {'account_name': 'tb6936720_2013'}, {'account_name': 'tb148858_88'}, {'account_name': 'tb758882'}, {'account_name': 'tb649577553'}, {'account_name': 'tbn14728717'}, {'account_name': 'tb30811339'}, {'account_name': 'tb420293898'}, {'account_name': 'tb665679606'}, {'account_name': 'tb87660062'}, {'account_name': 'tb45411906'}, {'account_name': 'tb582425706'}, {'account_name': 'tb97322127'}, {'account_name': 'tb71604560'}, {'account_name': 'tb97419255'}, {'account_name': 'tb902855234'}, {'account_name': 'tb9878687'}, {'account_name': 'tb784177147'}, {'account_name': 'tb8298462'}, {'account_name': 'tb6102909'}, {'account_name': 'tb757248069'}, {'account_name': 'tb77104848'}, {'account_name': 'tb92230114'}, {'account_name': 'tb998687481'}, {'account_name': 'tb84945552'}, {'account_name': 'tb467074525'}, {'account_name': 'tb81647860'}, {'account_name': 'tb563702_2010'}, {'account_name': 'tb48246026'}, {'account_name': 'tb91147190'}, {'account_name': 'tb48582074'}, {'account_name': 'tb614760047'}, {'account_name': 'tb167567111'}, {'account_name': 'tb79876135'}, {'account_name': 'tb930745131'}, {'account_name': 'tb16227383'}, {'account_name': 'tb568670513'}, {'account_name': 'tb565249342'}, {'account_name': 'tb58243077'}, {'account_name': 'tb15867440'}, {'account_name': 'tb28859747'}, {'account_name': 'tb519412242'}, {'account_name': 'tb48458497'}, {'account_name': 'tb72357540'}, {'account_name': 'tb63351622'}, {'account_name': 'tb60965219'}, {'account_name': 'tb22394113'}, {'account_name': 'tb5032815_2012'}, {'account_name': 'tb91132801'}, {'account_name': 'tb833271214'}, {'account_name': 'tb499435_2012'}, {'account_name': 'tb37225568'}, {'account_name': 'tb2874925_2013'}, {'account_name': 'tb834908170'}, {'account_name': 'tb64231018'}, {'account_name': 'tb99381812'}, {'account_name': 'tb87842906'}, {'account_name': 'tb142024706'}, {'account_name': 'tb26287211'}, {'account_name': 'tb232126201'}, {'account_name': 'tb324438445'}, {'account_name': 'tb69954984'}, {'account_name': 'tb621432780'}, {'account_name': 'tb759737798'}, {'account_name': 'tb641660068'}, {'account_name': 'tb352881400'}, {'account_name': 'tb25614014'}, {'account_name': 'tb480035_33'}, {'account_name': 'tb1713_76'}, {'account_name': 'tb21245858'}, {'account_name': 'tb5537785_2013'}, {'account_name': 'tb57219701'}, {'account_name': 'tb84610334'}, {'account_name': 'tb32816162'}, {'account_name': 'tb72923270'}, {'account_name': 'tb4898558_2012'}, {'account_name': 'tb6901599_00'}, {'account_name': 'tb9538573'}, {'account_name': 'tb668643807'}, {'account_name': 'tb852292785'}, {'account_name': 'tb663186184'}, {'account_name': 'tb17829983'}, {'account_name': 'tb4085869_88'}, {'account_name': 'tb206242853'}, {'account_name': 'tb88003278'}, {'account_name': 'tb527752742'}, {'account_name': 'tb50781259'}, {'account_name': 'tb8103377_11'}, {'account_name': 'tb726317875'}, {'account_name': 'tb44299480'}, {'account_name': 'tb538692024'}, {'account_name': 'tb52935579'}, {'account_name': 'tb89340182'}, {'account_name': 'tb_1120157'}, {'account_name': 'tb96352444'}, {'account_name': 'tb210573070'}, {'account_name': 'tb26786527'}, {'account_name': 'tb97419000'}, {'account_name': 'tb23438601'}, {'account_name': 'tb852668_2011'}, {'account_name': 'tb34809577'}, {'account_name': 'tb31360857'}, {'account_name': 'tb486796396'}, {'account_name': 'tb5196075_2011'}, {'account_name': 'tb9117513'}, {'account_name': 'tb99611380'}, {'account_name': 'tb476502388'}, {'account_name': 'tb73809951'}, {'account_name': 'tb20788297'}, {'account_name': 'tb73498165'}, {'account_name': 'tb56608259'}, {'account_name': 'tb78921470'}, {'account_name': 'tb9777341_2012'}, {'account_name': 'tb68759592'}, {'account_name': 'tb84553724'}, {'account_name': 'tb483384808'}, {'account_name': 'tb81211309'}, {'account_name': 'tb549192120'}, {'account_name': 'tb27508470'}, {'account_name': 'tb52648365'}, {'account_name': 'tb551305753'}, {'account_name': 'tb268721_77'}, {'account_name': 'tb8945764_2011'}, {'account_name': 'tb94788817'}, {'account_name': 'tb532452990'}, {'account_name': 'tb21368470'}, {'account_name': 'tb450400131'}, {'account_name': 'tb36525060'}, {'account_name': 'tb70154166'}, {'account_name': 'tb7657357_2011'}, {'account_name': 'tb495809244'}, {'account_name': 'tb590157790'}, {'account_name': 'tb1379520_2012'}, {'account_name': 'tb732133976'}, {'account_name': 'tb56291113'}, {'account_name': 'tb76735210'}, {'account_name': 'tb54488050'}, {'account_name': 'tb66656772'}, {'account_name': 'tb62514278'}, {'account_name': 'tb840921967'}, {'account_name': 'tb567637221'}, {'account_name': 'tb69289742'}, {'account_name': 'tb9311029_2012'}, {'account_name': 'tb56374516'}, {'account_name': 'tb67835853'}, {'account_name': 'tb49861769'}, {'account_name': 'tb88466721'}, {'account_name': 'tb7869141_2012'}, {'account_name': 'tb4644360_2012'}, {'account_name': 'tb479689267'}, {'account_name': 'tb98030019'}, {'account_name': 'tb9736586_2011'}, {'account_name': 'tb214908695'}, {'account_name': 'tb256966401'}, {'account_name': 'tb4489_1918'}, {'account_name': 'tb82254489'}, {'account_name': 'tb305805_2012'}, {'account_name': 'tb2507025_88'}, {'account_name': 'tb23799012'}, {'account_name': 'tb953577341'}, {'account_name': 'tb549237103'}, {'account_name': 'tb26273390'}, {'account_name': 'tb2402562_2012'}, {'account_name': 'tb7489749'}, {'account_name': 'tb972426025'}, {'account_name': 'tb58982462'}, {'account_name': 'tb24495404'}, {'account_name': 'tb19622961'}, {'account_name': 'tb99728809'}, {'account_name': 'tb619315985'}, {'account_name': 'tb38496371'}, {'account_name': 'tb35754411'}, {'account_name': 'tb587585_11'}, {'account_name': 'tb27940458'}, {'account_name': 'tb90649012'}, {'account_name': 'tb49395815'}, {'account_name': 'tb599379307'}, {'account_name': 'tb96605161'}, {'account_name': 'tb653451445'}, {'account_name': 'tb4370844'}, {'account_name': 'tblyy515'}, {'account_name': 'tb846154896'}, {'account_name': 'tb43747317'}, {'account_name': 'tb76461975'}, {'account_name': 'tb542973589'}, {'account_name': 'tb790369374'}, {'account_name': 'tb848134185'}, {'account_name': 'tb13234956'}, {'account_name': 'tb6430183_2012'}, {'account_name': 'tb86616493'}, {'account_name': 'tbtb0520'}, {'account_name': 'tb233586836'}, {'account_name': 'tbwanghuijuan211'}, {'account_name': 'tb58333567'}, {'account_name': 'tb13437814'}, {'account_name': 'tb74023081'}, {'account_name': 'tb92950784'}, {'account_name': 'tb46313315'}, {'account_name': 'tb2131889_2011'}, {'account_name': 'tb16161226'}, {'account_name': 'tb819089802'}, {'account_name': 'tb491758130'}, {'account_name': 'tb19556699'}, {'account_name': 'tb517933280'}, {'account_name': 'tb3689129_88'}, {'account_name': 'tb52129111'}, {'account_name': 'tb38062105'}, {'account_name': 'tb638813870'}, {'account_name': 'tb44807923'}, {'account_name': 'tb470673443'}, {'account_name': 'tb23418005'}, {'account_name': 'tb83083083'}, {'account_name': 'tb863977763'}, {'account_name': 'tb55966806'}, {'account_name': 'tb6981_34'}, {'account_name': 'tb67146698'}, {'account_name': 'tb150719055'}, {'account_name': 'tb58523393'}, {'account_name': 'tb984861807'}, {'account_name': 'tb3277115_99'}, {'account_name': 'tb9644873_2012'}, {'account_name': 'tb79616951'}, {'account_name': 'tb86248468'}, {'account_name': 'tb26925029'}, {'account_name': 'tb827807_2013'}, {'account_name': 'tb738789584'}, {'account_name': 'tb32102507'}, {'account_name': 'tb391632034'}, {'account_name': 'tb553214'}, {'account_name': 'tb40881118'}, {'account_name': 'tb455424905'}, {'account_name': 'tb218331600'}, {'account_name': 'tb810327916230'}, {'account_name': 'tb354929072'}, {'account_name': 'tb91129957'}, {'account_name': 'tb82398291'}, {'account_name': 'tb95542062'}, {'account_name': 'tb92931061'}, {'account_name': 'tb39896147'}, {'account_name': 'tb419204063'}, {'account_name': 'tb96004601'}, {'account_name': 'tb983340867'}, {'account_name': 'tb7142695_2013'}, {'account_name': 'tb6265490_00'}, {'account_name': 'tb245662614'}, {'account_name': 'tb31812908'}, {'account_name': 'tb703398255'}, {'account_name': 'tb30499231'}, {'account_name': 'tb773436244'}, {'account_name': 'tb813540974'}, {'account_name': 'tb97129246'}, {'account_name': 'tb1801266_2012'}, {'account_name': 'tb334523148'}, {'account_name': 'tb920069064'}, {'account_name': 'tb846185099'}, {'account_name': 'tb722965511'}, {'account_name': 'tb19579249'}, {'account_name': 'tb295630739'}, {'account_name': 'tb605722331'}, {'account_name': 'tb57012_11'}, {'account_name': 'tb46461090'}, {'account_name': 'tb6186228_2012'}, {'account_name': 'tb50502076'}, {'account_name': 'tb801525661'}, {'account_name': 'tb24585556'}, {'account_name': 'tb72228909'}, {'account_name': 'tb1494_01'}, {'account_name': 'tb488375366'}, {'account_name': 'tb603313213'}, {'account_name': 'tb79671426'}, {'account_name': 'tb88294393'}, {'account_name': 'tb38329406'}, {'account_name': 'tb72108145'}, {'account_name': 'tb51019609'}, {'account_name': 'tb6393364_2011'}, {'account_name': 'tbn65544436'}, {'account_name': 'tb79363238'}, {'account_name': 'tb30607826'}, {'account_name': 'tb552178654'}, {'account_name': 'tb3210841'}, {'account_name': 'tb500984121'}, {'account_name': 'tb335033876'}, {'account_name': 'tb34301039'}, {'account_name': 'tb221802_77'}, {'account_name': 'tb52578677'}, {'account_name': 'tb919792280'}, {'account_name': 'tb47266127'}, {'account_name': 'tb63960752'}, {'account_name': 'tb286553069'}, {'account_name': 'tb614507126'}, {'account_name': 'tb3885677_2012'}, {'account_name': 'tb914850_44'}, {'account_name': 'tb84890216'}, {'account_name': 'tb6226373_2012'}, {'account_name': 'tb886610474'}, {'account_name': 'tb466615_33'}, {'account_name': 'tb14372228'}, {'account_name': 'tb835549496'}, {'account_name': 'tb41963633'}, {'account_name': 'tb59460243'}, {'account_name': 'tb38060042'}, {'account_name': 'tb3701131_2012'}, {'account_name': 'tb19235121'}, {'account_name': 'tb53948999'}, {'account_name': 'tb98086_22'}, {'account_name': 'tb456051944'}, {'account_name': 'tb1562102_2012'}, {'account_name': 'tb9407376_00'}, {'account_name': 'tb638345305'}, {'account_name': 'tb82802598'}, {'account_name': 'tb984600016'}, {'account_name': 'tb25896758'}, {'account_name': 'tb33353487'}, {'account_name': 'tb98699580'}, {'account_name': 'tb703857142'}, {'account_name': 'tb486619462'}, {'account_name': 'tb21465024'}, {'account_name': 'aa远龙'}, {'account_name': 'tb809873788'}, {'account_name': 'tb13546448'}, {'account_name': 'tb782678934'}, {'account_name': 'tb21908'}, {'account_name': 'tb43867220'}, {'account_name': 'tb250327538'}, {'account_name': 'tb45674481'}, {'account_name': 'tb664884_33'}, {'account_name': 'tb237129208'}, {'account_name': 'tb42982506'}, {'account_name': 'tb725216614'}, {'account_name': 'tb753833730'}, {'account_name': 'tb240258769'}, {'account_name': 'tb19963918'}, {'account_name': 'tb231747180'}, {'account_name': 'tb710924057'}, {'account_name': 'tb621332458'}, {'account_name': 'tb4566615_2012'}, {'account_name': 'tb5873_1984'}, {'account_name': 'tb403397095'}, {'account_name': 'tb69214732'}, {'account_name': 'tb64393006'}, {'account_name': 'tb58539158'}, {'account_name': 'tb894833345'}, {'account_name': 'tb53327925'}, {'account_name': 'tb74413_55'}, {'account_name': 'tb591759880'}, {'account_name': 'tb35503_2013'}, {'account_name': 'tb45644264'}, {'account_name': 'tb12005a'}, {'account_name': 'tb267433758'}, {'account_name': 'tb641226629'}, {'account_name': 'tb88584090'}, {'account_name': 'tb24223235'}, {'account_name': 'tb134831280'}, {'account_name': 'tb87713566'}, {'account_name': 'tb894441572'}, {'account_name': 'tb581766123'}, {'account_name': 'tb956859886'}, {'account_name': 'tb178553973'}, {'account_name': 'tb138602261'}, {'account_name': 'tb93202522'}, {'account_name': 'tb375389291'}, {'account_name': 'tb1756038_201l'}, {'account_name': 'tb7902299_2013'}, {'account_name': 'tb815167320'}, {'account_name': 'tb86859566'}, {'account_name': 'tb23974334'}, {'account_name': 'tb182030123'}, {'account_name': 'tb70832345'}, {'account_name': 'tb6392991_2012'}, {'account_name': 'tb98649758'}, {'account_name': 'tb6602016'}, {'account_name': 'tb6944426_2011'}, {'account_name': 'tb6779727'}, {'account_name': 'tb183160_33'}, {'account_name': 'tb96991976'}, {'account_name': 'tb340005'}, {'account_name': 'tb580915274'}, {'account_name': 'tb82504821'}, {'account_name': 'tb626218518'}, {'account_name': 'tb40222226'}, {'account_name': 'tb74082060'}, {'account_name': 'tb317944280'}, {'account_name': 'tb27572414'}, {'account_name': 'tb92701061'}, {'account_name': 'tb16292500'}, {'account_name': 'tb32636941'}, {'account_name': 'tb938422541'}, {'account_name': 'tb3765204_77'}, {'account_name': 'tb15237823'}, {'account_name': 'tb236496992'}, {'account_name': 'tb79160166'}, {'account_name': 'tb65214896'}, {'account_name': 'tb59021207'}, {'account_name': 'tb231487862'}, {'account_name': 'tb96518727'}, {'account_name': 'tb450365293'}, {'account_name': 'tb595912173'}, {'account_name': 'tb292229823'}, {'account_name': 'tb315704837'}, {'account_name': 'tb877496795'}, {'account_name': 'tb262921446'}, {'account_name': 'tb6184451_11'}, {'account_name': 'tb374285013'}, {'account_name': 'tb56175427'}, {'account_name': 'tb30839299'}, {'account_name': 'tb97499741'}, {'account_name': 'tb827230203'}, {'account_name': 'tb888647477'}, {'account_name': 'tb6063084_2012'}, {'account_name': 'tb26357138'}, {'account_name': 'tb755013710'}, {'account_name': 'tb26673023'}, {'account_name': 'tb906262520'}, {'account_name': 'tb852685561'}, {'account_name': 'tb532489_11'}, {'account_name': 'tb510809583'}, {'account_name': 'tb561368020'}, {'account_name': 'tb4047362'}, {'account_name': 'tb6341_1919'}, {'account_name': 'tb254250403'}, {'account_name': 'tb8303330_2012'}, {'account_name': 'tb60753651'}, {'account_name': 'tb244283731'}, {'account_name': 'tb720171268'}, {'account_name': 'tb838721171'}, {'account_name': 'tb14237931'}, {'account_name': 'tb982602424'}, {'account_name': 'tb90656665'}, {'account_name': 'tb988689_2013'}, {'account_name': 'tb37050010'}, {'account_name': 'tb46763249'}, {'account_name': 'tb16204589'}, {'account_name': 'tb306138939'}, {'account_name': 'tb12217603'}, {'account_name': 'tb714679975'}, {'account_name': 'tb85741934'}, {'account_name': 'tb9436820_2012'}, {'account_name': 'tb53885629'}, {'account_name': 'tb609033170'}, {'account_name': 'tb51617191'}, {'account_name': 'tb179506184'}, {'account_name': 'tb60314593'}, {'account_name': 'tb899845873'}, {'account_name': 'tb2326215'}, {'account_name': 'tb451921215'}, {'account_name': 'tb12611190'}, {'account_name': 'tb51649529'}, {'account_name': 'tb475999199'}, {'account_name': 'tb9560771904'}, {'account_name': 'tb40001475'}, {'account_name': 'tb869840188'}, {'account_name': 'tb772492932'}, {'account_name': 'tb5520308'}, {'account_name': 'tb956933060'}, {'account_name': 'tb695416993'}, {'account_name': 'tb85748280'}, {'account_name': 'tb6469707'}, {'account_name': 'tb9943254'}, {'account_name': 'tb450400773'}, {'account_name': 'tb3693317_22'}, {'account_name': 'tb55824396'}, {'account_name': 'tb574201030'}, {'account_name': 'tb797202401'}, {'account_name': 'tb96179716'}, {'account_name': 'tb7126267_2012'}, {'account_name': 'tb75933104'}, {'account_name': 'tb38927357'}, {'account_name': 'tb57426951'}, {'account_name': 'tb73002178'}, {'account_name': 'tb177680_55'}, {'account_name': 'tb5014401_2012'}, {'account_name': 'tb976832586'}, {'account_name': 'tb381793706'}, {'account_name': 'tb787798387'}, {'account_name': 'tb859013860'}, {'account_name': 'tb87067818'}, {'account_name': 'tb5522689_2011'}, {'account_name': 'tb41045961'}, {'account_name': 'tb93533419'}, {'account_name': 'tb427843347'}, {'account_name': 'tb65541393'}, {'account_name': 'tb7715921_2012'}, {'account_name': 'tb31959423'}, {'account_name': 'tb63759068'}, {'account_name': 'tb91647183'}, {'account_name': 'tb905159220'}, {'account_name': 'tb44256651'}, {'account_name': 'tb932700862'}, {'account_name': 'tb813849307'}, {'account_name': 'tb33943599'}, {'account_name': 'tb876662933'}, {'account_name': 'tb880993201'}, {'account_name': 'tb63926344'}, {'account_name': 'tb865690766'}, {'account_name': 'tb506252_11'}, {'account_name': 'tb527174872'}, {'account_name': 'tb901314577'}, {'account_name': 'tb515755824'}, {'account_name': 'tb1494971_2011'}, {'account_name': 'tb222994103'}, {'account_name': 'tb742575885'}, {'account_name': 'tb5699601_11'}, {'account_name': 'tb596165_2011'}, {'account_name': 'tb4595711_88'}, {'account_name': 'tb70249897'}, {'account_name': 'tb371756_99'}, {'account_name': 'tb8339289_33'}, {'account_name': 'tb60558276'}, {'account_name': 'tb27222996'}, {'account_name': 'tb521679168'}, {'account_name': 'tb6141115_11'}, {'account_name': 'tb91819983'}, {'account_name': 'tb908283050'}, {'account_name': 'tb87520497'}, {'account_name': 'tb901849428'}, {'account_name': 'tb2583161_00'}, {'account_name': 'tb3734137'}, {'account_name': 'tb13808_2012'}, {'account_name': 'tb935271494'}, {'account_name': 'tb40367805'}, {'account_name': 'tbww137495185'}, {'account_name': 'tb317331020'}, {'account_name': 'tb91681998'}, {'account_name': 'tb445479156'}, {'account_name': 'tb188951371'}, {'account_name': 'tb976363782'}, {'account_name': 'tb44577891'}, {'account_name': 'tb23121_23'}, {'account_name': 'tb312403295'}, {'account_name': 'tb687786895'}, {'account_name': 'tb95595200'}, {'account_name': 'tb26853173'}, {'account_name': 'tb9935219_2012'}, {'account_name': 'tb429601784'}, {'account_name': 'tb497119283'}, {'account_name': 'tb786893777'}, {'account_name': 'tb52799647'}, {'account_name': 'tb580585_12'}, {'account_name': 'tb92558811'}, {'account_name': 'tb772274801'}, {'account_name': 'tb5965324_2011'}, {'account_name': 'tb65774746'}, {'account_name': 'tb886578763'}, {'account_name': 'tb20402892'}, {'account_name': 'tb210566673'}, {'account_name': 'tb773542865'}, {'account_name': 'tbfuxinxi'}, {'account_name': 'tb6469582_2012'}, {'account_name': 'tb912757243'}, {'account_name': 'tb48404594'}, {'account_name': 'tb302376042'}, {'account_name': 'tb878730654'}, {'account_name': 'tb75316912'}, {'account_name': 'tb95393602'}, {'account_name': 'tb337091864'}, {'account_name': 'tb867192936'}, {'account_name': 'tb30443016'}, {'account_name': 'tb35357591'}, {'account_name': 'tb231630213'}, {'account_name': 'tb91568699'}, {'account_name': 'tb3511749'}, {'account_name': 'tb4775216_2013'}, {'account_name': 'tb791091699'}, {'account_name': 'tb24077811'}, {'account_name': 'tb736868190'}, {'account_name': 'tb523054550'}, {'account_name': 'tb75961088'}, {'account_name': 'tb97916118'}, {'account_name': 'tb985721669'}, {'account_name': 'tb74308465'}, {'account_name': 'tb705230153'}, {'account_name': 'tb9023736'}, {'account_name': 'tb191370303'}, {'account_name': 'tb399321534'}, {'account_name': 'tb342047283'}, {'account_name': 'tb32807191'}, {'account_name': 'tb384036_2013'}, {'account_name': 'tb64117656'}, {'account_name': 'Tb31118581'}, {'account_name': 'tb213558530'}, {'account_name': 'tb247780536'}, {'account_name': 'tb988360047'}, {'account_name': 'tb401059893'}, {'account_name': 'tb900795671'}, {'account_name': 'tb446725502'}, {'account_name': 'tb404781120'}, {'account_name': 'tb939983025'}, {'account_name': 'tb631422968'}, {'account_name': 'tb553428902'}, {'account_name': 'tb5563585_2013'}, {'account_name': 'tb747966647'}, {'account_name': 'tb15018255391'}, {'account_name': 'tb626675444'}, {'account_name': 'tb760881798'}, {'account_name': 'tb17936409'}, {'account_name': 'tb580647_2012'}, {'account_name': 'tb456983958'}, {'account_name': 'tb29968709'}, {'account_name': 'tb252021197'}, {'account_name': 'tb559769285'}, {'account_name': 'tb94579995'}, {'account_name': 'tb393007946'}, {'account_name': 'tb372394886'}, {'account_name': 'tb88415766'}, {'account_name': 'tb1819783_2012'}, {'account_name': 'tb391667864'}, {'account_name': 'tb_0152084'}, {'account_name': 'tb566301831'}, {'account_name': 'tb67377002'}, {'account_name': 'tb147890665'}, {'account_name': 'Tb683739039'}, {'account_name': 'tb389895693'}, {'account_name': 'tb4996822448'}, {'account_name': 'tb92472608'}, {'account_name': 'tb70845490'}, {'account_name': 'tb33636676'}, {'account_name': 'tb5963795'}, {'account_name': 'tb735117290'}, {'account_name': 'tb538128943'}, {'account_name': 'tb89895469'}, {'account_name': 'tb769439303'}, {'account_name': 'tb91433288'}, {'account_name': 'tb610134531'}, {'account_name': 'tb39645781'}, {'account_name': 'tb84871290'}, {'account_name': 'tb34191836'}, {'account_name': 'tb474650701'}, {'account_name': 'tb75159548'}, {'account_name': 'tb258618481'}, {'account_name': 'tb633010351'}, {'account_name': 'tb6422709_2011'}, {'account_name': 'tb74169778'}, {'account_name': 'tb19174308'}, {'account_name': 'tb45833935'}, {'account_name': 'tb5334380'}, {'account_name': 'tb808858008'}, {'account_name': 'tb85088965'}, {'account_name': 'tb87858519'}, {'account_name': 'tb684864409'}, {'account_name': 'tb850945689'}, {'account_name': 'tb61384025'}, {'account_name': 'tb802638531'}, {'account_name': 'tb7350651_11'}, {'account_name': 'tb755618628'}, {'account_name': 'tb71824069'}, {'account_name': 'tb70290584'}, {'account_name': 'tb315170479'}, {'account_name': 'tb97327_23'}, {'account_name': 'tb509_33'}, {'account_name': 'tb284840960'}, {'account_name': 'tb677152614'}, {'account_name': 'tb34413425'}, {'account_name': 'tb314050516'}, {'account_name': 'tb505874492'}, {'account_name': 'tb989341420'}, {'account_name': 'tb920458238'}, {'account_name': 'tb404891408'}, {'account_name': 'tb31951776'}, {'account_name': 'tb51315477'}, {'account_name': 'tb47055102'}, {'account_name': 'tb388353434'}, {'account_name': 'tb7578555_2012'}, {'account_name': 'tb613110975'}, {'account_name': 'tb557804336'}, {'account_name': 'tb82285763'}, {'account_name': 'tb281242609'}, {'account_name': 'tb117931478'}, {'account_name': 'tb433262573'}, {'account_name': 'tb382938794'}, {'account_name': 'tb47538876'}, {'account_name': 'tb520604431'}, {'account_name': 'tb376190585'}, {'account_name': 'tb8576080_99'}, {'account_name': 'tb5981448_11'}, {'account_name': 'tb972915627'}, {'account_name': 'tb574421093'}, {'account_name': 'tb728330969'}, {'account_name': 'tb386851330'}, {'account_name': 'tb635588070'}, {'account_name': 'tb676741_2013'}, {'account_name': 'tb908405091'}, {'account_name': 'tb29926289'}, {'account_name': 'tb188517420'}, {'account_name': 'tb507853888'}, {'account_name': 'tb339143201'}, {'account_name': 'tb43352730'}, {'account_name': 'tb614375850'}, {'account_name': 'tb794925836'}, {'account_name': 'tb4112270139'}, {'account_name': 'tb53686547'}, {'account_name': 'tb14008045'}, {'account_name': 'tb750554046'}, {'account_name': 'tb622431613'}, {'account_name': 'tb669711413'}, {'account_name': 'tb440698622'}, {'account_name': 'tb313779680'}, {'account_name': 'tb668714369'}, {'account_name': 'tb81145204'}, {'account_name': 'tb395564749'}, {'account_name': 'tb9262442_2012'}, {'account_name': 'tb951033583'}, {'account_name': 'tb99905471'}, {'account_name': 'tb7333742_2012'}, {'account_name': 'tb70289495'}, {'account_name': 'tb75335292'}, {'account_name': 'tb43821091'}, {'account_name': 'tb498521449'}, {'account_name': 'tb68236939'}, {'account_name': 'tb488587497'}, {'account_name': 'tb61927805'}, {'account_name': 'tb34029413'}, {'account_name': 'tb2714_2000'}, {'account_name': 'tb754725794'}, {'account_name': 'tb752363805'}, {'account_name': 'tb529125127'}, {'account_name': 'tb793511581'}, {'account_name': 'tb68289497'}, {'account_name': 'tb171075930'}, {'account_name': 'tb980140566'}, {'account_name': 'tb621602646'}, {'account_name': 'tb25921174'}, {'account_name': 'tb41873322'}, {'account_name': 'tb14033122'}, {'account_name': 'tb71812810'}, {'account_name': 'tb14269164'}, {'account_name': 'tb30355622'}, {'account_name': 'tb645739795'}, {'account_name': 'tb359039927'}, {'account_name': 'tb432127415'}, {'account_name': 'tb531497'}, {'account_name': 'tb28824321'}, {'account_name': 'tb3740614555'}, {'account_name': 'tb955040832'}, {'account_name': 'tb308681928'}, {'account_name': 'tb69778_56'}, {'account_name': 'tb354400403'}, {'account_name': 'tb54745384'}, {'account_name': 'tb37469369'}, {'account_name': 'tb2889520_2012'}, {'account_name': 'tb973106231'}, {'account_name': 'tb976848109'}, {'account_name': 'tb314150322'}, {'account_name': 'tb312807572'}, {'account_name': 'tb88547505'}, {'account_name': 'tb428004332'}, {'account_name': 'tb1928-1949'}, {'account_name': 'tb664200974'}, {'account_name': 'tb58172931'}, {'account_name': 'tb3294540'}, {'account_name': 'tb536688084'}, {'account_name': 'tb5567473'}, {'account_name': 'tb610756076'}, {'account_name': 'tb836978716'}, {'account_name': 'tb37296640'}, {'account_name': 'tb852395682'}, {'account_name': 'tb153679312'}, {'account_name': 'tb743411847'}, {'account_name': 'tb2839750366'}, {'account_name': 'tb808329070'}, {'account_name': 'tb35776017'}, {'account_name': 'tb633436879'}, {'account_name': 'tb872806044'}, {'account_name': 'tb892760351'}, {'account_name': 'tb895346386'}, {'account_name': 'tb732804980'}, {'account_name': 'tb835569012'}, {'account_name': 'tb461592315'}, {'account_name': 'tb767752824'}, {'account_name': 'tb626829585'}, {'account_name': 'tb27504323'}, {'account_name': 'tb45674225'}, {'account_name': 'tb826442950'}, {'account_name': 'tb4313407'}, {'account_name': 'tb246182_33'}, {'account_name': 'tb39129798'}, {'account_name': 'tb198364275'}, {'account_name': 'tb442600174'}, {'account_name': 'tb97321328'}, {'account_name': 'tb440035731'}, {'account_name': 'tb562551980'}, {'account_name': 'tb483755934'}, {'account_name': 'tb309703635'}, {'account_name': 'tb4913813'}, {'account_name': 'tb996550115'}, {'account_name': 'tb81778_66'}, {'account_name': 'tb12093605'}, {'account_name': 'tb209258624'}, {'account_name': 'tb35306238'}, {'account_name': 'tb975698904'}, {'account_name': 'tb2258292998'}, {'account_name': 'tb9518606_00'}, {'account_name': 'tb25323186'}, {'account_name': 'tb343685119'}, {'account_name': 'tb995670345'}, {'account_name': 'tb62279548'}, {'account_name': 'tb914210451'}, {'account_name': 'tb414596241'}, {'account_name': 'tb684963639'}, {'account_name': 'tb855283663'}, {'account_name': 'tb347950484'}, {'account_name': 'tb5751151_22'}, {'account_name': 'tb212650001'}, {'account_name': 'tb2772802'}, {'account_name': 'tb341344432'}, {'account_name': 'tb498002249'}, {'account_name': 'tb658814197'}, {'account_name': 'tb98434348'}, {'account_name': 'tb506581160'}, {'account_name': 'tb904367_00'}, {'account_name': 'tb63021883'}, {'account_name': 'tb427808211'}, {'account_name': 'tb366641375'}, {'account_name': 'tb472694367'}, {'account_name': 'tb983310621'}, {'account_name': 'tb925402990'}, {'account_name': 'tb8592392'}, {'account_name': 'tb59079510'}, {'account_name': 'tb17366612'}, {'account_name': 'tb596999513'}, {'account_name': 'tb4091329_88'}, {'account_name': 'tb68727485'}, {'account_name': 'tb643595257'}, {'account_name': 'tb7004137_2011'}, {'account_name': 'tb61120944'}, {'account_name': 'tb585109457'}, {'account_name': 'tb505750032'}, {'account_name': 'tb35025128'}, {'account_name': 'lkjx214'}, {'account_name': 'tb440264198'}, {'account_name': 'tb970879807'}, {'account_name': 'tb483504211'}, {'account_name': 'tb762491903'}, {'account_name': 'tb22617427'}, {'account_name': 'tb194118_33'}, {'account_name': 'tb5358134'}, {'account_name': 'tb79207439'}, {'account_name': 'tb985424643'}, {'account_name': '18211829865'}, {'account_name': 'rong1988707601471'}, {'account_name': 'acc赵丽颖'}, {'account_name': 'tb380622728'}, {'account_name': 'dayday电玩批发'}, {'account_name': 'pxy19900402'}, {'account_name': 'huangdf89'}, {'account_name': 'justforyou0110'}, {'account_name': 'sd3285432'}, {'account_name': 'derlinming'}, {'account_name': '7分软肋'}, {'account_name': 'fanchenxi923'}, {'account_name': 'ganwei8886'}, {'account_name': 'huiguang888'}, {'account_name': 'qinxian3160635@163.com'}, {'account_name': '17337555813'}, {'account_name': 'tb170068816'}, {'account_name': 'fatcat1992'}, {'account_name': 'SUKY潘秀英'}, {'account_name': 'shctfsgg'}, {'account_name': 'tb41724757'}, {'account_name': '13147461961啊'}, {'account_name': 'scfsa想龙'}, {'account_name': 'dongchaoxin'}, {'account_name': 'tb04671107'}, {'account_name': 'fedzyj'}, {'account_name': 'lyj771 7'}, {'account_name': 'oliveolivelin'}, {'account_name': 'hwsfjq'}, {'account_name': 'jpshe2006'}, {'account_name': 'tb61912915'}, {'account_name': 'love593403544'}, {'account_name': 'tb501544257'}, {'account_name': 'love13610492728'}, {'account_name': 'q游工作室'}]


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