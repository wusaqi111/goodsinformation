from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import urllib.parse
from selenium.common.exceptions import WebDriverException
from pyquery import PyQuery as pq
from utils import dbUtil
import datetime
import json
import time
import random
from browsermobproxy import Server
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import re

server = Server(r"C:\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat")
server.start()
proxy = server.create_proxy()




def main(keyword,subkey,total_pages):


    total_pages=int(total_pages)
    # url = 'https://uland.taobao.com/semm/tbsearch?refpid=mm_26632258_3504122_32554087&keyword={0}'
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--incognito')#无痕模式
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-default-browser-check")
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option("useAutomationExtension", False)
    mobileEmulation = {'deviceName': 'iPhone X'}#模拟手机
    chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)

    chrome_options.add_experimental_option('excludeSwitches',
                                           ['enable-automation'])
    # chrome_options.add_argument("disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    # chrome_options.add_argument(r'--user-data-dir=C:\Users\沃丝尼达耶星星\AppData\Local\Google\Chrome\User Data')
    chrome_options.add_experimental_option('perfLoggingPrefs', {'enableNetwork': True})
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}

    # chrome_options.add_argument('--headless')  # 设置无头chrome
    driver = webdriver.Chrome(options=chrome_options,desired_capabilities=caps)
    with open('C:/Users/沃丝尼达耶星星/stealth.min.js') as f:
        js = f.read()
    # print(js)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": js
    })
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": '''
    #   function objKeySort(obj) {
    #     let newkey = Object.keys(obj).sort();
    #     let resStr = '';
    #     for (let i = 0; i < newkey.length; i++) {
    #             let str = obj[newkey[i]];
    #             console.log(i,newkey[i],str);
    #             resStr += str;
    #     }
    # }
    #   '''
    # })

    # driver.get("https://main.m.taobao.com/?ch=0&vt=2&_gp=0&dh_zy=&bookmark=&dh=&bookmark_pi=&mid=22l0pE")
    #
    # with open('C:\\Users\\沃丝尼达耶星星\\Desktop\\workplace\\taobao_cookies.txt', 'r', encoding='utf8') as f:
    #     listCookies = json.loads(f.read())
    # for cookie in listCookies:
    #     cookie_dict = {
    #         'domain': '.taobao.com',
    #         'name': cookie.get('name'),
    #         'value': cookie.get('value'),
    #         'path': '/',
    #         "expires": '',
    #         'sameSite': 'None',
    #         'secure': cookie.get('secure')
    #     }
    #     driver.add_cookie(cookie_dict)
    driver.get("https://main.m.taobao.com/?ch=0&vt=2&_gp=0&dh_zy=&bookmark=&dh=&bookmark_pi=&mid=22l0pE")
    time.sleep(random.randint(10,20)*0.1)
    proxy.new_har("video",options={'captureContent': True,'captureContent': True})
    driver.find_element(By.CLASS_NAME,"search").click()
    search=driver.find_element(By.CSS_SELECTOR,"input")
    search.clear()
    time.sleep(random.randint(5,10)*0.1)
    search.send_keys(keyword+subkey)
    time.sleep(random.randint(5,10)*0.1)
    # driver.find_element_by_css_selector("div[class ~= search-btn]")
    search.send_keys(Keys.ENTER)

    driver.refresh()
    time.sleep(2)
    goods_list = []
    # 按页爬取
    print('正在爬取：')
    for page in range(total_pages + 1):
        print('[INFO] 正在抓取第%d页...' % (page + 1))
        for i in range(50):
            js="window.scrollBy(0,50)"
            driver.execute_script(js)
            time.sleep(0.2)
            if(i%5==0):
                time.sleep(1)
        time.sleep(3)
    json_data = proxy.har
    # print("数据包：",json_data)
    for entry in json_data['log']['entries']:
        # 根据URL找到数据接口
        entry_url = entry['response']['content']
        # print(entry_url)
        if('text' in entry_url):
            entry_data=entry_url['text']
            res = re.match(' mtopjsonp(.*)',entry_data)
            # print("商品数据：",res)
            # if(page==total_pages):
            try:
                if(res):
                    # print('thits1:',res.group(1))
                    ll=res.group(1)
                    res1=re.match('.*?\((.*)\)$',ll)
                    result=json.loads(res1.group(1))
                    # print('商品数据:',res1.group(1))
                    if(result['data']=={}):
                        pass
                    else:
                        goods_list.append(result)
            except:
                pass
        # json_data = proxy.har
        # # print(json_data)
        # for entry in json_data['log']['entries']:
        #     # 根据URL找到数据接口
        #     entry_url = entry['response']['content']
        #     # print(entry_url)
        #     if('text' in entry_url):
        #         entry_data=entry_url['text']
        #         res = re.match(' mtopjsonp(.*)',entry_data)
        #         # print(res)
        #         if(page==total_pages):
        #             try:
        #                 if(res):
        #                     # print('thits1:',res.group(1))
        #                     ll=res.group(1)
        #                     res1=re.match('.*?\((.*)\)$',ll)
        #                     result=json.loads(res1.group(1))
        #                     # print('thits1:',res1.group(1))
        #                     if(result['data']=={}):
        #                         pass
        #                     else:
        #                         goods_list.append(result)
        #             except:
        #                 pass
        # 获取接口返回内容
    goods_sum=[]
    goods_list1=[]
    # print("商品数据：",goods_list)

    for i in goods_list:
        try:
            ii=i['data']['itemsArray']
            for num in range(len(ii)):
                goods_sum.append(ii[num])
        except:
            print(("无效包"))
    items=data_clean(goods_sum)
    # print("商品数据：",items)
    for item in items:
        if(item[4]==''):
            item[4]=0
        else:
            item[4]=int(item[4].strip().replace("万", "0000").replace("+", "").replace("人付款", ""))
        goods_list1.append([keyword, item[0],subkey, item[1],
                           item[2],
                           item[3].strip().replace("\ue667",""),
                           item[4],item[5].strip()])
    # print("商品数据：",goods_list1)
    print('[INFO] 数据获取完毕，爬虫运行结束')
    save(keyword,subkey,goods_list1)
    driver.quit()

