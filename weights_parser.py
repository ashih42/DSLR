from exceptions import ParserException

from colorama import Fore, Back, Style

class WeightsParser:
	__FEATURE_COUNT = 13
	__MODEL_COUNT = 4

	def __init__(self, filename):
		self.__line_number = 0
		with open(filename, 'r') as weights_file:
			self.mean = self.__parse_line(weights_file.readline().strip(), self.__FEATURE_COUNT)
			self.standard_deviation = self.__parse_line(weights_file.readline().strip(), self.__FEATURE_COUNT)
			self.theta = []
			for i in range(self.__FEATURE_COUNT + 1):
				self.theta.append(self.__parse_line(weights_file.readline().strip(), self.__MODEL_COUNT))

	def __parse_line(self, line, num_terms):
		self.__line_number += 1
		tokens = line.split()
		if len(tokens) != num_terms:
			raise ParserException('invalid number of terms at ' +
				Fore.GREEN + 'line ' + str(self.__line_number) + Fore.RESET + ': ' +
				Fore.MAGENTA + line + Fore.RESET + '\n (expecting %d terms)' % num_terms)
		lst = []
		for token in tokens:
			try:
				lst.append(float(token))
			except ValueError:
				raise ParserException('invalid term at ' +
					Fore.GREEN + 'line ' + str(self.__line_number) + Fore.RESET + ': ' +
					Fore.MAGENTA + token + Fore.RESET)
		return lst
