from exceptions import ParserException

from colorama import Fore, Back, Style

'''
Assumptions:
- Only care about Arithmancy and onwards, starting at Column 6
- Columns 0, 2 - 5 are useless and not even checked
- Column 1 is Hogwarts House, which might or might not be labeled
- Columns 6 - 18 are the important features, but some might be missing => fill from dummy values
'''

class PredictionDataParser:
	__FEATURES = ['Arithmancy', 'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Ancient Runes', 'History of Magic', 'Transfiguration', 'Potions', 'Care of Magical Creatures', 'Charms', 'Flying']
	__ALL_FIELD_COUNT = 19

	def __init__(self, filename, dummy_values):
		self.__line_number = 0
		self.houses = []
		self.data = []
		with open(filename, 'r') as data_file:
			first_line = data_file.readline().strip()
			self.__parse_headers(first_line)
			for line in data_file:
				try:
					self.__parse_line(line.strip(), dummy_values)
				except ParserException as e:
					print(Style.BRIGHT + Fore.RED + 'ParserException: ' + Style.RESET_ALL + Fore.RESET + str(e))

		print('Accepted %d, discarded %d rows of data\n' %
			(len(self.data), self.__line_number - 1 - len(self.data)))
		if len(self.data) == 0:
			raise ParserException('dataset is empty')

	def __parse_headers(self, line):
		self.__line_number += 1
		if line != 'Index,Hogwarts House,First Name,Last Name,Birthday,Best Hand,Arithmancy,Astronomy,Herbology,Defense Against the Dark Arts,Divination,Muggle Studies,Ancient Runes,History of Magic,Transfiguration,Potions,Care of Magical Creatures,Charms,Flying':
			raise ParserException('invalid headers at ' +
				Fore.GREEN + 'line ' + str(self.__line_number) + Fore.RESET + ': ' +
				Fore.MAGENTA + line + Fore.RESET + '\n' +
				'  Must define these headers: Index, Hogwarts House, First Name, Last Name, Birthday, Best Hand, Arithmancy, Astronomy, Herbology, Defense Against the Dark Arts, Divination, Muggle Studies, Ancient Runes, History of Magic, Transfiguration, Potions, Care of Magical Creatures, Charms, Flying')
		
	def __parse_line(self, line, dummy_values):
		self.__line_number += 1
		tokens = line.split(',')
		# check number of fields match the expected number
		if len(tokens) != self.__ALL_FIELD_COUNT:
			raise ParserException('invalid number of terms at ' +
				Fore.GREEN + 'line ' + str(self.__line_number) + Fore.RESET + ': ' +
				Fore.MAGENTA + line + Fore.RESET + '\n  (impossible to imputate data)')
		row_data = []
		for i in range(6, self.__ALL_FIELD_COUNT):
			try:
				row_data.append(float(tokens[i]))
			except ValueError:
				print(Style.BRIGHT + Fore.RED + 'Warning: ' + Style.RESET_ALL + Fore.RESET +
					'invalid ' + PredictionDataParser.__FEATURES[i - 6] + ' at ' +
					Fore.GREEN + 'line ' + str(self.__line_number) + Fore.RESET + ': ' +
					Fore.MAGENTA + tokens[i] + Fore.RESET + ', replacing with default mean value: ' +
					Fore.MAGENTA + '%.3f' % dummy_values[i - 6] + Fore.RESET)
				row_data.append(dummy_values[i - 6])
		self.data.append(row_data)
		self.houses.append(tokens[1])
