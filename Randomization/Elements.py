from Layout.WebLayout import WebLayout
import random
from Randomization.RandomHelper import RandomHelper

import enum

class ElementsChoices:
	class Alert(enum.Enum):
		Not = 0
		Top = 1
		Bottom = 2

	class Mixable(enum.IntEnum):
		Heading = 1
		Paragraph = 2
		List = 3
		FeaturedItem = 4
		Table = 5
		CallToAction = 6
		Collapse = 7

	class Composed(enum.Enum):
		Carousel = 2
		FeaturedItems = 3
		Cards = 4
		DescriptiveItems = 5
		MixOfMixable = 6
		Tabs = 7

	class DescriptorSimetry(enum.Enum):
		Left = 1
		Right = 2
		Center = 3
		Mixed = 4
		Split = 5
		Zigzag = 6

	class MixerSimetry():
		# - is A
		# * is B
		Alternately = "-*-*" #Inverse variations like "*-*-"" are not necessary because A and B are always chosen randomly
		Centered = "-**-"
		Split = "--**"
		CorneredLeft = "-***"
		CorneredRight = "***-" 

	class InputTypes:
		Submit = "submit" # Excluded from choices
		Choicer = "choicer" # Could be select, group of radios or checkboxes
		Text = "text"
		Date = "date"
		Time = "time"
		Number = "number"
		Range = "range"
		Checkbox = "checkbox"

	class PageTypes(enum.Enum):
		Landing = 1
		Content = 2
		Form = 3
		Dashboard = 4


	### - - - - - - - - - - Global Content
	generate_alert_choices = [Alert.Not, Alert.Top, Alert.Bottom] 
	featured_img_size_limits = [48, 120] #Because size will be globally used
	n_items_section_limits = [1, 3]
	n_section_limits = [1, 3]
	n_items_descriptor_limits = [1, 3]

	page_type_choices = [PageTypes.Content, PageTypes.Form]
	page_type_choices_p = [0.7, 0.3]

	#Mixer
	mixable_elements = [Mixable.Heading, Mixable.Paragraph, Mixable.List, Mixable.FeaturedItem] 
	mixable_elements_max_two_columns = [Mixable.Table, Mixable.CallToAction, Mixable.Collapse]
	mixer_simetry = [MixerSimetry.Alternately, MixerSimetry.Centered, MixerSimetry.Split]
	mixer_simetry_for_four = [MixerSimetry.CorneredLeft, MixerSimetry.CorneredRight]

	composed_elements = [Composed.Carousel, Composed.Tabs, Composed.FeaturedItems, Composed.Cards, Composed.DescriptiveItems, Composed.MixOfMixable]
	composed_elements_p = [0.1,0.1,0.1,0.1,0.1,0.5]
	#Content - Descriptor
	#TODO: Change names to descriptive_items
	descriptor_simetry = [DescriptorSimetry.Left, DescriptorSimetry.Right, DescriptorSimetry.Center, DescriptorSimetry.Mixed]
	descriptor_simetry_even = [DescriptorSimetry.Split, DescriptorSimetry.Zigzag]

	#Form
	n_form_rows_limits = [2,10]
	n_form_columns_choices = [1,2,3,4]
	n_form_columns_choices_p = [0.4,0.3,0.2,0.1]

	input_types = [InputTypes.Text, InputTypes.Date, InputTypes.Time, InputTypes.Number, InputTypes.Range, InputTypes.Checkbox, InputTypes.Choicer]
	input_types_p = [0.6, 0.06, 0.06, 0.06, 0.06, 0.06,0.1]

	def n_items_section_limits_specific():
		return random.randint(ElementsChoices.n_items_section_limits[0], ElementsChoices.n_items_section_limits[1])

	def n_sections_specific():
		return random.randint(ElementsChoices.n_section_limits[0], ElementsChoices.n_section_limits[1])

	def input_type_specific():
		return random.choices(ElementsChoices.input_types,ElementsChoices.input_types_p,k=1)[0]

	def n_form_columns_specific():
		return random.choices(ElementsChoices.n_form_columns_choices,ElementsChoices.n_form_columns_choices_p,k=1)[0]

	def n_form_rows_specific():
		return random.randint(ElementsChoices.n_form_rows_limits[0], ElementsChoices.n_form_rows_limits[1])

	def page_type_specific():
		return random.choices(ElementsChoices.page_type_choices,ElementsChoices.page_type_choices_p,k=1)[0]
		


