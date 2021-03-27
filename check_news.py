from chromedriver_autoinstaller import install as chrome_install
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from colorama import Fore, init as colorama_init
from os.path import dirname, realpath
from time import sleep
import utils

INTERVAL	=	30 # minutes
USER_DATA_DIR			=	r"D:/Selenium/User Data" 
PROFILE_DIRECTORY	=	r"Profile 2"
FILE_DIRECTORY		=	dirname(realpath(__file__))
S = "|^.#@"

SOURCES = {
	"Papers"	:	[rf"{FILE_DIRECTORY}\Papers"	, "https://paperswithcode.com/latest"],
	"Mails"		:	[rf"{FILE_DIRECTORY}\Mails"		, "https://outlook.live.com/mail/0/inbox"],
	"Videos"	:	[rf"{FILE_DIRECTORY}\Videos"	, "https://www.youtube.com/feed/subscriptions"],
	"Articles":	[rf"{FILE_DIRECTORY}\Articles", "https://towardsdatascience.com"]
	}

def check_for_new_papers(source):
	def scrape():
		N = 8
		papers = []
		for i in range(1, N+1):
			TITLE 			= f"/html/body/div[3]/div[2]/div[{i}]/div[2]/div/div[1]/h1/a"
			DESCRIPTION	= f"/html/body/div[3]/div[2]/div[{i}]/div[2]/div/div[1]/p[2]"
			LINK 				= f"/html/body/div[3]/div[2]/div[{i}]/div[1]/a"
			try:
				sel_title 			= driver.find_element_by_xpath(TITLE)
				sel_description	=	driver.find_element_by_xpath(DESCRIPTION)
				sel_link				= driver.find_element_by_xpath(LINK)
				
				title = sel_title.text
				title = title.encode(encoding = 'ascii', errors = 'replace') 
				title = title.decode('UTF-8').replace('\n', '')
				
				description = sel_description.text
				description = description.encode(encoding = 'ascii', errors = 'replace') 
				description = description.decode('UTF-8').replace('\n', '')
				
				link = sel_link.get_attribute('href')
				
				papers.append([title, description, link])
			except:
				print(utils.colored(f"Something went wrong '{i}'", Fore.RED))
				continue
		return papers
	
	directory, link = SOURCES[source] 
	with utils.wait_for_page_load(driver):
		driver.get(link)
	
	papers = scrape()

	latest = utils.get_latest_data(directory)
	utils.delete_folder_contents(directory)
	filename = utils.generate_file_name()
	
	with open(rf"{directory}\{filename}.txt", 'w', encoding="utf-8", errors='ignore') as file:
		for paper in papers:
			t, d, l = paper
			file.write(f"{t}{S}{d}{S}{l}\n")

	if latest is not None:
		for idx, paper in enumerate(papers):
			t, d, l = paper
			for line in latest:
				tl = line.split(S)[0]
				if t == tl:
					break
			else:
				print(f"{'-'*90}")
				print(f"|{utils.colored(idx+1, Fore.CYAN)}| {t}\n {d}")

def check_for_new_mails(source):
	def scrape():
		N = 8
		mails = []
		for i in range(1, N+1):
			MAIL = f"/html/body/div[2]/div/div[2]/div[1]/div[1]/div/div/div[3]/div[2]/div/div[1]/div[2]/div/div/div/div/div/div[{i}]"
			try:
				sel_mail = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, MAIL)))
				
				mail = sel_mail.text.split('\n')
				sender = mail[1]
				subject = mail[2]
				info = mail[3]
				
				mails.append([sender, subject, info])
			except:
				print(utils.colored(f"Something went wrong '{i}'", Fore.RED))
				print(f"The thing: {mail}")
				continue
		return mails
		
	directory, link = SOURCES[source] 
	driver.get(link) # cant wait_for_page_load here
	
	mails = scrape()

	latest = utils.get_latest_data(directory)
	utils.delete_folder_contents(directory)
	filename = utils.generate_file_name()
	
	with open(rf"{directory}\{filename}.txt", 'w', encoding="utf-8", errors='ignore') as file:
		for mail in mails:
				sender, subject = mail[:-1]
				file.write(f"{sender}{S}{subject}\n")

	if latest is not None:
		for mail in mails:
			sender, subject, info = mail
			for line in latest:
				su = line.split(S)[1].strip()
				if su == subject:
					break
			else:
				print(f"{'-'*90}")
				print(f"{sender}:\n {subject}\n    {info}")

