import json_serializer
import json_deserializer

def _json_to_yaml(str):
    i = 0
    indent = 0
    hyphen = False

    lenth = len(str)

    while i < lenth:

        ch = str[i]

        if ch == ' ':
            i = i + 1
            continue

        if ch == '{':
            indent = indent + 2
            if str[i - 1] == '-' or str[i - 2] == '-':
                str = str.replace(ch, '', 1)
                i = i + 1
            else:
                str = str.replace(ch, '\n' + indent * ' ', 1)
                i = i + indent

        elif ch == '}':
            str = str.replace(ch, '', 1)
            indent = indent - 2
            i = i - 1
            
        elif ch == ',':
            if str[i + 1] == ' ':
                if hyphen is True:
                    str = str.replace(ch + ' ', '\n' + indent * ' ' + '- ', 1)
                else:
                    str = str.replace(ch + ' ', '\n' + indent * ' ', 1)
            elif str[i + 1] == '"':
                if hyphen:
                    str = str.replace(ch + '"', '\n' + indent * ' ' + '- ', 1)
                else:
                    str = str.replace(ch, '\n' + indent * ' ', 1)
            elif str[i + 1].isdigit():
                if hyphen:
                    str = str.replace(ch, '\n' + indent*' ' + '- ', 1)
                else:
                    str = str.replace(ch, '\n' + indent * ' ', 1)
            else:
                str = str.replace(ch, '\n' + indent * ' ', 1)
            i = i + indent

        elif ch == '"':
            str = str.replace(ch, '', 1)
            i = i - 1

        elif ch == '[':
            hyphen = True
            indent = indent + 2
            str = str.replace(ch, '\n' + indent * ' ' + '- ', 1)
            i = i + indent

        elif ch == ']':
            hyphen = False
            str = str.replace(ch, '', 1)
            indent = indent - 2
            i = i - 1

        else:
            i = i + 1

        lenth = len(str)
        
    return str



def _yaml_to_json(str):

    lines = str.split('\n')
    indent = 2
    space = 0
    str = '{'

    for line in lines:

        if line == '':
            continue

        if line[0].isalpha():
            return '"' + line + '"' 
            
        space = line.count(' ')

        space = space - 1

        if str[len(str) - 1] == ']' and space < indent:
            indent = indent - 2

        if space < indent:

            if str[len(str) - 2] == ',':
                str = str[0 : len(str) - 2]

            str = str + '}'*int((indent - space)/2) + ', '
            if (str[len(str) - 3]) == '{':
                str = str[0 : len(str) - 2] + '}, '
            indent = space

        line = line[space : len(line)]
        colon = line.find(':')
        hyphen = line.find('-')

        if colon != -1:

            if str[len(str) - 1] == ']':
                str = str + ', '

            word1 = line[0 : colon]
            word2 = line[colon + 2 : len(line)]

            if word1 != '' and not word1[0].isdigit():
                word1 = '"' + word1 + '"'

            if word2.find('null') == -1 and word2 != '' and not word2[0].isdigit():
                word2 = '"' + word2 + '"'

            if word2 == ' ' or word2 == '':
                indent = indent + 2
                str = str + word1 + ': {'

            else:
                str = str + word1 + ': ' + word2 + ', '

        elif hyphen != -1:
            word = line[hyphen + 2 : len(line)]

            if word.find('null') == -1 and word != '' and not word[0].isdigit():
                word = '"' + word + '"'

            if str[len(str) - 1] == '{':
                str = str[0 : len(str) - 1] + '[' + word + ']'

            elif str[len(str) - 1] == ']':
                str = str[0 : len(str) - 1] + ', ' + word + ']'

    if space < indent:
        str = str + '}'*int((indent - space)/2)
        indent = space

    
    if str[len(str) - 2] == ',':
        str = str[0 : len(str) - 2]
    n = str.count('{') - str.count('}')
    str = str + '}'*n
    # str = str.replace(', ', ',')s
    return str



def dumps(obj):
    json = json_serializer.dumps(obj)
    res = _json_to_yaml(json)
    return res



def dump(obj, fp):
    string = dumps(obj)
    try:
        with open(fp, "w") as file:
            file.write(string)
    except FileNotFoundError:
        raise FileNotFoundError("file doesn't exist")



def loads(string):
    json = _yaml_to_json(string)
    obj = json_deserializer.loads(str(json))
    return obj



def load(fp):
    try:
        with open(fp, "r") as file:
            data = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("file doesn't exist")
    return loads(data)