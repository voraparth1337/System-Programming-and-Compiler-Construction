# Written by Parth V 
# Disclaimer : I am no expert in python but just a learner. In no way is this code perfect or the most 'pythonic' implementaion 
# It was written for practice and understanding the concepts. Feel free to extend or make it better. Cheers !! 
# www.parthvora.tk

#######################################################
#                  First and Follow                   #    
#                                                     #         
#######################################################

# '%' represents epsilon
g = [
    'S->AB|C',
    'A->D|a|%',
    'B->b',
    'C->%',
    'D->d',
]
first, follow, grammar = {}, {}, {}  # dictionary for each of both

# check if x is terminal or not
check_terminals = lambda x: ord(x) >= 97 and ord(x) <= 122

# check if x is non-terminal or not
check_non_terminals = lambda x: ord(x) >= 65 and ord(x) <= 90


def get_first(symbol):
    '''
    Function returns the first of the given non terminal
    :param symbol: non terminal
    :return: first of non terminal
    '''
    global first
    return first[symbol]


def get_follow(symbol):
    '''
        Function returns the follow of the given non terminal
        :param symbol: non terminal
        :return: follow of non terminal
        '''
    global follow
    return follow[symbol]


# converting grammar into dictionary of arrays
for item in g:
    temp = item.split(sep='->')
    grammar[temp[0]] = temp[1].split(sep='|')


def follow_recursion(left, right, index, me, f):
    '''
    Function uses recursion to get follow of a non terminal, based on three conditions
    :param left: lhs of the production
    :param right: rhs of the production
    :param index: index of occurrence 
    :param me: non terminal whose follow is to be found
    :param f: array containing follow
    :return: follow array of the non terminal
    '''
    global first, follow
    # if i am last and lhs of prod is me then my follow will be my follow like S->S
    if index == len(right) - 1 and me == left:
        return f
    # if i am last and lhs of prod is not me
    # B->AS follow S is follow of B
    elif index == len(right) - 1 and me != left:
        for item in get_follow(left):
            f.append(item)
    else:
        # easiest to check condition A->ASB follow of A will be first of S, in case S is epsilon, remove it and call
        right_side = right[index + 1]
        first_of_right_side = get_first(right_side)
        for j in first_of_right_side:
            if j != '%':
                f.append(j)
            else:
                # cant change string, so turning it into list, editing and then putting it back together
                temp_variable = list(right)
                temp_variable.pop(index + 1)  # removing the epsilon production
                right = ''.join(temp_variable)
                f = follow_recursion(left, right, index, me, f)
    return f


# this loop is like a first pass as it notes down all those firsts that are super easy to find
# and are not dependent on other grammar for their value
for item in grammar:
    f = []
    for each_item in grammar[item]:
        if check_terminals(each_item[0]):
            f.append(each_item)
    first[item] = f

# pass 2 for finding first , where first term in production is a non terminal, whose first
# will be the first of non terminal on lhs
for item in grammar:
    t = []
    for each_item in grammar[item]:
        f = each_item[0]
        if check_non_terminals(f):
            for sub_item in get_first(f):
                t.append(sub_item)
        else:
            t.append(f)
    first[item] = t

# printing first
print('*** First ***')
for item in first:
    print(item, first[item])

# ok now the tough part :p
for i in grammar.keys():
    t = []
    f = []
    if i == 'S':
        follow[i] = ['$']
    else:
        follow[i] = []
    for key, value in grammar.items():
        for each_item in value:
            if i in each_item:
                t.append([key, each_item])
    for item in t:
        left = item[0]
        right = item[1]
        index = right.index(i)
        f_temp = follow_recursion(left, right, index, i, [])
        for item in f_temp:
            f.append(item)

    for item in f:
        follow[i].append(item)

print('*** Follow ***')
for item in follow:
    t = set(follow[item])
    print(item, t)
