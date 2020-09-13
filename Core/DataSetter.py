from Core.WebGenerator import WebGenerator
from Core.ScreenShutter import ScreenShutter
from Core.FileManager import FileManager 
import time
import os

class DataSetter:
	def __init__(self, webgen: WebGenerator, screen_shutter: ScreenShutter=None, delete_previous_files: bool=True):
		self.webgen = webgen
		self.screen_shutter = screen_shutter
		self.delete_previous_files = delete_previous_files

	def batch(self,n_files,with_annotations=None, 
		with_color_variation=None, output_path=None):
		with_annotations, with_color_variation, output_path = self.load_defaults_if_none(
			with_annotations=self.webgen.with_annotations,
			with_color_variation=self.webgen.with_color_variation, 
			output_path = self.webgen.output_path
		)

		FileManager.prepare_output(output_path, self.delete_previous_files, with_annotations)

		#Generate HTML
		tic = time.time()
		count = 0
		for i in range(n_files):
			website = self.webgen.generate(with_annotations=True, with_color_variation=True) 
			FileManager.save(os.path.join(output_path,"html/rw_"+str(i)+".html"),website.render())
			count += 1
		tac = time.time()
		print("Generated {0} HTML files in {1} seconds. Files are in {2}.".format(count,round(tac-tic, 1),self.webgen.output_path))

		#Generate Screenshots
		if self.screen_shutter is not None:
			self.screen_shutter.capture_and_save()

	def load_defaults_if_none(self,**kwargs):
		for key, value in kwargs.items():
			if value is not None:
				yield value
			else:
				yield getattr(self.webgen,key)
