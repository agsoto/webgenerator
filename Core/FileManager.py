from shutil import copy
import shutil
import stat
import os
import glob
import fnmatch

class FileManager:
	@staticmethod
	def prepare_output(output_path, delete_previous_files, with_annotations):
		if delete_previous_files and os.path.exists(output_path):
			FileManager.rmtree_inside(output_path)

		FileManager.create_if_not_exists(output_path)

		css_output = os.path.join(output_path, "css")
		FileManager.create_if_not_exists(css_output)

		js_output = os.path.join(output_path, "js")
		FileManager.create_if_not_exists(js_output)

		images_output = os.path.join(output_path, "images")
		FileManager.create_if_not_exists(images_output)

		html_output = os.path.join(output_path, "html")
		FileManager.create_if_not_exists(html_output)

		dirpath = os.getcwd()
		if with_annotations:
			copy(os.path.join(dirpath,"Assets/via_pj_settings.json"), output_path)
		copy(os.path.join(dirpath,"Assets/vendor/bootstrap-dist-4.3.1/js/bootstrap.min.js"), js_output)
		copy(os.path.join(dirpath,"Assets/vendor/jquery-dist/jquery-3.2.1.slim.min.js"), js_output)
		copy(os.path.join(dirpath,"Assets/wg-extras.css"), css_output)

		#If color variation is set to true in the batch of datasetter this will be overrided
		if not os.path.isfile(os.path.join(css_output, "custom-bootstrap.css")):
			copy(os.path.join(dirpath,"Assets/vendor/bootstrap-dist-4.3.1/css/bootstrap.min.css"), css_output)
			os.rename(os.path.join(css_output, "bootstrap.min.css"), os.path.join(css_output, "custom-bootstrap.css"))

	@staticmethod
	def create_if_not_exists(path):
		if not os.path.exists(path):
			os.mkdir(path)

	@staticmethod
	def rmtree_inside(path):
		for root, dirs, files in os.walk(path, topdown=False):
			for name in files:
				filename = os.path.join(root, name)
				os.chmod(filename, stat.S_IWUSR)
				os.remove(filename)
			for name in dirs:
				os.rmdir(os.path.join(root, name))

	@staticmethod
	def get_html_paths_list(html_files_relative_path: str) -> list[int]:
		return glob.glob(os.path.join(os.getcwd(), html_files_relative_path+'*.html'))

	@staticmethod
	def count_html_files(html_files_relative_path: str) -> int:
		return len(fnmatch.filter(os.listdir(html_files_relative_path), '*.html'))

	@staticmethod
	def load_scripts(scripts: dict[str, str], scripts_path: str) -> dict[str, str]:
		for script_name in scripts.keys():
			with open(scripts_path+script_name+".js", "r") as f:
				scripts[script_name] = f.read()
		return scripts

	@staticmethod
	def save(filename, content):
		result = open(filename, ''"w+")
		result.write(content)
		result.close()