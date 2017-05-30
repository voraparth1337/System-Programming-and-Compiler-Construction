# Written by Parth V 
# Disclaimer : I am no expert in python but just a learner. In no way is this code perfect or the most 'pythonic' implementaion 
# It was written for practice and understanding the concepts. Feel free to extend or make it better. Cheers !! 
# www.parthvora.tk

# implementation of a recursive descent parser

# input grammar
grammar = [('E', 'x+T'), ('T', '(E)'), ('T', 'x')]

pointer = 0
# can be changed to input prompt
string = 'x+(x+x)$'


def function_E():
    '''
    Function to evaluate grammar for productions of E
    :return: True if string follows grammar, else false 
    '''
    global string, pointer
    if string[pointer] == 'x':
        pointer += 1
        if string[pointer] == '+':
            pointer += 1
            if function_T():
                return True
    return False


def function_T():
    '''
    Function to evaluate grammar for productions of E
    :return: True if string follows grammar, else false  
    '''
    global string, pointer
    if string[pointer] == '(':
        pointer += 1
        if function_E():
            if string[pointer] == ')':
                return True
    elif string[pointer] == 'x':
        pointer += 1
        return True

    return False


if function_E():
    print('Accepted')
else:
    print('Nope')
