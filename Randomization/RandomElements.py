from dominate.tags import *
from Randomization.Elements import ElementsChoices as wcc
from Elements.HtmlElements import FeaturedItemElement, CardElement, PlaceholderElement, TableElement, ListElement, CallToActionElement, TabsElement, CollapseElement, CarouselElement, FormElement
from Randomization.RandomHelper import RandomHelper as rh
from Randomization.RandomContent import RandomContent
import lorem
import random

class RandomHtml: #TODO: Remove wg-detect classes, not in use anymore
	def mixer(n_elements, section_iteration, with_annotations=False): 
		#TODO: Improve n elements criteria
		if n_elements == 1:
			element = random.choice(wcc.mixable_elements+wcc.mixable_elements_max_two_columns)
			col = div(cls="row my-3"+(" wg-detect" if with_annotations else ""), data_wg_type="mix").add(div(cls="col"))
			with col:
				RandomHtml.element_creator(element, section_iteration, with_annotations)
		elif n_elements == 2:
			elements = random.sample(wcc.mixable_elements+wcc.mixable_elements_max_two_columns, 2)
			row = div(cls="row my-3"+" wg-detect" if with_annotations else "", data_wg_type="mix")
			with row:
				col1 = div(cls="col")
				with col1:
					RandomHtml.element_creator(elements[0], section_iteration, with_annotations)
				col2 = div(cls="col")
				with col2:
					RandomHtml.element_creator(elements[1], section_iteration, with_annotations)    
		elif n_elements > 2:
			mixer_simetry_options = wcc.mixer_simetry
			if n_elements >= 4:
				mixer_simetry_options = mixer_simetry_options + wcc.mixer_simetry_for_four
			selected_mixer_simetry_str = RandomHtml.mixer_simetry_distribution(n_elements, random.choice(mixer_simetry_options)) #str(random.choice(mixer_simetry_options)) Originally the string value was given
			elements = random.sample(wcc.mixable_elements, 2)
			row = div(cls="row my-3"+" wg-detect" if with_annotations else "", data_wg_type="mix")
			for j in range(n_elements):
				curr_col = row.add(div(cls="col"))
				with curr_col:
					if selected_mixer_simetry_str[j] == '*':
						RandomHtml.element_creator(elements[0], section_iteration, with_annotations)
					else:
						RandomHtml.element_creator(elements[1], section_iteration, with_annotations)

	def element_creator(ele,section_iteration, with_annotations=False):
		if ele == wcc.Mixable.Heading: #TODO: Populate with RandomContent
			h1(lorem.get_sentence(1) , cls=("wg-detect" if with_annotations else ""), data_wg_type="heading")
		elif ele == wcc.Mixable.Paragraph: #TODO: Populate with RandomContent
			p(lorem.get_paragraph(word_range=(6,8), sentence_range=(6,8)), cls=("wg-detect" if with_annotations else ""), data_wg_type="paragraph")
		# elif ele == "button":
		#     with div(cls="text-center"):
		#         button(cls="btn btn-primary btn-lg").add_raw_string(get_word(random.randint(1,2)))
		elif ele == wcc.Mixable.Table:
			cols = random.randint(2,5)
			rows = random.randint(2,5)
			striped_class = " table-striped" if rh.flip_coin() else ""
			TableElement(RandomContent.matrix(rows,cols), cls="bg-white"+striped_class, data_wg_type="table")
		elif ele == wcc.Mixable.CallToAction:
			CallToActionElement(RandomContent.equi_text_from_ranges(heading=(13,20), description=(80,100), button=(13,13)), 
			CallToActionElement.Mode.Aside, cls=("wg-detect" if with_annotations else ""), data_wg_type="call_to_action") #TODO: randomize parameters
		elif ele == wcc.Mixable.FeaturedItem:
			shadow_class = " shadow" if rh.flip_coin() else ""
			FeaturedItemElement(RandomContent.title_description_action((20,20),(40,50),(13,13)), random.randint(80, 150), 
			True, shadow_class, cls="text-center"+" wg-detect" if with_annotations else "", data_wg_type="featured_item") #TODO: Randomize parameter
		elif ele == wcc.Mixable.List:
			ListElement(RandomContent.links(count_range=(3,6),length_range=(13,13), range_in_chars=True)
			, rh.flip_coin(), cls=("wg-detect" if with_annotations else ""), data_wg_type="list") #TODO: Create their own content generator
		elif ele == wcc.Mixable.Collapse:
			CollapseElement(RandomContent.titles_descriptions((2,5)), "collapse-ele-"+str(section_iteration)
			,cls="text-dark"+(" wg-detect" if with_annotations else ""), data_wg_type="collapse")

	def descriptive_items(n_items): 
		#TODO: Add parameters for randomization and content generation fron RandomContent
		# Calculate text length based on placeholder heigth
		shadow_class = " shadow" if rh.flip_coin() else ""
		img_width = random.randint(100,300)
		img_height = int(img_width * (random.randint(4,13)/10))
		paragraph_length = random.randint(1,3)
		descriptor_simetry_options = wcc.descriptor_simetry
		if n_items % 2 == 0:
			descriptor_simetry_options = descriptor_simetry_options + wcc.descriptor_simetry_even
		selected_vertical_simetry = random.choice(descriptor_simetry_options)
		start_from_left = rh.flip_coin()
		last_assigned_class = ""

		for i in range(n_items):
			if selected_vertical_simetry == wcc.DescriptorSimetry.Left:
				align_class = "float-left"
			elif selected_vertical_simetry == wcc.DescriptorSimetry.Right:
				align_class = "float-right" 
			elif selected_vertical_simetry == wcc.DescriptorSimetry.Center:
				align_class = "mx-auto"
			elif selected_vertical_simetry == wcc.DescriptorSimetry.Mixed:
				if start_from_left == True:
					if i % 2 == 0:
						align_class = "float-left"
					else:
						align_class = "float-right"
				else:
					if i % 2 == 0:
						align_class = "float-right"
					else:
						align_class = "float-left"
			elif selected_vertical_simetry == wcc.DescriptorSimetry.Zigzag:
				if (i+1) % 2 == 0:
					align_class = "mx-auto"
				else:
					if last_assigned_class == "":
						if start_from_left == True:
							align_class = "float-left"
							last_assigned_class = "left"
						else: 
							align_class = "float-right"
							last_assigned_class = "right"
					else:
						if last_assigned_class == "right":
							align_class = "float-left"
							last_assigned_class = "left"
						else: 
							align_class = "float-right"
							last_assigned_class = "right"

			elif selected_vertical_simetry == wcc.DescriptorSimetry.Split:
				if (i+1) <= (n_items / 2):
					if start_from_left:
						align_class = "float-left"
					else: 
						align_class = "float-right"
				else:
					if start_from_left:
						align_class = "float-right"
					else: 
						align_class = "float-left"
			col = div(cls="row").add(div(cls="col"))
			col.add(h2(lorem.get_sentence()))
			parag = col.add(p())
			with parag:
				br()
				#make_placeholder(img_width, img_height, align_class, False, True)
				PlaceholderElement(img_width,img_height, True, cls=align_class+" m-2"+shadow_class)
				span(lorem.get_paragraph(paragraph_length))

	def cards(n_items, with_annotations=False):
		col = div(cls="row"+" wg-detect" if with_annotations else "", data_wg_type = "cards").add(div(cls="col"))
		card_cols = col.add(div(cls="card-columns"))
		with_placeholder = rh.flip_coin()
		shadow_class = " shadow" if rh.flip_coin() else ""
		with card_cols:
			for i in range(n_items):
				CardElement(RandomContent.equi_text_from_ranges(title=(20,20),description=(40,50),muted=(13,13),action=(13,13)), 
				with_placeholder, cls="text-black"+shadow_class)

	def featured_items(n_items, with_annotations=False):
		row = div(cls="row py-3"+" wg-detect" if with_annotations else "", data_wg_type = "featured_items")
		size = random.randint(50,150)
		shadow_class = " shadow" if rh.flip_coin() else ""
		with row:
			for i in range(n_items):
				col = row.add(div(cls="col"))
				with col:
					FeaturedItemElement(RandomContent.title_description_action((20,20),(40,50),(13,13)), size, True,
					 shadow_class, cls="text-center")

	def form(n_rows):
		form_list = []
		for i in range(n_rows):
			n_cols = wcc.n_form_columns_specific()
			if n_cols > 1:
				form_inputs = []
				for j in range(n_cols):
					form_input = RandomContent.form_input()
					form_input["type"] = wcc.input_type_specific()

					while form_input["type"] == wcc.InputTypes.Checkbox: #Other than checkbox could be merged
						form_input["type"] = wcc.input_type_specific()

					if form_input["type"] == wcc.InputTypes.Choicer:
						form_input["choices"] = RandomContent.input_choices(random.randint(2,10))
					form_inputs.append(form_input)
				form_list.append(form_inputs)
			else:
				form_input = RandomContent.form_input()
				form_input["type"] = wcc.input_type_specific()
				if form_input["type"] == wcc.InputTypes.Choicer:
					form_input["choices"] = RandomContent.input_choices(random.randint(2,10))
					
				form_list.append(form_input)

		FormElement(form_list, cls="p-3")

			

	
	def sections(n_sections, with_annotations=False):
		created_elements = []
		for i in range(n_sections):
			section_elements = random.choices(wcc.composed_elements, wcc.composed_elements_p)[0]
			n_elements = wcc.n_items_section_limits_specific()
			#print("Elemento a crear: ", section_elements)
			if section_elements == wcc.Composed.Carousel and (section_elements not in created_elements):
				CarouselElement(RandomContent.titles((2,5),(13,20),True),random.randint(16,40),"carousel-ele-"+str(i), 
				cls="my-3"+(" wg-detect" if with_annotations else ""), data_wg_type = "carousel") #TODO: Organize corresponding probability
			elif section_elements == wcc.Composed.Tabs and (section_elements not in created_elements):
				TabsElement(RandomContent.random_dictionary((2,4)),rh.flip_coin(),
				cls="m-3"+(" wg-detect" if with_annotations else ""), data_wg_type = "tabs")
			elif section_elements == wcc.Composed.FeaturedItems: 
				RandomHtml.featured_items(random.randint(2,4), with_annotations=with_annotations)
			elif section_elements == wcc.Composed.Cards and created_elements.count(section_elements) < 2: 
				RandomHtml.cards(random.randint(3,6), with_annotations=with_annotations)
			elif section_elements == wcc.Composed.DescriptiveItems and (section_elements not in created_elements): 
				with div(cls=("wg-detect" if with_annotations else ""), data_wg_type = "descriptive_items"):
					RandomHtml.descriptive_items(n_elements)
			elif section_elements == wcc.Composed.MixOfMixable: 
				RandomHtml.mixer(n_elements, i, with_annotations)
			created_elements.append(section_elements)

	def mixer_simetry_distribution(n_elements, simetry):
		e1 = "*"
		e2 = "-"
		simetry_str = ""
		if simetry == wcc.MixerSimetry.Alternately:
			for i in range(n_elements):
				if i % 2 == 0:
					simetry_str += e1
				else:
					simetry_str += e2
		elif simetry == wcc.MixerSimetry.Centered:
			if n_elements < 3:
				RaiseError("Centered simetry must be greater than 2")
			if n_elements % 2 == 0:
				pivot = (n_elements/2)-1
				n_pivots = 2 #This could change if centered variations are considered
			else:
				pivot = ((n_elements-1)/2)
				n_pivots = 1

			for i in range(n_elements):
				if i == pivot or (n_pivots > 1 and i == pivot+1):
					simetry_str += e2
				else:
					simetry_str += e1
		elif simetry == wcc.MixerSimetry.CorneredLeft:
			for i in range(n_elements):
				if i == 0:
					simetry_str += e1
				else:
					simetry_str += e2
		elif simetry == wcc.MixerSimetry.CorneredRight:
			for i in range(n_elements):
				if i == n_elements-1:
					simetry_str += e1
				else:
					simetry_str += e2
		elif simetry == wcc.MixerSimetry.Split: #TODO: Add and handle exception of uneven number of elements
			if n_elements % 2 == 0:
				pivot = n_elements/2
			else:
				pivot = ((n_elements+1)-(2*random.randint(0,1)))/2 #Random asimetry
			for i in range(n_elements):
				if i < pivot:
					simetry_str += e1
				else:
					simetry_str += e2
		return simetry_str