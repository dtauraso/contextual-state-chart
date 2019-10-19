import sys
sys.path.insert(1, '/Users/David/Documents/github/contextual-state-chart')
import contextual_state_chart as hcssm

from collections import OrderedDict as od


def incrementLeftCount(node, var_store):

	i = var_store['i']
	input_ = var_store['input']
	if i >= len(input_):
		return False
	# increments the left count
	if input_[i] == '(':
		var_store['left_count'] += 1
		var_store['i'] += 1
		return True
	return False

def incrementRightCount(node, var_store):



	i = var_store['i']
	input_ = var_store['input']
	if i >= len(input_):
		return False

	# increments the right count
	if input_[i] == ')':
		var_store['right_count'] += 1
		var_store['i'] += 1
		return True
	return False

def leftSideEqualsRightSide(node, var_store):

	# is left count == right count
	left = var_store['left_count']
	right = var_store['right_count']
	if left == right:
		print('the parense are balanced')
		print(left, right)
	return left == right

def leftSideDoesNotEqualRightSide(node, var_store):

	# is left count != right count
	left = var_store['left_count']
	right = var_store['right_count']
	if left != right:
		#print('the parense are not balanced')
		#print(left, right)
		return True

	return False#left != right

def returnTrue(node, var_store):
	return True

def leftHeavy(node, var_store):
	left = var_store['left_count']
	right = var_store['right_count']
	if left > right:
		print('there are not enough right parenthesis')
		print(str(left - right) , 'right parenthesis are missing')

		return True
	return False

def rightHeavy(node, var_store):
	left = var_store['left_count']
	right = var_store['right_count']
	if left < right:
		print('there are not enough left parenthesis')
		print(str(right - left) , 'left parenthesis are missing')
		return True
	return False

def removeWhiteSpace(node, var_store):

	parenthesis = ''
	for i in var_store['input']:
		if i is not ' ':
			parenthesis += i
	var_store['input'] = parenthesis
	return True
def isWord(node, var_store):


	i = var_store['i']
	input_ = var_store['input']
	if i >= len(input_):
		return False
	letter = ''
	if (input_[i] != '(' and input_[i] != ')'):

		# assuming this will determine a letter
		while i < len(input_) and ((input_[i] >= 'A' and input_[i] <= 'Z') or (input_[i] >= 'a' and input_[i] <= 'z') or input_[i] == '_' ):

			letter += input_[i]
			i += 1

		if len(letter) > 0:

			print(letter)
		var_store['i'] = i
		return True
	return False

def isNumber(node, var_store):

	i = var_store['i']
	input_ = var_store['input']
	if i >= len(input_):
		return False
	collected_digit = ''
	if (input_[i] != '(' and input_[i] != ')'):



		if i < len(input_) and (input_[i] >= '0' and input_[i] <= '9'):
			#print(input_[i])
			collected_digit += input_[i]
			i += 1
		if len(collected_digit) > 0:
			print(collected_digit)

		var_store['i'] = i
		return True
	return False

def notWordNotNumber(node, var_store):
	return not isWord(node, var_store) and not isNumber(node, var_store)



# we want to know if the parenthesis are balanced
# if the parenthesis are not balanced we want to know what side(left or right) has a missing parense
# we also want to know how many of the missing side are missing
# we also want to have a word optioanlly detected after '('
# (word##())
# (#word#())
# (word##)
# (#word#)
# ()

'''
	stuff
		word0, #1, #2
		#0, word1, #3
		null
'''
# make a version that only does these cases
# (word##)
# (#word#)
# ()

