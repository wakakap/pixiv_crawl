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
# pyautogui，如果用这个似乎不能使用headless模式，注意。
import pyautogui

#################################################################################
def diary_write(str,path):
    fo = open(path+"/diary.txt", "a",encoding='utf-8')
    fo.write(str+'\n')
    fo.close()

def pixiv_img_dl(driver,url,path):
    #wait = WebDriverWait(driver,120)
    #driver.get(url)
    #wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.eAOnwx')))#加载到所要的项目加载完成
    #driver.execute_script("window.stop();")
    #以上等待的方法方法似乎效果不明显，它总是会等待完全加载才执行之后的代码
    driver.get(url)#这一步页面并没有完全加载就开始执行后面内容，原因未知，所以我之后设置了time延迟
    time.sleep(4)
    element = driver.find_element_by_css_selector("img.sc-LzMBt")#这个可能会变化，注意查看
    time.sleep(1)
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
    pyautogui.typewrite(['tab','tab','tab','tab','tab','tab','enter'])#切换到文件名位置回车保存
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
    time.sleep(6)
    img_group_list = driver.find_elements_by_class_name('sc-fzXfPg')#返回满足的所有元素的列表
    #img_group_list = driver.find_element_by_css_selector('div.x7wiBV0'+'a.PKslhVT')
    #img_group_list = driver.find_element_by_css_selector('.PKslhVT')#这个不能返回一个列表
    # 收集所有图片链接到列表
    imgurl_list=[]
    for img in img_group_list:
        imgurl = img.get_attribute('href')
        #print(imgurl)
        imgurl_list.append(str(imgurl))
    # 将收集到的数据写入文件
    #f = open('pixiv_list.txt', 'a', encoding='utf-8')
    #f.write('\n'+'page: '+str(page)+'\n')
    #f.write('\n'.join(imgurl_list))
    #f.close()
    time.sleep(1)
    return imgurl_list

###########  main  ############
####要爬的pixiv搜索页面url除去最后page的数字####
url = 'https://www.pixiv.net/search.php?word=%E3%82%A2%E3%82%B9%E3%82%AB%201000users&p='
####图片另存为的路径####
save_path = "E:/CODE/PY/PIXIV_CRAWL/tmp"
page = 1

diary_write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' start crawl',save_path)
#chrome_options = Options()
#chrome_options.add_argument('--headless')#无头模式
#driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Chrome()
#设置超时设置
#driver.set_page_load_timeout(10)
#driver.set_script_timeout(10)

########手动登录######
driver.get("https://pixiv.net")
time.sleep(60)#
# 获取cookies
cookie_list = driver.get_cookies()
diary_write(str(cookie_list),save_path)
#driver.get("https://pixiv.net")

#######另一种登录方法，测试出错未debug#########
#userNAME = 
#userPASS = 
#username = driver.find_element_by_xpath("//input[@autocomplete='username']")    
#submit = driver.find_element_by_xpath("//button[@type='submit']")
#userpass = driver.find_element_by_xpath("//input[@autocomplete='current-password']")
#username.send_keys(userNAME)
#time.sleep(2)
#userpass.send_keys(userPASS)
#time.sleep(2)
#submit.click()#点击该元素
#WebDriverWait(driver, 100)

