from data_analyzer import DataAnalyzer
from prediction_data_parser import PredictionDataParser
from weights_parser import WeightsParser
from exceptions import LogisticRegressionException

from colorama import Fore, Back, Style
import numpy as np
import math
import os

# Just using 13 (+ 1) features, starting with Arithmancy

class LogisticClassifier:
	__LABELS = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']
	__ANSWER_FILE = 'houses.csv'
	__WEIGHTS_FILE = 'weights.dat'
	__FEATURE_COUNT = 13
	__ALPHA = 0.001
	__SIGMOID = np.vectorize(lambda x: 1 / (1 + math.exp(-x)))
	____VERBOSE = os.getenv('DSLR_VERBOSE') == 'TRUE'

	def __init__(self, filename=None):
		if filename is not None:
			parser = WeightsParser(filename)
			self.__mean_list = parser.mean
			self.__stdev_list = parser.standard_deviation
			self.__theta = np.array(parser.theta)
			print('Loaded model parameters from ' + Fore.CYAN + filename + Fore.RESET + '\n')	

	def __save_weights_file(self, filename=__WEIGHTS_FILE):
		with open(filename, 'w') as weights_file:
			# write 1 row of all mean values
			for mean in self.__mean_list:
				weights_file.write('%f ' % mean)
			weights_file.write('\n')
			# write 1 row of all standard deviation values
			for stdev in self.__stdev_list:
				weights_file.write('%f ' % stdev)
			weights_file.write('\n')
			# write matrix theta row by row
			for row in self.__theta:
				for num in row:
					weights_file.write('%f ' % num)
				weights_file.write('\n')
		print('Saved model parameters in ' + Fore.CYAN + filename + Fore.RESET + '\n')	

	def __save_answer(self, predictions):
		with open(self.__ANSWER_FILE, 'w') as answer_file:
			answer_file.write('Index,Hogwarts House' + '\n')
			indices = range(len(predictions))
			for i, prediction in zip(indices, predictions):
				answer_file.write('%d,%s\n' %(i, prediction))
		print('Saved predictions in ' + Fore.CYAN + self.__ANSWER_FILE + Fore.RESET + '\n')

	def predict_data(self, filename):
		print(Style.BRIGHT + 'Making predictions for data in ' + Fore.MAGENTA + filename + Fore.RESET + Style.RESET_ALL)
		parser = PredictionDataParser(filename, self.__mean_list)
		sample_count = len(parser.houses)
		Y_labeled = np.array(parser.houses)
		Y_labeled = Y_labeled.reshape(sample_count, 1)
		X = np.array(parser.data)

		# Apply feature scaling:
		for i in range(X.shape[1]):
			X[:, i] = (X[:, i] - self.__mean_list[i]) / self.__stdev_list[i]
		X = np.c_[np.ones(sample_count), X]

		house_percent = self.__SIGMOID(np.matmul(X, self.__theta))
		predictions = np.argmax(house_percent, axis=1)
		predictions = predictions.tolist()		
		predictions = [LogisticClassifier.__LABELS[index] for index in predictions]
		indices = list(range(len(predictions)))

		print(Style.BRIGHT + 'Index\t\tGryffindor\tHufflepuff\tRavenclaw\tSlytherin\t' +
			Fore.BLUE + 'Prediction' + Fore.MAGENTA + '\tAssigned House' + Fore.RESET + '\tCorrect?' + Style.RESET_ALL)
		correct_count = 0
		for i, assigned, predicted in zip(indices, Y_labeled.flatten().tolist(), predictions):
			if assigned != '':
				if assigned == predicted:
					correct_count += 1
					correct_str = Fore.GREEN + 'YES' + Fore.RESET
				else:
					correct_str = Fore.RED + 'NO' + Fore.RESET
			else:
				correct_str = '🧙🤷'
				assigned = '(none)        '
			print('%d\t\t%.2f%%\t\t%.2f%%\t\t%.2f%%\t\t%.2f%%\t\t%s\t%s\t%s' % (i,
				house_percent[i][0] * 100, house_percent[i][1] * 100, house_percent[i][2] * 100, house_percent[i][3] * 100,
				Fore.BLUE + predicted + Fore.RESET, Fore.MAGENTA + assigned + Fore.RESET, correct_str))
		if correct_count > 0:
			print('\nCorrectly labeled: %d / %d ( %.2f%% )' % (
				correct_count, sample_count, correct_count / sample_count * 100))
		self.__save_answer(predictions)

	def train_data(self, filename):
		print(Style.BRIGHT + 'Training model for data in ' + Fore.MAGENTA + filename + Fore.RESET + Style.RESET_ALL)
		data_analyzer = DataAnalyzer(filename)
		self.__sample_count = data_analyzer.sample_count
		Y_labeled = data_analyzer.Y_labeled
		self.__X = data_analyzer.X[:, 9:]
		self.__mean_list = [data_analyzer.all_descriptions[i].mean for i in range(9, len(data_analyzer.all_descriptions))]
		self.__stdev_list = [data_analyzer.all_descriptions[i].standard_deviation for i in range(9, len(data_analyzer.all_descriptions))]

		# Apply feature scaling
		for i in range(self.__X.shape[1]):
			self.__X[:, i] = (self.__X[:, i] - self.__mean_list[i]) / self.__stdev_list[i]
		self.__X = np.c_[np.ones(self.__sample_count), self.__X]

		# Find theta for a model that determines GRYFFINDOR or NOT
		print(Style.BRIGHT + Fore.BLUE + 'Running gradient descent to determine GRYFFINDOR or NOT...' + Style.RESET_ALL + Fore.RESET)
		theta_gryffindor = self.__run_gradient_descent(np.where(Y_labeled == 'Gryffindor', 1, 0))
		# Find theta for a model that determines HUFFLEPUFF or NOT
		print(Style.BRIGHT + Fore.BLUE + 'Running gradient descent to determine HUFFLEPUFF or NOT...' + Style.RESET_ALL + Fore.RESET)
		theta_hufflepuff = self.__run_gradient_descent(np.where(Y_labeled == 'Hufflepuff', 1, 0))
		# Find theta for a model that determines RAVENCLAW or NOT
		print(Style.BRIGHT + Fore.BLUE + 'Running gradient descent to determine RAVENCLAW or NOT...' + Style.RESET_ALL + Fore.RESET)
		theta_ravenclaw = self.__run_gradient_descent(np.where(Y_labeled == 'Ravenclaw', 1, 0))
		# Find theta for a model that determines SLYTHERIN or NOT
		print(Style.BRIGHT + Fore.BLUE + 'Running gradient descent to determine SLYTHERIN or NOT...' + Style.RESET_ALL + Fore.RESET)
		theta_slytherin = self.__run_gradient_descent(np.where(Y_labeled == 'Slytherin', 1, 0))
		# Merge all theta in one matrix
		self.__theta = np.c_[theta_gryffindor, theta_hufflepuff, theta_ravenclaw, theta_slytherin]
		self.__save_weights_file()

	'''
	h(X) = sigmoid(X * theta)
	cost = 1 / m * sum( -Y * log(h(X)) - (1 - Y) * log(1 - h(X)) )
	'''
	def __compute_cost(self, theta, Y):
		cost = 1 / self.__sample_count * np.sum(
			np.multiply(-Y, np.log(self.__SIGMOID(self.__X @ theta)))
			- np.multiply(1 - Y, np.log(self.__SIGMOID(1 - (self.__X @ theta)))))
		if self.____VERBOSE:
			print(Fore.BLUE + 'Iteration' + Fore.RESET + ' %3d:\t' % self.iteration +
				Fore.BLUE + 'cost' + Fore.RESET + ' = %.3f' % cost)
		return cost

	'''
	theta = theta - alpha * sum((h(X) - Y) * X)
	'''
	def __run_gradient_descent(self, Y):
		theta = np.zeros((self.__FEATURE_COUNT + 1, 1))
		self.iteration = 0
		cost = self.__compute_cost(theta, Y)
		while True:
			self.iteration += 1
			theta = theta - self.__ALPHA * self.__X.T @ (self.__SIGMOID(self.__X @ theta) - Y)
			old_cost = cost
			cost = self.__compute_cost(theta, Y)
			if cost > old_cost:
			 	raise LogisticRegressionException('learning rate is too high')
			if abs(cost - old_cost) < 1e-6:
				break
		return theta