def check_for_new_videos(source):
	def scrape():
		TODAY = '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[1]/div[3]/ytd-shelf-renderer/div[1]/div[2]/ytd-grid-renderer/div[1]'
		v_idx, videos = 1, []
		while True:
			TITLE	= TODAY + rf'/ytd-grid-video-renderer[{v_idx}]/div[1]/div[1]/div[1]/h3/a'
			CHANNEL	= TODAY + rf'/ytd-grid-video-renderer[{v_idx}]/div[1]/div[1]/div[1]/div/div[1]/div[1]/ytd-channel-name/div/div/yt-formatted-string/a'
			LINK	= TODAY + rf'/ytd-grid-video-renderer[{v_idx}]/div[1]/ytd-thumbnail/a'
			try:
				sel_title	= driver.find_element_by_xpath(TITLE)
				sel_channel = driver.find_element_by_xpath(CHANNEL)
				sel_link = driver.find_element_by_xpath(LINK)
				
				title = sel_title.text
				channel = sel_channel.text			
				link = sel_link.get_attribute('href')
				
				videos.append([title, channel, link])
				v_idx += 1
			except:
				print(f"{v_idx}")
				break
		return videos
	
	directory, link = SOURCES[source] 
	with utils.wait_for_page_load(driver):
		driver.get(link)

	videos = scrape()

	latest = utils.get_latest_data(directory)
	utils.delete_folder_contents(directory)
	filename = utils.generate_file_name()
	
	with open(rf"{directory}\{filename}.txt", 'w', encoding="utf-8", errors='ignore') as file:
		for video in videos:
			t, c, l = video
			file.write(f"{t}{S}{c}{S}{l}\n")

	if latest is not None:
		for idx, video in enumerate(videos):
			t, c, l = video
			for line in latest:
				tl = line.split(S)[0]
				if t == tl:
					break
			else:
				print(f"{'-'*90}")
				print(f"|||{c.upper()}\n|{utils.colored(idx+1, Fore.CYAN)}|\n|||{t}")

def check_for_new_articles(source):
	def scrape():
		N = 8
		ARTICLES = '/html/body/div[1]/div/div[3]/div[2]/div/div[2]/div'
		articles = []
		for i in range(1, N+1):
			TITLE 				= ARTICLES + f'/div[{i}]/div/div/div/div[1]/div[2]/div/section/div[1]/h1/a'			
			DESCRIPTION 	= ARTICLES + f'/div[{i}]/div/div/div/div[1]/div[2]/div/section/div[2]/h2'
			LINK					=	ARTICLES + f'/div[{i}]/div/div/div/div[2]/a'
			if i == 1: #...
				TITLE 			= ARTICLES + f'/div[{i}]/div/div/div/div/div[1]/div[2]/div/section/div[1]/h1/a'
				DESCRIPTION = ARTICLES + f'/div[{i}]/div/div/div/div/div[1]/div[2]/div/section/div[2]/h2'
				LINK				=	ARTICLES + f'/div[{i}]/div/div/div/div/div[2]/a'
			try:
				sel_title = driver.find_element_by_xpath(TITLE)
				sel_description = driver.find_element_by_xpath(DESCRIPTION)
				sel_link = driver.find_element_by_xpath(LINK)
				
				title = sel_title.text
				title = title.encode(encoding = 'ascii', errors = 'replace') 
				title = title.decode('UTF-8').replace('\n', '')
				
				description = sel_description.text
				description = description.encode(encoding = 'ascii', errors = 'replace') 
				description = description.decode('UTF-8').replace('\n', '')
				
				link = sel_link.get_attribute('href')
				
				articles.append([title, description, link])
			except:
				print(utils.colored(f"Something went wrong '{i}'", Fore.RED))
				continue
		return articles

	directory, link = SOURCES[source] 
	with utils.wait_for_page_load(driver):
		driver.get(link)
	
	articles = scrape()

	latest = utils.get_latest_data(directory)
	utils.delete_folder_contents(directory)
	filename = utils.generate_file_name()
	
	with open(rf"{directory}\{filename}.txt", 'w', encoding="utf-8", errors='ignore') as file:
		for article in articles:
			t, d, l = article
			file.write(f"{t}{S}{d}{S}{l}\n")

	if latest is not None:
		for article in articles:
			t, d, l = article
			for line in latest:
				tl = line.split(S)[0]
				if t == tl:
					break
			else:
				print(f"{'-'*90}")
				print(f"{t}\n{d}")

def check():
	for source in SOURCES.keys():
		print(utils.colored(f"{source.upper()}", Fore.MAGENTA))
		globals()[f'check_for_new_{source.lower()}'](source)
		print(f"{'-'*90}")

if __name__=="__main__":
	colorama_init()
	chrome_install()
	preferences = Options()
	#preferences.add_argument("--headless")
	#preferences.add_argument("--disable-gpu")
	preferences.add_argument(f"--user-data-dir={USER_DATA_DIR}")
	preferences.add_argument(f"--profile-directory={PROFILE_DIRECTORY}")
	driver = webdriver.Chrome(options = preferences)
	driver.minimize_window()
	print(f"{'-'*90}\n{'-'*90}")

	while True:
		check()
		print(f"\nwaitin for {INTERVAL} minutes")
		sleep(INTERVAL * 60)