# then have a separated one of balanced parenthesis
vars = {
# missing 1 )
	'input' : '(((((Im_a_word56  (  ))  ((( ))))((( )))))()()()',#'(((((I\'m_a_word) (  ))  ((im_another_word( ))))((( )))))()()()',
	'i' : 0,
	# don't need 2 counts, but you can see the components you are counting
	'left_count' : 0,
	'right_count' : 0,

	# show how to do this with 1 count variable



	# this control graph uses string for states and cases
	'node_graph2' : [


		# current state -> [current_context [list of (next_state, next_context)]]

		#text template:

		#[	'name', [
		#	['next', [['0', [ <next state would be here> ]]]],
		#	['children',  [['0', [ <child would be here> ]]]],
		#	['functions', [['0', returnTrue ]]]]],
		# <child case would be here> = [ 'child_state', 'child_case']
		# <next state would be here> = [ 'next_state', 'next_state_case']

		# the style of choosing which next (state, case) to run is done using the if elif else style
		# if
		# elif
		# elif
		# else

		# next states are these ['(','0'], [')','0'], ['error', '0']
		['remove_white_space', [
			['next', [['0', [['(', '0' ] ]]]],
			['children',  [['0', [ ]]]],
			['functions', [['0', removeWhiteSpace ]]],
			['parents', [   ['0', [['root', '0']]  ]   ] ]
			# {'0':{'root': '0'}}
			]],

		['(' , [
			# heavyness, not_heavy will only be checked after all the characters are looked at
			['next', [['0', [['(','0'], ['stuff', '0'] ]]]],
			['children',  [['0', [  ]]]],
			['functions', [['0', incrementLeftCount ]]],
			['parents', [   ['0', []  ]   ] ]

			]],

		['stuff', [
			['next', [['0', [ ['(','0'], [')','0'], ['heavyness', '0']]]]],
			['children',  [['0', [ ['word', '0'], ['#', '0'], ['null', '0'] ]]]],
			['functions', [['0', returnTrue ]]],
			['parents', [   ['0', []  ]   ] ]

			]],


			['word', [
				['next', [['0', [ ['#', '1'] ]], ['1', [ ['#', '3']  ]]]],
				['children',  [['0', [  ]], ['1', []] ]],
				['functions', [['0', isWord ], ['1', isWord]]],
				['parents', [   ['0', [['stuff', '0']]  ], ['1', []]   ] ]
				# {'0':{'stuff': '0'}, '1':{}}
				]],

			['#', [
				['next', [['0', [ ['word', '1'] ]],    ['1', [ ['#', '2']  ]], ['2', []], ['3', []] ]],
				['children',  [['0', [  ]], ['1', []], ['2', []], ['3', []] ]],
				['functions', [['0', isNumber ], ['1', isNumber], ['2', isNumber], ['3', isNumber] ]],
				['parents', [   ['0', [['stuff', '0']]  ], ['1', []], ['2', []], ['3', []]   ] ]
				# {'0':{'stuff': '0'}, '1':{}, '2':{}, '3':{}}
				]],

			['null', [
				['next', [['0', [  ]]]],
				['children',  [['0', [  ]]]],
				['functions', [['0', notWordNotNumber ]]],
				['parents', [   ['0', [['stuff', '0']]  ]   ] ]
				# {'0':{'stuff': '0'}}
				]],


		[')' , [
			['next', [['0', [['(','0'], [')','0'], ['not_heavy', '0'], ['heavyness', '0']]]]],
			['children',  [['0', []]]],
			['functions', [['0', incrementRightCount ]]],
			['parents', [   ['0', []  ]   ] ]

			]],

		['not_heavy', [
			['next', [['0', []]]],
			['children',  [['0', []]]],
			['functions', [['0', leftSideEqualsRightSide ]]],
			['parents', [   ['0', []  ]   ] ]

			]],

		['heavyness', [
			['next', [['0', [] ]]],
			['children',  [['0', [['left_heavy', '0'], ['right_heavy', '0']] ]]],
			['functions', [['0', leftSideDoesNotEqualRightSide ]]],
			['parents', [   ['0', []  ]   ] ]

			]],

			['left_heavy', [
				['next', [['0', [ ] ]]],
				['children',  [['0', []]]],
				['functions', [['0', leftHeavy ]]],
				['parents', [   ['0', [['heavyness', '0']]  ]   ] ]
				# {'0':{'heavyness': '0'}}
				]],

			['right_heavy', [
				['next', [['0', [ ] ]]],
				['children',  [['0', []]]],
				['functions', [['0', rightHeavy ]]],
				['parents', [   ['0', [['heavyness', '0']]  ]   ] ]

				]]
		]
	}

hcssm.visit(['remove_white_space', '0'], vars, 0, True)
# these are things you can do with state machines with some things you may have seen from ravi's class
# a^nb^n where n >= 1
# using this make one that looks like this a^nb^nc^n where n >= 1
# see if you can extend this to a^n....
# need a primary counter and a secondary counter that you can reset each round

print('done w machine')
