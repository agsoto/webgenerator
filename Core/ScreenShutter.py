import glob
import os
from PIL import Image
from selenium import webdriver 
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from StyleManager.ColorManager import ColorManager
import fnmatch
import json
import time

class ScreenShutter:

	def __init__(self, full_screenshot: bool = False, window_size: tuple = (1024,768), 
		output_path:str = "./output/", input_path:str = "./output/html/", assets_path:str = "./Assets/",
		show_progress: bool = True, driver_path:str=""):
		self.full_screenshot = full_screenshot
		self.window_size = window_size
		self.input_path = input_path
		self.output_path = output_path
		self.assets_path = assets_path
		self.show_progress = show_progress
		self.driver_path = driver_path

	def take_screenshot(self, driver: WebDriver, full_page: bool = False, save_path: str = '', image_name: str = 'full_screenshot.png') -> str:
		"""
		Take full partial_screenshot of web page
		Args:
			driver: The Selenium web driver object
			save_path: The path where to store partial_screenshot
			image_name: The name of partial_screenshot image
		Returns:
			None
		"""
		total_width = driver.execute_script("return document.body.offsetWidth")
		total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
		viewport_width = driver.execute_script("return document.body.clientWidth")
		viewport_height = driver.execute_script("return window.innerHeight")
		image_name = os.path.abspath(save_path + '/' + image_name)

		if not full_page:
			driver.save_screenshot(image_name)
			return

		# Tried unsuccessfully also https://www.tutorialspoint.com/take-screenshot-of-full-page-with-selenium-python-with-chromedriver
		# and https://www.youtube.com/watch?v=u7p-HtjbZ3Y
		driver.execute_script("window.scrollTo(0, 0)")

		final_real_height = total_height
		composite_screenshot = Image.new('RGB', (total_width, final_real_height))
		y = 0
		while y < total_height:
			x = 0
			while x < total_width:
				driver.execute_script(f"window.scrollTo({x}, {y})")

				scroll_y = int(driver.execute_script("return window.scrollY"))

				partial_shot_file_name = "temp_shot.png"
				driver.save_screenshot(partial_shot_file_name)
				partial_screenshot = Image.open(partial_shot_file_name)

				offset = (x, scroll_y)

				composite_screenshot.paste(partial_screenshot, offset)
				del partial_screenshot
				os.remove(partial_shot_file_name)
				x = x + viewport_width
			y = y + viewport_height 

		composite_screenshot.save(image_name)

	def capture_and_save(self,max_shoots=100000): #TODO: Refactor, a lot of messy code
		# get a list of all the files to open
		window_width = self.window_size[0]
		window_height = self.window_size[1]
		glob_folder = os.path.join(os.getcwd(), self.input_path+'*.html')

		files_count = len(fnmatch.filter(os.listdir(self.input_path), '*.html'))

		html_file_list = glob.glob(glob_folder)
		index = 1

		options = webdriver.ChromeOptions()
		#WARNING: Changing headless to False will cause fullscrenshot to be broken
		#	this is because the screenshot takes the dimensions of the screen resolution
		options.headless = True 
		
		if self.driver_path != "":
			driver = webdriver.Chrome(options=options, executable_path=self.driver_path)
		else:
			driver = webdriver.Chrome(options=options)

		tic = time.time()
		count = 0 
		annotations = {}
		imgs_metadatas = {}
		img_id_list = []

		scripts = {"labeler":"", "prepare_shutting":"", "bridge_metadata":""}
		annotations_file_exists = os.path.isfile(self.output_path+'via_pj_settings.json')

		if annotations_file_exists:
			via_pj_file = open(self.output_path+'via_pj_settings.json', "r")
			via_pj = json.load(via_pj_file)
			with open(self.assets_path+"annotations_maker.js", "r") as f:
				scripts["labeler"] = f.read()
			
		with open(self.assets_path+"prepare_shutting.js", "r") as f:
			scripts["prepare_shutting"] = f.read()
		with open(self.assets_path+"extract_meta.js", "r") as f:
			scripts["extract_meta"] = f.read()
		for html_file in html_file_list:
			if count > max_shoots:
				break
			else:
				count += 1
				if self.show_progress:
					progress = round(count/files_count, 2)*100
					print("{0}/{1} files generated [{2}%]".format(count,files_count,progress))

			# get the name into the right format
			temp_name = "file://" + html_file

			# open in webpage
			driver.get(temp_name)
			save_name = os.path.basename(temp_name)[:-5] + '.png'       
			
			#script execution only to get palette
			driver.execute_script(scripts["extract_meta"])
			layout_type = driver.execute_script("return window.layout;")
			palette = driver.execute_script("return window.palette;")
			
			if palette is not None:
				palette = json.loads(palette)
				ColorManager.compile_color(primary=palette["primary"], secondary=palette["secondary"], light=palette["light"], 
				dark=palette["dark"], enable_gradients=palette["enable-gradients"])
				#driver.execute_script("window.location.reload();")
			
			driver.refresh()

			if not self.full_screenshot:
				driver.execute_script("window.screenshotHeight = "+str(window_height)+";")

			driver.execute_script(scripts["prepare_shutting"])

			if annotations_file_exists:
				driver.execute_script(scripts["labeler"])

			try:
				WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'page-content')))
			except TimeoutException:
				print("Loading took too much time!")

			self.take_screenshot(driver, full_page=self.full_screenshot, save_path=self.output_path+"images/", image_name=save_name)
				
			img_file_size = os.path.getsize(self.output_path+"images/"+save_name)

			json_variable = driver.execute_script("return window.annotations;")
			element_name_id = save_name+str(img_file_size) #Because VIA annotations use name+filesize
			imgs_metadatas[element_name_id] = { 
				"filename": save_name, 
				"size": img_file_size, 
				"regions": json_variable,
				"file_attributes": {
					"caption": "",
					"public_domain": "yes",
					"image_url": "",
					"layout_type": layout_type
				}
			}
			img_id_list.append(element_name_id)

			annotations[element_name_id] = json_variable

			# In case of different shots in the future
			# img = Image.open(os.getcwd(), save_name)
			# box = (1, 1, 1000, 1000)
			# area = img.crop(box)
			# area.save('cropped_image' + str(index), 'png')

		driver.quit()
		
		if annotations_file_exists:
			via_pj_file.close()

			via_pj["_via_img_metadata"] = imgs_metadatas
			via_pj["_via_image_id_list"] = img_id_list

			with open(self.output_path+'web_gen_annotations.json', 'w') as f:
				json.dump(annotations, f)

			with open(self.output_path+'via_pj_settings.json', 'w') as f:
				json.dump(via_pj, f)

		tac = time.time()
		print("Generated {0} PNG files in {1} seconds. Files are in {2}.".format(count,round(tac-tic, 1),self.output_path))