# -*-coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm

from urllib.parse import urljoin

import time


orihtml=input("请输入要爬取的网址:")


browser=webdriver.Chrome()

browser.get(orihtml)



'''
//*[@id="bilibiliPlayer"]/div[1]/div[2]/div/div[1]/div[1]/span[1]

//*[@id="comment"]/div/div[2]/div[1]/div[3]/div[1]/div[2]/p
//*[@id="comment"]/div/div[2]/div[1]/div[3]/div[2]/div[2]/p
//*[@id="comment"]/div/div[2]/div[1]/div[3]/div[3]/div[2]/p
//*[@id="comment"]/div/div[2]/div[1]/div[3]/div[4]/div[2]/p

//*[@id="comment"]/div/div[2]/div[1]/div[3]/div[20]/div[2]/p

//*[@id="comment"]/div/div[2]/div[1]/div[4]/div[7]/div[2]/p

//*[@id=\"comment\"]/div/div[2]/div[1]/div[4]/a[5]"
//*[@id="comment"]/div/div[2]/div[1]/div[4]/a[5]
'''
WebDriverWait(browser,30,0.2).until(
	EC.element_to_be_clickable((By.XPATH,"//*[@id=\"bilibiliPlayer\"]/div[1]/div[2]/div/div[1]/div[1]/span[1]"))
)
'''
#首次下拉
js=r"window.scrollTo(0,document.body.scrollHeight)"
browser.execute_script(js)

WebDriverWait(browser,10,0.2).until(
	EC.element_to_be_clickable((By.XPATH,"//*[@id=\"comment\"]/div/div[2]/div[1]/div[4]/div[1]/div[2]/p"))
)

#一次下拉 然后网页会展开
js=r"window.scrollTo(0,document.body.scrollHeight)"
browser.execute_script(js)
#print("Here 1")

#第二次下拉 这次才能下拉到底部
js=r"window.scrollTo(0,document.body.scrollHeight)"
browser.execute_script(js)
#print("Here 2")
'''
#找到总页数为止
while True:
	try:
		pagesnum=browser.find_element_by_xpath("//*[@id=\"comment\"]/div/div[2]/div[1]/div[2]/div[2]/a[4]").text
		break
	except:
		#下拉
		js=r"window.scrollBy(0,33)"
		browser.execute_script(js)

#每页20个评论
commentperpage=20
#获取评论页数
#pagesnum=browser.find_element_by_xpath("//*[@id=\"comment\"]/div/div[2]/div[1]/div[4]/a[4]").text
print(pagesnum)
#要查找的关键词
keyword="礼物！赶"	#我送你了一个崩坏3的3周年礼物！赶快拆开它吧！

#为死循环设定错误的弹出出口
dont=0
max=40


txtpath=__file__
txtpath=txtpath[:txtpath.rfind("\\")+1]
print("文件将保存在:",txtpath+"honkai3.txt")
f=open(txtpath+"forhonkai3.txt","w+",encoding="utf-8")

#int(pagesnum)

#在每页获取评论 如果有分享链接 就登陆进去输入uid
for page in range(int(pagesnum)):
	for commentnum in range(commentperpage):
		while dont<=max:
			try:
				comment=browser.find_element_by_xpath("//*[@id=\"comment\"]/div/div[2]/div[1]/div[4]/div["+str(commentnum+1)+"]/div[2]/p").text
				if keyword in comment:
					print("We found it.")
					print(comment)
					#找到了 输出到某个文件夹
					f.write(comment)
					f.write("\n")
				else:
					print("Not here;test")
					#print("Test;The comment is:",comment)
					pass
				dont=0
				break
			except:
				dont+=1
				print("Error Occur: Now the num is",commentnum+1)
				js=r"window.scrollBy(0,33)"
				browser.execute_script(js)
			if dont==max:
				print("无法找到评论")
				f.close()
				exit(0)
	
	#打开下一页评论 只尝试30次
	while dont<=max:
		try:
			#不同页面的下一页位置不一样 //*[@id="comment"]/div/div[2]/div[1]/div[4]/a[5]
			#nexttarget=browser.find_element_by_xpath("//button[@value='下一页']")
			target=browser.find_element_by_xpath("//*[@id=\"comment\"]/div/div[2]/div[1]/div[4]")
			nexttarget=browser.find_element_by_link_text("下一页")
			
			'''
			#将定位到的下一页拉到可视区域内
			chrome.execute_script("arguments[0].scrollIntoView(false);",nexttarget)
			'''
			dont=0
			break
		except:
			dont+=1
			#下拉
			js=r"window.scrollBy(0,233)"
			browser.execute_script(js)
		if dont==max:
			print("无法找到下一页")
			f.close()
			exit(0)
	actions=ActionChains(browser)
	actions.move_to_element(nexttarget)
	actions.click()
	actions.perform()
	
f.close()
time.sleep(5)
browser.quit()