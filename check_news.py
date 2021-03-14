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

USER_DATA_DIR		=	r"D:/Selenium/User Data" 
PROFILE_DIRECTORY	=	r"Profile 2"

FILE_DIRECTORY		=	dirname(realpath(__file__))
SOURCES = {
	"Papers"	:	[rf"{FILE_DIRECTORY}\Papers"	, "https://paperswithcode.com/latest"],
	"Mails"		:	[rf"{FILE_DIRECTORY}\Mails"		, "https://outlook.live.com/mail/0/inbox"],
	"Videos"	:	[rf"{FILE_DIRECTORY}\Videos"	, "https://www.youtube.com/feed/subscriptions"],
	"Articles"	:	[rf"{FILE_DIRECTORY}\Articles"	, "https://towardsdatascience.com"]
	}

def check_for_new_papers(source):	
	N = 8
	directory, link = SOURCES[source] 
	with utils.wait_for_page_load(driver):
		driver.get(link)
	
	papers = []
	for i in range(1, N+1):
		TITLE 			= f"/html/body/div[3]/div[2]/div[{i}]/div[2]/div/div[1]/h1/a"
		DESCRIPTION	= f"/html/body/div[3]/div[2]/div[{i}]/div[2]/div/div[1]/p[2]"
		try:
			sel_title 		= driver.find_element_by_xpath(TITLE)
			sel_description	=	driver.find_element_by_xpath(DESCRIPTION)
			papers.append([sel_title.text, sel_description.text])
		except:
			print(utils.colored(f"Something went wrong '{i}'", Fore.RED))
			continue

	latest = utils.get_latest_data(directory)
	utils.delete_folder_contents(directory)

	filename = utils.generate_file_name()
	with open(rf"{directory}\{filename}.txt", 'w', encoding="utf-8", errors='ignore') as file:
		for paper in papers:
			file.write("%s|^.#@%s\n" % (paper[0], paper[1]))

	if latest is not None:
		for paper in papers:
			t, d = paper
			for line in latest:
				tl = line.split("|^.#@")[0]
				if t == tl:
					break
			else:
				print(f"{'-'*90}")
				print(f"{t}\n{d}")

def check_for_new_mails(source):
	N = 8
	directory, link = SOURCES[source] 
	driver.get(link) # cant wait_for_page_load here
	
	mails = []
	for i in range(1, N+1):
		MAIL = f"/html/body/div[2]/div/div[2]/div[1]/div[1]/div/div/div[3]/div[2]/div/div[1]/div[2]/div/div/div/div/div/div[{i}]"
		try:
			sel_sender = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, MAIL)))
			mails.append(sel_sender.text.split('\n'))
		except:
			print(utils.colored(f"Something went wrong '{i}'", Fore.RED))
			break

	latest = utils.get_latest_data(directory)
	utils.delete_folder_contents(directory)

	filename = utils.generate_file_name()
	with open(rf"{directory}\{filename}.txt", 'w', encoding="utf-8", errors='ignore') as file:
		for mail in mails:
			if len(mail) > 3:
				file.write("%s|^.#@%s\n" % (mail[1], mail[2]))

	if latest is not None:
		for mail in mails:
			if len(mail) > 3:
				sender, subject = mail[1], mail[2]
				for line in latest:
					tl = line.split("|^.#@")[1]
					if subject == tl.strip():
						break
				else:
					print(f"{'-'*90}")
					print(f" {sender}: {subject}")

def check_for_new_videos(source):
	TODAY = '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[1]/div[3]/ytd-shelf-renderer/div[1]/div[2]/ytd-grid-renderer/div[1]'
	directory, link = SOURCES[source] 
	with utils.wait_for_page_load(driver):
		driver.get(link)

	v_idx, videos = 1, []
	while True:
		TITLE	= TODAY + f'/ytd-grid-video-renderer[{v_idx}]/div[1]/div[1]/div[1]/h3/a'
		CHANNEL	= TODAY + f'/ytd-grid-video-renderer[{v_idx}]/div[1]/div[1]/div[1]/div/div[1]/div[1]/ytd-channel-name/div/div/yt-formatted-string/a'
		LINK	= TODAY + f'/ytd-grid-video-renderer[{v_idx}]/div[1]/ytd-thumbnail/a'
		try:
			sel_title	= driver.find_element_by_xpath(TITLE)
			sel_channel = driver.find_element_by_xpath(CHANNEL)
			sel_link = driver.find_element_by_xpath(LINK)
			videos.append([sel_title.text, sel_channel.text, sel_link.get_attribute('href')])
			v_idx += 1
		except:
			# TODO: print(utils.colored(f"Something went wrong '{i}'", Fore.RED))
			break

	latest = utils.get_latest_data(directory)
	utils.delete_folder_contents(directory)

	filename = utils.generate_file_name()
	with open(rf"{directory}\{filename}.txt", 'w', encoding="utf-8", errors='ignore') as file:
		for video in videos:
			file.write("%s|^.#@%s|^.#@%s\n" % (video[0], video[1], video[2]))

	if latest is not None:
		for idx, video in enumerate(videos):
			t, c, l = video
			for line in latest:
				tl = line.split("|^.#@")[0]
				if t == tl:
					break
			else:
				print(f"{'-'*90}")
				print(f"|||{c.upper()}\n|{utils.colored(idx+1, Fore.CYAN)}|\n|||{t}")

def check_for_new_articles(source):
	N = 8
	ARTICLES = '/html/body/div[1]/div/div[3]/div[2]/div/div[2]/div'
	directory, link = SOURCES[source] 
	with utils.wait_for_page_load(driver):
		driver.get(link)
	
	articles = []
	for i in range(1, N+1):
		TITLE 			= ARTICLES + f'/div[{i}]/div/div/div/div[1]/div[2]/div/section/div[1]/h1/a'
		DESCRIPTION 	= ARTICLES + f'/div[{i}]/div/div/div/div[1]/div[2]/div/section/div[2]/h2'
		if i == 1: #...
			TITLE 		= ARTICLES + f'/div[{i}]/div/div/div/div/div[1]/div[2]/div/section/div[1]/h1/a'
			DESCRIPTION = ARTICLES + f'/div[{i}]/div/div/div/div/div[1]/div[2]/div/section/div[2]/h2'
		try:
			sel_title = driver.find_element_by_xpath(TITLE)
			sel_description = driver.find_element_by_xpath(DESCRIPTION)
			articles.append([sel_title.text, sel_description.text])
		except:
			print(utils.colored(f"Something went wrong '{i}'", Fore.RED))
			continue

	latest = utils.get_latest_data(directory)
	utils.delete_folder_contents(directory)

	filename = utils.generate_file_name()
	with open(rf"{directory}\{filename}.txt", 'w', encoding="utf-8", errors='ignore') as file:
		for article in articles:
			file.write("%s|^.#@%s\n" % (article[0], article[1]))

	if latest is not None:
		for article in articles:
			t, d = article
			for line in latest:
				tl = line.split("|^.#@")[0]
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