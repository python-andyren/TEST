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
content = [{'account_name': '严燕华11'}, {'account_name': '开心4581374626'}, {'account_name': 't_1494478466103_0235'}, {'account_name': '微笑后表情终于有点难过'}, {'account_name': '狄鸿掎cd'}, {'account_name': '杨斌杀神哥'}, {'account_name': '南渡小公司'}, {'account_name': '艾芊芊_艾芊芊'}, {'account_name': '我爱我家wj138'}, {'account_name': '凯文锂'}, {'account_name': '马丽梅梅梅'}, {'account_name': 'yhxwl28'}, {'account_name': '万物皆由神造'}, {'account_name': '景莲莲莲'}, {'account_name': '关婉深'}, {'account_name': '何志伟888'}, {'account_name': '陈现法0121'}, {'account_name': 'xiaomeng25883'}, {'account_name': '嘿哈cn'}, {'account_name': '会过去8811'}, {'account_name': '利利珊珊'}, {'account_name': '有故事的雪花'}, {'account_name': '沉淀在月光下的一抹苍凉'}, {'account_name': 't_1505894217045_0208'}, {'account_name': '花好月圆阳'}, {'account_name': '鬼魅乱尘'}, {'account_name': 'wuqiaomeng'}, {'account_name': '老公王栋'}, {'account_name': '一直被模'}, {'account_name': '阿乐0904'}, {'account_name': '甘欣情愿'}, {'account_name': '林倩仪2012'}, {'account_name': '次梦炎'}, {'account_name': '虎博华福'}, {'account_name': '蝴蝶仔泪01'}, {'account_name': 'w狠狠的爱自己'}, {'account_name': '泪如雨下只为你'}, {'account_name': '雨果的巴黎圣'}, {'account_name': '情深惠玲'}, {'account_name': '花落倾城xx'}, {'account_name': '天真的代价x'}, {'account_name': '海边小草的小草'}, {'account_name': '华少e站网购'}, {'account_name': '永亮实木家居'}, {'account_name': '田鑫新'}, {'account_name': '夕颜昔颜初心'}, {'account_name': 'u9biyz4sptk'}, {'account_name': '青云流氓'}, {'account_name': '林玮93'}, {'account_name': '北海葬爱54'}, {'account_name': '我就是我19900707'}, {'account_name': '开业致富'}, {'account_name': 'tiger8512'}, {'account_name': '第五雪峰'}, {'account_name': '熊韵涵123'}, {'account_name': '何果果15905144818'}, {'account_name': '黄永木木'}, {'account_name': '飞翔的燕子luping'}, {'account_name': '典坊鞋吧'}, {'account_name': '芝麻111555'}, {'account_name': '北溟y鱼'}, {'account_name': '郑双阳王金花'}, {'account_name': '大掌柜大1'}, {'account_name': '我怕谁5211'}, {'account_name': '桐宝贝7889'}, {'account_name': '廖胤凯'}, {'account_name': '华为520612'}, {'account_name': '黄锦源211'}, {'account_name': '馨兰幽香'}, {'account_name': 'zihudie0507'}, {'account_name': '孟涛31'}, {'account_name': '小海盗218'}, {'account_name': 'W淘淘网络W'}, {'account_name': '徐大官人88'}, {'account_name': '丿逍遥丶丿'}, {'account_name': 'tuhuijuan_1987'}, {'account_name': '走路带风19980731'}, {'account_name': '你说行不行82475'}, {'account_name': 'wyan666'}, {'account_name': '再过十年你在哪'}, {'account_name': 't_1506178225081_033'}, {'account_name': '露滴中的一枚早晨'}, {'account_name': '我爱我家741852'}, {'account_name': 'teresg'}, {'account_name': '晴楸落叶'}, {'account_name': '白加黑青春'}, {'account_name': '当年情198'}, {'account_name': 'wmtung2010'}, {'account_name': '艾雪一个人走'}, {'account_name': '一以人字'}, {'account_name': 'zt20090112'}, {'account_name': '我要去北上广'}, {'account_name': '超对的选泽'}, {'account_name': '木子贝贝高'}, {'account_name': '跋山涉水bas'}, {'account_name': '曾月兰15'}, {'account_name': 'xm_dingyq'}, {'account_name': '警钟偿命'}, {'account_name': 'ypffff8'}, {'account_name': '就喜欢你的眼'}, {'account_name': 'xingxiancheng0513'}, {'account_name': 'wang羽羽5146'}, {'account_name': '一切随风59667411'}, {'account_name': '为你沧桑的浪漫'}, {'account_name': '爱上海峰'}, {'account_name': 'ylh11811'}, {'account_name': '躺磺涤'}, {'account_name': '小汤队长'}, {'account_name': '刘恋5211'}, {'account_name': '随缘31500'}, {'account_name': '喃喃的袜子'}, {'account_name': '丽珠456'}, {'account_name': '欢迎吧于'}, {'account_name': '小飞扬66a'}, {'account_name': '蓉daisy'}, {'account_name': '谷底的高贵'}, {'account_name': '邹益喻ni'}, {'account_name': '赖以未来'}, {'account_name': '文思8235'}, {'account_name': 'zhx天使的翅膀'}, {'account_name': '曹操马力'}, {'account_name': '执意走爱下去'}, {'account_name': 'tietengqf840'}, {'account_name': '多来米你好'}, {'account_name': '卢景飞888'}, {'account_name': '细雨中的山村'}, {'account_name': '啊13147461961'}, {'account_name': '蒙头小君'}, {'account_name': '橘子香蕉大橙子'}, {'account_name': '王泽敏wang'}, {'account_name': '紫萝兰_89'}, {'account_name': '甜梦园的芭比'}, {'account_name': '简单的我们斐楠'}, {'account_name': '哥想约你可以吗'}, {'account_name': '花仙子4258140'}, {'account_name': '掌亿矫'}, {'account_name': '了了然393'}, {'account_name': 't_1483594702498_0262'}, {'account_name': '巴菲猫101'}, {'account_name': '廖宏滨'}, {'account_name': 'yly9243'}, {'account_name': '哈密瓜_6233'}, {'account_name': '苏浅笑梨涡'}, {'account_name': 'zeus君主'}, {'account_name': '狗狗19890313'}, {'account_name': '黄孟光'}, {'account_name': 'zcxi0513'}, {'account_name': '谕莆恿'}, {'account_name': '诔垦庇m'}, {'account_name': '小2蛋蛋10'}, {'account_name': '李柯稼管玉莹'}, {'account_name': '美丽心情爱果冻'}, {'account_name': '厝赣碧'}, {'account_name': '张红芳199838863'}, {'account_name': '开了花的苹果'}, {'account_name': 'yentzu0224'}, {'account_name': 'zhen20125207'}, {'account_name': '幸邦鑫0904'}, {'account_name': '琴琴9941'}, {'account_name': '杨学龙65'}, {'account_name': '杨jing博'}, {'account_name': '心有爱而美'}, {'account_name': '网上神偷'}, {'account_name': 'zuimdhh'}, {'account_name': '无影随风浪心'}, {'account_name': '夏天之问'}, {'account_name': '秀秀20100730'}, {'account_name': '柯启娜'}, {'account_name': '如果的如果的96'}, {'account_name': '我是牢山的'}, {'account_name': '刘彬2883'}, {'account_name': 'ychchbvhkv'}, {'account_name': '玖梦520'}, {'account_name': '狼道1981'}, {'account_name': '王兴旺550'}, {'account_name': '星魂是只傲娇喵'}, {'account_name': 'yjl880421l'}, {'account_name': '子子的麻麻'}, {'account_name': '炎焰炙冷心'}, {'account_name': '张晓全888'}, {'account_name': 't_1503299246314_0284'}, {'account_name': 'tb_4511884'}, {'account_name': '金1302263'}, {'account_name': '梁素伟'}, {'account_name': 't_1493620139069_051'}, {'account_name': 't_1537346487137_0515'}, {'account_name': '笑疯狂007'}, {'account_name': '高高兴兴上班啦'}, {'account_name': '爷就是玩玩'}, {'account_name': '莲叶何田田200761'}, {'account_name': '啊星52066'}, {'account_name': '杰gg471738418'}, {'account_name': '郭大兴sss'}, {'account_name': '李小姐19890'}, {'account_name': '买家120'}, {'account_name': 'yococo5'}, {'account_name': '了若星辰小朗'}, {'account_name': 'yxd913924'}, {'account_name': '永爱宇欣'}, {'account_name': '微笑家阳光'}, {'account_name': '馨媛鑫'}, {'account_name': '航心中永远的永远'}, {'account_name': '田胜蕊'}, {'account_name': '李刚之子要加薪'}, {'account_name': '碧绿色星星'}, {'account_name': '会飞的小青牛'}, {'account_name': '错过变不在拥有灬'}, {'account_name': '枫木山村人'}, {'account_name': '李洪新1993'}, {'account_name': '魏铭庭'}, {'account_name': '张河昌'}, {'account_name': '玉轩1989'}, {'account_name': '繁花似入梦'}, {'account_name': '低压开关柜'}, {'account_name': '巧巧1340'}, {'account_name': '玛雅色菌'}, {'account_name': '思念的沉沦15997513560'}, {'account_name': '美美淘淘物'}, {'account_name': 'xxxholicweiyou'}, {'account_name': '碉楼玉器2'}, {'account_name': '权威xie'}, {'account_name': 'wozainashenghuo123'}, {'account_name': '为爱表演'}, {'account_name': '邯雨来袭'}, {'account_name': '魅力芯漾007'}, {'account_name': '心中有你72044521'}, {'account_name': '王子加公主888'}, {'account_name': '梦想18908043276'}, {'account_name': '宏禧园'}, {'account_name': '靳卫红1'}, {'account_name': 'w518梅'}, {'account_name': '金燕燕1987'}, {'account_name': '光大购物商城'}, {'account_name': '冬天的雨那样寒冷'}, {'account_name': '喊刚腹'}, {'account_name': '呆呆的木头99'}, {'account_name': '杜进进1'}, {'account_name': 't_1487948389143_0791'}, {'account_name': '小黑兔49'}, {'account_name': '我心飞扬2393'}, {'account_name': '提笔写心情1990'}, {'account_name': 'w124363305'}, {'account_name': '传说而已65433'}, {'account_name': '郭祥昆杨爱玲'}, {'account_name': 'tsytdc888'}, {'account_name': 'yanxi_祝福'}, {'account_name': '邓名丽'}, {'account_name': '唐砂伊'}, {'account_name': '辰宇宇诺'}, {'account_name': '肥龙ing'}, {'account_name': '金宣123'}, {'account_name': '心岛未晴820'}, {'account_name': 'zhoumimi18'}, {'account_name': '现在在这里'}, {'account_name': '小爱人生路'}, {'account_name': 'w441785271'}, {'account_name': '美美学'}, {'account_name': 'vip超买家'}, {'account_name': '果果198711'}, {'account_name': '贰王红'}, {'account_name': 'yuanxiaoli一生一世'}, {'account_name': 'z-b-i-l-y'}, {'account_name': '张艳华6'}, {'account_name': '邱成丽'}, {'account_name': '李晚霞1928'}, {'account_name': '小僧不流氓'}, {'account_name': '浅樱漫舞。'}, {'account_name': '幸福的四口之家666'}, {'account_name': '昊哥么么哒'}, {'account_name': '海蓝冰玉36'}, {'account_name': '静和王子'}, {'account_name': '四奶奶不孬'}, {'account_name': '言辞1234'}, {'account_name': '明秀147'}, {'account_name': '独舞的妖73'}, {'account_name': 'zc1051565927'}, {'account_name': '运51800'}, {'account_name': '网上通天地'}, {'account_name': '井里只哇'}, {'account_name': '冷洫族龙龙'}, {'account_name': 'xia李春霞'}, {'account_name': '林宝怡27265773'}, {'account_name': '纳兰容若850625'}, {'account_name': '鹏鹏爱霞霞love'}, {'account_name': '囝囝头1981'}, {'account_name': '林依韩22'}, {'account_name': '樱花的第七音符hj'}, {'account_name': '张张张大帅呀'}, {'account_name': '夏侯淳焦kb'}, {'account_name': 'xieqinghua_521'}, {'account_name': '木子思远1'}, {'account_name': '呵呵了第几'}, {'account_name': '孟详文'}, {'account_name': '靓2468'}, {'account_name': '小石头july'}, {'account_name': '曾涛爱你'}, {'account_name': '张宇高歌'}, {'account_name': '文仔17342873963'}, {'account_name': '尹瑞霞2013'}, {'account_name': '马姐姐59780323'}, {'account_name': 'wxyabc123_123'}, {'account_name': '稍等正在路上'}, {'account_name': '清风2016520'}, {'account_name': '姚安勇'}, {'account_name': '温暖的大好人1'}, {'account_name': '简派名品'}, {'account_name': '一片祥和206'}, {'account_name': '岁月静好123120'}, {'account_name': '垚博茜博爱妈'}, {'account_name': '独爱你宝宝'}, {'account_name': '老闫兰兰'}, {'account_name': '我荒废的心会一直爱你1314'}, {'account_name': '玉挽玲'}, {'account_name': '龙恩的浩荡'}, {'account_name': '锦御瑾秋'}, {'account_name': 'wangxing1693643219'}, {'account_name': '蕾蕾最爱24'}, {'account_name': '少女心2007'}, {'account_name': '宅男宅女宅不宅'}, {'account_name': '牙签盅ak47'}, {'account_name': '梁华向v2008'}, {'account_name': '冰雪2266'}, {'account_name': '我是小星星°'}, {'account_name': '熄灭的灯根'}, {'account_name': '蔡莉莉_007'}, {'account_name': '森林麋鹿78'}, {'account_name': '陌锌辰'}, {'account_name': '见男无心'}, {'account_name': '只因你倾心'}, {'account_name': '凝神听风zx'}, {'account_name': '刁媛媛dyy0'}, {'account_name': 'zhenglvzhou'}, {'account_name': '陈理想11'}, {'account_name': '浩瀚330303'}, {'account_name': '流xing羽'}, {'account_name': '宏发商业69383654'}, {'account_name': '粒粒粒粒75'}, {'account_name': 'zwl文玲828508'}, {'account_name': '小平平1117'}, {'account_name': 'xiaxiang2942'}, {'account_name': 'y1562244588'}, {'account_name': '我亚瑟'}, {'account_name': '王不可为'}, {'account_name': 'zj_jqz'}, {'account_name': '黄挺888'}, {'account_name': '倾国倾城倾你妹1122'}, {'account_name': 'xiaojian199555'}, {'account_name': '飞向火星88'}, {'account_name': '萍水相逢324624'}, {'account_name': '吉苏卜于缪'}, {'account_name': '从头再来6223'}, {'account_name': '彭一波95'}, {'account_name': 'wytbbs'}, {'account_name': '铁板鱿鱼2001'}, {'account_name': '林晓璇1998'}, {'account_name': '炫酷又能打的媛姐姐'}, {'account_name': '我爱我的家520411110103'}, {'account_name': '宝宝明明6826'}, {'account_name': '李在华54'}, {'account_name': '糯米style'}, {'account_name': '冯云豹853181958'}, {'account_name': 'yin13763318564'}, {'account_name': 't_1515069332165_0249'}, {'account_name': '好好的一份'}, {'account_name': '淡淡人生方'}, {'account_name': '吴玉波1983'}, {'account_name': '超辣小辣椒874195516'}, {'account_name': '回头客5209'}, {'account_name': '千薰泪幻'}, {'account_name': '朕是女皇715'}, {'account_name': '刘国冬1991'}, {'account_name': '蛋蛋的忧伤5662'}, {'account_name': 'vcycx'}, {'account_name': 'xhsujianyun'}, {'account_name': 'wanglan_1973'}, {'account_name': '于祥议111'}, {'account_name': '那情重来'}, {'account_name': '下雨天了在一起'}, {'account_name': '钓鱼的情怀'}, {'account_name': '蹲虎萝涛'}, {'account_name': '无情逝去'}, {'account_name': 'zlzlzl10086'}, {'account_name': '芙蓉凤姐哦'}, {'account_name': '妍菇凉1223'}, {'account_name': 'xiaofanfeng'}, {'account_name': '我是爱国人士'}, {'account_name': '千千千思哟'}, {'account_name': '认识或不认识'}, {'account_name': '时光是好人'}, {'account_name': '张愿扶主'}, {'account_name': 'zhufei217'}, {'account_name': '可人可人'}, {'account_name': 't_1515301024606_0493'}, {'account_name': '少为48'}, {'account_name': '皇太子86'}, {'account_name': '子嘉宝贝8'}, {'account_name': '讨厌你198410'}, {'account_name': '他们叫我闷油瓶'}, {'account_name': '罗洛兰佩洛斯'}, {'account_name': '潘荣0217'}, {'account_name': '感恩雨楠'}, {'account_name': '墨衣莫依66'}, {'account_name': '黄玉婷306519133'}, {'account_name': '翔翔0217'}, {'account_name': '小熊小猫2160'}, {'account_name': '时光是个美人0217'}, {'account_name': '我爱婷婷13140'}, {'account_name': '郑茜文'}, {'account_name': '五毛硬币11'}, {'account_name': '珊瑚岩2012'}]


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