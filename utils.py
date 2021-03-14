from colorama import Style
import time, os
from datetime import date
#BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE

#
def colored(w, c):
	return c + str(w) + Style.RESET_ALL
#
class wait_for_page_load(object):
	def __init__(self, browser):
		self.browser = browser
	def __enter__(self):
		self.old_page = self.browser.find_element_by_tag_name('html')
	def page_has_loaded(self):
		new_page = self.browser.find_element_by_tag_name('html')
		return new_page.id != self.old_page.id
	def __exit__(self, *_):
		self.wait_for(condition_function = self.page_has_loaded)
	def wait_for(self, condition_function):
		start_time = time.time()
		while start_time > time.time() - 3:
			if condition_function():
				return True
			else:
				print("Site not ready...")
				time.sleep(0.25)
		return False
#
def generate_file_name():
	current_date = str(date.today())
	current_date = current_date.replace('-','_')
	current_time = str(time.strftime("%H:%M:%S", time.localtime()))
	current_time = current_time.replace(':','_')
	filename = f"{current_date}__{current_time}"
	return filename
#
def delete_folder_contents(folder):
	for f in os.listdir(folder):
		file_path = os.path.join(folder, f)
		os.remove(file_path)
#
def get_latest_data(folder):
	latest = None
	for file in os.listdir(folder):
		file_path = os.path.join(folder, file)
		with open(file_path, 'r', encoding="utf-8") as f:
			latest = f.readlines()
	return latest
#