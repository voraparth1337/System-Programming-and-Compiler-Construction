# Written by Parth V 
# Disclaimer : I am no expert in python but just a learner. In no way is this code perfect or the most 'pythonic' implementaion 
# It was written for practice and understanding the concepts. Feel free to extend or make it better. Cheers !! 
# www.parthvora.tk

#############################################
#     Lexical Analyser - Simple version     #                                                                       
#                                           #                                    
#############################################

import re

f = open('program.txt', 'r')


def is_keyword(string):
    l = ["include", "auto", "double", "int", "struct", "break", "else", "long", "switch", "case", "enum", "register",
         "typedef", "char", "extern", "return", "union", "const", "float", "short", "unsigned", "continue", "for",
         "signed", "void", "default", "goto", "sizeof", "volatile", "do", "if", "static", "while", "main"]
    return string in l


def is_number(c):
    try:
        float(c)
        return True
    except ValueError:
        return False


pat_string = re.compile('(\".*\")')  # to check strings
pat = re.compile('([^a-zA-Z0-9\_\.])')  # split on everything except a-zA-Z0-9_.

for line in f:
    keyword = []
    number = []
    character = []
    string = []
    identifiers = []
    header = []
    line = line.replace('\n', '')
    line = line.strip()
    if '"' in line:
        temp = re.split(pat_string, line.replace('(', '').replace(')', ''))
        temp = list(filter(lambda x: x.replace('\\n', ''), temp))
    else:
        temp = re.split(pat, line)

    temp = list(filter(lambda x: x != '', temp))
    temp = list(filter(lambda x: x != ' ', temp))
    temp = set(temp)
    print('__')
    print(temp)
    if temp:
        for item in temp:
            if is_keyword(item):
                keyword.append(item)
            elif is_number(item):
                number.append(item)
            elif '.h' in item:
                header.append(item)
            elif len(item) == 1 and not str(item).isalnum():
                character.append(item)
            elif re.search(pat_string, item):
                string.append(item)
            else:
                identifiers.append(item)
    print('Keywords' + str(keyword))
    print('id' + str(identifiers))
    print('string' + str(string))
