from exceptions import ParserException

from colorama import Fore, Back, Style
from datetime import datetime
import re

'''
Assumptions:
- Colume 0 is Index				=> unused
- Column 1 is Hogwarts House	=> THE TARGET (not a feature, but well Parser doesn't care)
- Column 2 is First Name		=> expand to 2 features: length and first letter
- Column 3 is Last Name			=> expand to 2 features: length and first letter
- Column 4 is Birthday			=> expand to 4 features: year, month, day of month, day of week
- Column 5 is Best Hand			=> expand to 1 numeric feature
- All remaining column fields are float values
'''

class TrainingDataParser:
	__DATE_PATTERN = re.compile(r'\d\d\d\d-\d\d-\d\d')

	def __init__(self, filename):
		self.headers = []
		self.data = []
		self.__line_number = 0

		with open(filename, 'r') as data_file:
			first_line = data_file.readline().strip()
			self.__parse_headers(first_line)
			for line in data_file:
				try:
					self.__parse_line(line.strip())
				except ParserException as e:
					print(Style.BRIGHT + Fore.RED + 'ParserException: ' + Style.RESET_ALL + Fore.RESET + str(e))

		print('Accepted %d, discarded %d rows of data\n' %
			(len(self.data), self.__line_number - 1 - len(self.data)))
		if len(self.data) == 0:
			raise ParserException('dataset is empty')
		
	def __parse_headers(self, line):
		self.__line_number += 1
		tokens = line.split(',')
		if not (len(tokens) >= 6 and tokens[0] == 'Index' and tokens[1] == 'Hogwarts House' and tokens[2] == 'First Name' and tokens[3] == 'Last Name' and tokens[4] == 'Birthday' and tokens[5] == 'Best Hand'):
			raise ParserException('invalid headers at ' +
				Fore.GREEN + 'line ' + str(self.__line_number) + Fore.RESET + ': ' +
				Fore.MAGENTA + line + Fore.RESET + '\n' +
				'  Must define at least these 6 headers: Index, Hogwarts House, First Name, Last Name, Birthday, Best Hand')
		
		self.headers = ['Hogwarts House', 'First Name Length', 'First Name Initial', 'Last Name Length', 'Last Name Initial',
			'Birth Year', 'Birth Month', 'Birth Day of Month', 'Birth Day Of Week', 'Best Hand']
		for i in range(6, len(tokens)):
			self.headers.append(tokens[i])

	def __parse_line(self, line):
		self.__line_number += 1
		tokens = line.split(',')

		# check number of columns match the number of headers defined
		if len(tokens) - 6 + 10 != len(self.headers):
			raise ParserException('invalid data at ' +
				Fore.GREEN + 'line ' + str(self.__line_number) + Fore.RESET + ': ' +
				Fore.MAGENTA + line + Fore.RESET)

		# first field, Index, is ignored

		# check Hogwarts House field
		house = tokens[1]
		if not (house == '' or house == 'Gryffindor' or house == 'Hufflepuff' or house == 'Ravenclaw' or house == 'Slytherin'):
			raise ParserException('invalid data at ' +	Fore.GREEN + 'line ' + str(self.__line_number) + Fore.RESET + ': ' +
				'Hogwarts House: ' + Fore.MAGENTA + house + Fore.RESET)

		# check First Name field
		first_name = tokens[2]
		if len(first_name) == 0 or not first_name.isalpha():
			raise ParserException('invalid data at ' +	Fore.GREEN + 'line ' + str(self.__line_number) + Fore.RESET + ': ' +
				'First Name: ' + Fore.MAGENTA + first_name + Fore.RESET)
		first_name_length = len(first_name)
		first_name_first_letter = ord(first_name.upper()[0]) - ord('A')

		# check Last Name field
		last_name = tokens[3]
		if len(last_name) == 0 or not last_name.isalpha():
			raise ParserException('invalid data at ' +	Fore.GREEN + 'line ' + str(self.__line_number) + Fore.RESET + ': ' +
				'First Name: ' + Fore.MAGENTA + last_name + Fore.RESET)
		last_name_length = len(last_name)
		last_name_first_letter = ord(last_name.upper()[0]) - ord('A')

		# check Birthdate field
		birthdate = tokens[4]
		if not TrainingDataParser.__DATE_PATTERN.match(birthdate):
			raise ParserException('invalid data at ' +	Fore.GREEN + 'line ' + str(self.__line_number) + Fore.RESET + ': ' +
				'Birthdate: ' + Fore.MAGENTA + birthdate + Fore.RESET)
		try:
			birth_year = int(birthdate[0:4])
			birth_month = int(birthdate[5:7])
			birth_day_of_month = int(birthdate[8:])
			birth_day_of_week = datetime(birth_year, birth_month, birth_day_of_month).weekday()		# monday => 0, ... , sunday => 6
		except ValueError:
			raise ParserException('invalid data at ' +	Fore.GREEN + 'line ' + str(self.__line_number) + Fore.RESET + ': ' +
				'Birthdate: ' + Fore.MAGENTA + birthdate + Fore.RESET)

		# check Best Hand field
		best_hand = tokens[5]
		if not (best_hand == 'Left' or best_hand == 'Right'):
			raise ParserException('invalid data at ' +	Fore.GREEN + 'line ' + str(self.__line_number) + Fore.RESET + ': ' +
				'Best Hand: ' + Fore.MAGENTA + best_hand + Fore.RESET)
		best_hand_number = -1 if best_hand == 'Left' else 1

		row_data = [house, float(first_name_length), float(first_name_first_letter), float(last_name_length), float(last_name_first_letter),
			float(birth_year), float(birth_month), float(birth_day_of_month), float(birth_day_of_week), float(best_hand_number)]

		# check all remaining fields
		for i in range(6, len(tokens)):
			try:
				row_data.append(float(tokens[i]))
			except ValueError:
				raise ParserException('invalid data at ' + Fore.GREEN + 'line ' + str(self.__line_number) + Fore.RESET + ': ' +
					self.headers[i] + ': ' + Fore.MAGENTA + tokens[i] + Fore.RESET)

		self.data.append(row_data)
