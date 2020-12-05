#interpreter

import math
import operator as op
from functools import reduce
from parser1 import expression_parser
import sys

lisp_to_python_dic = {
    '+':lambda *x: reduce(op.add, *x), '-':lambda *x: reduce(op.sub, *x),
    '*':lambda *x: reduce(op.mul, *x), '/':lambda *x: reduce(op.truediv, *x),
    '>':lambda *x: reduce(op.gt, *x), '<':lambda *x: reduce(op.lt, *x),
    '>=':lambda *x: reduce(op.ge, *x), '<=':lambda *x: reduce(op.le, *x),
    '=':lambda *x: reduce(op.eq, *x),
    'abs':     abs,
    'append':  lambda *x: reduce(op.add, *x),
    'apply':   lambda x: x[0](x[1:]),
    'begin':   lambda *x: x[-1],
    'car':     lambda x: x[0],
    'cdr':     lambda x: x[1:],
    'cons':    lambda x, y: [x] + y,
    'reverse': lambda x: x[::-1],
    'eq?':     op.is_,
    'equal?':  op.eq,
    'length':  len,
    'list':    lambda *x: list(x),
    'list?':   lambda x: isinstance(x, list),
    'map':     map,
    'max':     max,
    'min':     min,
    'not':     op.not_,
    'null?':   lambda x: x == [],
    'number?': lambda x: isinstance(x, int) or isinstance(x, float),
    'procedure?': callable,
    'round':   round,
    'symbol?': lambda x: isinstance(x, str),
    }

lisp_to_python_dic.update(vars(math))

dic_new2 = {}

mem = {}

def isList(vlist):
    if vlist[0] == "'":
        return True
    else:
        False

def lambda_procedure(parms, body, *args):
    dic_new = {}
    for k, v in list(zip(parms, list(*args))):
        dic_new[k] = v
    dic_new2.update(lisp_to_python_dic)
    dic_new2.update(dic_new)
    return eval(body, dic_new2)

def atom_procedure(var): #True False를 T NIL로 바꿔주기!!
    if isinstance(var, str):#찐 string인지 심볼인지 #찐 string이면 mem에 있는지
        if var in mem:
            return True
        elif var[0] == "'":
            return True
    elif isinstance(var, int):
        return True
    elif isinstance(var, float):
        return True

def numberp_procedure(var):
    if isinstance(var,int) or isinstance(var,float):
        return True
    elif isinstance(var,str):
        if var in mem:
            if isinstance(mem[var],int) or isinstance(mem[var],float):
                return True

def zerop_procedure(var):
    if isinstance(var,int):
        if var == 0:
            return True
    elif isinstance(var,float): #int일때랑 합쳐줘도 되나?
        if var == 0:
            return True
    elif isinstance(var,str):
        if var in mem:
            if mem[var] == 0:
                return True
    else: #숫자가 아닐 때.. 사실 나중에 Error 처리 해줘야하는데 일단 False로
        return False        

def eval(x, dic):
    if isinstance(x, str):
        if x in mem:
            return mem[x]
        else:
            return lisp_to_python_dic[x]
    elif not isinstance(x, list):
        return x
    elif x[0] == "'":
        (_, exp) = x
        return exp
    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        exp = eval(conseq,dic) if eval(test, dic) else eval(alt,dic)
        return eval(exp, dic)
    elif x[0] == 'define':
        (_, var, exp) = x
        dic[var] = eval(exp, dic)
    elif x[0] == 'SETQ':
        (_, var, exp) = x
        mem[var]=eval(exp,dic)
        return mem[var]
    elif x[0] == 'CAR':
        (_, carList) = x
        if isList(carList) == True:
            return carList[1][0]
    elif x[0] == 'CDR':
        (_, cdrList) = x
        if isList(cdrList) == True:
            cdrList = cdrList[1][1:]
            return cdrList
    elif x[0]=='REVERSE':
        (_,reverselist)=x
        if isList(reverselist)==True:
            reverselist[1].reverse()
            return reverselist[1]       
    ########## Predicate 함수 ############
    elif x[0] == 'ATOM':
        (_, var) = x
        return atom_procedure(var)

    #(NULL X) ;  X가 NIL일 때만 참(true)을 반환함.
    #elif x[0] == 'NULL':
    
    elif x[0] == 'NUMBERP':
        (_, var) = x
        return numberp_procedure(var)
    elif x[0] == 'ZEROP':
        (_, var) = x
        return zerop_procedure(var)
    
    #(MINUSP X) ; X가 음수일 때만 참(true)을 반환함. X가 숫자가 아니면 ERROR 발생
    #elif x[0] == 'MINUSP':

    #(EQUAL X Y) ;  X와 Y가 같으면 참(true)을 반환함
    #elif x[0] == 'EQUAL':

    #(< X Y) ;  X < Y 이면 참(true)을 반환함.
    #elif x[0] == '<':

    #(>= X Y) ;  X >= Y 이면 참(true)을 반환함.
    #elif x[0] == '>=':
    
    #(STRINGP X) ;  X가 STRING일 때만 참(true)을 반환함.
    #elif x[0] == 'STRINGP':

    elif x[0] == 'lambda':
        (_, parms, body, *args) = x
        return lambda_procedure(parms, body, args)
    else:
        proc = eval(x[0], dic)
        args = [eval(exp, dic) for exp in x[1:]]
        try: return proc(args)
        except TypeError:
            args=[eval(exp,dic) for exp in x[0:]]
            return args


def main():  
     while(True):
        userInput = input("> ")
        print(eval(expression_parser(userInput).pop(0), lisp_to_python_dic))

if __name__ == "__main__":
    main()

