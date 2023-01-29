import os
from PIL import Image
from selenium import webdriver 
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from Core.Annotator import Annotator
from StyleManager.ColorManager import ColorManager
from Core.FileManager import FileManager
import json
import time

class ScreenShutter:

	def __init__(self, full_screenshot: bool = False, window_size: tuple[int, int] = (1024,768), 
		output_path:str = "./output/", input_path:str = "./output/html/", assets_path:str = "./Assets/",
		show_progress: bool = True, driver_path:str=""):
		self.full_screenshot = full_screenshot
		self.window_width: int = window_size[0]
		self.window_height: int = window_size[1]
		self.input_path = input_path
		self.output_path = output_path
		self.assets_path = assets_path
		self.show_progress = show_progress
		options = webdriver.ChromeOptions()
		#WARNING: Changing headless to False will cause fullscrenshot to be broken
		#	this is because the screenshot takes the dimensions of the screen resolution
		options.headless = True 
		
		if driver_path != "":
			self.driver = webdriver.Chrome(options=options, executable_path=driver_path)
		else:
			self.driver = webdriver.Chrome(options=options)
		self.driver.set_window_size(self.window_width, self.window_height)

	def take_screenshot(self, full_page: bool = False, save_path: str = '', image_name: str = 'full_screenshot.png'):
		"""
		Takes a screenshot of the current webpage
		Args:
			driver: The Selenium web driver object
			save_path: The path where to store partial_screenshot
			image_name: The name of partial_screenshot image
		Returns:
			None
		"""
		total_width: int = self.driver.execute_script("return document.body.offsetWidth")
		total_height: int = self.driver.execute_script("return document.body.parentNode.scrollHeight")
		viewport_width: int = self.driver.execute_script("return document.body.clientWidth")
		viewport_height: int = self.driver.execute_script("return window.innerHeight")
		image_name = os.path.abspath(save_path + '/' + image_name)

		if not full_page:
			self.driver.save_screenshot(image_name)
			return

		# Tried unsuccessfully also https://www.tutorialspoint.com/take-screenshot-of-full-page-with-selenium-python-with-chromedriver
		# and https://www.youtube.com/watch?v=u7p-HtjbZ3Y
		self.driver.execute_script("window.scrollTo(0, 0)")

		final_real_height = total_height
		composite_screenshot = Image.new('RGB', (total_width, final_real_height))
		y = 0
		while y < total_height:
			x = 0
			while x < total_width:
				self.driver.execute_script(f"window.scrollTo({x}, {y})")

				scroll_y = int(self.driver.execute_script("return window.scrollY"))

				partial_shot_file_name = "temp_shot.png"
				self.driver.save_screenshot(partial_shot_file_name)
				partial_screenshot = Image.open(partial_shot_file_name)

				offset = (x, scroll_y)

				composite_screenshot.paste(partial_screenshot, offset)
				del partial_screenshot
				os.remove(partial_shot_file_name)
				x = x + viewport_width
			y = y + viewport_height 

		composite_screenshot.save(image_name)

	def capture_and_save(self,annotate:bool=True, max_shoots:int=100000): #TODO: Refactor, a lot of messy code
		files_count = FileManager.count_html_files(self.input_path)
		html_files_paths = FileManager.get_html_paths_list(self.input_path)
		annotator = None
		tic, count = time.time(), 0

		scripts = {"annotations_maker":"", "prepare_shutting":"", "extract_meta":""}
		FileManager.load_scripts(scripts, self.assets_path)

		if annotate:
			annotator = Annotator(self.assets_path, self.output_path)
			
		for html_file_path in html_files_paths:
			if count > max_shoots:
				break
			else:
				count += 1
				if self.show_progress:
					progress = round(count/files_count, 2)*100
					print("{0}/{1} files generated [{2}%]".format(count,files_count,progress))

			self.driver.get("file://"+html_file_path)
			image_name = os.path.basename(html_file_path)[:-5] + '.png'
			
			self.driver.execute_script(scripts["extract_meta"])
			
			palette = self.driver.execute_script("return window.palette;")
			self.apply_color_palette(palette)

			if not self.full_screenshot:
				self.driver.execute_script("window.screenshotHeight = "+str(self.window_height)+";")

			self.driver.execute_script(scripts["prepare_shutting"])
			self.driver.execute_script(scripts["annotations_maker"])

			try:
				WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.ID, 'page-content')))
			except TimeoutException:
				print("Loading took too much time!")

			self.take_screenshot(full_page=self.full_screenshot, save_path=self.output_path+"images/", image_name=image_name)
			if annotate and annotator:	
				img_file_size = os.path.getsize(self.output_path+"images/"+image_name)
				layout_type = self.driver.execute_script("return window.layout;")
				json_annotation = self.driver.execute_script("return window.annotations;")
				annotator.add_annotation(image_name, img_file_size, json_annotation, layout_type)

		tac = time.time()
		print("Generated {0} PNG files in {1} seconds. Files are in {2}.".format(count,round(tac-tic, 1),self.output_path))

	def apply_color_palette(self, palette: str):
		if palette is not None:
			palette = json.loads(palette)
			ColorManager.compile_color(primary=palette["primary"], secondary=palette["secondary"], light=palette["light"], 
						dark=palette["dark"], enable_gradients=palette["enable-gradients"])
			self.driver.refresh()

	def __del__(self) -> None:
		self.driver.quit()