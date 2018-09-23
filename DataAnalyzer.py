from TrainingDataParser import TrainingDataParser
from Description import Description
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt
import numpy as np
import string
import os

'''
Assumptions:
- Colume 0 is Index				=> unused
- Column 1 is Hogwarts House	=> THE ANSWER
- Column 2 is First Name		=> expand to 2 features: length and first letter
- Column 3 is Last Name			=> expand to 2 features: length and first letter
- Column 4 is Birthday			=> expand to 4 features: year, month, day of month, day of week
- Column 5 is Best Hand			=> expand to 1 numeric feature
- Column 6 ... are all float values
'''

class DataAnalyzer:
	__GRAPHING_ALPHA = 0.5
	__HISTOGRAM_DIRECTORY = 'Histograms/'
	__SCATTERPLOT_DIRECTORY = 'ScatterPlots/'
	__PAIRPLOT_DIRECTORY = 'PairPlots/'
	
	def __init__(self, filename):
		parser = TrainingDataParser(filename)
		self.__feature_headers = parser.headers[1:]
		self.__feature_count = len(self.__feature_headers)

		data = np.array(parser.data, dtype=object)
		self.__gryffindor_data = data[ data[:, 0] == 'Gryffindor' ]
		self.__hufflepuff_data = data[ data[:, 0] == 'Hufflepuff' ]
		self.__ravenclaw_data = data[ data[:, 0] == 'Ravenclaw' ]
		self.__slytherin_data = data[ data[:, 0] == 'Slytherin' ]
		self.__gryffindor_data = self.__gryffindor_data[:, 1:]
		self.__hufflepuff_data = self.__hufflepuff_data[:, 1:]
		self.__ravenclaw_data = self.__ravenclaw_data[:, 1:]
		self.__slytherin_data = self.__slytherin_data[:, 1:]
		self.__gryffindor_data = self.__gryffindor_data.astype(float)
		self.__hufflepuff_data = self.__hufflepuff_data.astype(float)
		self.__ravenclaw_data = self.__ravenclaw_data.astype(float)
		self.__slytherin_data = self.__slytherin_data.astype(float)

		self.sample_count = data.shape[0]
		self.Y_labeled = data[:, 0]
		self.Y_labeled = self.Y_labeled.reshape(self.sample_count, 1)
		self.X = data[:, 1:]
		self.X = self.X.astype(float)

		self.all_descriptions = []
		for column in self.X.T:
			self.all_descriptions.append(Description(column))
		self.__gryffindor_descriptions = []
		for column in self.__gryffindor_data.T:
			self.__gryffindor_descriptions.append(Description(column))
		self.__hufflepulff_descriptions = []
		for column in self.__hufflepuff_data.T:
			self.__hufflepulff_descriptions.append(Description(column))
		self.__ravenclaw_descriptions = []
		for column in self.__ravenclaw_data.T:
			self.__ravenclaw_descriptions.append(Description(column))
		self.__slytherin_descriptions = []
		for column in self.__slytherin_data.T:
			self.__slytherin_descriptions.append(Description(column))

	def show_pair_plot(self):
		try:
			os.stat(self.__PAIRPLOT_DIRECTORY)
		except:
			os.mkdir(self.__PAIRPLOT_DIRECTORY)
		fig = plt.figure(figsize=(40, 40))
		for i in range(0, self.__feature_count):
			for j in range(0, self.__feature_count):
				self.__generate_subplot(i, j)
		fig.tight_layout()
		filename = self.__PAIRPLOT_DIRECTORY + 'Pair Plot'
		plt.savefig(filename)
		print('Saved pair plot at ' + Fore.BLUE + filename + Fore.RESET)

	def __generate_subplot(self, i, j):
		plt.subplot(self.__feature_count, self.__feature_count, j + i * self.__feature_count + 1)
		if i == j:
			plt.hist(self.__gryffindor_data[:,i].tolist(), label='Gryffindor', color='red',
				fill=True, alpha=DataAnalyzer.__GRAPHING_ALPHA)
			plt.hist(self.__hufflepuff_data[:,i].tolist(), label='Hufflepuff', color='gold',
				fill=True, alpha=DataAnalyzer.__GRAPHING_ALPHA)
			plt.hist(self.__ravenclaw_data[:,i].tolist(), label='Ravenclaw', color='blue',
				fill=True, alpha=DataAnalyzer.__GRAPHING_ALPHA)
			plt.hist(self.__slytherin_data[:,i].tolist(), label='Slytherin', color='green',
				fill=True, alpha=DataAnalyzer.__GRAPHING_ALPHA)
		else:
			plt.scatter(self.__gryffindor_data[:, i].tolist(), self.__gryffindor_data[:, j].tolist(),
				label='Gryffindor', color='red', alpha=DataAnalyzer.__GRAPHING_ALPHA, s=1)
			plt.scatter(self.__hufflepuff_data[:, i].tolist(), self.__hufflepuff_data[:, j].tolist(),
				label='Hufflepuff', color='gold', alpha=DataAnalyzer.__GRAPHING_ALPHA, s=1)
			plt.scatter(self.__ravenclaw_data[:, i].tolist(), self.__ravenclaw_data[:, j].tolist(),
				label='Ravenclaw', color='blue', alpha=DataAnalyzer.__GRAPHING_ALPHA, s=1)
			plt.scatter(self.__slytherin_data[:, i].tolist(), self.__slytherin_data[:, j].tolist(),
				label='Slytherin', color='green', alpha=DataAnalyzer.__GRAPHING_ALPHA, s=1)
		plt.xticks([], [])
		plt.yticks([], [])
		if i == 0:
			plt.title(self.__feature_headers[j])
		if j == 0:
			plt.ylabel(self.__feature_headers[i])
		print('Generating subplot %2d, %2d ' % (i, j))

	def show_scatter_plots(self):
		try:
			os.stat(self.__SCATTERPLOT_DIRECTORY)
		except:
			os.mkdir(self.__SCATTERPLOT_DIRECTORY)
		for i in range(0, self.__feature_count):
			for j in range(i + 1, self.__feature_count):
				self.__generate_scatter_plot(i, j)

	def __generate_scatter_plot(self, i, j):
		plt.clf()
		plt.scatter(self.__gryffindor_data[:, i].tolist(), self.__gryffindor_data[:, j].tolist(),
			label='Gryffindor', color='red', alpha=DataAnalyzer.__GRAPHING_ALPHA)
		plt.scatter(self.__hufflepuff_data[:, i].tolist(), self.__hufflepuff_data[:, j].tolist(),
			label='Hufflepuff', color='gold', alpha=DataAnalyzer.__GRAPHING_ALPHA)
		plt.scatter(self.__ravenclaw_data[:, i].tolist(), self.__ravenclaw_data[:, j].tolist(),
			label='Ravenclaw', color='blue', alpha=DataAnalyzer.__GRAPHING_ALPHA)
		plt.scatter(self.__slytherin_data[:, i].tolist(), self.__slytherin_data[:, j].tolist(),
			label='Slytherin', color='green', alpha=DataAnalyzer.__GRAPHING_ALPHA)
		plt.xlabel(self.__feature_headers[i])
		plt.ylabel(self.__feature_headers[j])
		plt.title('%s vs %s' % (self.__feature_headers[j], self.__feature_headers[i]))
		plt.legend(loc='upper right')
		filename = self.__SCATTERPLOT_DIRECTORY + '%02d, %02d : %s vs %s' % (
			i, j, self.__feature_headers[j], self.__feature_headers[i])
		plt.savefig(filename)
		print('Saved scatter plot at ' + Fore.BLUE + filename + Fore.RESET)

	def show_histograms(self):
		try:
			os.stat(self.__HISTOGRAM_DIRECTORY)
		except:
			os.mkdir(self.__HISTOGRAM_DIRECTORY)
		self.__generate_histogram(0, bins=list(range(0, 15)))													# First Name Length
		self.__generate_histogram(1, bins=list(range(0, 27)), xticks=list(string.ascii_uppercase))				# First Name Initial
		self.__generate_histogram(2, bins=list(range(0, 15)))													# Last Name Length
		self.__generate_histogram(3, bins=list(range(0, 27)), xticks=list(string.ascii_uppercase))				# Last Name Initial
		year_bins = list(range(int(np.amin(self.X[:, 4])), int(np.amax(self.X[:, 4])) + 2, 1))
		self.__generate_histogram(4, bins=year_bins)															# Birth Year
		self.__generate_histogram(5, bins=list(range(1, 14)))													# Birth Month
		self.__generate_histogram(6, bins=list(range(1, 33)))													# Birth Day of Month
		self.__generate_histogram(7, bins=list(range(0, 8)),													# Birth Day of Week
			xticks=['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'])
		self.__generate_histogram(8, bins=list(range(-1, 2)), xticks=['Left', '', 'Right'])						# Best Hand
		for i in range(9, self.__feature_count):																	# Other Features
			self.__generate_histogram(i)

	def __generate_histogram(self, i, bins=None, xticks=None):
		plt.clf()
		plt.hist(self.__gryffindor_data[:,i].tolist(), label='Gryffindor', color='red',
			bins=bins, fill=True, alpha=DataAnalyzer.__GRAPHING_ALPHA)
		plt.hist(self.__hufflepuff_data[:,i].tolist(), label='Hufflepuff', color='gold',
			bins=bins, fill=True, alpha=DataAnalyzer.__GRAPHING_ALPHA)
		plt.hist(self.__ravenclaw_data[:,i].tolist(), label='Ravenclaw', color='blue',
			bins=bins, fill=True, alpha=DataAnalyzer.__GRAPHING_ALPHA)
		plt.hist(self.__slytherin_data[:,i].tolist(), label='Slytherin', color='green',
			bins=bins, fill=True, alpha=DataAnalyzer.__GRAPHING_ALPHA)
		feature_name = self.__feature_headers[i]
		plt.xlabel(feature_name)
		if xticks is not None:
			plt.xticks(bins, xticks)
		plt.ylabel('Count')
		plt.title('Distribution of ' + feature_name)
		plt.legend(loc='upper right')
		filename = self.__HISTOGRAM_DIRECTORY + '%02d : %s' % (i, feature_name)
		plt.savefig(filename)
		print('Saved histogram at ' + Fore.BLUE + filename + Fore.RESET)

	def describe(self):
		print(Style.BRIGHT + Fore.CYAN + 'ALL STUDENTS:' + Style.RESET_ALL + Fore.RESET)
		self.__print_descriptions(self.all_descriptions)
		print()
		print(Style.BRIGHT + Fore.CYAN + 'GRYFFINDOR:' + Style.RESET_ALL + Fore.RESET)
		self.__print_descriptions(self.__gryffindor_descriptions)
		print()
		print(Style.BRIGHT + Fore.CYAN + 'HUFFLEPUFF:' + Style.RESET_ALL + Fore.RESET)
		self.__print_descriptions(self.__hufflepulff_descriptions)
		print()
		print(Style.BRIGHT + Fore.CYAN + 'RAVENCLAW:' + Style.RESET_ALL + Fore.RESET)
		self.__print_descriptions(self.__ravenclaw_descriptions)
		print()
		print(Style.BRIGHT + Fore.CYAN + 'SLYTHERIN:' + Style.RESET_ALL + Fore.RESET)
		self.__print_descriptions(self.__slytherin_descriptions)
		print()

	def __print_descriptions(self, descriptions):
		# print feature headers
		print(Style.BRIGHT + Fore.BLUE + '\t\t\t', end='')
		for header in self.__feature_headers:
			print('%-20.20s \t' % header, end='')
		print(Style.RESET_ALL + Fore.RESET)
		# print row of COUNT
		print(Style.BRIGHT + 'COUNT\t\t\t' + Style.RESET_ALL, end='')
		for description in descriptions:
			print('%-20.6f \t' % description.count, end='')
		print()
		# print row of MEAN
		print(Style.BRIGHT + 'MEAN\t\t\t' + Style.RESET_ALL, end='')
		for description in descriptions:
			print('%-20.6f \t' % description.mean, end='')
		print()
		# print row of STANDARD DEVIATION
		print(Style.BRIGHT + 'STANDARD DEVIATION\t' + Style.RESET_ALL, end='')
		for description in descriptions:
			print('%-20.6f \t' % description.standard_deviation, end='')
		print()
		# print row of VARIANCE
		print(Style.BRIGHT + 'VARIANCE\t\t' + Style.RESET_ALL, end='')
		for description in descriptions:
			print('%-20.6f \t' % description.variance, end='')
		print()
		# print row of MINIMUM
		print(Style.BRIGHT + 'MINIMUM\t\t\t' + Style.RESET_ALL, end='')
		for description in descriptions:
			print('%-20.6f \t' % description.min, end='')
		print()
		# print row of 25 PERCENTILE
		print(Style.BRIGHT + '25 PERCENTILE\t\t' + Style.RESET_ALL, end='')
		for description in descriptions:
			print('%-20.6f \t' % description.percentile_25, end='')
		print()
		# print row of 50 PERCENTILE
		print(Style.BRIGHT + '50 PERCENTILE\t\t' + Style.RESET_ALL, end='')
		for description in descriptions:
			print('%-20.6f \t' % description.percentile_50, end='')
		print()
		# print row of 75 PERCENTILE
		print(Style.BRIGHT + '75 PERCENTILE\t\t' + Style.RESET_ALL, end='')
		for description in descriptions:
			print('%-20.6f \t' % description.percentile_75, end='')
		print()
		# print row of MAXIMUM
		print(Style.BRIGHT + 'MAXIMUM\t\t\t' + Style.RESET_ALL, end='')
		for description in descriptions:
			print('%-20.6f \t' % description.max, end='')
		print()
		# print row of MODE
		print(Style.BRIGHT + 'MODE\t\t\t' + Style.RESET_ALL, end='')
		for description in descriptions:
			print('%-20.6f \t' % description.mode, end='')
		print()
