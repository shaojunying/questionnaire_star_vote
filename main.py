import os
import random
import re
import time
import matplotlib.pyplot as plt

import requests
from PIL import Image
from pyquery import PyQuery as pq
from ctypes import *

YDMApi = windll.LoadLibrary('yundamaAPI')
username = b'shaojunying'
password = b'QrWbR6NffhRCFPr'

user_agents = [
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) "
    "Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",

]
curid = "31500328"
# curid = "24637779"
for _ in range(40):
    base_url = "https://www.wjx.cn/m/" + curid + ".aspx"
    html = requests.get(base_url)
    data = pq(html.text)
    prefer_data = [1, 0, 1, 1, -1, 1, 0, 2, 2, 1, 1, 1, 2]
    all_questions = data.find("div.ui-controlgroup").items()
    list = []
    for i in all_questions:
        list.append(len(i.children()))
    rndnum = re.findall('rndnum="(.*?)"', html.text)[0]
    jqnonce = re.findall('jqnonce="(.*?)"', html.text)[0]
    data222 = ""
    for index, i in enumerate(list):
        choice = 0
        random_num = random.randint(0, i)
        if random.random() > 0.3 and prefer_data[index] != -1:
            choice = prefer_data[index]
        data222 += str(index + 1) + "$" + str(choice + 1) + "}"
    # print(data)
    start_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(int(time.time()) - random.randint(1, 60 * 3)))

    raw_t = round(time.time(), 3)
    t = int(str(raw_t).replace('.', ''))
    ktimes = 24
    a = jqnonce
    b = ktimes % 10
    if b == 0:
        b = 1
    c = []

    for d in range(len(a)):
        e = ord(a[d]) ^ b
        c.append(chr(e))
    jqsign = "".join(c)
    params = {
        "curid": curid,
        "starttime": start_time,
        # validate_text: xdce
        "source": "directphone",
        "submittype": "1",
        "ktimes": str(ktimes),
        "hlv": "1",
        "rn": rndnum,
        "t": t,
        "jqnonce": jqnonce,
        "jqsign": jqsign,
    }

    header = {"Connection": "keep-alive",
              "Cookie": "acw_tc=707c9fdd15433207510264221e602225055a12665b3a05d8ab47c64d7e9867; .ASPXANONYMOUS=smYrT9y81AEkAAAAYzViOTk3MjgtOTc2YS00NmViLWFkOTQtMTA0YjE4MzQyNDgxaLMvdhD_boQYpBwFOPkpK9vaOac1; UM_distinctid=1675515d4ac278-0ba6f365b928a8-4313362-144000-1675515d4ad130; Hm_lvt_21be24c80829bd7a683b2c536fcf520b=1543320753,1543335112; ASP.NET_SessionId=oi0myyfqz11jx411z5kbmf3u; jac31500328=72063181; CNZZDATA4478442=cnzz_eid%3D333430093-1543320442-%26ntime%3D1543399730; jpckey=%u4E2D%u5B66; LastActivityJoin=31500328,102131823481; Hm_lpvt_21be24c80829bd7a683b2c536fcf520b=1543404792",
              "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
              "DNT": "1",
              "Host": "www.wjx.cn",
              "Origin": "https://www.wjx.cn",
              "Referer": "https://www.wjx.cn/m/24637779.aspx",
              "User-Agent": user_agents[0],
              "X-Requested-With": "XMLHttpRequest"}
    url = "https://www.wjx.cn/joinnew/processjq.ashx"
    ip_pool = [
        "117.90.252.129:9000",
        "110.189.152.86:34975",
        "203.93.125.238:31566",
        "47.96.136.190:8118",
        "113.200.27.10:36708",
        "183.129.207.82:12719",
        "183.129.207.82:11453",
        "58.251.49.4:58729",
        "210.22.176.146:39038",
        "222.92.85.37:51511",
        "115.218.219.190:9000",
        "115.218.216.2:9000",
        "139.196.138.176:80",
        "125.117.133.55:9000",
        "175.155.75.242:8888"
    ]
    ip = ip_pool[random.randrange(0, len(ip_pool))]
    proxy_ip = 'http://' + ip
    proxies = {'http': proxy_ip}
    data222 = {"submitdata": data222[:-2]}
    for i in range(1):
        html = requests.post(url=url, params=params, data=data222, headers=header)
    if html.text == "7〒您输入的验证码有误，请重新输入！":
        verification_url = "https://www.wjx.cn/wjx/join/AntiSpamImageGen.aspx?"
        data1 = {"q": curid, "t": "1543404803769"}
        img = requests.get(verification_url, params=data1, headers=header).content

        with open("1.png", "wb") as file:
            file.write(img)

        img = Image.open("1.png")
        plt.imshow(img)
        plt.show()

        print('\r\n>>>正在一键识别...')
        codetype = 1004
        result = c_char_p(b"                              ")
        timeout = 60
        filename = b'1.png'
        appId = 1  # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
        appKey = b'22cc5376925e9387a23cf797cb9ba745'  # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
        # 一键识别函数，无需调用 YDM_SetAppInfo 和 YDM_Login，适合脚本调用
        captchaId = YDMApi.YDM_EasyDecodeByPath(username, password, appId, appKey, filename, codetype, timeout, result)

        print("一键识别：验证码ID：%d，识别结果：%s" % (captchaId, result.value))

        temp = params
        temp["validate_text"] = result.value
        html = requests.post(url=url, params=temp, data=data222, headers=header)
        print("输入验证码之后的结果", html.text)
        # verification = input("请输入验证码对应的字符(4个)")
        # if len(verification) == 4:
        #     temp = params
        #     temp["validate_text"] = verification
        #     print(temp)
        #     print(data222)
        #     html = requests.post(url=url, params=temp, data=data222, headers=header)
        #     print("输入验证码之后的结果", html.text)
        # else:
        #     print("错误")
