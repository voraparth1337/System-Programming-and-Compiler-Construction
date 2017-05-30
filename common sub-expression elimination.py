# Written by Parth V
# Disclaimer : I am no expert in python but just a learner. In no way is this code perfect or the most 'pythonic' implementaion
# It was written for practice and understanding the concepts. Feel free to extend or make it better. Cheers !!
# www.parthvora.tk

###############################################
#        Common Subexpression Elimination     #
#                                             #
###############################################
import re

operator = re.compile('\)([\+\-\*\/])')
counter = 1
opr = ['+', '-', '*', '/']

exp_reg = {}
# input string
string = 'z = (a+b)*(a+b)*(d+b)/c;'

# cleaning input
string = string.replace('\n', '').replace(' ', '').replace(';', '')

split_string = string.split(sep='=')

lhs = split_string[0]
rhs = split_string[1]

l = re.split(operator, rhs)

# completing braces
for item in l:
    if '(' in item:
        l.insert(l.index(item), item + ')')
        l.remove(item)

# checking for sub expressions
for item in l:
    if item not in exp_reg.keys() and item not in opr:
        exp_reg[item] = counter
        counter += 1

# adding declarations for sub expressions
for index, item in enumerate(l):
    if item in exp_reg.keys():
        l[index] = 't' + str(exp_reg[item])

# final output
for key, values in exp_reg.items():
    print('float t' + str(values) + ' = ' + str(key) + ';')
print(lhs + '=' + ''.join(l) + ';')
