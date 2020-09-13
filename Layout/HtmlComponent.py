from dominate.tags import *
from dominate.util import escape
from Core.Enums import *

class HtmlComponent(html_tag):
	def __init__(self, tag_name, *args, **kwargs): #TODO: add bool for init super or not 
		self.tag_name = tag_name
		super(HtmlComponent, self).__init__(*args, **kwargs)
		#self.build()

	def build(self):
		pass

	@property
	def content(self):
		return self._content
		
	@content.setter
	def content(self, c):
		if self.content_type == ContentType.List:
			if not isinstance(c, list):
				raise TypeError("Content must be a list")
			if not c: 
				raise Exception("Content cannot be empty")
		self._content = c

	def add_class(self, _cls):
		if "class" in self.attributes: 
			if self.attributes['class'] != "":
				self.attributes['class'] = self.attributes['class']+" "
			self.attributes['class'] = self.attributes['class']+_cls
		else:
			self.attributes['class'] = _cls
		
	def _render(self, sb, indent_level, indent_str, pretty, xhtml):
		pretty = pretty and self.is_pretty

		t = type(self)
		name = self.tag_name

		# Workaround for python keywords and standard classes/methods
		# (del, object, input)
		if name[-1] == '_':
			name = name[:-1]

		# open tag
		sb.append('<')
		sb.append(name)

		for attribute, value in sorted(self.attributes.items()):
			if value is not False: # False values must be omitted completely
				sb.append(' %s="%s"' % (attribute, escape(unicode(value), True)))

		sb.append(' />' if self.is_single and xhtml else '>')

		if not self.is_single:
			inline = self._render_children(sb, indent_level + 1, indent_str, pretty, xhtml)

			if pretty and not inline:
				sb.append('\n')
				sb.append(indent_str * indent_level)

			# close tag
			sb.append('</')
			sb.append(name)
			sb.append('>')

		return sb

class EmptyHtmlComponent():
	def __init__(self):
		pass

	def build(self):
		pass