from Elements.HtmlElement import HtmlElement
from dominate.tags import *
from Core.Enums import *
from Randomization.Elements import ElementsChoices

class FeaturedItemElement(HtmlElement):
	tag_name = "div"
	content_type = ContentType.Multi

	def __init__(self, content, placeholder_size, show_placeholder_size, placeholder_extra_class, *args, **kwargs):
		self.content = content
		self.placeholder_size = placeholder_size
		self.show_placeholder_size = show_placeholder_size
		self.placeholder_extra_class = placeholder_extra_class
		self.content_type = FeaturedItemElement.content_type
		self.args = args
		self.kwargs = kwargs
		self.build()

	def build(self):
		super().__init__(FeaturedItemElement.tag_name, *self.args, **self.kwargs)
		with self:
			PlaceholderElement(self.placeholder_size, self.placeholder_size, True, 
			 cls="text-black rounded-circle mx-auto "+self.placeholder_extra_class)
			h2(self.content[0])
			p(self.content[1])
			a(href="#", cls="btn btn-primary").add(self.content[2])


class CardElement(HtmlElement):
	tag_name = "div"
	content_type = ContentType.Multi

	def __init__(self, content, with_placeholder, *args, **kwargs):
		self.content = content
		self.with_placeholder = with_placeholder
		self.content_type = CardElement.content_type
		self.args = args
		self.kwargs = kwargs
		self.build()

	def build(self):
		super().__init__(CardElement.tag_name, *self.args, **self.kwargs)
		self.add_class("card")
		with self:
			if self.with_placeholder:
				#make_placeholder(286,180, "card-img-top", False, True)
				PlaceholderElement(cls="card-img-top")
			body = div(cls="card-body")
			with body:
				h5(cls="card-title").add_raw_string(self.content["title"])
				p(cls="card-text").add_raw_string(self.content["description"])
				actions = div(cls="d-flex justify-content-between align-items-center")
				with actions:
					btn_group = div(cls="btn-group")
					with btn_group:
						button(cls="btn btn-sm btn-outline-secondary", type="button").add_raw_string(self.content["action"])
						#button(cls="btn btn-sm btn-outline-secondary", type="button").add_raw_string(text_btn_2)
					small(cls="text-muted").add_raw_string(self.content["muted"])


class PlaceholderElement(HtmlElement):
	tag_name = "span"
	content_type = ContentType.Multi

	def __init__(self, width=None, height=100, show_size=False, measure_unit=MeasureUnit.Px, *args, **kwargs):
		self.width = width
		self.height = height
		self.show_size = show_size
		self.measure_unit = measure_unit
		self.content_type = PlaceholderElement.content_type
		self.args = args
		self.kwargs = kwargs
		self.build()

	def build(self):
		super().__init__(PlaceholderElement.tag_name, *self.args, **self.kwargs)
		#placeholder_wrapper = span(cls="placeholder "+align_class,)
		self.add_class("placeholder")
		style_string = ""
		size_string = ""
		if self.width is not None:
			style_string += "width: "+str(self.width)+self.measure_unit.value+";"
			size_string += str(self.width)+(self.measure_unit.value if self.measure_unit != MeasureUnit.Px else "")

		if self.height is not None:
			style_string += "height: "+str(self.height)+self.measure_unit.value+";"
			size_string += ("x" if self.measure_unit == MeasureUnit.Px else " X ")+str(self.height)+(self.measure_unit.value if self.measure_unit != MeasureUnit.Px else "")
		
		self.attributes["style"] = style_string

		if self.show_size:
			with self:
				span().add(size_string)

class TableElement(HtmlElement): 
	#TODO: 
	# Add table heading
	tag_name = "table"
	content_type = ContentType.Multi

	def __init__(self, content, *args, **kwargs):
		self.content = content
		self.content_type = TableElement.content_type
		self.args = args
		self.kwargs = kwargs
		self.build()

	def build(self):
		super().__init__(TableElement.tag_name, *self.args, **self.kwargs)
		#placeholder_wrapper = span(cls="placeholder "+align_class,)
		self.add_class("table")
		with self:
			for i in self.content:
				curr_row = tr()
				with curr_row:
					for j in i:
						td(j)

