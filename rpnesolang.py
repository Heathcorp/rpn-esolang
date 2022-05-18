# RPN Esolang interpreter
# usage: python rpnesolang.py <file>

import sys
import re

def handle_instruction(stack: list, line: str):
	
	if re.search('^-?[0-9]+$', line):
		# integer, push to stack
		stack.append(int(line))

	elif re.search('^-?[0-9]+(\.?[0-9]+)?$', line):
		# floating point number, push to stack
		stack.append(float(line))

	elif re.search('^\'.*\'$', line):
		# string, parse and push to stack
		stack.append(str(line[1:len(line) - 2]))

	elif re.search('^\+$', line):
		# addition
		value1 = stack[len(stack) - 2]
		value2 = stack[len(stack) - 1]
		stack.pop()
		stack.pop()
		stack.append(value1 + value2)

	elif re.search('^\-$', line):
		# subtraction
		value1 = stack[len(stack) - 2]
		value2 = stack[len(stack) - 1]
		stack.pop()
		stack.pop()
		stack.append(value1 - value2)

	elif re.search('^\*$', line):
		# multiplication
		value1 = stack[len(stack) - 2]
		value2 = stack[len(stack) - 1]
		stack.pop()
		stack.pop()
		stack.append(value1 * value2)

	elif re.search('^\/$', line):
		# division
		value1 = stack[len(stack) - 2]
		value2 = stack[len(stack) - 1]
		stack.pop()
		stack.pop()
		stack.append(value1 / value2)

	elif re.search('^=$', line):
		# equality
		value1 = stack[len(stack) - 2]
		value2 = stack[len(stack) - 1]
		stack.pop()
		stack.pop()
		stack.append(value1 == value2)

	elif re.search('^>$', line):
		# more than
		value1 = stack[len(stack) - 2]
		value2 = stack[len(stack) - 1]
		stack.pop()
		stack.pop()
		stack.append(value1 > value2)

	elif re.search('^<$', line):
		# less than
		value1 = stack[len(stack) - 2]
		value2 = stack[len(stack) - 1]
		stack.pop()
		stack.pop()
		stack.append(value1 < value2)

	elif re.search('^>=$', line):
		# more than or equal
		value1 = stack[len(stack) - 2]
		value2 = stack[len(stack) - 1]
		stack.pop()
		stack.pop()
		stack.append(value1 >= value2)

	elif re.search('^<=$', line):
		# less than or equal
		value1 = stack[len(stack) - 2]
		value2 = stack[len(stack) - 1]
		stack.pop()
		stack.pop()
		stack.append(value1 <= value2)


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('No file specified!')
		exit(-1)

	filename = sys.argv[1]

	# main memory stack
	stack = []

	with open(filename, 'r') as file:
		line = file.readline()

		while line:
			handle_instruction(stack, line)
			print(stack)

			line = file.readline()