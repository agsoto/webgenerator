import json
import os


class Annotator:
	'''
		This class generates the region annotations of a webpage
	'''
	def __init__(self, annotations_file_path: str, output_path: str):
		self.annotations_file_path = annotations_file_path
		self.output_path = output_path
		self.annotations_json_content = {}
		self.annotations_file = None
		self.imgs_annotations_metadatas = {}
		self.annotations = {}
		self.annotations_file_exists = os.path.isfile(annotations_file_path+'via_pj_settings.json')
		if self.annotations_file_exists:
			self.annotations_file = open(annotations_file_path+'via_pj_settings.json', "r")
			self.annotations_json_content = json.load(self.annotations_file)
			self.annotations_file.close()

	def add_annotation(self, image_name:str, img_file_size, annotation:str, layout_type):
		element_name_id = image_name+str(img_file_size) #Because VIA annotations use name+filesize
		self.imgs_annotations_metadatas[element_name_id] = { 
			"filename": image_name, 
			"size": img_file_size, 
			"regions": annotation,
			"file_attributes": {
				"caption": "",
				"public_domain": "yes",
				"image_url": "",
				"layout_type": layout_type
			}
		}

		self.annotations[element_name_id] = annotation

	def __del__(self) -> None:
	
		self.annotations_json_content["_via_image_id_list"] = list(self.imgs_annotations_metadatas)
		self.annotations_json_content["_via_img_metadata"] = self.imgs_annotations_metadatas

		with open(self.output_path+'web_gen_annotations.json', 'w') as f:
			json.dump(self.annotations, f)

		with open(self.output_path+'via_pj_settings.json', 'w') as f:
			json.dump(self.annotations_json_content, f)