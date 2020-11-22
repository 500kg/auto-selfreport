import os
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import yagmail
import argparse
import datetime

def login(username, password, browser):
    url = "https://uis.fudan.edu.cn/authserver/login"

    #先登录
    browser.get(url)

    browser.find_element_by_name("username").send_keys("20210240183")
    browser.find_element_by_name("password").send_keys("Fdu990202")

    browser.find_element_by_id("idcheckloginbtn").click()

    url = "https://elife.fudan.edu.cn/public/front/search.htm?id=2c9c486e4f821a19014f82381feb0001"

    browser.get(url)
    
    browser.find_element_by_xpath("//*[@id='login_table_div']/div[2]/input").click()

def get_browser():
    chrome_options = Options()
    # headless本地报错
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    if os.path.exists("./chrome/chromedriver.exe"):
        browser = webdriver.Chrome("C:\Github\科技强国\chrome\chromedriver.exe", chrome_options=chrome_options)
    else:
        browser = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options)
    return browser

def get_account():
    # win10 本地测试
    if os.name == 'nt':
        try:
            with open("account.txt") as account:   
                username = account.readline()
                password = account.readline()
        except:
            print("FAK")
    # 在github上整，系统是linux的话不要怪我
    else:
        username = os.environ['PASSWORD']
        password = os.environ['PASSWORD']
    return username, password

def reserve(browser, date, hour):
    url = "https://elife.fudan.edu.cn/public/front/search.htm?id=2c9c486e4f821a19014f82381feb0001"

    browser.get(url)

    browser.find_element_by_xpath("/html/body/div/div/div[3]/table[1]/tbody/tr/td[2]/table/tbody/tr[5]/td/a").click()

    # 到羽毛球预约界面了。
    # 快进到正确日期
    current_url = browser.current_url
    url_2 = current_url + '&ordersId=&currentDate=2020-'+ date
    browser.get(url_2)
    time.sleep(10)
    #约个1600-1700的场
    #还得看看这玩意能约不
    xpth = "//*[font='" + hour + "']/../td[6]/img"

    file = "[" + date + ',' + hour + "]"
    try: 
        ava = browser.find_element_by_xpath(xpth).get_attribute("src")
    except :
        file += "错误，请检查时间格式"
        return file
    if(ava == 'https://elife.fudan.edu.cn/images/front/index/button/no.gif'):
        file += "指定时间已无空闲场次或您已预约"
        return file

    browser.find_element_by_xpath(xpth).click()

    browser.find_element_by_xpath("//*[@id='btn_sub']").click()
    file += "预约成功"
    return file

def writefile(res, path):
    with open(path, 'a') as f:
        f.write(res + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--day", default = "02")#默认周一周三
    parser.add_argument("--hour", default = "16:00")#默认1600-1700
    args = parser.parse_args()
    hour = args.hour
    day = args.day  
    days = []
    
    current_day = time.localtime()[6]

    path = './res.txt'
    

    browser = get_browser()
    username, password = get_account()
    login(username, password, browser)
    """
    #格式：date: "11-24" hour: "16:00"
    """
    #date = "11-24"
    #hour = "16:00"
    
    for ch in day:
        target_day = int(ch)
        x = (target_day - current_day + 7)%7
        if(x <= 2):
            date = (datetime.datetime.now() + datetime.timedelta(days = x)).strftime("%m-%d")
            print(date, hour)
            res = reserve(browser, date, hour)
            writefile(res, path)