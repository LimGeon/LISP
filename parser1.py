### Lisp Intrepreter in Python
## Parser
# hyo test
from functools import reduce
import re 

def bracket_parser(data):
    if data[0] == '(': 
        return [data[0], data[1:]]

def quote_parser(data):
    if data[0] == "'": #처음 오는게 '이면
        if data[1] == '(': #그 다음에 ( 오면 -> LIST
            tmp = ["'"]
            tmp2 = list_parser(data[2:])
            tmp.append(tmp2[0])
            return [tmp, data[tmp2[1]+2:]]
        else: #심볼처리
            atom_reg_ex = re.compile('\w+') #문자 or 숫자
            atom_match = atom_reg_ex.match(data[1:]) #다음것부터.. 공백올때까지
            if atom_match:
                L = []
                L.append(data[0])
                L.append(data[1:atom_match.end()+1].upper())
                return [L,data[atom_match.end()+1:]]    
            
def list_parser(data): #리스트 생성 # ( 다음 부터 불러옴..
    L = []
    index = 0
    while True:
        if(data[index] == '('): #새로운 리스트
            tmp = list_parser(data[index + 1:]) #괄호 다음부터 list_parser로 새로 돌리기
            T = ["'"]
            T.append(tmp[0])
            L.append(T)
            index = index + tmp[1]
        elif(data[index] == ')'): #리스트 끝
            index = index + 1
            return [L,index]
        elif data[index] not in ('\t','\n','\r','\f','\v'): #공백이 아니면
           list_reg_ex = re.compile('\w+')
           list_match = list_reg_ex.match(data[index:])
           if list_match:
               L.append(atom(data[index:list_match.end()+index].upper()))
               index = index + list_match.end()-1
        index = index + 1       


def space_parser(data): # 공백으로 시작하면f
    space_reg_ex = re.compile('\s+') #공백과 매치
    space_match = space_reg_ex.match(data)
    if space_match:
        return [data[:space_match.end()], data[space_match.end():]]
    

def number_parser(data): #숫자로 시작하면
    number_reg_ex = re.compile('\d+')
    if data[0] == '-' and data[1].isdigit():
        data = data[1:]
        number_match = number_reg_ex.match(data)
        if number_match:
            return['-'+data[:number_match.end()], data[number_match.end():]]

    number_match = number_reg_ex.match(data)
    if number_match:
        return[data[:number_match.end()], data[number_match.end():]]



def identifier_parser(data):
    identifier_reg_ex = re.compile('\w+')
    identifier_match = identifier_reg_ex.match(data)
    if identifier_match:
        return[data[:identifier_match.end()], data[identifier_match.end():]]

keywords_li = ['define', 'lambda', '*', '+', '-', '/', '<', '>', '<=', '>=', '%', 'if', '=',
               'length', 'abs', 'append', 'pow', 'min', 'max', 'round', 'not', 'quote','reverse']

def keyword_parser(data):
    for item in keywords_li:
        if data.startswith(item):
            return key_parser(data)

def declarator_parser(data):
    if data[:6] == 'define':
        return ['define', data[6:]]

def lambda_parser(data):
    if data[:6] == 'lambda':
        return ['lambda', data[6:]]

arithmetic_operators = ['*', '+', '-', '/', '%']

def arithemetic_parser(data):
    for item in arithmetic_operators:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]

binary_operations = ['<=', '>=', '<', '>', '=', 'pow', 'append']

def binary_parser(data):
    for item in binary_operations:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]

unary_operations = ['length', 'abs', 'round', 'not']

def unary_parser(data):
    for item in unary_operations:
        if data.startswith(item):
            return [data[:len(item)], data[len(item):]]

def if_parser(data):
    if data[:2] == 'if':
        return [data[:2], data[2:]]

def atom(s):
    try: return int(s)
    except TypeError:
        return s
    except ValueError:
        try: return float(s)
        except ValueError:
            return str(s)

def expression_parser(data):
    res = value_parser(data)
    rest = res.pop(1)
    token = res.pop(0)
    print("data:", data)
    print("rest:", rest)
    print("token:", token)
    print()
    if token == '(':
        L = []
        while rest[0] != ')':
            nex = expression_parser(rest)
            rest = nex.pop(1)
            token = nex.pop(0)
            #print(token)
            if token[0] == ' ' or token == '\n':
                continue
            L.append(atom(token))
        rest = rest[1:]
        return [L, rest]
    else:
        return [token, rest]

def any_one_parser_factory(*args):
    return lambda data: (reduce(lambda f, g: f if f(data)  else g, args)(data))

value_parser = any_one_parser_factory(space_parser, bracket_parser, quote_parser, 
                                    number_parser, keyword_parser, identifier_parser)
key_parser = any_one_parser_factory(declarator_parser, lambda_parser, if_parser,
                                    binary_parser, arithemetic_parser, unary_parser)

def main():
    # file_name = input()
    # with open(file_name, 'r') as f:
    #     data = f.read().strip()
    while(True):
        userInput = input("> ")
        print(expression_parser(userInput))

if __name__ == "__main__":
    main()
