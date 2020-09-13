from Layout.HtmlComponent import HtmlComponent
from dominate.tags import *
from Core.Enums import *

class SidebarComponent(HtmlComponent):
	tag_name = "div"
	content_type = ContentType.List

	def __init__(self, content, canonical_width, *args, **kwargs):
		self.content = content
		self.canonical_width = canonical_width
		self.content_type = SidebarComponent.content_type
		self.args = args
		self.kwargs = kwargs
		#self.build()

	def build(self):
		super().__init__(SidebarComponent.tag_name, *self.args, **self.kwargs)
		#self.add_class("border-right")
		self.attributes['id'] = "sidebar-wrapper"
		links_list = div(cls="list-group list-group-flush", style="width:"+str(self.canonical_width)+"vh;")
		with links_list:
			for e in self._content:
				a(cls="list-group-item list-group-item-action", href="#").add(e)
		self.add(links_list)
		pass

class HeaderComponent(HtmlComponent): 
	tag_name = "header"
	content_type = ContentType.Multi

	class Mode(enum.Enum): #TODO: Make this modes actually work
		Heading = 1
		Carousel = 2
		Image = 3

	def __init__(self, content, canonical_height, mode, *args, **kwargs):
		self.content = content
		self.canonical_height = canonical_height
		self.content_type = HeaderComponent.content_type
		self.mode = mode
		self.args = args
		self.kwargs = kwargs
		#self.build()

	def content_type_equivalent(self):
		if self.mode == HeaderComponent.Mode.Carousel:
			self.content_type = ContentType.List
			self.content = self.content #Reset content to call validator

	def build(self):
		self.content_type_equivalent()
		super().__init__(HeaderComponent.tag_name, *self.args, **self.kwargs)
		self.add_class("d-flex align-items-center justify-content-center") #Just to center content :(
		self.attributes["style"] = "height: "+str(self.canonical_height)+"vh;"
		with self:
			if self.mode == HeaderComponent.Mode.Heading:
				h1(self.content, cls="p-2 text-center")


class NavbarComponent(HtmlComponent):
	tag_name = "nav"
	content_type = ContentType.List

	class Align():
		Left = "ml-auto"
		Right = "mr-auto"
		Center = "mx-auto"

	def __init__(self, content, canonical_height, alignment, *args, **kwargs):
		self.alignment = alignment
		self.content = content
		self.canonical_height = canonical_height
		self.args = args
		self.kwargs = kwargs

	def build(self):
		super().__init__(NavbarComponent.tag_name, *self.args, **self.kwargs)
		self.add_class('navbar navbar-expand-md')
		with self:
			button(cls="navbar-toggler", type="button", data_toggle="collapse", data_target="#main-nav").add(span(cls="navbar-toggler-icon"))
			links_container = div(cls="collapse navbar-collapse", id="main-nav")
			links_container.attributes["style"] = "height: "+str(self.canonical_height)+"vh;"
			with links_container:
				ul_list = ul(cls="navbar-nav "+self.alignment)
				with ul_list:
					for l in self.content:
						a_tag = li(cls="nav-item").add(a(cls="nav-link",href="#"))
						a_tag.add_raw_string(l)
						
				# if self.search_bar:
				# 	search_box = form(cls="form-inline my-2 my-lg-0")
				# 	with search_box:
				# 		input(cls="form-control mr-sm-2", type="search", placeholder="Buscar")
				# 		button(cls="btn btn-primary my-2 my-sm-0", type="submit").add_raw_string("Buscar")

class FooterComponent(HtmlComponent):
	tag_name = "footer"
	content_type = ContentType.Multi

	class Mode(enum.Enum):
		CallToAction = 1
		BackgroundOnly = 2
		Credits = 3

	def __init__(self, content, canonical_height, mode, *args, **kwargs):
		self.content = content
		self.canonical_height = canonical_height
		self.content_type = FooterComponent.content_type
		self.mode = mode
		self.args = args
		self.kwargs = kwargs
		#self.build()

	def build(self):
		super().__init__(FooterComponent.tag_name, *self.args, **self.kwargs)
		self.add_class("jumbotron mb-0")
		self.attributes["style"] = "height: "+str(self.canonical_height)+"vh;"
		footer_content = self.add(div(cls="container"))
		with footer_content:
			if self.mode == FooterComponent.Mode.Credits:
				span(cls="text-muted").add_raw_string(self.content[0])