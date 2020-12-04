#interpreter

import math
import operator as op
from functools import reduce
from parser1 import expression_parser

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

def lambda_procedure(parms, body, *args):
    dic_new = {}
    for k, v in list(zip(parms, list(*args))):
        dic_new[k] = v
    dic_new2.update(lisp_to_python_dic)
    dic_new2.update(dic_new)
    return eval(body, dic_new2)

def setq_procedure(sym, var):
    mem[sym] = var
    return var

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

def zerop_procedure(var):
    if isinstance(var,int):
        if var == 0:
            return True
        else:
            return False
    elif isinstance(var,int): #정수일때랑 합쳐줘도 되나?
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
        if x in dic:
            return dic[x]
        else:
            return mem[x]
    elif not isinstance(x, list):
        return x
    elif x[0] == 'quote':
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
        (_, var, data) = x
        return setq_procedure(var, data)
    elif x[0] == 'ATOM':
        (_, var) = x
        return atom_procedure(var)
    elif x[0] == 'ZEROP':
        (_, var) = x
        return zerop_procedure(var)
    elif x[0] == 'lambda':
        (_, parms, body, *args) = x
        return lambda_procedure(parms, body, args)
    else:
        proc = eval(x[0], dic)
        args = [eval(exp, dic) for exp in x[1:]]
        return proc(args)

#print(eval(['define', 'x', 100], lisp_to_python_dic))

#print(eval(['define', 'y', 5], lisp_to_python_dic))

#print(eval(['lambda', ['x', 'y'], ['*', 'x', 'y'], 5, 2], lisp_to_python_dic))

#print(eval(['*', ['+', 5, 7], ['/', 4, 2]], lisp_to_python_dic))

#print(eval(['*', 'x', 'x'], lisp_to_python_dic))

#print(eval(expression_parser('(+ 5 (* 3 2) )')[0], lisp_to_python_dic))

#print(eval(['>', 5 ,10], lisp_to_python_dic))

#print(eval(['if', ['<', 5 ,10], ['+', 10, 5],['-', 10, 5]], lisp_to_python_dic))

def main():  
     while(True):
        userInput = input("> ") #d #s #f
        print(eval(expression_parser(userInput).pop(0), lisp_to_python_dic))

if __name__ == "__main__":
    main()

