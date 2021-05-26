from Randomization.WebLayout import WebLayoutProbabilities
from Core.WebGenerator import WebGenerator
from Core.ScreenShutter import ScreenShutter
from Core.DataSetter import DataSetter
class Main:
	def run():
		# Set probabilities and settings
		# self,with_sidebar_p, with_header_p, with_navbar_p, with_footer_p, 
    	# layouts_p, boxed_body_p, generate_alert_p, big_header_p, sidebar_first_p, 
		# navbar_first_p, bg_color_classes_p
		layout_p = WebLayoutProbabilities(None,0.6,0.6,None,None,None,None,None,None,None,None)
		generator = WebGenerator(layout_p, with_annotations=True, with_color_variation=True)

		# Generate one webpage
		generator.generate_and_save_single()

		# Set screenshots settings  
		screen_shutter = ScreenShutter(full_screenshot=False, window_size=(800,600))

		# Generate multiple webpages and screenshots
		data_setter = DataSetter(generator, screen_shutter, delete_previous_files=False)
		data_setter.batch(10)

Main.run()