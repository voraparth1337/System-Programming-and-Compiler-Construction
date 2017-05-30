# Written by Parth V
# Disclaimer : I am no expert in python but just a learner. In no way is this code perfect or the most 'pythonic' implementaion
# It was written for practice and understanding the concepts. Feel free to extend or make it better. Cheers !!
# www.parthvora.tk

# Implementation of two pass macro processor

program_lines = [] 
list_of_macros = []
# macro defintion table
mdt = [] 
# macro name table
mnt = []
# Arguement list array
arg_list = []
output = []


def print_output(mdt, mnt, arg_list):
    '''
    function to print output
    :param mdt: mdt table 
    :param mnt: mnt table
    :param arg_list: ala
    :return: prints the mdt, mnt and ala for each macro
    '''
    print("----MACRO DEFINITION TABLE---- ")
    print('{:10}'.format('INDEX') + '{:>10}'.format('DEFINITION'))

    for item in mdt:
        print('{:10}'.format(str(item['index'])) + ' '.join(item['def']))
    print('\n')
    print('----MACRO NAME TABLE----')
    print('{:10}'.format('ID') + '{:10}'.format('NAME') + '{:10}'.format('MDT index'))
    for item in mnt:
        print('{:10}'.format(str(item[0])) + '{:10}'.format(str(item[1])) + '{:10}'.format(str(item[2])))

    print('\n')
    for index, l in enumerate(arg_list):
        print('----ARG LIST FOR MACRO----', index + 1)
        print('{:10}'.format('Index') + '{:10}'.format('Arguement'))
        for item in l:
            print('{:10}'.format(str(item['index'])) + '{:10}'.format(item['arg']))
        print('\n')


def replace_args(l, macro_index):
    '''
    replaces a list with arguements replaced with their positional arguements
    :param l: line from source code
    :param macro_index: index number of macro
    :return: replaces a list with arguements replaced with their positional arguements
    '''
    arguement_list = [(x['index'], x['arg']) for x in arg_list[macro_index]]
    for index, item in enumerate(l):
        if '&' in item:
            l[index] = '#' + str(
                list(filter(lambda x: x[1] == item.replace('&', '').split(sep='=')[0], arguement_list))[0][0])
    return l


def replace_positions(arg, macro_index):
    '''
    return a list where macro defintion arguements are replaced with original passed
    arguements
    :param arg: actual passed arguements 
    :param macro_index: index of macro in mdt
    :return: return a list where macro defintion arguements are replaced with original passed
    arguements
    '''
    a = []
    arg.insert(0, 0)
    for i in range(macro_index + 1, len(mdt)):
        output = []
        if 'MEND' in mdt[i - 1]['def']:
            break
        else:
            for item in mdt[i - 1]['def']:
                if '#' in item:
                    output.append(arg[int(item.split(sep='#')[1])])
                else:
                    output.append(item)

        a.append(output)
    return a


with open('source_code.txt', 'r') as f:
    # searching for macro definitions and storing them 
    counter = 1
    macro = 0
    for line in f:
        line = line.replace('\t', ' ').replace('\n', '').replace(' ', ',')
        if 'MACRO' in line:
            flag = 1
            first_line = True
            macro += 1  # macro counter for mnt index
        elif 'MEND' in line:
            flag = 0
            mdt.append({'index': counter, 'def': line})
            counter += 1
        elif flag == 1 and first_line:
            l = line.split(sep=',')
            name = l[0]
            arguement = []
            for i in range(1, len(l)):
                arguement.append({'index': i, 'arg': l[i].replace('&', '').split(sep='=')[0]})
            arg_list.append(arguement)
            mnt.append([macro, name, counter])
            mdt.append({'index': counter, 'def': list(filter(lambda x: x != '', replace_args(l, macro - 1)))})
            counter += 1
            first_line = False
        elif flag == 1 and not first_line:
            l = line.split(sep=',')
            mdt.append({'index': counter, 'def': list(filter(lambda x: x != '', replace_args(l, macro - 1)))})
            counter += 1
        elif 'START' in line:
            flag = 2
            program_lines.append(line.split(sep=','))
        elif flag == 2:
            program_lines.append(line.split(sep=','))

print_output(mdt, mnt, arg_list)
print('----OUTPUT----')
for item in program_lines:
    # searching for macro name in macro name table
    if item[0] in [item[1] for item in mnt]:
        # fetching its index
        mdt_index = list(filter(lambda x: x[1] == item[0], mnt))[0][2]
        # getting its arguements
        arg = [item[i] for i in range(1, len(item))]
        # replacing arguements in mdt with actual arguements
        a = replace_positions(arg, mdt_index)
        for item in a:
            print(' '.join(list(filter(lambda x: x != '', item))))
    # printing of normal statements
    else:
        print(' '.join(list(filter(lambda x: x != '', item))))
