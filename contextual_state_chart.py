from collections import OrderedDict as od
def makeOrderedDicts(next_states):

	case_state_case_entries = od()
	#print(next_states)
	for cases_ in next_states[1:][0]:
		state_case_entries = od()
		#print(cases_)

		for case_ in cases_[1:]:
			#print(case_)
			for state_case in case_:
				state = state_case[0]
				case__ = state_case[1]

				state_case_entries[state] = case__
		case_state_case_entries[cases_[0]] = state_case_entries
	return case_state_case_entries
def makedTupleOfOrderedDicts(lists):


	'''
	structure example
	['value_ignore' , 	 [
		['next', [['0',[['reset_for_next_round_of_input','0'], ['op_ignore','0'], ['value_ignore', 'valid_op']]], ['valid_op', [['op','0']]]]]],
		['children',  [['0',[]], ['valid_op', []]]],
		['functions' , [['0', parseChar], ['valid_op', validOp]]]]
	'''
	#print(lists)
	state_name = lists[0]
	#print(lists)
	next_states = lists[1][0]

	children = lists[1][1]
	functions = lists[1][2]
	#print(lists[1][2])
	parents = lists[1][3]
	#print('parents')
	#print(parents)

	#print('make dict')
	next_states_case_state_case_entries = makeOrderedDicts(next_states)

	children_case_state_case_entries = makeOrderedDicts(children)
	#print('parents')
	parents_case_state_case_entries = makeOrderedDicts(parents)
	#print('done with parents')
	#print(parents_case_state_case_entries)
	case_function_entries = od()

	for case_function in functions[1]:

		case_ = case_function[0]
		function = case_function[1]
		case_function_entries[case_] = function


	return (state_name, od([('next', next_states_case_state_case_entries), ('children', children_case_state_case_entries), ('functions', case_function_entries),
	('parents', parents_case_state_case_entries)]))
'''
result for makedTupleOfOrderedDicts
expects and actual
('value_ignore', OrderedDict([
		('next', OrderedDict([('0', OrderedDict([('reset_for_next_round_of_input', '0'), ('op_ignore', '0'), ('value_ignore', 'valid_op')])), ('valid_op', OrderedDict([('op', '0' )])  )])),
		('children', OrderedDict([('0', OrderedDict()), ('valid_op', OrderedDict())])),
		('functions', OrderedDict([('0', <function <lambda> at 0x103d0a0d0>), ('valid_op', <function <lambda> at 0x103d0a158>)]))]))
'''

def doesNextStatesExist(next_states):

	return len(next_states) > 0 and len(next_states[0]) > 0


def isParent(children):

	return children != od()



def hasParent(graph, state, case_):
	#print(state, case_)
	#print(graph['node_graph3'][state]['parents'])
	return len(graph['node_graph3'][state]['parents'][case_].keys()) > 0

class ChildParent():
	def __init__(self, child, parent):
		self.child = child
		self.parent = parent


def getIndents(count):

	indent = ''

	while (count > 0):

		indent += '    '
		count -= 1

	return indent


def printStack(bottom):

	tracker = bottom[0]
	stack = []
	print('start stack')
	while (tracker != None):

		stack.append(tracker.child)
		tracker = tracker.parent

	for i, item in enumerate(stack):

		print(stack[i])
	print('end stack')



def isBottomAtTheParentOfCurrentState(parent_cases, bottom_state, bottom_case):

	for p, parent_case in enumerate(parent_cases):

		parent = parent_cases[p][0]

		parent_case = parent_cases[p][1]

		if(bottom_state == parent and bottom_case == parent_case):

			return True


	return False

def getNextStates(tracker, continuing_next_states, indents, graph):


	#print(tracker.parent, tracker.child)
	state1 = tracker.child[0]
	case1 = tracker.child[1]
	#print('printing stack')
	# todo: need to delete the bottom of the list as we ascend it, not ignore it
	# for python tracker.parent is to what javascript is to tracker
	while (tracker.parent != None and len(continuing_next_states) == 0):

		indents -= 1
		tracker = tracker.parent
		state1 = tracker.child[0]
		case1 = tracker.child[1]
		#print(tracker)
		#print(state1, case1)			

		# need to exit the main loop
		if (state1 == 'root'):

			return [tracker, [], indents]


		continuing_next_states = [list(a) for a in graph['node_graph3'][state1]['next'][case1].items()]
		# print(continuing_next_states)

	return [tracker, continuing_next_states, indents]


def makeNextStates(next_states):
	new_next_states = []

	next_states = [list(a) for a in next_states]

	for n, next_state in enumerate(next_states):

		new_next_states.append([next_states[n][0], next_states[n][1]])




	return new_next_states

def printLevel(graph, state, case_, indents, m, chosen_level):

	if (indents == chosen_level):

		print(getIndents(indents), '|'+ state + '|', case_, 'passed', 'i', '|' + graph['input'][m] + '|', m)




def printLevels(graph, state, case_, indents, m, chosen_level):

	if (indents >= chosen_level):

		print(getIndents(indents), '|'+ state + '|', case_, 'passed', 'i', '|' + graph['input'][m] + '|', m)





def printLevelsBounds(graph, state, case_, indents, m, input_length, chosen_start_level, chosen_end_level):


	print(getIndents(indents), '('+  '\'' + state + '\'' + ',' , case_ + ',', 'f=' + graph['node_graph3'][state]['functions'][case_].__name__ + ',', str(indents) + ')')#, '|' + graph['input'][m] + '|'/*,'i ='*/, m/*, input_length*/)
		#console.log()





def printVarStore(graph):

	m = graph['input']
	return '|' + graph['input'][m] + '|'


