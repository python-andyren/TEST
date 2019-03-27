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

content = [{'account_name': 'bhkh1970'}, {'account_name': 'arclige1987'}, {'account_name': 'baby雪婧'}, {'account_name': 'baihongyan21'}, {'account_name': 'because李静'}, {'account_name': 'a小飞a234'}, {'account_name': 'a果子'}, {'account_name': 'botao900422'}, {'account_name': 'bhyy17086395'}, {'account_name': 'aoe神话吕布'}, {'account_name': 'aoeabc7'}, {'account_name': 'beibeilulu1314'}, {'account_name': 'bocheng1237'}, {'account_name': 'a老庄'}, {'account_name': 'asqf0001'}, {'account_name': 'annzyj'}, {'account_name': 'baby2918'}, {'account_name': 'buandingdeshenghuo'}, {'account_name': 'baomiaomiao2011'}, {'account_name': 'bmyfby123'}, {'account_name': 'anxing13148687'}, {'account_name': 'aquarius琳'}, {'account_name': 'bufanmeng0555'}, {'account_name': 'aqxiaonan'}, {'account_name': 'bowenw'}, {'account_name': 'brook_魅夜'}, {'account_name': 'avery18'}, {'account_name': 'a图四'}, {'account_name': 'bingbingdrs'}, {'account_name': 'baikai522'}, {'account_name': 'bonjourking'}, {'account_name': 'b63130'}, {'account_name': 'azhong5168'}, {'account_name': 'a皮皮豆'}, {'account_name': 'apple1984_2009'}, {'account_name': 'a那错过的风景'}, {'account_name': 'baibingqing7'}, {'account_name': 'azxc3232'}, {'account_name': 'bu19930310'}, {'account_name': 'aszx231'}, {'account_name': 'awuzaio'}, {'account_name': 'asq280253932'}, {'account_name': 'buhuatuo'}, {'account_name': 'babylee9264'}, {'account_name': 'blookgg2000'}, {'account_name': 'bang101010'}, {'account_name': 'baby冷静'}, {'account_name': 'athena680'}, {'account_name': 'b616902343'}, {'account_name': 'bqb18254752234'}, {'account_name': 'A曾苏颜'}, {'account_name': 'bbnn20120211'}, {'account_name': 'baodao198311'}, {'account_name': 'awrfor'}, {'account_name': 'babygril520'}, {'account_name': 'berberzxh'}, {'account_name': 'aq13682111492'}, {'account_name': 'bo爱家爱琪qi'}, {'account_name': 'a小五619957535'}, {'account_name': 'bigbigfly126'}, {'account_name': 'beijing七环'}, {'account_name': 'ayukay'}, {'account_name': 'bean碧'}, {'account_name': 'baishuai187'}, {'account_name': 'apple007gg'}, {'account_name': 'bomi233'}, {'account_name': 'boya016'}, {'account_name': 'a时间的味道a'}, {'account_name': 'baozhe092'}, {'account_name': 'bibimame'}, {'account_name': 'asd3545611'}, {'account_name': 'bookdongcc'}, {'account_name': 'bunny的触手'}, {'account_name': 'asd912088501'}, {'account_name': 'beky1213'}, {'account_name': 'beibei336699'}, {'account_name': 'baoxiaoni123'}, {'account_name': 'bgm柳华'}, {'account_name': 'baidan0911'}, {'account_name': 'a逼c滴e爱抚'}, {'account_name': 'baiyang18'}, {'account_name': 'a杜杜1314'}, {'account_name': 'baiwei309598164'}, {'account_name': 'benjiurenjian'}, {'account_name': 'bangeguoer'}, {'account_name': 'a小猴驾到66'}, {'account_name': 'atiantian田'}, {'account_name': 'anthony1988'}, {'account_name': 'as7224536'}, {'account_name': 'bneaek'}, {'account_name': 'a离歌a'}, {'account_name': 'bingqu6'}, {'account_name': 'a中意我'}, {'account_name': 'a黎明之前a'}, {'account_name': 'beli2ve1'}, {'account_name': 'bhpphb'}, {'account_name': 'blueice0512'}, {'account_name': 'anqin512658387'}, {'account_name': 'bansi5'}, {'account_name': 'beijiana'}, {'account_name': 'asongzichen'}, {'account_name': 'anzai198704'}, {'account_name': 'bao弋'}, {'account_name': 'a大靓靓'}, {'account_name': 'a罗姐945'}, {'account_name': 'anne滢1202'}, {'account_name': 'a蒲公英二号'}, {'account_name': 'being5'}, {'account_name': 'bing121978'}, {'account_name': 'avbknt'}, {'account_name': 'bmmty0'}, {'account_name': 'benjun2010'}, {'account_name': 'an_王'}, {'account_name': 'bravelin1983'}, {'account_name': 'beiougongzhu1987'}, {'account_name': 'boice容和欧巴'}, {'account_name': 'buqinhan69'}, {'account_name': 'baba538'}, {'account_name': 'baiiqgg'}, {'account_name': 'bin_173722882'}, {'account_name': 'a盛延勇'}, {'account_name': 'aoqinghappy'}, {'account_name': 'awevy'}, {'account_name': 'buhuiba9979'}, {'account_name': 'bn这一生何求'}, {'account_name': 'babylove988'}, {'account_name': 'a紫凌云'}, {'account_name': 'a月月2016'}, {'account_name': 'anxuan3145'}, {'account_name': 'bessiepi'}, {'account_name': 'a流年呐么伤i'}, {'account_name': 'babe8808'}, {'account_name': 'bo2_3'}, {'account_name': 'babynuo1'}, {'account_name': 'bmwnew212921'}, {'account_name': 'bfx岛屿'}, {'account_name': 'anyue_wz'}, {'account_name': 'a刘赋星'}, {'account_name': 'as731934764'}, {'account_name': 'a城主'}, {'account_name': 'boefeng'}, {'account_name': 'a待姐长发及腰时'}, {'account_name': 'a陈程'}, {'account_name': 'a图鸿展大'}, {'account_name': 'baobaoaihaoy'}, {'account_name': 'bishihaoziwei'}, {'account_name': 'baobao04136'}, {'account_name': 'betyia'}, {'account_name': 'a欧货名品馆'}, {'account_name': 'bobbytank'}, {'account_name': 'bp31m209'}, {'account_name': 'a个性挑战a'}, {'account_name': 'barrycheungyw'}, {'account_name': 'a生活点滴a'}, {'account_name': 'boge1717'}, {'account_name': 'bodaxia1984'}, {'account_name': 'bbu1472044'}, {'account_name': 'bosllop'}, {'account_name': 'bitter09'}, {'account_name': 'bh2722'}, {'account_name': 'baibian2012'}, {'account_name': 'ar7208'}, {'account_name': 'ayh0663'}, {'account_name': 'a天涯梧桐'}, {'account_name': 'bin369bin369'}, {'account_name': 'aoteman1010'}, {'account_name': 'bnbnbn1218'}, {'account_name': 'a梦哆啦_jason'}, {'account_name': 'biux5514'}, {'account_name': 'b606y'}, {'account_name': 'betty6781'}, {'account_name': 'bingchengjy'}, {'account_name': 'benjack0119'}, {'account_name': 'as为所欲为'}, {'account_name': 'a高玉轩'}, {'account_name': 'b86217385'}, {'account_name': 'baiyang白杨6'}, {'account_name': 'a丽琼0613'}, {'account_name': 'arlene199211'}, {'account_name': 'blc0926'}, {'account_name': 'ayong8686'}, {'account_name': 'bandonghai'}, {'account_name': 'baquanda'}, {'account_name': 'ben桂彬'}, {'account_name': 'bengkuixia'}, {'account_name': 'aqing0227'}, {'account_name': 'a王敬娟'}, {'account_name': 'baby哲的礼物'}, {'account_name': 'a东京绽开的樱花'}, {'account_name': 'anny09432112'}, {'account_name': 'bao1057857211'}, {'account_name': 'a爱国'}, {'account_name': 'baby1314520_99'}, {'account_name': 'bob896745426'}, {'account_name': 'ben15878110100'}, {'account_name': 'beijake'}, {'account_name': 'breeze0913'}, {'account_name': 'bixiangqun88'}, {'account_name': 'bingmugua5'}, {'account_name': 'baishaona900715'}, {'account_name': 'beiyukou888'}, {'account_name': 'baby静0815'}, {'account_name': 'baiqing198329'}, {'account_name': 'a周嘉莉'}, {'account_name': 'brysjqwe'}, {'account_name': 'asd132698'}, {'account_name': 'bbq小倩'}, {'account_name': 'b250736985'}, {'account_name': 'bjhelei219'}, {'account_name': 'a风中的承诺2'}, {'account_name': 'asia陈'}, {'account_name': 'Bonnie942'}, {'account_name': 'baby156123'}, {'account_name': 'a林马文'}, {'account_name': 'ari910'}, {'account_name': 'a猫zai'}, {'account_name': 'baobeixuanba20120106'}, {'account_name': 'asdfg1594'}, {'account_name': 'blisssunshinemyeye'}, {'account_name': 'bbpp20141314'}, {'account_name': 'baby117247'}, {'account_name': 'bigshot66'}, {'account_name': 'anpeng121088'}, {'account_name': 'a小时候可猛'}, {'account_name': 'a江演77'}, {'account_name': 'baby墨信'}, {'account_name': 'bin339237677'}, {'account_name': 'ao秋天来了'}, {'account_name': 'ansonfly'}, {'account_name': 'beibeiyanyan598'}, {'account_name': 'aqing0509'}, {'account_name': 'aohua12354'}, {'account_name': 'apfghd'}, {'account_name': 'apple2230689'}, {'account_name': 'asdxiaozhu12'}, {'account_name': 'a球球1988'}, {'account_name': 'baby20151110'}, {'account_name': 'b7160304'}, {'account_name': 'baifeng1568'}, {'account_name': 'a丶c丶'}, {'account_name': 'bobofly1231'}, {'account_name': 'benben08198'}, {'account_name': 'bmyguanq'}, {'account_name': 'buaajys'}, {'account_name': 'bo1981605'}, {'account_name': 'asdfghjkl5370'}, {'account_name': 'baixiaozhu008'}, {'account_name': 'bill770467977'}, {'account_name': 'a懂就行了'}, {'account_name': 'brucewu95'}, {'account_name': 'biiiidr'}, {'account_name': 'bluesky081'}, {'account_name': 'asdfjkl1900'}, {'account_name': 'a峰23'}, {'account_name': 'bp198'}, {'account_name': 'aysgmhxh'}, {'account_name': 'aoe188309'}, {'account_name': 'b107324727'}, {'account_name': 'asdzxc19901'}, {'account_name': 'azhong000000'}, {'account_name': 'baobao乐辉'}, {'account_name': 'anyangwuliang'}, {'account_name': 'as65432132497004'}, {'account_name': 'batch18728'}, {'account_name': 'bingxinnvhai冰心女孩'}, {'account_name': 'bspmkcf'}, {'account_name': 'as973621344'}, {'account_name': 'beats美行代购'}, {'account_name': 'as四季花开987'}, {'account_name': 'as15859283162'}, {'account_name': 'baolinkai2012'}, {'account_name': 'benjamin2010qq'}, {'account_name': 'a艳艳薯片'}, {'account_name': 'boboman1'}, {'account_name': 'bsht2008'}, {'account_name': 'a大雁飞翔a'}, {'account_name': 'BOBO398429395'}, {'account_name': 'boomshakalakabaa'}, {'account_name': 'birui861105'}, {'account_name': 'av3q25k'}, {'account_name': 'binjuan1209'}, {'account_name': 'bing97153465'}, {'account_name': 'a种呀种太阳'}, {'account_name': 'a苏打绿茶a'}, {'account_name': 'asdf'}, {'account_name': 'bbhaqq'}, {'account_name': 'a刘宗康'}, {'account_name': 'bobo111031'}, {'account_name': 'bbb77855'}, {'account_name': 'bolilinger'}, {'account_name': 'baby_hyh'}, {'account_name': 'baby大清'}, {'account_name': 'an暖心人'}, {'account_name': 'bjjxiaoning'}, {'account_name': 'arthur41386889'}, {'account_name': 'a春夏秋冬94400507'}, {'account_name': 'bo150323'}, {'account_name': 'a孙媛媛'}, {'account_name': 'baixuefeng1023'}, {'account_name': 'bao705572633'}, {'account_name': 'blank5521'}, {'account_name': 'bmy787801887'}, {'account_name': 'a安辰55'}, {'account_name': 'ayanggu123'}, {'account_name': 'bskjjr'}, {'account_name': 'bing1714843'}, {'account_name': 'annie8552'}, {'account_name': 'ava半仙'}, {'account_name': 'best精英科技'}, {'account_name': 'a起个名脑细胞全废'}, {'account_name': 'appesl_2007'}, {'account_name': 'baobaosu20151014'}, {'account_name': 'bb小吕宝贝'}, {'account_name': 'borage月月'}, {'account_name': 'beckybroken'}, {'account_name': 'baixiujuan2013'}, {'account_name': 'baby花飞'}, {'account_name': 'apdhww'}, {'account_name': 'baobao2838777'}, {'account_name': 'bai1110'}, {'account_name': 'babykissing1'}, {'account_name': 'asd佳期如梦'}, {'account_name': 'baby轩轩55'}, {'account_name': 'bupiaoliang'}, {'account_name': 'a山鹰天空'}, {'account_name': 'bb352059182'}, {'account_name': 'attoxu'}, {'account_name': 'boxiudo'}, {'account_name': 'bingbingtang0927'}, {'account_name': 'ayoko_98'}, {'account_name': 'asia126'}, {'account_name': 'batoo2326'}, {'account_name': 'babychen92405001'}, {'account_name': 'bt2baby'}, {'account_name': 'aq19788'}, {'account_name': 'asd1314521ppp'}, {'account_name': 'bgsqesy960325'}, {'account_name': 'baby江小姐'}, {'account_name': 'bingxue021'}, {'account_name': 'blfydiwxf'}, {'account_name': 'binbin4558569'}, {'account_name': 'bingwei0714'}, {'account_name': 'an宁宁666'}, {'account_name': 'babykailly'}, {'account_name': 'as532001593'}, {'account_name': 'boy201709'}, {'account_name': 'bb18838'}, {'account_name': 'beetty521'}, {'account_name': 'a张林5860'}, {'account_name': 'aphelle'}, {'account_name': 'a王庆莉'}, {'account_name': 'antidote李'}, {'account_name': 'bobo5304012'}, {'account_name': 'ballking1988'}, {'account_name': 'blablabla曾经沧海难为水'}, {'account_name': 'baoxiaojun88'}, {'account_name': 'arrogantlee'}, {'account_name': 'bobo5238'}, {'account_name': 'baobeiqi422'}, {'account_name': 'bcj973'}, {'account_name': 'aqhhms01522'}, {'account_name': 'belongyx'}, {'account_name': 'anthonywwy07'}, {'account_name': 'baijin5211314'}, {'account_name': 'baby风过云轻'}, {'account_name': 'a邓红昌'}, {'account_name': 'Baby羽2016'}, {'account_name': 'baifaiyi'}, {'account_name': 'bmsskhtgas'}, {'account_name': 'binqian0706'}, {'account_name': 'a庆王子贺'}, {'account_name': 'a会哭的彩虹'}, {'account_name': 'bjcyvip'}, {'account_name': 'az_yy'}, {'account_name': 'aszjqz1002'}, {'account_name': 'bh13823852029'}, {'account_name': 'a空谷幽兰a'}, {'account_name': 'a疯狂小妖a'}, {'account_name': 'bulingli01'}, {'account_name': 'b0ny1p6996'}, {'account_name': 'baby2826'}, {'account_name': 'a朵朵秀英'}, {'account_name': 'bmw556655'}, {'account_name': 'baobao荆俊智'}, {'account_name': 'a杰然不彤'}, {'account_name': 'bh5223'}, {'account_name': 'bns1019'}, {'account_name': 'ayin1992'}, {'account_name': 'annwang0828'}, {'account_name': 'buddy仔'}, {'account_name': 'boqifeng111222'}, {'account_name': 'anshack'}, {'account_name': 'as550196457'}, {'account_name': 'baishang19905'}, {'account_name': 'balletshu'}, {'account_name': 'avivi_10'}, {'account_name': 'ayres59'}, {'account_name': 'anycalltb1'}, {'account_name': 'beifengzhishen77'}, {'account_name': 'as都会撒的谎'}, {'account_name': 'a_禾子'}, {'account_name': 'a级职业杀手'}, {'account_name': 'avgirl90012'}, {'account_name': 'bu18752117602'}, {'account_name': 'autumnsunlove'}, {'account_name': 'bbczlh'}, {'account_name': 'bjh13903305287'}, {'account_name': 'as快乐每一天⑧⑧⑧⑧'}, {'account_name': 'baiyou66699'}, {'account_name': 'berniceh'}, {'account_name': 'bingyaosheng'}, {'account_name': 'bairuiaiyu'}, {'account_name': 'asdsafg'}, {'account_name': 'bdd199009'}, {'account_name': 'bellaandztxy'}, {'account_name': 'anwenming2014'}, {'account_name': 'biao520222'}, {'account_name': 'babystoreee'}, {'account_name': 'anzhiruosu5266'}, {'account_name': 'baihulai80'}, {'account_name': 'anyang123456a'}, {'account_name': 'aresi999'}, {'account_name': 'a太平'}, {'account_name': 'aqwe45987'}, {'account_name': 'banlv662'}, {'account_name': 'baben816'}, {'account_name': 'as15921051901'}, {'account_name': 'bengbeng_com'}, {'account_name': 'babyface521'}, {'account_name': 'bo哥0668'}, {'account_name': 'bly309309'}, {'account_name': 'bn脸叔'}, {'account_name': 'bb13110920829'}, {'account_name': 'baijiu'}, {'account_name': 'bensonlee1229'}, {'account_name': 'bulachun'}, {'account_name': 'baoyafeng企鹅'}, {'account_name': 'book薇'}, {'account_name': 'a白雪00'}, {'account_name': 'aozaiguo'}, {'account_name': 'bqpyueyue'}, {'account_name': 'az721130'}, {'account_name': 'apple891131'}, {'account_name': 'a阳光zy'}, {'account_name': 'app劲哥哥'}, {'account_name': 'arrive5'}, {'account_name': 'bbeijingtiananmen'}, {'account_name': 'a丶monologue凌'}, {'account_name': 'a周琼璇'}, {'account_name': 'bibbysun11'}, {'account_name': 'ar傻丫头'}, {'account_name': 'axyybza，'}, {'account_name': 'bajo1'}, {'account_name': 'a倾城百合花'}, {'account_name': 'bendan748264'}, {'account_name': 'a亮先生'}, {'account_name': 'a嘉嘉aa'}, {'account_name': 'baby92525'}, {'account_name': 'baobeishuxingfu'}, {'account_name': 'bbaaa7585712'}, {'account_name': 'batty0205'}, {'account_name': 'bg7nnt'}, {'account_name': 'bboyszero'}, {'account_name': 'bongsuming'}, {'account_name': 'blackhaojay'}, {'account_name': 'bubutaro'}, {'account_name': 'boutinp1'}, {'account_name': 'april仄仄'}, {'account_name': 'bq13597559758'}, {'account_name': 'b06813'}, {'account_name': 'bbba007'}, {'account_name': 'baobao117629'}, {'account_name': 'baby4861980'}, {'account_name': 'answerekin'}, {'account_name': 'b221881751015065889'}, {'account_name': 'a邻家小妹的'}, {'account_name': 'b576597430'}, {'account_name': 'banilu'}, {'account_name': 'black255'}, {'account_name': 'baby20140716'}, {'account_name': 'ariel19901017'}, {'account_name': 'bqrgogvtkud'}, {'account_name': 'binger031112'}, {'account_name': 'bi站在雨中的女孩'}, {'account_name': 'baonimanyi201'}, {'account_name': 'apple秋天的童话'}, {'account_name': 'bmw38508'}, {'account_name': 'a短发女生'}, {'account_name': 'asd1314qwer'}, {'account_name': 'ansenjia'}, {'account_name': 'beibei5837'}, {'account_name': 'aoaoao332'}, {'account_name': 'bb小蜗牛'}, {'account_name': 'as279412524'}, {'account_name': 'boking11'}, {'account_name': 'asulongzhang'}, {'account_name': 'a秋和她的小野菊'}, {'account_name': 'bobo_yc'}, {'account_name': 'at滚犊子'}, {'account_name': 'a初妆66'}, {'account_name': 'bsong26646694'}, {'account_name': 'b12小行星小王子'}, {'account_name': 'baihehua121266'}, {'account_name': 'bttanzongqin'}, {'account_name': 'areshouzhu'}, {'account_name': 'asd72308888'}, {'account_name': 'as554068414'}, {'account_name': 'b147895233'}, {'account_name': 'as100116'}, {'account_name': 'baizhan1985'}, {'account_name': 'bb60520'}, {'account_name': 'bulelove20082008'}, {'account_name': 'a浩淼'}, {'account_name': 'bsyrong'}, {'account_name': 'annettecat'}, {'account_name': 'asa801209liang'}, {'account_name': 'bo9327918899'}, {'account_name': 'away_ll'}, {'account_name': 'bkf326'}, {'account_name': 'baby奕带'}, {'account_name': 'bb1314200'}, {'account_name': 'asd4352367'}, {'account_name': 'boy9968'}, {'account_name': 'bubing_1984'}, {'account_name': 'baobaoloveu0715'}, {'account_name': 'bczlxy'}, {'account_name': 'a单眼皮的熊猫'}, {'account_name': 'binbangll'}, {'account_name': 'bskzone'}, {'account_name': 'bty46164'}, {'account_name': 'buqinggaimo'}, {'account_name': 'borepig'}, {'account_name': 'bboymarsjie0917'}, {'account_name': 'asassas99'}, {'account_name': 'a_curse'}, {'account_name': 'a用力微笑a'}, {'account_name': 'b6190266'}, {'account_name': 'btpoco'}, {'account_name': 'as无限极兰兰'}, {'account_name': 'baby丨丶不哭'}, {'account_name': 'app杨康'}, {'account_name': 'blclub170'}, {'account_name': 'bbing712'}, {'account_name': 'badunxiansheng'}, {'account_name': 'ayy1980'}, {'account_name': 'a面朝花海'}, {'account_name': 'baoguo0509'}, {'account_name': 'be12345'}, {'account_name': 'blithe_wenhua'}, {'account_name': 'anywini'}, {'account_name': 'bpxduck28782'}, {'account_name': 'aodia123'}, {'account_name': 'ayn19880116'}, {'account_name': 'binjian174'}, {'account_name': 'bt桃涛淘'}, {'account_name': 'a小雪代购'}, {'account_name': 'babiiiyoyo'}, {'account_name': 'benzlot'}, {'account_name': 'applelht1'}, {'account_name': 'azucenalily'}, {'account_name': 'anyangmengjun1980515'}, {'account_name': 'atiao88'}, {'account_name': 'annie1000_2006'}, {'account_name': 'asd479127412'}, {'account_name': 'bby1317'}, {'account_name': 'bgt18739912559'}, {'account_name': 'bbqmcmc10'}, {'account_name': 'a卫雪'}, {'account_name': 'ataob2011'}, {'account_name': 'asdlyt2'}, {'account_name': 'a艾妍希'}, {'account_name': 'apdtdt'}, {'account_name': 'asp728'}, {'account_name': 'bitter1123'}, {'account_name': 'binnong2008'}, {'account_name': 'applehl244650415'}, {'account_name': 'bsq879'}, {'account_name': 'ayingjiayou6688'}, {'account_name': 'asd1985321'}, {'account_name': 'baofahu1110'}, {'account_name': 'awujinga'}, {'account_name': 'b55患得患失'}, {'account_name': 'baby灬卟哭'}, {'account_name': 'axkncrh65777'}, {'account_name': 'bingxingtianqu'}, {'account_name': 'bcm16888'}, {'account_name': 'bokeili01'}, {'account_name': 'anysyanyan'}, {'account_name': 'beibei19901013'}, {'account_name': 'bendan贺'}, {'account_name': 'b13480450002'}, {'account_name': 'asdfgh末'}, {'account_name': 'beojtb'}, {'account_name': 'awqjusoqd44031'}, {'account_name': 'belong'}, {'account_name': 'app火星救援'}, {'account_name': 'aze0592'}, {'account_name': 'bryan_zhao050922'}, {'account_name': 'asdzxc_123有朋'}, {'account_name': 'aotemanfuren'}, {'account_name': 'apple刘海萍'}, {'account_name': 'bodo0208'}, {'account_name': 'axbxbxb'}, {'account_name': 'baobei801314ll'}, {'account_name': 'bihailin198591'}, {'account_name': 'anough莫'}, {'account_name': 'budawei037'}, {'account_name': 'boejnqp21746'}, {'account_name': 'aoxiao999'}, {'account_name': 'boboan_1129'}, {'account_name': 'bdqguwnin14252'}, {'account_name': 'atylqeftu431865'}, {'account_name': 'aslk121314'}, {'account_name': 'bbbji'}, {'account_name': 'asd刘波'}, {'account_name': 'awen320321'}, {'account_name': 'bhuatkvwh526222'}, {'account_name': 'anywangpeng'}, {'account_name': 'b444026756'}, {'account_name': 'bing174757'}, {'account_name': 'barttai'}, {'account_name': 'aqaqaq22'}, {'account_name': 'boaevno57255'}, {'account_name': 'bjllt'}, {'account_name': 'bajingbu9101'}, {'account_name': 'bmyzk77'}, {'account_name': 'as8252557'}, {'account_name': 'binost'}, {'account_name': 'beyondchaiyi'}, {'account_name': 'baliming11'}, {'account_name': 'ben15982493633'}, {'account_name': 'bingjie最帅'}, {'account_name': 'bk7798775537'}, {'account_name': 'bingbohe1217'}, {'account_name': 'bstwpjbb'}, {'account_name': 'annyshi'}, {'account_name': 'baozhihua0562'}, {'account_name': 'awei5300118'}, {'account_name': 'b5508089'}, {'account_name': 'bgchair2008'}, {'account_name': 'bqrdnnfn'}, {'account_name': 'biy自己喜欢就好'}, {'account_name': 'bear小熊521'}, {'account_name': 'bkhm2307'}, {'account_name': 'boungblood'}, {'account_name': 'bobomiao14'}, {'account_name': 'blame白色'}, {'account_name': 'bellelovebig'}, {'account_name': 'asdyudsa'}, {'account_name': 'bao2536146'}, {'account_name': 'ba0202'}, {'account_name': 'bgdndq'}, {'account_name': 'aqr小雪'}, {'account_name': 'baby萌小言'}, {'account_name': 'babasic'}, {'account_name': 'bdxlzl'}, {'account_name': 'badaokuang'}, {'account_name': 'a廖春梅'}, {'account_name': 'aoo3226407'}, {'account_name': 'asdfa1986'}, {'account_name': 'b497958392'}, {'account_name': 'atao7'}, {'account_name': 'beiced2'}, {'account_name': 'baby栢儿'}, {'account_name': 'bqm2894'}, {'account_name': 'auliang亮'}, {'account_name': 'boredato'}, {'account_name': 'bulk丿楠'}, {'account_name': 'anqianma'}, {'account_name': 'bpf1982'}, {'account_name': 'atao768768'}, {'account_name': 'appel31'}, {'account_name': 'a丽l蔡396'}, {'account_name': 'a何田子'}, {'account_name': 'asd1314520aa'}, {'account_name': 'antahjj'}, {'account_name': 'bbecause0fyou'}, {'account_name': 'boboyam77'}, {'account_name': 'arthur1892'}, {'account_name': 'aoyuan结合家'}, {'account_name': 'a杰仔妈妈'}, {'account_name': 'bibitao9'}, {'account_name': 'a范二青年丶'}, {'account_name': 'barg82'}, {'account_name': 'aqianyongrong'}, {'account_name': 'bb王伟倩倩'}, {'account_name': 'binbin927'}, {'account_name': 'balllinht'}, {'account_name': 'bm20130808'}, {'account_name': 'btbhqn98'}, {'account_name': 'bhhy504'}, {'account_name': 'a酷酷玉儿'}, {'account_name': 'anny小陈'}, {'account_name': 'bnmm147'}, {'account_name': 'bb20072008bb'}, {'account_name': 'badu181999'}, {'account_name': 'azona猫'}, {'account_name': 'axlchen627'}, {'account_name': 'aqwerty08'}, {'account_name': 'a娇0125'}, {'account_name': 'b3698858'}, {'account_name': 'bluedream59188'}, {'account_name': 'bai876220'}, {'account_name': 'bee5494'}, {'account_name': 'anqila青'}, {'account_name': 'bread在路上'}, {'account_name': 'ban妈妈爱你航航'}, {'account_name': 'aopld7k5'}, {'account_name': 'bb特爱大爆炸'}, {'account_name': 'bin123彬'}, {'account_name': 'b02051107'}, {'account_name': 'baoappleking'}, {'account_name': 'ar110907'}, {'account_name': 'a型香菇'}, {'account_name': 'bluepola'}, {'account_name': 'a小阳11'}, {'account_name': 'bill253'}, {'account_name': 'baobaocaner_2008'}, {'account_name': 'bo破碎球'}, {'account_name': 'b5769530'}, {'account_name': 'appleyy2008'}, {'account_name': 'a丶轩'}, {'account_name': 'bobottyou123'}, {'account_name': 'ashen927'}, {'account_name': 'bfycrdt32'}, {'account_name': 'basiswen'}, {'account_name': 'asd901107'}, {'account_name': 'beibei10181'}, {'account_name': 'asd123aqw'}, {'account_name': 'bai23ni'}, {'account_name': 'asd小菲菲'}, {'account_name': 'bestseven23'}, {'account_name': 'asdfas'}, {'account_name': 'bng88933'}, {'account_name': 'basrgps'}, {'account_name': 'as331643554'}, {'account_name': 'biling252'}, {'account_name': 'bbdf2002'}, {'account_name': 'benzs320tw'}, {'account_name': 'bear371976188'}, {'account_name': 'bnbn9266'}, {'account_name': 'a小七20038087'}, {'account_name': 'binganshifu'}, {'account_name': 'bm141349'}, {'account_name': 'apirl03'}, {'account_name': 'a宝宝怡'}, {'account_name': 'a柠檬a思羽a'}, {'account_name': 'blindarqys'}, {'account_name': 'baitiantian16900'}, {'account_name': 'asd63858321'}, {'account_name': 'brother_cn'}, {'account_name': 'believe9076'}, {'account_name': 'as2609011371'}, {'account_name': 'asdf96824'}, {'account_name': 'bo550536036'}, {'account_name': 'aoling56958575'}, {'account_name': 'babydanxia'}, {'account_name': 'as8604ok'}, {'account_name': 'asd18884166'}, {'account_name': 'beartico'}, {'account_name': 'bai1472580'}, {'account_name': 'bonjshen'}, {'account_name': 'ayangwawa'}, {'account_name': 'bittyhaifei88'}, {'account_name': 'askewlin'}, {'account_name': 'a彤彤16'}, {'account_name': 'a逆水行舟3138'}, {'account_name': 'a先生8888'}, {'account_name': 'a毕燕松'}, {'account_name': 'bltiii'}, {'account_name': 'babayetu'}, {'account_name': 'arena86'}, {'account_name': 'asdfghj504310321'}, {'account_name': 'any0809'}, {'account_name': 'bt5515'}, {'account_name': 'bihan521'}, {'account_name': 'aq6529070'}, {'account_name': 'bbk272'}, {'account_name': 'blue_jack111'}, {'account_name': 'arron0830'}, {'account_name': 'applechi0628'}, {'account_name': 'bibo_1986'}, {'account_name': 'a天使的微笑6'}, {'account_name': 'anxinmulin'}, {'account_name': 'beiping5212000'}, {'account_name': 'bonnie_pink7'}, {'account_name': 'banxiaweiliang19911988'}, {'account_name': 'belovrit123'}, {'account_name': 'ayy初恋'}, {'account_name': 'aweizhiyun'}, {'account_name': 'bjijay14'}, {'account_name': 'baimeihua100'}, {'account_name': 'aoxiang999888'}, {'account_name': 'aslamjaafar'}, {'account_name': 'bcfeng'}, {'account_name': 'breeze_02'}, {'account_name': 'bilieber'}, {'account_name': 'asf7350068'}, {'account_name': 'blbzllhf'}, {'account_name': 'bluevery0612'}, {'account_name': 'beauty梨'}, {'account_name': 'a东风小康5'}, {'account_name': 'bisengsheng'}, {'account_name': 'baidugx'}, {'account_name': 'billwt'}, {'account_name': 'babyqiu888'}, {'account_name': 'baobei13zuiai'}, {'account_name': 'bourne19891123'}, {'account_name': 'boygogo81'}, {'account_name': 'baby美美的幸福lala'}, {'account_name': 'asd6502316'}, {'account_name': 'april919'}, {'account_name': 'binglan868'}, {'account_name': 'avr43'}, {'account_name': 'a心似柠檬酸'}, {'account_name': 'boring'}, {'account_name': 'anything78'}, {'account_name': 'baby243643814'}, {'account_name': 'baimeiyan89'}, {'account_name': 'asc1208'}, {'account_name': 'averydhwu'}, {'account_name': 'berm否'}, {'account_name': 'belrlx15'}, {'account_name': 'billy14553'}, {'account_name': 'a李兆兴'}, {'account_name': 'betty琳'}, {'account_name': 'bluebobo1'}, {'account_name': 'axb19890914'}, {'account_name': 'aploiek'}, {'account_name': 'a叶秋香'}, {'account_name': 'beemiel'}, {'account_name': 'briandu2007'}, {'account_name': 'azhm_1992'}, {'account_name': 'bsbsdd'}, {'account_name': 'a明天慧更郝'}, {'account_name': 'annsi思思'}, {'account_name': 'bin4530558'}, {'account_name': 'awen1230801'}, {'account_name': 'bianganxue'}, {'account_name': 'bawwk平'}, {'account_name': 'austinv3v'}, {'account_name': 'baoerjingxian'}, {'account_name': 'bettyxu1990'}, {'account_name': 'benfei236'}, {'account_name': 'a丶cry丨漓殇'}, {'account_name': 'baobaowangna'}, {'account_name': 'banban_178'}, {'account_name': 'baiwuya0459'}, {'account_name': 'asin2015'}, {'account_name': 'art0059'}, {'account_name': 'asislly'}, {'account_name': 'bin5796621'}, {'account_name': 'bigredtrunk'}, {'account_name': 'blyljrl67617'}, {'account_name': 'annie52399'}, {'account_name': 'bestboy7'}, {'account_name': 'bain84147'}, {'account_name': 'baowu315'}, {'account_name': 'bao61905305'}, {'account_name': 'ascxb7550'}, {'account_name': 'aq1000222'}, {'account_name': 'baike白可'}, {'account_name': 'ayaya301225'}, {'account_name': 'bao1216197754'}, {'account_name': 'baixinge'}, {'account_name': 'bay白123'}, {'account_name': 'baobaook0012'}, {'account_name': 'a何以笙箫默2000'}, {'account_name': 'bown456'}, {'account_name': 'bbtwo'}, {'account_name': 'a好帅郝帅'}, {'account_name': 'bbmm9592'}, {'account_name': 'babyblue0099'}, {'account_name': 'as525345230'}, {'account_name': 'beebedx1908'}, {'account_name': 'asdf3453'}, {'account_name': 'asdfgh12345123'}, {'account_name': 'apple_狼'}, {'account_name': 'benxiaoqing520'}, {'account_name': 'az1385788909'}, {'account_name': 'bn306000625'}, {'account_name': 'banzuohong0606'}, {'account_name': 'bingbing2185'}, {'account_name': 'as_1993'}, {'account_name': 'ariesqwe'}, {'account_name': 'a小博宁'}, {'account_name': 'aprilqy'}, {'account_name': 'as1518135937'}, {'account_name': 'boyssss8'}, {'account_name': 'an安安1014'}, {'account_name': 'anning0016'}, {'account_name': 'baishilong403'}, {'account_name': 'bingxue381225014'}, {'account_name': 'banwd520'}, {'account_name': 'bbmuda'}, {'account_name': 'axbabyhp'}, {'account_name': 'a小丽876335201'}, {'account_name': 'a从来都是我的错a'}, {'account_name': 'baihe502108'}, {'account_name': 'a神123'}, {'account_name': 'bt86955722'}, {'account_name': 'a徐a菡a'}, {'account_name': 'bobo牙套妹'}, {'account_name': 'anquan54321'}, {'account_name': 'brenna张'}, {'account_name': 'asa_98'}, {'account_name': 'a朱俊亚201029'}, {'account_name': 'baobao20090608'}, {'account_name': 'aweiweia88'}, {'account_name': 'baoqing312'}, {'account_name': 'aries花妞25416711'}, {'account_name': 'big大米米'}, {'account_name': 'blue丫娇'}, {'account_name': 'bigo333x'}, {'account_name': 'bobcnc123'}, {'account_name': 'b9847361'}, {'account_name': 'baby杰992'}, {'account_name': 'an筱爽'}, {'account_name': 'benswallow88'}, {'account_name': 'bld490834'}, {'account_name': 'btn30560b8'}, {'account_name': 'binibin4078'}, {'account_name': 'ansonlkw'}, {'account_name': 'bingeing'}, {'account_name': 'annmi5媚'}, {'account_name': 'azuresky0819'}, {'account_name': 'bestseller456'}, {'account_name': 'baifanghao'}, {'account_name': 'anqianxin宝贝'}, {'account_name': 'breathless_001'}, {'account_name': 'buhaoshile'}, {'account_name': 'asdktv75191779'}, {'account_name': 'avctry'}, {'account_name': 'baby惠敏'}, {'account_name': 'anxueanxue3'}, {'account_name': 'baby918626'}, {'account_name': 'bingyin24'}, {'account_name': 'a李小倩123'}, {'account_name': 'axl140429'}, {'account_name': 'boiling'}, {'account_name': 'asd1234Ⅴ'}, {'account_name': 'bjackhung'}, {'account_name': 'baokuoz'}, {'account_name': 'bozige520'}, {'account_name': 'baosaomi5155'}, {'account_name': 'applelove9999'}, {'account_name': 'BSG770056'}, {'account_name': 'bazcl5388'}, {'account_name': 'aonyhdi'}, {'account_name': 'bloodrany'}, {'account_name': 'b68夜杨'}, {'account_name': 'ay593467309'}, {'account_name': 'a莹得有滢'}, {'account_name': 'asdf逗比'}, {'account_name': 'bm_2009'}, {'account_name': 'asd8352717'}, {'account_name': 'asdlaoqi'}, {'account_name': 'aouyang一君'}, {'account_name': 'as8389748'}, {'account_name': 'b15259525911'}, {'account_name': 'baby柠柠檬'}, {'account_name': 'bamboo晚竹'}, {'account_name': 'a徐b红c丽d'}, {'account_name': 'bauercoo'}, {'account_name': 'baiyang142'}, {'account_name': 'baozhen0915'}, {'account_name': 'bu19811130'}, {'account_name': 'asus12342001'}, {'account_name': 'bin499703232'}, {'account_name': 'banyuewan2001'}, {'account_name': 'asnql'}, {'account_name': 'baby_junjin'}, {'account_name': 'bcchiu714'}, {'account_name': 'beyondmachao'}, {'account_name': 'b9829104'}, {'account_name': 'baby小楹楹'}, {'account_name': 'bipeng654321'}, {'account_name': 'apple_mini8'}, {'account_name': 'bie_lam'}, {'account_name': 'as1394753196'}, {'account_name': 'august654'}, {'account_name': 'atviptv'}, {'account_name': 'awaying123'}, {'account_name': 'a虹宝in'}, {'account_name': 'atyaimn'}, {'account_name': 'baby倩889'}, {'account_name': 'blackliutw'}, {'account_name': 'a心太荒谬'}, {'account_name': 'asyolee'}, {'account_name': 'baoshuangcom'}, {'account_name': 'bearjudo6123'}, {'account_name': 'azt1982'}, {'account_name': 'apeape77'}, {'account_name': 'applespo'}, {'account_name': '15910942141'}, {'account_name': '13978454162小黑爱小白'}, {'account_name': 'btx1874'}, {'account_name': 'aaaaa39557059'}, {'account_name': '0113fang'}, {'account_name': '888小弟弟'}]


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