# Written by Parth V 
# Disclaimer : I am no expert in python but just a learner. In no way is this code perfect or the most 'pythonic' implementaion 
# It was written for practice and understanding the concepts. Feel free to extend or make it better. Cheers !! 
# www.parthvora.tk

#################################################################################
#                            Removing left recursion                            # 
#                             only direct recursion                             #                                
#################################################################################

# input grammar
grammar = [
    'A->AbBe|Ae|c|d',
    'B->Bz|y',
    'C->d'
]

# removing left recursion
final = {}
counter = 0


def remove(lhs, rhs):
    '''
    Function removes left recursion from grammar given its lhs and rhs
    :param lhs: lhs of grammar
    :param rhs: all the rhs of grammar
    :return: grammar without recursion
    '''
    global counter
    production = lhs
    issues = []
    non_issues = []
    final = []
    rhs = rhs.split('|')
    for item in rhs:
        if item[0] == production:
            issues.append(item)
        else:
            non_issues.append(item)
    for item in issues:
        new = chr(87 + counter)
        counter += 1
        for i in non_issues:
            string = lhs + ' -> ' + i + new + ' | ' + new
            final.append(string)
        string = item[1:]
        new_prod = new + ' -> ' + string + new + ' | ' + '$'
        final.append(new_prod)
    return final


# checking and removing recursion if any
for i, item in enumerate(grammar):
    temp = item.strip().split(sep='->')
    if temp[0] == temp[1][0]:
        mod = remove(temp[0], temp[1])
        grammar[i] = mod

# printing output
for item in grammar:
    print(item)