def visit(node, graph, indents, debug):
	# assume graph is nested lists
	# does depth first tranversal for each subgraph(each subgraph is a state name that has children)
	# does breath first traversal for within each subgraph
	#print("got here")
	#print(graph['node_graph2'])
	#[print(a) for a in graph['node_graph2']]
	graph['node_graph3'] = od([ makedTupleOfOrderedDicts(a) for a in graph['node_graph2']])
	#print(graph['node_graph2'])
	x = node[0]
	y = node[1]
	next_states = [node]
	action = {}
	bottom = []
	# assumes [state, case_] actually runs
	parent = ChildParent(['root', 0], None)
	bottom.append(parent)
	ii = 0
	#console.log(getIndents(indents), 'start state', node)
	while(len(next_states) != 0):

		#print(ii)

		if(ii == 200):
			#exit(1)
			pass


		#print(getIndents(indents), 'next_states', next_states)

		state = ''
		case_ = 0
		state_changed = False

		# machine will stop running if all have failed(there must be more than 0 states for this to be possible) or error state runs
		# loop ends after the first state passes
		j = 0
		while(j < len(next_states)):

			#print('next_states', next_states)
			state = next_states[j][0]
			case_ = next_states[j][1]
			#print(cases)
			# for same next state at multiple cases
			#for case__ in cases:
			#	case_ = case__
			#print('|' + state + '|', case_)

			maybe_parent = graph['node_graph3'][ state ]['children'][ case_ ]
			did_function_pass = graph['node_graph3'][state]['functions'][case_]([state, case_], graph)
			#print(did_function_pass)
			if (did_function_pass):
				#print(state, case_)
				#print('next states', graph['node_graph2'][state]['next'][case_])
				#print(maybe_parent)

				#if (state == 'error'):

				#	print('you have invalid input')
				#	exit()

				# this case is for getting the children from the parent
				# needs to always check before the isParent
				if (hasParent(graph, state, case_)):
					# x = (lowest_bottom, indent_number)
					# push the state to the bottom if bottom happens to be one of state's parents
					# only checks the state and not the case
					bottom_state = bottom[0].child[0]
					bottom_case = bottom[0].child[1]

					parent_cases = [list(a) for a in graph['node_graph3'][state]['parents'][case_].items()]
					#print('next_states', parent_cases)
					parent_cases = makeNextStates(parent_cases)
					if (isBottomAtTheParentOfCurrentState(parent_cases, bottom_state, bottom_case)):

						new_parent = ChildParent([state, case_], bottom[0])
						# link passing state to its parent on bottom of stack, extending the stack by 1, vertically
						bottom[0] = new_parent
						indents += 1
						#print('indent increasing', indents)



				#print('maybe_parent', maybe_parent, isParent(maybe_parent))

				# for when passing the current state(it is in the current next states) has a child(called next states)
				if (isParent(maybe_parent)):
					# x = (lowest_bottom, next_states)
					#print('here')
					# add passing state horizontally
					bottom[0].child = [state, case_]

					# getting the children
					children = [list(a) for a in graph['node_graph3'][state]['children'][case_].items()]
					#print('next_states', children)
					children = makeNextStates(children)
					next_states = []
					for i, child in enumerate(children):

						next_states.append(children[i])

					if debug:

						m = graph['i']
						printLevelsBounds(graph, state, case_, indents, m, len(graph['input']), 0, -1)




				# for when passing the current state(it is in the current next states) does not have a child but has neighbor states(called next states)
				else:
					# x = (next_states)
					# x_total = (lowest_bottom, next_states, indent_number)
					# there is a problem with how dict_items is being used

					#print(graph['node_graph2'][state]['next'])
					next_states = [list(a) for a in graph['node_graph3'][state]['next'][case_].items()]


					next_states = makeNextStates(next_states)
					#print('next_states', next_states)
					if debug:
						m = graph['i']
						printLevelsBounds(graph, state, case_, indents, m, len(graph['input']), 0, -1)
					# add passing state horizontally
					bottom[0].child = [state, case_]



				state_changed = True

				break


			j += 1
			#if state_changed:
			#	break

		#printStack(bottom)
		# if a child fails and
		#print(next_states, state_changed)
		# hit end state at any level below top level
		if (len(next_states) == 0):

			# x_total = (lowest_bottom, next_states, indent_number)

			# have linked list representing the stack
			# first item is in bottom[0]

			# travel up stack untill either hits root or hits neighbors of a prev visited level
			tracker_continuing_next_states_indents = getNextStates(bottom[0], next_states, indents, graph)
			#print(tracker_continuing_next_states_indents)
			tracker = tracker_continuing_next_states_indents[0]
			continuing_next_states = tracker_continuing_next_states_indents[1]
			indents = tracker_continuing_next_states_indents[2]


			bottom[0] = tracker
			next_states = continuing_next_states
			#print('next_states 5', next_states)

			state_changed = True
			# might not actually be true ever
			'''
			/*
			if (tracker == null)
				console.log('done runing machine')
			*/
			'''


		#print( )
		# if all fail then all will be rerun unless this condition is here
		if(not state_changed and len(next_states) > 0):
			# all next_states failed so this level cannot be finished
			# travel up like before but choose the next child after the tracker

			print('error at ')
			print(getIndents(indents), next_states, 'on')
			print(getIndents(indents), '('+  '\'' + state + '\'' + ',' , case_ + ',', 'f=' + graph['node_graph3'][state]['functions'][case_].__name__ + ',', str(indents) + ')')
			break

			#print(next_states, 'have failed so your state machine is incomplete')
			#exit()
		#if(not state_changed):
		#	print("we are screwed", len(next_states))
		ii += 1


	#print(getIndents(indents), '1state machine is finished', '|'+ state + '|', case_)
	#print(getIndents(indents), 'exit visit', node)
	#print(graph)
