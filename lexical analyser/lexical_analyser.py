# Written by Parth V 
# Disclaimer : I am no expert in python, just a learner. In no way is this code perfect or the most 'pythonic' implementaion 
# It was written for practice and understanding the concepts. Feel free to extend it or make it better. Cheers !! 
# www.parthvora.tk

# Implementation of a lexical analyzer for 'C'
import re

major = []
id_ = []


def is_keyword(string):
    '''
    Function checks if the token passed is a keyword or not
    :param string: token input 
    :return: True if keyword, else false
    '''
    l = ["include", "auto", "double", "int", "struct", "break", "else", "long", "switch", "case", "enum", "register",
         "typedef", "char", "extern", "return", "union", "const", "float", "short", "unsigned", "continue", "for",
         "signed", "void", "default", "goto", "sizeof", "volatile", "do", "if", "static", "while", "main"]
    return string in l


def is_number(s):
    '''
    Function checks if a given token is a number or not, checks also for fractional numbers
    :param s: token 
    :return: True if number , else false
    '''
    try:
        float(s)
        return True
    except ValueError:
        return False


# regular expression for statements containing strings (.*)
pat = re.compile('(\".*\")')

# main part
with open('program.txt', 'r') as f, open('program.txt', 'r') as f1:
    for line in f:
        line = line.replace('\n', '').replace('\t', '')
        # check if string is present
        if '"' in line:
            l = re.split(pat, line)
            l = l + [char for char in line if not char.isalnum()]

        else:
            # regular expression to split a line into individual tokens
            l = re.split('([^a-zA-Z0-9_\.])', line)
        major.append(list(filter(lambda x: not (x == '' or x == ' '), l)))
        major = list(filter(lambda x: not len(x) == 0, major))

f.close()
f1.close()
# printing tokens for each line
for index, item_list in enumerate(major):
    print('------------------------------- Tokens on line -------------------------------------------', index)
    keywords = []
    numbers = []
    headers = []
    identifiers = []
    strings = []
    characters = []
    for each_token in item_list:
        if not re.search(pat, each_token):
            if is_keyword(each_token):
                keywords.append(each_token)
            elif is_number(each_token):
                numbers.append(each_token)
            elif '.h' in each_token:
                headers.append(each_token)
            elif len(str(each_token)) == 1 and not str(each_token).isalnum():
                characters.append(each_token)
            else:
                identifiers.append(
                    each_token.replace(')', '').replace('(', '').replace(';', '').replace(',', '').replace('&', ''))
                id_.append(
                    each_token.replace(')', '').replace('(', '').replace(';', '').replace(',', '').replace('&', ''))
        else:
            strings.append(each_token.replace('"', ''))

    if len(keywords) != 0:
        print('*** KEYWORDS ARE ***\n', keywords)
    if len(strings) != 0:
        print('*** STRINGS ARE ***\n', strings)
    if len(numbers) != 0:
        print('*** NUMBERS ARE ***\n', numbers)
    if len(headers) != 0:
        print('*** HEADERS ARE ***\n', headers)
    if len(list(map(lambda x: x.replace(' ', ''), set(filter(lambda x: x != '', identifiers))))) != 0:
        print('*** IDENTIFIERS ARE ***\n',
              list(map(lambda x: x.replace(' ', ''), set(filter(lambda x: x != '', identifiers)))))
    print('*** CHARACTERS ***\n', characters)