########用cookie登录#############
#pixiv_cookielist = [{'domain': 'www.pixiv.net', 'expiry': 1731923377, 'httpOnly': False, 'name': 'ki_t', 'path': '/', 'secure': False, 'value': '1574156977623%3B1574156977623%3B1574156977623%3B1%3B1'}, {'domain': '.pixiv.net', 'expiry': 1574158759, 'httpOnly': False, 'name': '__utmb', 'path': '/', 'secure': False, 'value': '235335808.4.9.1574156959763'}, {'domain': '.pixiv.net', 'expiry': 1574156996, 'httpOnly': False, 'name': '_gat_UA-1830249-138', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.pixiv.net', 'httpOnly': False, 'name': '__utmc', 'path': '/', 'secure': False, 'value': '235335808'}, {'domain': '.pixiv.net', 'expiry': 1574243304.321487, 'httpOnly': True, 'name': 'login_bc', 'path': '/', 'secure': True, 'value': '1'}, {'domain': '.pixiv.net', 'expiry': 1637228959, 'httpOnly': False, 'name': '__utmv', 'path': '/', 'secure': False, 'value': '235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=16643188=1^9=p_ab_id=8=1^10=p_ab_id_2=4=1^11=lang=zh=1'}, {'domain': '.www.pixiv.net', 'expiry': 1731836935, 'httpOnly': False, 'name': 'login_ever', 'path': '/', 'secure': False, 'value': 'yes'}, {'domain': '.pixiv.net', 'expiry': 1576748914.583227, 'httpOnly': True, 'name': 'PHPSESSID', 'path': '/', 'secure': True, 'value': '16643188_4127ff787e80ee6e300df4f1950198be'}, {'domain': '.pixiv.net', 'expiry': 1605692914.583267, 'httpOnly': False, 'name': 'module_orders_mypage', 'path': '/', 'secure': True, 'value': '%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D'}, {'domain': '.pixiv.net', 'expiry': 1637228914.583195, 'httpOnly': False, 'name': 'c_type', 'path': '/', 'secure': True, 'value': '22'}, {'domain': '.pixiv.net', 'expiry': 1637228914.58325, 'httpOnly': False, 'name': 'b_type', 'path': '/', 'secure': True, 'value': '1'}, {'domain': '.pixiv.net', 'expiry': 1637228914.583242, 'httpOnly': False, 'name': 'a_type', 'path': '/', 'secure': True, 'value': '0'}, {'domain': '.pixiv.net', 'expiry': 1589924959, 'httpOnly': False, 'name': '__utmz', 'path': '/', 'secure': False, 'value': '235335808.1574156901.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'}, {'domain': 'www.pixiv.net', 'expiry': 1637228914.583284, 'httpOnly': False, 'name': 'yuid_b', 'path': '/', 'secure': True, 'value': 'MReIOBA'}, {'domain': 'www.pixiv.net', 'expiry': 1574243314.583278, 'httpOnly': False, 'name': 'is_sensei_service_user', 'path': '/', 'secure': True, 'value': '1'}, {'domain': '.pixiv.net', 'expiry': 1576748914.041396, 'httpOnly': True, 'name': 'device_token', 'path': '/', 'secure': True, 'value': '81fea3f0af07b8236d8491fb73b4cf76'}, {'domain': 'www.pixiv.net', 'expiry': 1731923377, 'httpOnly': False, 'name': 'ki_r', 'path': '/', 'secure': False, 'value': ''}, {'domain': '.pixiv.net', 'expiry': 1637228959, 'httpOnly': False, 'name': '_ga', 'path': '/', 'secure': False, 'value': 'GA1.2.66106697.1574156901'}, {'domain': '.pixiv.net', 'expiry': 1574243359, 'httpOnly': False, 'name': '_gid', 'path': '/', 'secure': False, 'value': 'GA1.2.64685155.1574156905'}, {'domain': 'www.pixiv.net', 'expiry': 1637228878.120416, 'httpOnly': False, 'name': 'first_visit_datetime_pc', 'path': '/', 'secure': True, 'value': '2019-11-19+18%3A47%3A57'}, {'domain': '.pixiv.net', 'expiry': 1637228914.583257, 'httpOnly': True, 'name': 'd_type', 'path': '/', 'secure': True, 'value': '2'}, {'domain': '.pixiv.net', 'expiry': 1731836878.120488, 'httpOnly': False, 'name': 'p_ab_id', 'path': '/', 'secure': True, 'value': '8'}, {'domain': '.pixiv.net', 'expiry': 1574157500, 'httpOnly': False, 'name': '__utmt', 'path': '/', 'secure': False, 'value': '1'}, {'domain': '.pixiv.net', 'expiry': 1637228914.041406, 'httpOnly': True, 'name': 'privacy_policy_agreement', 'path': '/', 'secure': True, 'value': '1'}, {'domain': '.pixiv.net', 'expiry': 1637228959, 'httpOnly': False, 'name': '__utma', 'path': '/', 'secure': False, 'value': '235335808.66106697.1574156901.1574156901.1574156901.1'}, {'domain': '.pixiv.net', 'expiry': 1731836878.120496, 'httpOnly': False, 'name': 'p_ab_id_2', 'path': '/', 'secure': True, 'value': '4'}, {'domain': '.pixiv.net', 'expiry': 1731836878.120504, 'httpOnly': False, 'name': 'p_ab_d_id', 'path': '/', 'secure': True, 'value': '1712693997'}]
##这里的cookielist是手动登陆一次后获取的，之后就可以用cookie登录。
#for k in pixiv_cookielist:
#    driver.add_cookie(k)
#driver.get("https://pixiv.net")


while 1:
    try:
        list = pixiv_search_imglist(driver,url,page)
        diary_write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+str(url)+str(page),save_path)
    except Exception as e:
        diary_write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+str(url)+str(page),save_path)
        break
    i=0
    while i<len(list):
        try:                       
            pixiv_img_dl(driver,list[i],save_path)#遇到动图等其他格式时，try报错然后跳过。
            diary_write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" dl_success: "+str(list[i]),save_path)
        except Exception as er:
            diary_write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" error "+str(list[i]),save_path)
            diary_write(str(er),save_path)
        i = i+1
    page = page+1
    if page>8:
        break
# 关闭浏览器
diary_write(('\n')+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' END Normally'+('\n'),save_path)
driver.quit()
