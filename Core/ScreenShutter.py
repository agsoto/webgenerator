import os
import json
import time
from PIL import Image
from selenium import webdriver 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from Core.Annotator import Annotator
from StyleManager.ColorManager import ColorManager
from Core.FileManager import FileManager

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

	def get_window_page_properties(self) -> tuple[int, int, int, int]:
		script = '''
			return { "page_width": document.body.offsetWidth, 
					"page_height": document.body.parentNode.scrollHeight,
					"viewport_width": document.body.clientWidth,
					"viewport_height": window.innerHeight
			};
		'''
		page_properties: dict = self.driver.execute_script(script)

		return page_properties["page_width"], page_properties["page_height"], page_properties["viewport_width"], page_properties["viewport_height"]

	def take_screenshot(self, full_page: bool = False, save_path: str = '', image_name: str = 'full_screenshot.png'):
		"""
			Takes a screenshot of the current webpage. Fullpage shutting is made scrolling down
			the page, taking multiple screenshots and merging the images.
		Args:
			full_page: Determines if the screenshot is taken with the total height of the page
			save_path: The path where to store partial_screenshot
			image_name: The name of partial_screenshot image
		Returns:
			None
		"""
		def create_new_blank_canvas(page_width, page_height):
			return Image.new('RGB', (page_width, page_height))

		def get_current_scroll():
			return int(self.driver.execute_script("return window.scrollY"))

		def scroll_to(y, x):
			self.driver.execute_script(f"window.scrollTo({x}, {y})")

		def append_temp_shot(composite_screenshot):
			temp_partial_shot_file_name = "temp_partial_shot.png"
			self.driver.save_screenshot(temp_partial_shot_file_name)
			temp_partial_shot = Image.open(temp_partial_shot_file_name)
			composite_screenshot.paste(temp_partial_shot, offset)
			del temp_partial_shot
			os.remove(temp_partial_shot_file_name)

		page_width, page_height, viewport_width, viewport_height = self.get_window_page_properties()
		new_image_full_path = os.path.abspath(save_path + '/' + image_name)

		if not full_page:
			self.driver.save_screenshot(new_image_full_path)
			return 

		# For the full page screenshot we tried unsuccessfully: https://www.tutorialspoint.com/take-screenshot-of-full-page-with-selenium-python-with-chromedriver
		#  and https://www.youtube.com/watch?v=u7p-HtjbZ3Y
		scroll_to(0, 0) 

		composite_screenshot = create_new_blank_canvas(page_width, page_height)
		y = 0
		while y < page_height:
			x = 0
			while x < page_width:
				scroll_to(y, x)
				scroll_y = get_current_scroll()
				offset = (x, scroll_y)
				append_temp_shot(composite_screenshot)
				x = x + viewport_width
			y = y + viewport_height 

		composite_screenshot.save(new_image_full_path)

	def capture_and_save(self, annotate:bool=True, max_shoots:int=100000): 

		def get_webpage_metadata():
			webpage_metadata = self.driver.execute_script('return { "palette": window.palette, "layout_type": window.layout }')
			return webpage_metadata["layout_type"], webpage_metadata["palette"] 

		def set_max_height_for_javascript_annotator(max_height):
			self.driver.execute_script("window.screenshotHeight = "+str(max_height)+";")

		def wait_for_page_content(seconds=3, page_content_id='page-content'):
			try:
				WebDriverWait(self.driver, seconds).until(EC.presence_of_element_located((By.ID, page_content_id)))
			except TimeoutException:
				print("Loading took too much time!")

		def execute_scripts_on_browser(scripts):
			for script in scripts.values():
				self.driver.execute_script(script)

		def load_html_file_on_browser(html_file_path):
			self.driver.get("file://"+html_file_path)

		def get_current_screenshot_file_name(html_file_path):
			return os.path.basename(html_file_path)[:-5] + '.png'

		def get_json_annotations():
			return self.driver.execute_script("return window.annotations;")

		files_count = FileManager.count_html_files(self.input_path)
		html_files_paths = FileManager.get_html_paths_list(self.input_path)
		annotator = None
		tic, count = time.time(), 0

		scripts = {"annotations_maker":"", "prepare_shutting":"", "extract_meta":""}
		FileManager.read_scripts_from_js_files(scripts, self.assets_path)
		
		if annotate:
			annotator = Annotator(self.assets_path, self.output_path)
			
		for html_file_path in html_files_paths:
			if count > max_shoots: break
			count += 1

			if self.show_progress: 
				print(f"{count}/{files_count} screenshots generated [{round(count/files_count, 2)*100}%]")

			load_html_file_on_browser(html_file_path)

			if not self.full_screenshot:
				set_max_height_for_javascript_annotator(self.window_height)

			self.driver.execute_script(scripts["extract_meta"])
			layout_type, palette = get_webpage_metadata()

			self.compile_css_color_palette(palette)
			self.driver.refresh()

			wait_for_page_content()
			self.driver.execute_script(scripts["prepare_shutting"])
			self.driver.execute_script(scripts["annotations_maker"])

			screenshot_file_name = get_current_screenshot_file_name(html_file_path)
			self.take_screenshot(full_page=self.full_screenshot, save_path=self.output_path+"images/", image_name=screenshot_file_name)
			if annotate and annotator:
				img_file_size = os.path.getsize(self.output_path+"images/"+screenshot_file_name)
				json_annotations = get_json_annotations()
				annotator.add_annotation(screenshot_file_name, img_file_size, json_annotations, layout_type)

		tac = time.time()
		print(f"Generated {count} PNG files in {str(round(tac-tic, 1))} seconds. Files are in {self.output_path}.")

	def compile_css_color_palette(self, palette: str | None):
		if palette is not None:
			palette = json.loads(palette)
			ColorManager.compile_color(primary=palette["primary"], secondary=palette["secondary"], light=palette["light"], 
						dark=palette["dark"], enable_gradients=palette["enable-gradients"])

	def __del__(self) -> None:
		self.driver.quit()