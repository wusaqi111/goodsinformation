from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import json

def browser_initial():
    """"
    进行浏览器初始化
    """
    os.chdir('C:\\Users\\沃丝尼达耶星星\\Desktop\\workplace ')#C:\Users\沃丝尼达耶星星\Desktop\workplace  'E:\\pythonwork'
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
    browser = webdriver.Chrome(executable_path= "C:/Users/沃丝尼达耶星星/Downloads/chromedriver_win32/chromedriver.exe",options=chrome_options)
    log_url = 'https://main.m.taobao.com/?ch=0&vt=2&_gp=0&dh_zy=&bookmark=&dh=&bookmark_pi=&mid=22l0pE'
    return log_url,browser

def get_cookies(log_url,browser):
    """
    获取cookies保存至本地
    """
    browser.get(log_url)
    time.sleep(20)     # 进行扫码
    dictCookies = browser.get_cookies()
    jsonCookies = json.dumps(dictCookies) #  转换成字符串保存

    with open('taobao_cookies.txt', 'w') as f:
        f.write(jsonCookies)
    print('cookies保存成功！')

if __name__ == "__main__":
    tur = browser_initial()
    get_cookies(tur[0], tur[1])