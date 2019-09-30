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
import re
import os

#为死循环设定错误的弹出次数
dont=0
max=15

def myprecious(sourcefile,uid="35317399"):
	global dont
	global max
	flag=0
	f=open(sourcefile,"r",encoding="utf-8")
	#读取每一行
	for line in f:
		if "https://" in line:
			src=re.findall(r"http.*share",line)
			print(src)
			
			if flag==0:
				browser=webdriver.Chrome()
				browser.get(src[0])
				flag+=1
			else:
				js="window.open(arguments[0])"
				browser.execute_script(js,src[0])
				
				handles=browser.window_handles
				handletotal=len(handles)
				#print(handles)
				#print(handletotal)
				browser.switch_to.window(handles[handletotal-1])
				
			
			WebDriverWait(browser,30,0.2).until(
				EC.element_to_be_clickable((By.XPATH,"//*[@id=\"frame\"]/div/input"))
			)
			#点击输入框 输入uid 并拆开礼物
			target=browser.find_element_by_xpath("//*[@id=\"frame\"]/div/input")
			actions=ActionChains(browser)
			actions.move_to_element(target)
			actions.click()
			actions.send_keys(uid)
			actions.perform()
			
			time.sleep(0.1)
			
			nexttarget=browser.find_element_by_xpath("//*[@id=\"frame\"]/div/img[2]")
			actions=ActionChains(browser)
			actions.move_to_element(nexttarget)
			actions.click()
			actions.perform()
			
			#返回获得的奖励
			while True:
				try:
					award=browser.find_element_by_xpath("//*[@id=\"frame\"]/div/div[5]/div/div[1]/div[2]").text
					print(award)
					dont=0
					break
				except:
					dont+=1
					#print(dont)
					if dont==max:
						print("这个似乎被领取过了")
						dont=0
						break
		
		if flag==1:	#因为刚才已经加了1了
			print("Here!")
			flag+=1
		elif flag==2:
			handles=browser.window_handles
			if len(handles)>1:
				browser.close()
			handles=browser.window_handles
			browser.switch_to.window(handles[0])
	
	print("已经都领完啦！三周年快乐！")
	
	f.close()
	browser.quit()
'''
//*[@id="frame"]/div/input

//*[@id="frame"]/div/img[2]

//*[@id="frame"]/div/div[5]/div/div[1]/div[2]

'''


if __name__=="__main__":

	uid=input("请输入你的uid:")

	path=__file__
	path=path[:-10]
	print(path)
	
	if not os.path.exists(path+"forhonkai3.txt"):
		txtpath=input("请输入forhonkai.txt所在文件名:")
		txtpath+="\\forhonkai3.txt"
	else:
		txtpath=path+"forhonkai3.txt"
		
	myprecious(txtpath,uid)