class CallToActionElement(HtmlElement):
	tag_name = "div"
	content_type = ContentType.Multi

	class Mode(enum.Enum):
		Center = 0
		Aside = 1
		AsideDescription = 2

	def __init__(self, content, mode, *args, **kwargs):
		self.mode = mode
		self.content = content
		self.content_type = CallToActionElement.content_type
		self.args = args
		self.kwargs = kwargs
		self.build()

	def build(self): #TODO: Build heading and description independently
		super().__init__(CallToActionElement.tag_name, *self.args, **self.kwargs)
		#placeholder_wrapper = span(cls="placeholder "+align_class,)
		self.add_class("row align-items-center justify-content-center")
		with self:
			if "heading" in self.content:
				if "description" in self.content:
					if self.mode == CallToActionElement.Mode.Center:
						self.add_class(row, "text-center p-2")
						text_container = div(cls="w-100")
						with text_container:
							h1(self.content["heading"])
							p(self.content["description"])
						button(cls="btn btn-primary m-3").add(self.content["button"])
					elif self.mode == CallToActionElement.Mode.Aside:
						text_container = div(cls="col-10")
						with text_container:
							h1(self.content["heading"])
							p(self.content["description"])
						button(cls="btn btn-primary m-3").add(self.content["button"])
					elif selfmode == CallToActionElement.Mode.AsideDescription:
						self.add_class("p-2")
						h1(self.content["heading"])
						text_container = div(cls="d-flex align-items-center")
						# if random.choice([True, False]):
						# 	text_container = div(cls="d-flex align-items-center")
						# else:
						# 	text_container = div(cls="d-flex align-items-center flex-row-reverse")
						with text_container:
							p(self.content["description"])
							button(cls="btn btn-primary m-3").add(self.content["button"])
				else:
					button(cls="btn btn-primary m-3").add(content["button"])

class ListElement(HtmlElement): 
	#tag_name = "ul" | "ol" -> defined based on ordered parameter
	content_type = ContentType.List

	def __init__(self, content, ordered, *args, **kwargs):
		self.ordered = ordered
		self.content = content
		self.content_type = ListElement.content_type
		self.args = args
		self.kwargs = kwargs
		self.build()

	def build(self):
		tag_name = "ol"
		if not self.ordered:
			tag_name = "ul"
		super().__init__(tag_name, *self.args, **self.kwargs)
		#placeholder_wrapper = span(cls="placeholder "+align_class,)
		#self.add_class("table")
		with self:
			for ele in self.content:
				li(ele)

class TabsElement(HtmlElement): 
	tag_name = "div"
	content_type = ContentType.Dictionary

	def __init__(self, content, are_pills, *args, **kwargs):
		self.are_pills = are_pills
		#self.show_vertical = show_vertical TODO: add vertical option
		self.content = content
		self.content_type = TabsElement.content_type
		self.args = args
		self.kwargs = kwargs
		self.build()

	def build(self):
		super().__init__(TabsElement.tag_name, *self.args, **self.kwargs)
		tab_type_class = "nav-tabs"
		if self.are_pills:
			tab_type_class = "nav-pills"

		with self:
			links_container = div(cls="nav "+tab_type_class)
			with links_container:
				for tab_name in self.content:
					a(tab_name.capitalize(),cls="nav-item nav-link", id=tab_name+"-tab", data_toggle="tab", href="#"+tab_name, 
					 role="tab", aria_controls=tab_name)

			tabs_content_container = div(cls="tab-content")
			with tabs_content_container:
				for tab_name in self.content:
					div(self.content[tab_name],cls="tab-pane fade border p-3", id=tab_name, role="tabpanel", aria_labelledby=tab_name)


class TabsElement(HtmlElement): 
	tag_name = "div"
	content_type = ContentType.Dictionary

	def __init__(self, content, are_pills, *args, **kwargs):
		self.are_pills = are_pills
		#self.show_vertical = show_vertical TODO: add vertical option
		self.content = content
		self.content_type = TabsElement.content_type
		self.args = args
		self.kwargs = kwargs
		self.build()

	def build(self):
		super().__init__(TabsElement.tag_name, *self.args, **self.kwargs)
		tab_type_class = "nav-tabs"
		if self.are_pills:
			tab_type_class = "nav-pills"

		with self:
			links_container = div(cls="nav "+tab_type_class)
			with links_container:
				for i, tab_name in enumerate(self.content):
					a(tab_name.capitalize(),cls="nav-item nav-link"+(" active" if i == 0 else ""), id=tab_name+"-tab", 
					 data_toggle="tab", href="#"+tab_name, role="tab", aria_controls=tab_name)

			tabs_content_container = div(cls="tab-content")
			with tabs_content_container:
				for i, tab_name in enumerate(self.content):
					div(self.content[tab_name],cls="tab-pane fade border p-3"+(" show active" if i == 0 else ""), 
					 id=tab_name, role="tabpanel", aria_labelledby=tab_name)

