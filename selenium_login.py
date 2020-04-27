from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import requests
import base64
import json
import urllib

#建立浏览器实例
browser = webdriver.Chrome("C:\\Users\\jiangcw\\chromedriver.exe")

#打开网址
browser.get('http://localhost:8080/login')

time.sleep(2)

#使用标签选择器
inputs = browser.find_elements_by_tag_name('input')
inputs[1].send_keys('123')
inputs[2].send_keys('123')

#定位滑块选择器
button = browser.find_element_by_class_name('dv_handler')
#建立动作的对象
action = ActionChains(browser)
#按住拖动
action.click_and_hold(button).perform()
#动作释放
action.reset_actions()
#拖动位置
action.move_by_offset(270,0).perform()


#选择元素
myimg = browser.find_element_by_xpath('//*[@id="app"]/div/section[2]/div/table/tr[4]/td[2]/img')

#截取元素图
myimg.screenshot('code.png')



#截取屏幕
# browser.get_screenshot_as_file('register.png')

# 图像处理
import cv2
#读图
img = cv2.imread('./code.png',cv2.IMREAD_GRAYSCALE)
#写图
cv2.imwrite('./code1.png',img)



#请求百度接口

# res = requests.get('https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【官网获取的AK】&client_secret=【官网获取的SK】')
res = requests.get('https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=OlntzXdROYFdrG2RzjtG9MQ2&client_secret=iXEY4CpxOkQoYviBVZqV2v3q9PixEtNL')

#转码
res = json.loads(str(res.text))
token = res['access_token']


#识别图像
url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token=' + token

#构造头部
header = {'Content-Type':'application/x-www-form-urlencoded'}

# 构造图片
img = open('./code1.png','rb')
temp_img = img.read()
img.close()


#构建参数
data = {'image':base64.b64encode(temp_img)}
#编码
data = urllib.parse.urlencode(data)

#发送请求
res = requests.post(url=url,data=data,headers=header)

crack_code = json.loads(res.text)['words_result'][0]['words']

crack_code = str(crack_code).split(' ')

print(crack_code)


time.sleep(2)


#输入验证码
browser.find_elements_by_tag_name('input')[3].send_keys(crack_code)


#延迟等待
time.sleep(10)


#关闭浏览器
browser.close()