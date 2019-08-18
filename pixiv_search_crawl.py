#运行前输入法调成英文！！
#本代码抓取pixiv登录情况下搜索的页面所有page的所有图片原图
import csv
import requests  
import time
import os
# 导入selenium的浏览器驱动接口
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 导入chrome选项
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# pyautogui
import pyautogui

#################################################################################
def pixiv_img_dl(driver,url,path):
    wait = WebDriverWait(driver,40)
    driver.get(url)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.sc-LzNbu')))
    driver.execute_script("window.stop();")#加载到所要的项目加载完成就停止加载进行下一步
    element = driver.find_element_by_css_selector("img.sc-LzNbu")#有些图片是登录才能看，所以可能会报错找不到
    action = ActionChains(driver).move_to_element(element)#移动到该元素
    action.context_click(element)#右键点击该元素
    #action.send_keys(Keys.ARROW_DOWN)#点击键盘向下箭头v                        
    #action.send_keys(v)#键盘输入V保存图 这里会出问题，总会变成选择第一个，目前不知道怎么处理，先用下面移动的方法。
    action.perform()#执行保存
    #time.sleep(5)一些操作间注意延时，模拟真人操作，否则无间隙操作会出现bug。
    pyautogui.typewrite(['v'])
    time.sleep(2)
    pyautogui.typewrite(['tab','tab','tab','tab','tab','tab','enter'])#切换到路径位置
    time.sleep(2)
    pyautogui.typewrite(path)#输入保存路径
    pyautogui.typewrite(['enter'])
    time.sleep(2)
    pyautogui.typewrite(['tab','tab','tab','tab','tab','enter'])#切换到文件名位置回车保存
    time.sleep(4)
    return
################################################################################
def pixiv_search_imglist(driver,url,page):
    driver.get(url+str(page))
    #图片不是全部加载，下拉后才会加载新的,有些时候会用到
    # 逐渐滚动浏览器窗口，令ajax逐渐加载
    #for i in range(1, 10):
    #    #js = "var q=document.body.scrollTop=" + str(500 * i)  # PhantomJS
    #    js = "var q=document.documentElement.scrollTop=" + str(500 * i)  # 谷歌 和 火狐 获取滚动条位置
    #    driver.execute_script(js)
    #    print('=====================================')
    #    time.sleep(3)
    img_group_list = driver.find_elements_by_class_name('PKslhVT')#返回满足的所有元素的列表
    #img_group_list = driver.find_element_by_css_selector('div.x7wiBV0'+'a.PKslhVT')
    #img_group_list = driver.find_element_by_css_selector('.PKslhVT')#这个不能返回一个列表
    # 收集所有图片链接到列表
    imgurl_list=[]
    for img in img_group_list:
        imgurl = img.get_attribute('href')
        print(imgurl)
        imgurl_list.append(str(imgurl))
    # 将收集到的数据写入文件
    f = open('pixiv_list.txt', 'a', encoding='utf-8')
    f.write(+'\n'+'page: '+str(page)+'\n')
    f.write('\n'.join(imgurl_list))
    f.close()
    time.sleep(5)
    return imgurl_list

###########  main  ############
#chrome_options = Options()
#chrome_options.add_argument('--headless')#无头模式
#driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Chrome()
#设置超时设置
#driver.set_page_load_timeout(10)
#driver.set_script_timeout(10)

########手动登录######
#driver.get("https://pixiv.net")
#time.sleep(300)#
## 获取cookies
#cookie_list = driver.get_cookies()
#print(cookie_list)
#driver.get("https://pixiv.net")

#######另一种登录方法，测试出错未debug#########
#userNAME = 
#userPASS = 
#username = driver.find_element_by_xpath("//input[@autocomplete='username']")    
#userpass = driver.find_element_by_xpath("//input[@autocomplete='current-password']")
#submit = driver.find_element_by_xpath("//button[@type='submit']")
#username.send_keys(userNAME)
#time.sleep(2)
#userpass.send_keys(userPASS)
#time.sleep(2)
#submit.click()#点击该元素
#WebDriverWait(driver, 100)

