# RPN Esolang interpreter
# usage: python rpnesolang.py <file>

import sys
import re

# main stack memory
stack = []
# program memory
pc = 0
lines = []
# loop stack
loops = []
skipLoop = False
loopToSkip = -1
# labels and their pcs
labels = {}
# function call stack: list[programCounter]
calls = []
skipFunctionDef = False

def handle_instruction(line: str):
	global skipLoop
	global pc
	global loopToSkip
	global skipFunctionDef

	if re.search('^(#.*)?$', line) and not (skipLoop or skipFunctionDef):
		# comment or empty line, ignore
		return False

	elif re.search('^-?[0-9]+$', line) and not (skipLoop or skipFunctionDef):
		# integer, push to stack
		stack.append(int(line))

	elif re.search('^-?[0-9]+\.[0-9]+$', line) and not (skipLoop or skipFunctionDef):
		# floating point number, push to stack
		stack.append(float(line))

	elif re.search('^\'.*\'$', line) and not (skipLoop or skipFunctionDef):
		# string, parse and push to stack
		text = str(line[1:len(line) - 1])
		text = text.replace('\\n', '\n')
		stack.append(text)

	elif re.search('^\+$', line) and not (skipLoop or skipFunctionDef):
		# addition
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 + value2)

	elif re.search('^\-$', line) and not (skipLoop or skipFunctionDef):
		# subtraction
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 - value2)

	elif re.search('^\*$', line) and not (skipLoop or skipFunctionDef):
		# multiplication
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 * value2)

	elif re.search('^\/$', line) and not (skipLoop or skipFunctionDef):
		# division
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 / value2)

	elif re.search('^=$', line) and not (skipLoop or skipFunctionDef):
		# equality
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 == value2)

	elif re.search('^>$', line) and not (skipLoop or skipFunctionDef):
		# more than
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 > value2)

	elif re.search('^<$', line) and not (skipLoop or skipFunctionDef):
		# less than
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 < value2)

	elif re.search('^>=$', line) and not (skipLoop or skipFunctionDef):
		# more than or equal
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 >= value2)

	elif re.search('^<=$', line) and not (skipLoop or skipFunctionDef):
		# less than or equal
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 <= value2)

	elif re.search('^%$', line) and not (skipLoop or skipFunctionDef):
		# modulo
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 % value2)

	# everything is highly experimental, but the following instructions especially
	elif re.search('^copy$', line) and not (skipLoop or skipFunctionDef):
		# copy nth stack element (from the top down)
		offset = stack.pop()
		value = stack[len(stack) - 1 - offset]
		stack.append(value)

	elif re.search('^<<$', line) and not (skipLoop or skipFunctionDef):
		# print and pop the element at the top of the stack
		value = stack.pop()
		print(value, end='')

	elif re.search('^>>$', line) and not (skipLoop or skipFunctionDef):
		# get an input line and place at the top of stack
		# parse it as a number if it looks like one
		text = input()
		value = text
		if re.search('^-?[0-9]+$', text):
			# integer
			value = int(text)
		elif re.search('^-?[0-9]+\.[0-9]+'):
			# float
			value = float(text)
		stack.append(value)

	elif re.search('^\[$', line) and not skipFunctionDef:
		# pops top of stack, if it was 0 then skip to the closing brace
		loops.append(pc)
		if not skipLoop:
			value = stack.pop()
			if value == 0:
				skipLoop = True
				loopToSkip = pc

	elif re.search('^\]$', line) and not skipFunctionDef:
		# pops top of stack, if it was not 0 then go back to the opening brace
		loopStart = loops.pop()
		if not skipLoop:
			value = stack.pop()
			if value != 0:
				pc = loopStart
				loops.append(loopStart)

		elif loopToSkip == loopStart:
			# reached the end of the skip
			loopToSkip = -1
			skipLoop = False

	elif re.search('^\w+:$', line) and not (skipLoop or skipFunctionDef):
		# goto label definition for functions
		label = line[:-1]
		labels[label] = pc
		skipFunctionDef = True

	elif re.search('^call \w+$', line) and not (skipLoop or skipFunctionDef):
		# call the function
		label = line[5:]
		calls.append(pc)
		pc = labels[label]

	elif re.search('^return$', line) and not skipLoop:
		# return
		if skipFunctionDef:
			skipFunctionDef = False
		else:
			pc = calls.pop()

	return True


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('No file specified!')
		exit(-1)

	filename = sys.argv[1]

	with open(filename, 'r') as file:
		rawlines = file.read().splitlines()

		for line in rawlines:
			lines.append(line)
			line = file.readline()

		while pc < len(lines):
			if handle_instruction(lines[pc]): pass #print(pc, calls, stack, loops, skipLoop, skipFunctionDef)
			pc += 1
