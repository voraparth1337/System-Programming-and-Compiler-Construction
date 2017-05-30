# Written by Parth V
# Disclaimer : I am no expert in python but just a learner. In no way is this code perfect or the most 'pythonic' implementaion
# It was written for practice and understanding the concepts. Feel free to extend or make it better. Cheers !!
# www.parthvora.tk

# Implementation of operator precedence parser using the algortihm from the 'Dragon book'
import sys

# stack implementation
class Stack:
    def __init__(self):
        self.array = []

    def push_stack(self,character):
        self.array.append(character)

    def pop_stack(self):
        return self.array.pop()

    def look_stack(self):
        return self.array[-1]

# operator precendece table for 4 operators
operator_table = [
    ['X','i','+','*','$'],
    ['i','#','>','>','>'],
    ['+','<','>','<','>'],
    ['*','<','>','>','>'],
    ['$','<','<','<','#']
]

operators = ['+','*']
# can be changed to input prompt
input_string = 'i+i*i*i$'

print('Input String is ' + input_string)

#stack initialization and pushing $ onto stack
stack = Stack()
stack.push_stack('$') 

output = []

counter = 0

temp_row = [ x[0] for x in operator_table ]
temp_column = operator_table[0]
temp_list = list(input_string)

# Checking for a valid input string
for i in range(len(temp_list)-2):
    if temp_list[i] in operators and temp_list[i+1] in operators:
        print('Invalid String')
        sys.exit()

print('Operator table')
for i in operator_table:
    print(i)

# main algorithm implementaion,
# push on '<' or '='
# pop on '>'
# # indicates error 
while True:
    top_stack = stack.look_stack()
    character = input_string[counter]
    index_stack = temp_row.index(top_stack)
    charcter_stack = temp_column.index(character)
    print('String pointer ' + input_string[counter])
    print('Stack top ' + stack.look_stack())
    if operator_table[index_stack][charcter_stack] == '>':
        print('From operator table ">", poping ' + stack.look_stack())
        output.append(stack.pop_stack())
    if operator_table[index_stack][charcter_stack] == '<':
        print('From operator table "<", pushing ' + input_string[counter])
        stack.push_stack(input_string[counter])
        counter+=1
    if operator_table[index_stack][charcter_stack] == '#' and stack.look_stack() == '$' and input_string[counter] == '$':
        print('Success')
        print('Output is ' + str(output))
        break
        sys.exit()
    if operator_table[index_stack][charcter_stack] == '#':
        print('Error')
        print('Stack top ' + stack.look_stack())
        print('Input pointer at ',input_string[counter])
        break
        sys.exit()


