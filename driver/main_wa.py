# coding: utf-8
import os, socket, xlrd, time, datetime, sys
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from random import randint
import pandas as pd
from openpyxl import load_workbook
import pkg_resources as res




texto = input("Digite a mensagem que deseja enviar.\nAo terminar, pressione a tecla ENTER.\n\n")
vec_text = texto.split("+")
os.system('CLS')



def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except :
        is_connected()

usuario = os.getenv('username')
path = '--user-data-dir=C:\\Users\\'+usuario+'\\AppData\\Local\\Google\\Chrome\\User Data\\'

options = webdriver.ChromeOptions()
options.add_argument(path)
options.add_argument('--profile-directory=Default')
driver = webdriver.Chrome(executable_path='./driver/chromedriver.exe', options=options)
driver.get("http://web.whatsapp.com")
sleep(20)

def send_whatsapp_msg(phone_no,text):
    driver.get("https://web.whatsapp.com/send?phone={}&source=&data=#".format(phone_no))
    sleep(10)

    time.sleep(5)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,'//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')))
    txt_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    global no_of_message

    for x in text:
        txt_box.send_keys(x)
        ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()

    time.sleep(randint(1,4))
    txt_box.send_keys('\n')


for mobile_no in mobile_no_list:
    try:
        send_whatsapp_msg(mobile_no,vec_text)
    except Exception as e:
        is_connected()


driver.close()
driver.quit()


mobile_no = ['5512982494455']


for mobile_no in mobile_no_list:
    try:
        send_whatsapp_msg(mobile_no,vec_links)
    except Exception as e:
        is_connected()