# (☞ﾟヮﾟ)☞  predict.py data.csv weights.dat

from logistic_classifier import LogisticClassifier
from exceptions import ParserException, LogisticRegressionException

from colorama import Fore, Back, Style
import sys

def main():
	# check argv
	if len(sys.argv) != 3:
		print('usage: ' + Fore.RED + 'python3' + Fore.BLUE + ' predict.py ' + Fore.RESET + 'data_file.csv weights.dat')
		sys.exit(-1)
	data_file = sys.argv[1]
	weights_file = sys.argv[2]
	try:
		model = LogisticClassifier(weights_file)
		model.predict_data(data_file)
	except IOError as e:
		print(Style.BRIGHT + Fore.RED + 'I/O Error: ' + Style.RESET_ALL + Fore.RESET + str(e))
	except ParserException as e:
		print(Style.BRIGHT + Fore.RED + 'ParserException: ' + Style.RESET_ALL + Fore.RESET + str(e))
	except LogisticRegressionException as e:
		print(Style.BRIGHT + Fore.RED + 'Logistic Regression Exception: ' + Style.RESET_ALL + Fore.RESET + str(e))

if __name__ == '__main__':
	main()
