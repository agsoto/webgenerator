import types
#from dominate import dom_tag
class DominateExtensions:

	def bound_add_class(target):
		def add_class(target, _cls):
			if "class" in target.attributes: 
				if target.attributes['class'] != "":
					target.attributes['class'] = target.attributes['class']+" "
				target.attributes['class'] = target.attributes['class']+_cls
			else:
				target.attributes['class'] = _cls
		target.add_class = types.MethodType(add_class,target)