########用cookie登录#############
driver.get("https://pixiv.net")
pixiv_cookielist = [{'domain': '.pixiv.net', 'expiry': 1566095147, 'httpOnly': False, 'name': '__utmb', 'path': '/', 'secure': False, 'value': '235335808.2.9.1566093347476'}, {'domain': 'www.pixiv.net', 'expiry': 1723859747, 'httpOnly': False, 'name': 'ki_t', 'path': '/', 'secure': False, 'value': '1566093347448%3B1566093347448%3B1566093347448%3B1%3B1'}, {'domain': '.pixiv.net', 'expiry': 1566179554.0174, 'httpOnly': True, 'name': 'login_bc', 'path': '/', 'secure': True, 'value': '1'}, {'domain': '.pixiv.net', 'expiry': 1629165347, 'httpOnly': False, 'name': '__utmv', 'path': '/', 'secure': False, 'value': '235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=16643188=1^9=p_ab_id=8=1^10=p_ab_id_2=3=1^11=lang=zh=1'}, {'domain': '.pixiv.net', 'httpOnly': False, 'name': '__utmc', 'path': '/', 'secure': False, 'value': '235335808'}, {'domain': '.www.pixiv.net', 'expiry': 1723773261, 'httpOnly': False, 'name': 'login_ever', 'path': '/', 'secure': False, 'value': 'yes'}, {'domain': '.pixiv.net', 'expiry': 1568685239.011246, 'httpOnly': True, 'name': 'PHPSESSID', 'path': '/', 'secure': True, 'value': '16643188_1c2f3fdc59df630e95c307de58913ec9'}, {'domain': '.pixiv.net', 'expiry': 1597629289.779774, 'httpOnly': False, 'name': 'module_orders_mypage', 'path': '/', 'secure': True, 'value': '%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D'}, {'domain': '.pixiv.net', 'expiry': 1629165239.011196, 'httpOnly': False, 'name': 'c_type', 'path': '/', 'secure': True, 'value': '22'}, {'domain': '.pixiv.net', 'expiry': 1629165239.011305, 'httpOnly': False, 'name': 'b_type', 'path': '/', 'secure': True, 'value': '1'}, {'domain': '.pixiv.net', 'expiry': 1629165239.011285, 'httpOnly': False, 'name': 'a_type', 'path': '/', 'secure': True, 'value': '0'}, {'domain': '.pixiv.net', 'expiry': 1629165347, 'httpOnly': False, 'name': '__utma', 'path': '/', 'secure': False, 'value': '235335808.886623600.1566093154.1566093287.1566093287.1'}, {'domain': '.pixiv.net', 'expiry': 1629165239.011325, 'httpOnly': True, 'name': 'd_type', 'path': '/', 'secure': True, 'value': '2'}, {'domain': 'www.pixiv.net', 'expiry': 1629165239.011119, 'httpOnly': False, 'name': 'first_visit_datetime_pc', 'path': '/', 'secure': True, 'value': '2019-08-18+10%3A53%3A57'}, {'domain': '.pixiv.net', 'expiry': 1629165238.126809, 'httpOnly': True, 'name': 'privacy_policy_agreement', 'path': '/', 'secure': True, 'value': '1'}, {'domain': '.pixiv.net', 'expiry': 1568685238.126774, 'httpOnly': True, 'name': 'device_token', 'path': '/', 'secure': True, 'value': '58d5f59a6afec2e5692efcfde717d228'}, {'domain': '.pixiv.net', 'expiry': 1581861347, 'httpOnly': False, 'name': '__utmz', 'path': '/', 'secure': False, 'value': '235335808.1566093287.1.1.utmcsr=accounts.pixiv.net|utmccn=(referral)|utmcmd=referral|utmcct=/login'}, {'domain': 'www.pixiv.net', 'expiry': 1629165239.011394, 'httpOnly': False, 'name': 'yuid_b', 'path': '/', 'secure': True, 'value': 'QghGQGA'}, {'domain': 'www.pixiv.net', 'expiry': 1566179639.011377, 'httpOnly': False, 'name': 'is_sensei_service_user', 'path': '/', 'secure': True, 'value': '1'}, {'domain': '.pixiv.net', 'expiry': 1566179554, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.820310768.1566093154'}, {'domain': '.pixiv.net', 'expiry': 1723773153.004903, 'httpOnly': False, 'name': 'p_ab_id_2', 'path': '/', 'secure': True, 'value': '3'}, {'domain': 'www.pixiv.net', 'expiry': 1723859747, 'httpOnly': False, 'name': 'ki_r', 'path': '/', 'secure': False, 'value': ''}, {'domain': '.pixiv.net', 'expiry': 1629165154, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.2.886623600.1566093154'}, {'domain': '.pixiv.net', 'expiry': 1723773153.004944, 'httpOnly': False, 'name': 'p_ab_d_id', 'path': '/', 'secure': True, 'value': '339243034'}, {'domain': '.pixiv.net', 'expiry': 1566093886, 'httpOnly': False, 'name': '__utmt', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.pixiv.net', 'expiry': 1723773153.004859, 'httpOnly': False, 'name': 'p_ab_id', 'path': '/', 'secure': True, 'value': '8'}]
#这里的cookielist是手动登陆一次后获取的，之后就可以用cookie登录。
for k in pixiv_cookielist:
    driver.add_cookie(k)
driver.get("https://pixiv.net")

####要爬的pixiv搜索页面url除去最后page的数字####
url = 'https://www.pixiv.net/search.php?word=尻神様%2010000users&order=date_d&p='
####图片另存为的路径####
save_path = "C:/Users/LENOVO/Downloads/temp/tmp"
page = 1

while 1:
    try:
        list = pixiv_search_imglist(driver,url,page)
    except Exception as e:
        print("list error page= "+str(page))
        break
    i=0
    while i<len(list):
        try:
            pixiv_img_dl(driver,list[i],save_path)
        except Exception as e:
            print("Exception: No."+str(i+1))
        i = i+1
    page = page+1

# 关闭浏览器
driver.quit()