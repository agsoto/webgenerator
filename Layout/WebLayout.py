from random import choices
import random
import dominate # https://github.com/Knio/dominate
from dominate.tags import *
from dominate.util import raw
from lorem import * # https://github.com/JarryShaw/lorem#usage
from utils import *
from dominate import document
from dominate import dom_tag 
from Layout.HtmlComponent import EmptyHtmlComponent
from Core.DominateExtensions import DominateExtensions

class WebLayout(document):
	def __init__(self,boxed_body,layout,sidebar_first,navbar_first,force_sizes=None):
		super().__init__(title='Dominate', doctype='<!DOCTYPE html>', request=None)
		self.wrapper = self.body.add(div(id="full-wrapper"))
		DominateExtensions.bound_add_class(self.wrapper)
		DominateExtensions.bound_add_class(self.body)
		self.boxed_body = boxed_body
		self.layout = layout
		self.sidebar_first = sidebar_first
		self.navbar_first = navbar_first
		self.force_sizes = force_sizes
		self._header = EmptyHtmlComponent()
		self.navbar = EmptyHtmlComponent()
		self.sidebar = EmptyHtmlComponent()
		self._footer = EmptyHtmlComponent()
	
	def build(self):
		#doc = dominate.document(title='Result')
		with self.head:
			meta(name="viewport", content="width=device-width, initial-scale=1.0")
			meta(name="author", content="Web Generator")
			meta(name="wg-layout", content=str(self.layout))
			link(rel='stylesheet', href='../css/custom-bootstrap.css')
			link(rel='stylesheet', href='../css/wg-extras.css')
			# script(src="https://code.jquery.com/jquery-3.2.1.slim.min.js", integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN", crossorigin="anonymous")
			script(type='text/javascript', src="../js/jquery-3.2.1.slim.min.js")
			script(type='text/javascript', src='../js/bootstrap.min.js')
			comment("Layout: "+str(self.layout))
		with self.wrapper:
			#Global margin
			if self.boxed_body is not None:
				x = self.boxed_body["x"]
				y = self.boxed_body["y"]
				if x > 5:
					self.wrapper.add_class("px-sm-5 px-3")
					self.body.add_class("px-md-"+str(x-5))
				elif x > 3:
					self.wrapper.add_class("px-sm-"+str(x)+" px-3")
				else:
					self.wrapper.add_class("px-"+str(x))

				self.wrapper.add_class("py-"+str(y))


			if self.has_sidebar:
				if self.layout == 1:
					if self.sidebar_first: 
						self.sidebar.build()
					self.wrapper.add_class('d-flex')
					main_container = div(cls="w-100")
					with main_container:  
						self.build_header_navbar()
						div(cls="container-fluid py-3", id="page-content")
						if self.has_footer:
							self._footer.build()
					if not self.sidebar_first: 
						self.sidebar.build()

				if self.layout == 2:
					self.build_header_navbar()
					main_container = div(cls="d-flex")
					if self.sidebar_first:
						with main_container:
							self.sidebar.build()
					if self.has_footer():
						with main_container: 
							content_container = div(cls="flex-grow-1") #TODO: Rethink another easier way
							with content_container:
								div(cls="container-fluid py-3", id="page-content")
								self._footer.build()
							if not self.sidebar_first:
								self.sidebar.build()
					else:
						with main_container:
							div(cls="container-fluid py-3", id="page-content")
							if not self.sidebar_first:
								self.sidebar.build()

				if self.layout == 3:
					self.build_header_navbar()
					main_container = div(cls="d-flex")
					with main_container:
						if self.sidebar_first:
							self.sidebar.build()
						div(cls="container-fluid py-3", id="page-content")
						if not self.sidebar_first:
							self.sidebar.build()
					if self.has_footer():
						self._footer.build()

				if self.layout == 4:
					main_container = div(cls="d-flex")
					with main_container:
						if self.sidebar_first:  
							self.sidebar.build()
						temp_div = div(cls="w-100")
						with temp_div:
							self.build_header_navbar()
							div(cls="container-fluid py-3", id="page-content")
						if not self.sidebar_first:
							self.sidebar.build()
					if(self.has_footer()):
						self._footer.build()
				# Layout 5 depends on the CSS RULE!
			else:
				make_menu_header()
				div(cls="container-fluid py-3", id="page-content")
				if has_footer:
					make_footer(random.randint(sizes_limits["footer"][0],sizes_limits["footer"][1]), "credits")
			
			# self.add_header_navbar()
			# self.add(self.sidebar)
			#self.main_doc = doc

	def build_header_navbar(self):
		if self.navbar_first:
			self.navbar.build()
		if self.has_header():
			self._header.build()
		if not self.navbar_first:
			self.navbar.build()
	
	def add(self, *args):
		'''
		Adding tags to a a weblayout that build the content where it's called if it
		the elements aren't None.
		'''
		not_none_args = []
		for arg in args:
			if arg is not None:
				not_none_args.append(arg)
		return self._entry.add(*not_none_args)

	def save(self, output_path="./output/"):
		result = open(output_path+"rw.html","w+")
		result.write(self.render())
		result.close()

	def has_footer(self):
		return not isinstance(self._footer, EmptyHtmlComponent)

	def has_header(self):
		return not isinstance(self._header, EmptyHtmlComponent)

	def has_navbar(self):
		return not isinstance(self.navbar, EmptyHtmlComponent)

	def has_sidebar(self):
		return not isinstance(self.sidebar, EmptyHtmlComponent)