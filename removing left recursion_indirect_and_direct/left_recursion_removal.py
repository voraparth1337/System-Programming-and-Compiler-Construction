# Written by Parth V 
# Disclaimer : I am no expert in python but just a learner. In no way is this code perfect or the most 'pythonic' implementaion 
# It was written for practice and understanding the concepts. Feel free to extend or make it better. Cheers !! 
# www.parthvora.tk

#################################################################################
#   Program to remove left recursion from grammar-  both direct and indirect    #                                                                          
#                                                                               #
#################################################################################

# import replace_list python file 
from replace_list import replace_l

mapping = {}

# specifing input grammar
grammar = ['A->Bxy|x',
           'B->CD',
           'C->A|c',
           'D->d'
           ]

new_char_pointer = 80


def remove_left_recursion(string):
    global new_char_pointer
    temp = []
    character = chr(new_char_pointer)
    new_char_pointer += 1
    productions = get_productions(string)
    root = string[0]
    clean = list(filter(lambda x: x[0] != root, productions))
    unclean = list(filter(lambda x: x[0] == root, productions))
    for item in clean:
        new_prod = item + character
        clean = replace_l(clean, item, new_prod)
    for item in unclean:
        item = item[1:] + character
        temp.append(character + '->$|' + item)
    return root + '->' + '|'.join(clean), temp[0]


def get_productions(string):
    '''
    Function gets production for the input non terminal
    :param string: Non terminal
    :return:  production
    '''
    return str(string.split(sep='->')[1]).split(sep='|')


def replace_g(grammar):
    '''
    Function replaces grammar of non terminals that have alphabets with numbers for
    easier processing
    :param grammar: grammar statement
    :return: modified grammer
    '''
    new_grammar = []
    for line in grammar:
        line = list(line)
        for index, character in enumerate(line):
            if character in mapping.keys():
                line[index] = mapping[line[index]]
        new_grammar.append(''.join(line))
    return new_grammar


def re_replace(grammar):
    '''
    Function replaces grammar dict with a grammar from mapping dict , output purposes 
    :param grammar: input grammar
    :return: modified grammar dict
    '''
    final_ans = []
    for line in grammar:
        line = list(line)
        for index, character in enumerate(line):
            if character in mapping.values():
                line[index] = chr(int(character) + 64)
        final_ans.append(''.join(line))
    return final_ans


# putting grammar into dict 
for i, item in enumerate(grammar):
    mapping[item[0]] = str(i + 1)

grammar = replace_g(grammar)
print('--- REPLACE GRAMMAR---')
print(grammar)
final_ans = []

# checks for indirect recursion by comparing each pair of grammar
for i in range(len(grammar)):
    flag = 0
    for j in range(len(grammar)):
        i_p = get_productions(grammar[i])
        j_p = get_productions(grammar[j])
        for index_i in range(len(i_p)):
            each_production_of_i = i_p[index_i]
            if each_production_of_i[0] == grammar[j][0] and i != j:
                print('-----NEED TO REPLACE-----')
                i_p.remove(each_production_of_i)
                for each_production_of_j in j_p:
                    print('Replacing grammar production   ', each_production_of_j)
                    temp_string = each_production_of_i.replace(each_production_of_i[0], each_production_of_j)
                    print('New production produced   ', temp_string)
                    i_p.append(temp_string)
                    print('Updated i_p     ', i_p)

        root = grammar[i][0]
        update = root + '->' + '|'.join(i_p)
        print('Update---------', update)
        grammar.remove(grammar[i])
        # checking for direct recursion in grammar
        for item in i_p:
            if item[0] == root:
                flag = 1
                print('Serious Recursion Detected ....!!!!!!!!')
                x, y = remove_left_recursion(update)
        if flag == 1:
            print('Serious Recursions Solvedddd', x, y)
            grammar.insert(i, x)
            grammar.append(y)
        else:
            grammar.insert(i, update)

grammar = set(grammar)
print(re_replace(grammar))
