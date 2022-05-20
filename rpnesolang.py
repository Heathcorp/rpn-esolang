# RPN Esolang interpreter
# usage: python rpnesolang.py <file>

import sys
import re

from matplotlib import offsetbox

# main stack memory
stack = []
# program memory
pc = 0
lines = []
# loop stack
loops = []
skipLoop = False
loopToSkip = -1

def handle_instruction(line: str):
	global skipLoop
	global pc
	global loopToSkip
	if re.search('^(#.*)?$', line) and not skipLoop:
		# comment or empty line, ignore
		return False

	elif re.search('^-?[0-9]+$', line) and not skipLoop:
		# integer, push to stack
		stack.append(int(line))

	elif re.search('^-?[0-9]+\.?[0-9]+$', line) and not skipLoop:
		# floating point number, push to stack
		stack.append(float(line))

	elif re.search('^\'.*\'$', line) and not skipLoop:
		# string, parse and push to stack
		stack.append(str(line[1:len(line) - 2]))

	elif re.search('^\+$', line) and not skipLoop:
		# addition
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 + value2)

	elif re.search('^\-$', line) and not skipLoop:
		# subtraction
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 - value2)

	elif re.search('^\*$', line) and not skipLoop:
		# multiplication
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 * value2)

	elif re.search('^\/$', line) and not skipLoop:
		# division
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 / value2)

	elif re.search('^=$', line) and not skipLoop:
		# equality
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 == value2)

	elif re.search('^>$', line) and not skipLoop:
		# more than
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 > value2)

	elif re.search('^<$', line) and not skipLoop:
		# less than
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 < value2)

	elif re.search('^>=$', line) and not skipLoop:
		# more than or equal
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 >= value2)

	elif re.search('^<=$', line) and not skipLoop:
		# less than or equal
		value2 = stack.pop()
		value1 = stack.pop()
		stack.append(value1 <= value2)

	# everything is highly experimental, but the following instructions especially
	elif re.search('^\[[0-9]+\]$', line) and not skipLoop:
		# copy nth stack element (from the top down)
		offset = int(line[1:len(line) - 2])
		value = stack[len(stack) - 1 - offset]
		stack.append(value)

	elif re.search('^<<$', line) and not skipLoop:
		# print and pop the element at the top of the stack
		value = stack.pop()
		print(value)

	elif re.search('^{$', line):
		# pops top of stack, if it was 0 then skip to the closing brace
		loops.append(pc)
		if not skipLoop:
			value = stack.pop()
			if value == 0:
				skipLoop = True
				loopToSkip = pc
			
				

	elif re.search('^}$', line):
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

	return True


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('No file specified!')
		exit(-1)

	filename = sys.argv[1]

	with open(filename, 'r') as file:
		line = file.readline()

		while line:
			lines.append(line)
			line = file.readline()

		while pc < len(lines):
			if handle_instruction(lines[pc]): pass #print(stack, loops, skipLoop, pc)
			pc += 1