class CollapseElement(HtmlElement): 
	tag_name = "div"
	content_type = ContentType.List

	def __init__(self, content, _id, *args, **kwargs):
		self.id = _id
		self.content = content
		self.content_type = CollapseElement.content_type
		self.args = args
		self.kwargs = kwargs
		self.build()

	def build(self):
		super().__init__(CollapseElement.tag_name, *self.args, **self.kwargs)
		self.attributes["id"] = self.id
		with self:
			for i, ele in enumerate(self.content):
				first_word_id = (ele[0].split(' ', 1)[0]).lower()+"-"+str(i+1)
				card = div(cls="card")
				with card:
					c_header = div(cls="card-header", id="heading-"+first_word_id)
					c_header.add(
						button(ele[0], cls="btn btn-link collapsed", data_toggle="collapse", data_target="#collapse-"+first_word_id,
						 aria_controls="heading-"+first_word_id)
					)
					collapse = div(id="collapse-"+first_word_id, cls="collapse", aria_labelledby="heading-"+first_word_id, data_parent="#"+self.id)
					collapse.add(div(ele[1], cls="card-body text-black"))

class CarouselElement(HtmlElement): #TODO: Add parameters to populate with real placeholders or web images
	tag_name = "div"
	content_type = ContentType.List

	def __init__(self, content, canonical_height, _id, *args, **kwargs):
		self.canonical_height = canonical_height
		self.id = _id
		self.content = content
		self.content_type = CarouselElement.content_type
		self.args = args
		self.kwargs = kwargs
		self.build()

	def build(self):
		super().__init__(CarouselElement.tag_name, *self.args, **self.kwargs)
		self.attributes["id"] = self.id
		self.attributes["data-ride"] = "carousel"
		self.add_class("carousel slide")
		with self:
			indicators = ol(cls="carousel-indicators")
			items_container = div(cls="carousel-inner")
			for i, ele in enumerate(self.content):
				with indicators:
					li(data_target="#"+self.id, data_slide_to=str(i), cls=("active" if i == 0 else ""))
				
				with items_container: #TODO: Split the long line
					div(div(h1(ele, cls="pt-5"), cls="d-block w-100 text-center", style="background-color: darkgrey; height: "+str(self.canonical_height)+"vh;"), cls="carousel-item"+(" active" if i == 0 else ""))

			a(span(cls="carousel-control-prev-icon"),cls="carousel-control-prev", href="#"+self.id,
			 role="button", data_slide="prev")
			a(span(cls="carousel-control-next-icon"),cls="carousel-control-next", href="#"+self.id,
			 role="button", data_slide="next")

class FormElement(HtmlElement): #TODO: Add extra options for form construction
	tag_name = "form"
	content_type = ContentType.List

	def __init__(self, content, *args, **kwargs):
		self.content = content
		self.content_type = FormElement.content_type
		self.args = args
		self.kwargs = kwargs
		self.build()

	def build_input(self, ele, is_alone_in_row=True):
		self.attributes["data-wg-type"] = "form"
		ele_id = ElementsUtils.idefy(ele["name"])
		if "choices" in ele:
			if is_alone_in_row:
				legend(ele["name"])
				with div(data_wg_type="radios"):
					for opt in ele["choices"]:
						opt_id = ele_id+"_"+ElementsUtils.idefy(opt)
						with div(cls="form-check"):
							input_(cls="form-check-input", type="radio", name=ele_id, 
							id=opt_id
							)
							label(opt,cls="form-check-label",_for=opt_id)
			else:
				label(ele["name"], _for=ele_id)
				selector = select(cls="form-control", id=ele_id, data_wg_type="select")
				with selector:
					for opt in ele["choices"]:
						option(opt)
		else:
			if "type" in ele:
				ele_type = ele["type"]
			else:
				ele_type = "text"

			if ele_type == ElementsChoices.InputTypes.Checkbox and is_alone_in_row:
				with div(cls="custom-switch"):
					input_(type=ele["type"], id=ele_id, cls="custom-control-input")
					label(ele["name"],_for=ele_id, cls="custom-control-label", data_wg_type=ele["type"])
			elif ele_type == ElementsChoices.InputTypes.Range:
				label(ele["name"],_for=ele_id)
				input_(type=ele["type"], id=ele_id, cls="custom-range", data_wg_type=ele["type"])
			elif ele_type == ElementsChoices.InputTypes.Submit:
				input_(ele["name"],type=ele["type"], id=ele_id, cls="btn btn-primary", data_wg_type=ele["type"])
			else:
				label(ele["name"],_for=ele_id)
				input_(type=ele["type"], id=ele_id, cls="form-control", data_wg_type=ele["type"])
		

	def build(self):
		super().__init__(FormElement.tag_name, *self.args, **self.kwargs)
		with self:
			for ele in self.content:
				if type(ele) is list:
					row_elements = ele
					row = div(cls="form-row")
					for row_ele in row_elements:
						with row:
							with div(cls="form-group col-md"):
								self.build_input(row_ele, False)
				else:
					input_container = div(cls="form-group")
					with input_container:
						self.build_input(ele)

						
class ElementsUtils:
	def idefy(text):
		return text.lower().replace(" ","_")