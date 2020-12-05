#interpreter
#xxeol test
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

def isList(vlist):
    if isinstance(vlist, list):
        if vlist[0] == "'":
            if isinstance(vlist[1], list):
                return [True,0] #직접 list 입력
    elif isinstance(vlist, str):
        if vlist in mem:
            if mem[vlist][0] == "'" and isinstance(mem[vlist][1],list):
                return [True,1] #mem에 저장되어있는 list
def lambda_procedure(parms, body, *args):
    dic_new = {}
    for k, v in list(zip(parms, list(*args))):
        dic_new[k] = v
    dic_new2.update(lisp_to_python_dic)
    dic_new2.update(dic_new)
    return eval(body, dic_new2)

def list_procedure(*args):
    T = ["'"]
    L = []
    for k in list(args): #차례로 받아오기
        if isinstance(k, str): #str 일때 -> mem에 없으면 에러!
            if k in mem:
                L.append(mem[k])
            # else : -> 에러처리
        elif isinstance(k, int) or isinstance(k, float):
            L.append(k)
        elif isinstance(k, list): # ' 으로 시작하는.. -> symbol 인지 list 인지 구별 해줘야하나?
            if k[0] == "'": # '으로 시작하면
                L.append(k[1])
    T.append(L)
    return T

##수정요망##
def atom_procedure(var):  # True False를 T NIL로 바꿔주기!!
    if isinstance(var, str):  # 찐 string인지 심볼인지 #찐 string이면 mem에 있는지
        if var in mem:
            return True
    elif isinstance(var,list):
        if var[0]=="'":
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
    elif x[0] == "'": # ["'" , "X"]
        if not isinstance(x[1],list):
            (_, exp) = x
            return exp
        else:
            return x
    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        exp = eval(conseq,dic) if eval(test, dic) else eval(alt,dic)
        return eval(exp, dic)
    elif x[0] == 'define':
        (_, var, exp) = x
        dic[var] = eval(exp, dic)
    elif x[0] == 'SETQ':
        (_, var, exp) = x
        if isinstance(eval(exp,dic), list):
            L = ["'"]
            L.append(eval(exp,dic))
            mem[var] = L
            return L
        else:
            mem[var]=eval(exp,dic)
            return mem[var]
    elif x[0] == 'LIST':
        (_, *args) = x
        return list_procedure(*args)
    ########## Predicate 함수 ############
    elif x[0] == 'ATOM':
        (_, var) = x
        return atom_procedure(var)
    elif x[0] == 'NTH':
        (_, exp, nthList) = x
        if isList(nthList)[0]: #true 이면
            if isList(nthList)[1] == 0: # 직접 입력
                return nthList[1][exp]
            elif isList(nthList)[1] == 1: #저장된 리스트
                return mem[nthList][1][exp]
    elif x[0]=='CONS':
        (_, var, consList) = x
        L=[]
        if isinstance(var,int) or isinstance(var,float):
            L.append(var)
        elif isinstance(var, str):
            if var in mem:
                L.append(mem[var])
        elif atom_procedure(var):
            L.extend(var[1])
        if isinstance(consList, str):
            if consList in mem:
                L.extend(mem[consList])
        elif isList(consList)[0]:  # true 이면
            if isList(consList)[1] == 0:  # 직접 입력
                L.extend(consList[1])
            elif isList(consList)[1] == 1:  # 저장된 리스트
                L.extend(mem[consList][1])
        return L
    #(NULL X) ;  X가 NIL일 때만 참(true)을 반환함.
    #elif x[0] == 'NULL':
    elif x[0] == 'CAR':
        (_, carList) = x
        if isList(eval(carList,dic))[0]: #true 이면
            if isList(eval(carList,dic))[1] == 0: # 직접 입력
                return eval(carList,dic)[1][0]
            elif isList(eval(carList,dic))[1] == 1: #저장된 리스트
                return mem[eval(carList,dic)][1][0]
    elif x[0] == 'CDR':
        (_, cdrList) = x
        if isList(eval(cdrList,dic))[0]: #true 이면
            if isList(eval(cdrList,dic))[1] == 0: # 직접 입력
                T = ["'"]
                T.append(eval(cdrList,dic)[1][1:])
                return T
            elif isList(eval(cdrList,dic))[1] == 1: #저장된 리스트
                T = ["'"]
                T.append(mem[eval(cdrList,dic)][1][1:])
                return T
    elif x[0] == 'REVERSE':
        (_, reverselist) = x
        if isList(reverselist)[0]:
            reverselist[1].reverse()
            return reverselist[1]
    elif x[0]=='LENGTH':
        (_,lengthList)=x
        if isList(lengthList)[0]:
            if isList(lengthList)[1]==0:
                return len(lengthList[1])
            elif isList(lengthList)[1]==1:
                return len(mem[lengthList][1])
        else :
            return False
    elif x[0] == 'NUMBERP':
        (_, var) = x
        return numberp_procedure(var)
    elif x[0] == 'ZEROP':
        (_, var) = x
        return zerop_procedure(var)
    elif x[0] == 'APPEND':
        (_, *args) = x
        appendedList = [] #들어온 리스트들을 모두 담아줄 리스트
        print(args)
        for exp in args:
            if isList(eval(exp,dic))[0]: #True면..
                if isList(eval(exp,dic))[1] == 0: # 직접 입력
                    for val in eval(exp,dic)[1]:
                        appendedList.append(val)
                elif isList(eval(exp,dic))[1]==1: #저장된 리스트
                    for val in mem[eval(exp,dic)][1]:
                        appendedList.append(val)   
        T = ["'"]
        T.append(appendedList)
        return T
    
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