import sass
import os
import palettable
import random
import colorsys
from StyleManager.PalettableChoices import color_palette_choices
from colorharmonies import Color, complementaryColor, triadicColor, splitComplementaryColor, tetradicColor, analogousColor, monochromaticColor
class ColorManager:
	#Big TODO: Clean this up, messy code using this class
	class ClassesStyle:
		Default = {"body":"","wrapper":"","header":"secondary","navbar":"light","sidebar":"light","footer":""}
		Inverse = {"body":"dark","wrapper":"light","header":"primary","navbar":"dark","sidebar":"secondary","footer":""}
		NoLimits = {"body":"light","wrapper":"light","header":"dark","navbar":"dark","sidebar":"dark","footer":""}

	class SeedColors:
		Red = "#fe2712" 
		Orange = "#fb9902" 
		Yellow = "#fefe33"
		Green = "#66b032"
		Blue = "#0247fe"
		Violet = "#8601af"

	seed_color_choices = [SeedColors.Red, SeedColors.Orange, SeedColors.Yellow, SeedColors.Green, SeedColors.Blue, SeedColors.Violet]

	def hex_to_rgb(color_str):
		color_str = color_str.lstrip('#')
		return tuple(int(color_str[i:i+2], 16) for i in (0, 2, 4))

	def shift_color_component(original,amount):
		return amount * original + (1 - amount) * original

	def lighter_color(colors):
		lighter = colors[0]
		for c in colors:
			if lightness(c[0], c[1], c[2]) > lightness(lighter[0], lighter[1], lighter[2]):
				lighter = c

	def lightness(r,g,b):
		return (((r * 299) + (g * 587) + (b * 114)) / 1000)

	def is_light_color(color,above_criteria=125):
		#color = color[0]
		return ColorManager.lightness(color[0], color[1], color[2]) > above_criteria

	def are_light_colors(*args,above_criteria=125):
		for arg in args:
			yield ColorManager.is_light_color(color, above_criteria)

	def lighter_bubble_sort(array):
		n = len(array)
		for i in range(n):
			already_sorted = True
			for j in range(n - i - 1):
				if ColorManager.lightness(array[j][0], array[j][1], array[j][2]) < ColorManager.lightness(array[j+1][0], array[j+1][1], array[j+1][2]):
					array[j], array[j + 1] = array[j + 1], array[j]
					already_sorted = False
			if already_sorted:
				break
		return array

	def random_palette_set_and_name():
		palette_options = ["colorbrewer", "cmocean", "cartocolors"]
		palette_set = random.choice(palette_options)
		palette_name = random.choice(color_palette_choices[palette_set])
		return palette_set, palette_name 

	def palette_to_colors(palette_set=None, palette_name=None):
		
		if palette_name is None and palette_set is None:
			palette_set, palette_name = random_palette_group_and_name()

		if palette_set == "colorbrewer":
			current_palette = palettable.colorbrewer.get_map(palette_name, "sequential", 4).colors
		elif palette_set == "cartocolors":
			current_palette = palettable.cartocolors.sequential.get_map(palette_name+"_4", "sequential").colors
		elif palette_set == "cmocean":
			current_palette = palettable.cmocean.sequential.get_map(palette_name+"_4", "sequential").colors

		current_palette = ColorManager.lighter_bubble_sort(current_palette) #Some palettes are ordered darker to lighter

		primary = current_palette[1],
		secondary = current_palette[2],
		light = current_palette[0],
		dark = current_palette[3],
		
		return primary, secondary, light, dark

	def random_pleasing_color():
		h = random.uniform(0.0, 1.0)
		s = random.uniform(0.4, 1.0)
		if s > 0.65: #Limit of pleasing colors not affected by lightness
			light_color = random.choice([True, False])
			if light_color:
				l = random.uniform(0.83, 0.95)
			else:
				l = random.uniform(0.2,0.3)
		else:
			l = random.uniform(0.2, 0.95)
		return colorsys.hls_to_rgb(h, l, s)

	def random_harmonic_palette():
		seed_color = ColorManager.random_pleasing_color()
		seed_color = [seed_color[0]*255, seed_color[1]*255, seed_color[2]*255]
		
		if random.choice([True, False]):
			new_color = Color(seed_color,"","")
			current_palette = tetradicColor(new_color)
			current_palette.append(seed_color)
		else:
			current_palette = ColorManager.random_monochromatic(seed_color)

		current_palette = ColorManager.lighter_bubble_sort(current_palette) #Some palettes are ordered darker to lighter

		primary = current_palette[1],
		secondary = current_palette[2],
		light = current_palette[0],
		dark = current_palette[3],
		return primary, secondary, light, dark

	def random_monochromatic(seed_color):

		colors = []
		k_l = 0.3
		step = random.uniform(0.2, 0.2)
		is_light = ColorManager.lightness(seed_color[0], seed_color[1], seed_color[2]) > 150
		seed_color = colorsys.rgb_to_hls(seed_color[0]/255, seed_color[1]/255, seed_color[2]/255)
		l = 0.18 * (-1 if is_light else 1)
		s = 0.05 * (-1 if is_light else 1)
		for i in range(4):
			l_step = seed_color[1] + (i*l)
			s_step = seed_color[2] + (i*s)
			is_hurting_color = s_step > 0.7 and (l_step >= 0.4 and l_step <= 0.6)
			is_collapsed_color = s_step < 0.05 or s_step > 0.95 or l_step < 0.05 or l_step > 0.95

			if is_hurting_color and is_light:
				s_step = s_step - 0.2
				l_step = 0.6
			elif is_hurting_color:
				s_step = s_step - 0.1
				l_step = 0.4
			elif is_collapsed_color:
				if is_light:
					s_step = random.uniform(0.1, 0.3)
					l_step = random.uniform(0.28, 0.4)
				else:
					s_step = random.uniform(0.5, 0.7)
					l_step = random.uniform(0.8, 0.95)

			new_color = colorsys.hls_to_rgb(seed_color[0], l_step, s_step)
			seed_color = [seed_color[0], l_step, s_step]
			new_color = new_color[0]*255, new_color[1]*255, new_color[2]*255
			colors.append(new_color)

		return colors
		
	def random_palette(generation_strategy=None):
		if generation_strategy is None:			
			#generation_strategy = "random"
			generation_strategy = random.choice(["palettable","harmonic"])

		if generation_strategy == "palettable":
			random_palettable = ColorManager.random_palette_set_and_name()
			return ColorManager.palette_to_colors(random_palettable[0], random_palettable[1])
		else:
			return ColorManager.random_harmonic_palette()

	def compile_color(primary=None, secondary=None, light=None, dark=None, enable_gradients=True, output_path="./output/"):
		
		if primary is None and secondary is None and light is None and dark is None:
			primary, secondary, light, dark = palette_to_colors()

		sass_vars = {
			"$body-bg" : "#FFF",
			"$primary" : primary,
			"$secondary" : secondary,
			"$light" : light,
			"$dark" : dark,
			"$enable-gradients": "true" if enable_gradients else "false"
		}

		scss = ""
		for var in sass_vars:
			scss = scss + var+":"+sass_vars[var]+"; \n"
		scss += '@import "../Assets/vendor/bootstrap-dist-4.3.1/scss/bootstrap";'
		#print(palett.cartocolors.sequential.BluGrn_6.colors)

		with open(output_path+'custom-bootstrap.scss', 'w') as example_scss:
			example_scss.write(scss)
		sass.compile(dirname=(output_path, output_path+'css'), output_style='compressed')
		os.remove(output_path+'custom-bootstrap.scss')

	def tuple_to_str(color_tuple):
		color_tuple = color_tuple[0]
		return "rgb({0}, {1}, {2})".format(color_tuple[0], color_tuple[1], color_tuple[2])

	def bg_class_resolver(primary, secondary, light, dark, html_component, color_classes, enable_gradients=True):
		bg_class = ""
		palette_dict = {
			"primary": primary, 
			"secondary": secondary,
			"light": light,
			"dark": dark,
		}
		if html_component in color_classes:
			str_color = color_classes[html_component]
			if str_color != "":
				bg_class = "bg-{0}{1}".format("gradient-" if enable_gradients else "",str_color)

			if str_color in palette_dict:
				color = palette_dict[str_color][0]
				if not ColorManager.is_light_color(color, 125):
					if html_component == "navbar":
						bg_class = bg_class + " navbar-dark"
					elif html_component != "body": #Body wouln't have text color (Wrapper manage inner text color)
						bg_class = bg_class + " text-white"
				else:
					if html_component == "navbar":
						bg_class = bg_class + " navbar-light"
			
			#Check if text in wrapper should be white 
			if html_component =="wrapper":
				if color_classes["wrapper"] == "" and "body" in color_classes:
					str_body_color = color_classes["body"]
					if str_body_color in palette_dict:
						body_color = palette_dict[str_color]
						if not ColorManager.is_light_color(body_color, 125):
							bg_class = " text-white"

		return bg_class




