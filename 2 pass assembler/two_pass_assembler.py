# Written by Parth V 
# Disclaimer : I am no expert in python but just a learner. In no way is this code perfect or the most 'pythonic' implementaion 
# It was written for practice and understanding the concepts. Feel free to extend or make it better. Cheers !! 
# www.parthvora.tk

# implementaion of two pass assembler
# input program has replaced empty labels with **** for easier processing
print("***** TWO PASS ASSEMBLER *****")
list_of_lines = []
symbol_table = []
literal_table = []
lc = 0
ic = []
import copy


def add_to_st(str, x, y, z):
    '''
    Function adds values to symbol table
    :param str: name of symbol 
    :param x: value of symbol
    :param y:  length of symbol
    :param z: type
    :return: void
    '''
    str = str.split(sep='(')[0]
    if not check_st(str):
        symbol_table.append({'id': 0, 'name': str, 'value': x, 'len': y, 'r/a': z})
    else:
        for item in symbol_table:
            if item['r/a'] == 1 and item['name'] == str:
                symbol_table.remove(item)
                add_to_st(str, x, y, z)


def check_st(str):
    '''
    check for entry in symbol table 
    '''
    return len(list(filter(lambda x: x['name'] == str, symbol_table))) == 1


def add_to_lt(str, x, y, z):
    '''
        Function adds values to literal table
        :param str: name of literal 
        :param x: value of literal
        :param y:  length of literal
        :param z: type
        :return: void
        '''
    literal_table.append({'id': 1, 'literal': str, 'value': x, 'length': y, 'r/a': z})


def get_size(str):
    '''
    Function returns size of instruction
    :param str: ins name
    :return: size 
    '''
    return (str == 'RR' and 2) or ((str == 'RX' or st == 'RS' or st == 'RS') and 4) or (str == 'SS' and 5) or -1


def is_instruction(str):
    '''
    Function checks if the given string is an instruction or not
    :param str: input
    :return: True if instruction else False
    '''
    return (str in ins_table.keys())


def return_id(type, value):
    '''
    Function returns id of symbol/ literal, based on type.
    :param type: S for symbol, l for literal
    :param value: name of the symbol
    :return: id 
    '''
    return (type == 'L' and list(filter(lambda x: x['literal'] == value, literal_table))[0]['id']) or (
        type == 'S' and list(filter(lambda x: x['name'] == value, symbol_table))[0]['id'])


def return_value(type, value):
    '''
        Function returns value of symbol/ literal, based on type.
        :param type: S for symbol, l for literal
        :param value: name of the symbol
        :return: value
        '''
    return (type == 'L' and list(filter(lambda x: x['literal'] == value, literal_table))[0]['value']) or (
        type == 'S' and list(filter(lambda x: x['name'] == value, symbol_table))[0]['value'])


def return_alloc(type, value):
    '''
        Function returns type of symbol/ literal, based on type.
        :param type: S for symbol, l for literal
        :param value: name of the symbol
        :return: type 
        '''
    return (type == 'L' and list(filter(lambda x: x['literal'] == value, literal_table))[0]['r/a']) or (
        type == 'S' and list(filter(lambda x: x['name'] == value, symbol_table))[0]['r/a'])


# writing lines as list
with open('Source_code.txt', 'r') as f, open('ins.txt', 'r') as f1:
    for line in f:
        list_of_lines.append(
            list(filter(lambda x: x != '', line.replace('\n', '').replace('\t', '').replace(' ', ',').split(sep=','))))
    ins_table = {line.split(sep=' ')[0]: line.split(sep=' ')[1].replace('\n', '') for line in f1}
f.close()
f1.close()

# removing empty listm
list_of_lines = list(filter(lambda x: len(x) != 0, list_of_lines))

