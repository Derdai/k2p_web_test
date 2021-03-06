# -*- coding: UTF-8 -*-
#!/usr/bin/env python
############################################################
#
# FILE NAME  :   adaptor.py
# VERSION    :   1.0
# DESCRIPTION:   接口函数
# AUTHOR     :   LiuLu <lu.liu@phicomm.com>
# CREATE DATE:   04/06/2017
#
##############################################################
from selenium import webdriver
import os, sys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import log

import functools
driver = webdriver.Chrome()
#driver = webdriver.Firefox()
networkRestartTime = 120
rebootTime = 120

def exceptCheck(fun):
	@functools.wraps(fun)
	def wrapper(*args):
		f = sys._getframe()
		funcName = f.f_back.f_code.co_name
		try:
			fun(*args)
		except Exception as e:
			exceptionsName = str(e.__class__)
			exceptionsName = exceptionsName.split('.')[-1]
			exceptionsName = exceptionsName.split("'")[-2]
			print('**Error**:funcName:%s, %s, %s'%(funcName, exceptionsName, args[0]))
			log.writewebErrToLog(funcName, exceptionsName, args[0])
	return wrapper

@exceptCheck
def waitandClick(xpath):
	WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
	driver.find_element_by_xpath(xpath).click()

@exceptCheck
def waitandSendkeys(xpath, keys):
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
	driver.find_element_by_xpath(xpath).clear()
	driver.find_element_by_xpath(xpath).send_keys(keys)

@exceptCheck
def alwaysOpenSwitch(xpath, switchValue='data-value'):
	WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
	button = driver.find_element_by_xpath(xpath)
	if button.get_attribute(switchValue) == '0':
		button.click()
		waitforDisappear('//*[@id="Pop"]')

@exceptCheck
def alwaysCloseSwitch(xpath, switchValue='data-value'):
	WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
	button = driver.find_element_by_xpath(xpath)
	if button.get_attribute(switchValue) == '1':
		button.click()

@exceptCheck
def waitforDisappear(xpath):
	time.sleep(1)
	process = driver.find_element_by_xpath(xpath)
	WebDriverWait(driver, 20).until_not(lambda driver: process.is_displayed())

@exceptCheck
def waitforDisplay(xpath):
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
	process = driver.find_element_by_xpath(xpath)
	WebDriverWait(driver, 20).until(lambda driver: process.is_displayed())


def openDriver():
	driver.get("http://p.to")
	driver.maximize_window()

def closeDriver():
	#time.sleep(15) 
	time.sleep(3)
	driver.quit()
	#os.system('killall chromedriver')
	#os.system('killall geckodriver')

def refresh():
	driver.refresh()

def elementIsDisplayed(xpath):
	try:
		driver.find_element_by_xpath(xpath)
	except NoSuchElementException as e:
		return False
	return True

def clickApp():
	time.sleep(1)
	waitforDisplay('//*[@id="Con"]/div[1]/ul[1]/a[4]/li')
	waitandClick('//*[@id="Con"]/div[1]/ul[1]/a[4]/li')
	waitforDisplay('//*[@id="Content"]')
	time.sleep(1)

def srcollAction(site):
	scrollTop = '0'
	if site == 'top':
		scrollTop = '0'
	elif site == 'bottom':
		scrollTop = '10000'
	driver.execute_script("var q = document.getElementById('Content').scrollTop=%s" % scrollTop)
#判断data是否在表格中，在就返回行号，否则返回0
def getElementInTable(tableXpath, baseXpath, arrData):
	table = driver.find_element_by_xpath(tableXpath)
	#table的总行数，包含标题
	table_rows = len(table.find_elements_by_tag_name('tr'))
	#tabler的总列数
	table_cols = len(arrData) - 1
	flag = False
	for row in range(2,table_rows + 1):
		for col in xrange(1,table_cols + 1):
			xpath = '%s/tr[%d]/td[%d]' %(baseXpath, row, col)
			if arrData[col] == driver.find_element_by_xpath(xpath).text:
				if col == table_cols:
					flag = True
			else:
				break
		if flag == True:
			return row
	log.writeInfo('no such line:')
	for key in arrData:
		log.writeInfo('\t%s = %s\n' % (key, data[key]))
	return 0

def getText(xpath):
	if not elementIsDisplayed(xpath):
		return False
	else:
		return driver.find_element_by_xpath(xpath).text

if __name__ == '__main__':
	openDriver()
	waitandClick('dhlahal')





