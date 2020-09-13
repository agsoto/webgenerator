import lorem  # https://github.com/JarryShaw/lorem#usage
import random
import typing
import itertools
from array import *

class RandomContent: #Standarize contents as dictionaries
	def links(count_range, length_range, range_in_chars=False): 
		n_elements = random.randint(count_range[0], count_range[1])
		if range_in_chars:
			return list(itertools.islice(RandomContent.equi_text(n_elements, length_range), n_elements))
		else:
			return list(itertools.islice(lorem.sentence(count=n_elements,word_range=(length_range), comma=(0,0)), n_elements))
	
	def title(length_range, range_in_chars=False): 
		if range_in_chars:
			return list(itertools.islice(RandomContent.equi_text(1, length_range), 1))
		else:
			return lorem.get_word(random.randint(length_range[0], length_range[1]), func="capitalize") #TODO: Fix and test

	def titles(count_range, length_range, range_in_chars=False):
		n_elements = random.randint(count_range[0], count_range[1])
		if range_in_chars:
			return list(itertools.islice(RandomContent.equi_text(n_elements, length_range), n_elements))
		else:
			return lorem.get_word(random.randint(length_range[0], length_range[1]), func="capitalize") #TODO: Fix and test

	def credits(length_range, range_in_chars=False): 
		if range_in_chars:
			return list(itertools.islice(RandomContent.equi_text(1, length_range), 1))
		else:
			return lorem.get_word(random.randint(length_range[0], length_range[1]), func="capitalize")

	def title_description_action(title_range, description_range, action_range, range_in_chars=False):
		return [list(itertools.islice(RandomContent.equi_text(1, title_range), 1)),
				list(itertools.islice(RandomContent.equi_text(1, description_range), 1)), 
				list(itertools.islice(RandomContent.equi_text(1, action_range), 1))]

	def random_dictionary(count_range): #TODO: customize parameters
		d = dict()
		n_items = random.randint(count_range[0], count_range[1])
		for i in range(n_items):
			d[lorem.get_word()] = lorem.get_paragraph(sentence_range=(1,3))
		return d

	def titles_descriptions(count_range): #TODO: customize parameters
		result_items = []
		n_items = random.randint(count_range[0], count_range[1])
		for i in range(n_items):
			result_items.insert(0,[lorem.get_sentence(),lorem.get_paragraph()])
		return result_items

	def equi_text_from_ranges(**kwargs):
		d = dict()
		for attr, value in kwargs.items():
			d[attr] = list(itertools.islice(RandomContent.equi_text(1, value), 1))[0]
		return d

	def equi_text(count, char_range):
		min_chars = char_range[0]
		max_chars = char_range[1]
		n_chars_longest_word = len(max(lorem._TEXT, key=len))

		if min_chars < n_chars_longest_word:
			raise IndexError("min_chars must be equal or greater than the longest word in the pool: "+str(n_chars_longest_word))
		if min_chars > max_chars:
			raise IndexError("min_chars must be lower or equal than max_chars")

		#tolerance = max_chars - min_chars
		n_chars_shortest_word = len(min(lorem._TEXT, key=len))
		n_pool_items = len(lorem._TEXT)

		for _ in range(count):
			pool = lorem._gen_pool()
			text = lorem.get_word(1, func="capitalize")
			for n_word in itertools.cycle(pool):
				if ((len(text)+len(n_word)) < min_chars) or (len(text)+len(n_word) < max_chars):
					text += " " + n_word
				else:
					remaining_n_chars = max_chars-len(text)
					if remaining_n_chars < n_chars_shortest_word+1:
						break
					else: 
						pass #TODO: Add break word feature
			yield text

	def matrix(n_rows, n_cols): #TODO: Recieve content range as parameter
		content = [[0 for x in range(n_cols)] for y in range(n_rows)] 
		for i in range(0, n_rows):
			for j in range(0, n_cols-1):
				content[i][j] = lorem.get_word()
		return content

	def form_input():
		r_name = lorem.get_word(count=random.randint(1,3))
		r_name = r_name[0].upper() + r_name[1:]
		r_desc = lorem.get_word(count=random.randint(3,6))
		r_desc = r_desc[0].upper() + r_desc[1:]
		return {"name":r_name, "description": r_desc}
		
	def input_choices(n_choices):
		choices = []
		for i in range(n_choices):
			r_choice = lorem.get_word(count=random.randint(1,3))
			r_choice = r_choice[0].upper() + r_choice[1:]
			choices.append(r_choice)
		return choices
		