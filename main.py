# Program to get and adjust links from an Youtube playlist. After links had prepared, program will sends
# to a specific contact/group trough WhatsApp  Web.
# Author: Fumachi, E. F.
# effumachi@gmail.com
# Version: 3.141.5
# Free for Non-Commercial use.
import time, os, sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class ytPlaylist():


	def __init__(self):
		self.user = os.getenv('username')


	def mkdir(self, name_dir):
		self.name_dir = name_dir
		try:
			os.mkdir(self.name_dir)
		except OSError:
			print(f"ATENTION: {self.name_dir} exist!")
		else:
			print(f"SUCCESS: {self.name_dir} created!")


	def create_file(self):
		today_date = datetime.now().strftime('%Y%m%d_%H%M%S')
		self.name_file = today_date+'.txt'
		with open('./'+self.name_dir+'/'+self.name_file, 'a') as file:
			file.write(today_date+'\n')
			file.close()


	def prepareLink(self):
		try:
			sys.argv[1]
			URL = sys.argv[1]
		except IndexError:
			URL = input('Enter Youtube Playlist Link: ')
		address = URL.split('?')
		first = address[0].split('/')

		if first[3] == 'playlist':
			self.url = URL
		else:
			self.url = 'https://www.youtube.com/playlist?'+address[1]


	def options(self, name_chrome):
		self.name_chrome = name_chrome
		options = webdriver.ChromeOptions()
		options.add_argument(f'--user-data-dir=C:\\Users\\{self.user}\\AppData\\Local\\Google\\Chrome\\User Data\\')
		options.add_argument(f'--profile-directory={self.name_chrome}')
		self.driver = webdriver.Chrome(executable_path=r'./driver/chromedriver.exe',options=options)


	def numberVideos(self):
		self.driver.get(str(self.url))
		time.sleep(5)
		videos = self.driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-playlist-sidebar-renderer/div/ytd-playlist-sidebar-primary-info-renderer/div[1]/yt-formatted-string[1]/span[1]')
		self.num_videos = int(videos.text)
		yday = self.driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-playlist-sidebar-renderer/div/ytd-playlist-sidebar-primary-info-renderer/h1/yt-formatted-string/a')
		self.yesterday = '*LINKS - '+yday.text+'*'


	def vec_links(self):
		self.vec_links = []
		for i in range(1,self.num_videos+1):
		   	a = self.driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-playlist-video-list-renderer/div[3]/ytd-playlist-video-renderer[%s]/div[2]/a" %i)
		   	self.driver.execute_script("arguments[0].scrollIntoView();",a)
		   	link = a.get_attribute('href').split("&")
		   	self.vec_links.append(link[0])
		   	with open('./'+self.name_dir+'/'+self.name_file, 'a') as file:
		   		file.write(link[0]+'\n')
		   		file.close()


	def sendWA(self):
		try:
			sys.argv[2]
			self.group = []
			self.group.append(sys.argv[2])
		except IndexError:
			# self.group is a list with name and/or number to send yt playlist links
			# if will use number MUST BE in country format, ie, for brazilian numbers +55 DDD 99999-9999
			self.group = ['group name of whatsapp','+55 11 9xxxx-xxxx']
		self.driver.get('https://web.whatsapp.com')
		time.sleep(20)
		for gr in self.group:
			search = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/div[1]/div/label/div/div[2]')
			time.sleep(2)
			search.click()
			search.send_keys(gr)
			time.sleep(3)
			search.send_keys(Keys.RETURN)
			text_box = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]')
			time.sleep(1)
			text_box.click()
			text_box.send_keys(self.yesterday)
			text_box.send_keys(Keys.RETURN)
			for j in self.vec_links:
				text_box.send_keys(j)
				time.sleep(1)
				ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).perform()
				time.sleep(10)
				text_box.send_keys(Keys.RETURN)
			text_box.send_keys('*END*')
			text_box.send_keys(Keys.RETURN)


	def driverClose(self):
		time.sleep(4)
		self.driver.close()


w = ytPlaylist()
w.mkdir('LINKS_ENVIADOS')	# LINKS_ENVIADOS is the name folder that you want to create
w.create_file()
w.prepareLink()
w.options('F')
w.numberVideos()
w.vec_links()
w.sendWA()
w.driverClose()
