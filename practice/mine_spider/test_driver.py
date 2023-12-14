from time import sleep
from selenium import webdriver
 
driver = webdriver.Edge()
 
driver.get(r'https://www.douyin.com/video/7300081063383158068')
 
sleep(5)
# driver.close()