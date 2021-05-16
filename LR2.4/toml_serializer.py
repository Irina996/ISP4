from logging import error
import json_serializer
import json_deserializer

def _json_to_toml(str):

    new_str = ''
    indent = 0
    i = 0

    while i < len(str):
        if str[i] == '"':
            i = i + 1
            j = i
            while str[j] != '"':
                j = j + 1
            word = str[i : j]

            if i == 1 and j == len(str) - 1:
                new_str = 'toml_str = ' + str
                break
            
            if str[j + 1] == ':':
                if str[j + 3] == '{':
                    word = indent*' ' + '[' + word + ']\n'
                    indent = indent + 2
                else: 
                    word = indent*' ' + word + ' = '
                new_str = new_str + word
            else:
                new_str = new_str + '"' + word + '"\n'
            i = j

        if str[i].isdigit():
            j = i
            while str[j].isdigit():
                j = j + 1
            word = str[i : j]
            new_str = new_str + word + '\n'
            i = j

        if str[i] == '[':
            def find_end(k):
                while str[k]!= ']':
                    if str[k] == '[':
                        k = find_end(k + 1)
                    k = k + 1
                return k

            def create_word(s):
                j = 0
                while j < len(s):
                    if s[j].isalpha()  and s[j - 1] != '"':
                        k = j
                        while s[k].isalpha():
                            k = k + 1
                        s = s.replace(s[j : k], '"' + s[j : k] + '"')
                        j = k
                    j = j + 1
                return s
                   
            j = find_end(i + 1)
            word = str[i : j + 1]
            if word.find(',') == -1:            
                word = create_word(word)
            new_str = new_str + word + '\n'
            i = j

        if str[i].isalpha():
            j = i
            while str[j].isalpha():
                j = j + 1
            word = str[i : j]
            new_str = new_str + '"' + word + '"\n'
            i = j

        if str[i] == '}':
            indent = indent - 2

        i = i + 1
    return new_str


def _toml_dict_to_json(str):
    i = 1
    while i < len(str):
        if str[i] == '[':
            str = str[0: i] + _toml_dict_to_json(str[i : len(str)])
        elif str[i] == ']':
            str = str[0:i + 1]
            return str
        i = i + 1
    return ValueError


def _toml_to_json(str):

    if str[len(str) - 2] == ']':
        return _toml_dict_to_json(str)

    indent = 0
    lines = str.split('\n')
    str = '{'
    
    for line in lines:

        space = line.count(' ')
        if line != '' and line[space] != '[':
            space = space - 2

        if space < indent:
            if str[len(str) - 2] == ',':
                str = str[0 : len(str) - 2]
            str = str + '}'*int((indent - space)/2) + ', '
            indent = space

        if line != '' and line[space] == '[':
            str = str + '"' + line[space + 1 : len(line) - 1] + '": {'
            indent = indent + 2

        elif line != '':
            ind = line[space : len(line)].find(' ')
            word1 = line[0 : space + ind]
            word1 = word1.replace(' ', '')
            word2 = line[space + ind + 3 : len(line)]
            if word2.find('null') != -1:
                word2 = word2.replace('"', '')
            str = str + '"' + word1 + '": ' + word2 + ', '

    if space < indent:
        str = str + '}'*int((indent - space)/2)
        indent = space

    str = str[0 : len(str) - 2]
    n = str.count('{') - str.count('}')
    str = str + '}'*n

    if str.find("toml_str") != -1:
        str = str.replace('"toml_str": ', '')
        str = str.replace('{', '')
        str = str.replace('}', '')

    str = str.replace('""', '"')
    return str



def dumps(obj):
    json = json_serializer.dumps(obj)
    res = _json_to_toml(json)
    return res



def dump(obj, fp):
    string = dumps(obj)
    try:
        with open(fp, "w") as file:
            file.write(string)
    except FileNotFoundError:
        raise FileNotFoundError("file doesn't exist")



def loads(string):
    json = _toml_to_json(string)
    obj = json_deserializer.loads(json)
    return obj



def load(fp):
    try:
        with open(fp, "r") as file:
            data = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("file doesn't exist")
    return loads(data)