def save(keyword,subkey,list):
    content = "淘宝[" + keyword + subkey + "]销售数据,获取共" + str(len(list)) + "条数据"
    db = dbUtil()
    m = datetime.datetime.now().strftime("%Y-%m")

    for category, title,subkeycat, discount, original_price, shop, monthly_sales,pid in list:
        s_sql = "select count(id) from goods_subkey where  pid=\"" + pid + "\" and monthly=\"" + m + "\" and shop=\"" + shop + "\" and monthly_sales=\"" + str(monthly_sales) +"\""
        c_sql="select count(id) from category_new where subkey=\"" + subkeycat + "\""
        c_sql1="select count(id) from category where content=\"" + subkeycat + "\""
        c_res= db.query_noargs(c_sql)
        c_res1= db.query_noargs(c_sql1)
        s_res = db.query_noargs(s_sql)
        # print(s_res)
        # category_sql = ""
        if c_res[0][0] == 0:
            category_sql="insert into category_new VALUES (NULL,\""+category+"\",\"" + subkeycat + "\")"
            db.query_noargs(category_sql)
        if c_res1[0][0] == 0:
            category_sql1="insert into category VALUES (NULL,\"" + subkeycat + "\")"
            db.query_noargs(category_sql1)
        goods_sql = ""
        if s_res[0][0] == 0:
            goods_sql = "insert into goods_subkey VALUES (NULL, \"" + pid + "\",\"" + title + "\",\"" + category + "\",\"" + subkeycat + "\"," + str(
                discount) + "," + str(original_price) + ",\"" + shop + "\"," + str(monthly_sales) + ",\"" + m + "\")"
        else:
            goods_sql = "update  goods_subkey set discount=" + str(discount) + ",original_price=\"" + str(
                original_price) + "\",monthly_sales=\"" + str(
                monthly_sales) + "\" where category= \"" + category+ "\"and subkeycat=\"" + subkeycat+ "\" and pid=\"" + pid + "\" and monthly=\"" + m + "\""
        db.query_noargs(goods_sql)
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "insert into slog VALUES (NULL, \"【爬虫启动】爬取数据：" + content + "\",\"" + t + "\")"
    db.query_noargs(sql)
    db.close_commit()


def data_clean(list):
    for i in list:
        try:
            title=i['title']
            original_price=float(i['price'].strip())
            discount_price=float(i['priceShow']['price'].strip())
            # shop=i['shopInfo']['shopInfoList'][0]
            if(i['shopInfo']['shopInfoList'][0]=="进店"):
                shop="未知店铺信息"
            else:
                shop=i['shopInfo']['shopInfoList'][0]
            monthly_sales=i['realSales']
            pid=i['item_id']
            yield [title, discount_price, original_price, shop, monthly_sales,pid]
        except:
            pass

# def spider(key,subkey, total_pages):
#     main(key,subkey, total_pages)



# def spider(key,subkey, total_pages):


if __name__ == '__main__':
    main('CPU','英特尔',3)