# main logic , processing pseudo ops first  PASS 1
for item in list_of_lines:
    if 'START' in item:
        program_name = item[0]
        start_add = item[2]
        add_to_st(item[0], 0, 1, 'R')
    elif 'USING' in item:
        base_register = item[3]
    elif 'END' in item:
        ic.append([lc, item[0], '-', '-'])
    elif 'EQU' in item:
        add_to_st(item[0], item[2], 1, 'A')
    elif 'LTORG' in item:
        # adjusting lc
        if lc % 8 != 0:
            next_lc = lc + (8 - (lc % 8))
        else:
            next_lc = lc
        for item in literal_table:
            item['value'] = next_lc
            next_lc += 4
        lc = next_lc
    elif 'DC' in item:
        add_to_st(item[0], lc, 4, 'R')
        ic.append([lc, item[1], item[2], '-'])
        lc += 4
    elif 'DS' in item:
        add_to_st(item[0], lc, 4 * int(item[2].replace('F', '')), 'R')
        ic.append([lc, item[1], item[2], '-'])
        lc += 4 * int(item[2].replace('F', ''))
    else:
        if item[0] != '****':
            add_to_st(item[0], lc, 4, 'R')
        for sub_item in item:
            if sub_item == '****':
                pass
            elif is_instruction(sub_item):
                if len(item) == 4:
                    ic.append([lc, item[1], item[2], item[3]])
                else:
                    ic.append([lc, item[1], item[2], '-'])
                lc = lc + get_size(ins_table[sub_item])
            elif str(sub_item).isnumeric():
                pass
            elif '=' in sub_item:
                add_to_lt(sub_item.replace('=', ''), 1, 4, 'R')
            else:
                add_to_st(sub_item, 1, 1, 1)
print('------------------------Pass 1-------------------------')
print('Program Name', program_name)
print('Start Address', start_add)
print('Base Register', base_register)

print('----SYMBOL TABLE----')
print('{:10}'.format('ID'), '{:10}'.format('SYMBOL'), '{:10}'.format('VALUE'), '{:10}'.format('LENGTH'),
      '{:10}'.format('R/A'))
print('--------------------------------------')
for index, item in enumerate(symbol_table):
    item['id'] = index + 1
    print('{:10}'.format(str(item['id'])), '{:10}'.format(item['name']), '{:10}'.format(str(item['value'])),
          '{:10}'.format(str(item['len'])), '{:10}'.format(str(item['r/a'])))

print('----LITERAL TABLE----')
print('{:10}'.format('ID'), '{:10}'.format('LITERAL'), '{:10}'.format('VALUE'), '{:10}'.format('LENGTH'),
      '{:10}'.format('R/A'))
print('--------------------------------------')
for index, item in enumerate(literal_table):
    item['id'] = index + 1
    print('{:10}'.format(str(item['id'])), '{:10}'.format(item['literal']), '{:10}'.format(str(item['value'])),
          '{:10}'.format(str(item['length'])), '{:10}'.format(str(item['r/a'])))

print("--LOCATION COUNTER IS-- ", lc)
pass_2 = []

# pass 2
for x in ic:
    temp = copy.deepcopy(x)
    if 'BNE' in x:
        x[2] = '-'
        x[3] = 'LOOP'
        temp[1] = 'BC'
        temp[2] = '7'
    for i, y in enumerate(x):
        if str(y).replace('(4)', '') in [x['name'] for x in symbol_table]:
            x[i] = 'id#' + str(return_id('S', str(y).replace('(4)', '')))
            if return_alloc('S', str(y).replace('(4)', '')) == 'A':
                temp[i] = str(return_value('S', str(y).replace('(4)', '')))
            else:
                temp[i] = str(return_value('S', str(y).replace('(4)', ''))) + '(0,' + str(base_register) + ')'
        elif '=' in str(y):
            x[i] = 'LT#' + str(return_id('L', y.replace('=', '')))
            temp[i] = str(return_value('L', y.replace('=', ''))) + '(0,' + str(base_register) + ')'
    pass_2.append(temp)

# print statements
print('----Intermediate Table----')
print('{:10}'.format('LC'), '{:10}'.format('INSTRUCTION'), '{:10}'.format('SOMETHING'), '{:10}'.format('Somethingelse'))
print('--------------------------------------')
for item in ic:
    print('{:10}'.format(str(item[0])), '{:10}'.format(item[1]), '{:10}'.format(str(item[2])),
          '{:10}'.format(str(item[3])))
print('------------------FINAL OUTPUT OF PASS 2-----------')
print('{:10}'.format('LC'), '{:10}'.format('INSTRUCTION'), '{:10}'.format('SOMETHING'), '{:10}'.format('Somethingelse'))
print('--------------------------------------')
for item in pass_2:
    print('{:10}'.format(str(item[0])), '{:10}'.format(item[1]), '{:10}'.format(str(item[2])),
          '{:10}'.format(str(item[3])))
