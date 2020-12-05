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
    'LIST' : 3,
    }

lisp_to_python_dic.update(vars(math))

dic_new2 = {}

mem = {}

def addQuote(vlist):
    reList = ["'",]
    reList.append(vlist)
    return reList

def isList(vlist):
    if isinstance(vlist, list):
        if vlist[0] == "'":
            if isinstance(vlist[1], list):
                return [True,0] #직접 list 입력
    elif isinstance(vlist, str):
        if vlist in mem:
            if isinstance(mem[vlist],list):
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
    print("args 제대로 출력: ", args)
    for k in args: #차례로 받아오기
        print("k이다 임마!: ", k)
        L.append(eval(k,lisp_to_python_dic))
            
        print("이건 L이다", L)
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
        elif x in lisp_to_python_dic:
            return lisp_to_python_dic[x]
        return x
    elif not isinstance(x, list):
        return x
    elif x[0] == "'": # ["'" , "X"]
        #print("x[1]: ", x[1])
        print("쿼트로 들어옴")
        (_, exp) = x
        print("exp 쿼트 안에 있는거: ",exp)
        if not isinstance(x[1],list):
            print("리스트 보내기")
            #print("exph: ",exp)
            return exp
        elif isinstance(x[1],list):
            if x[1][0] in dic:
                tmp = eval(exp, dic)
                print("tmp: ",tmp)
                return tmp
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
            mem[var] = eval(exp,dic)
            return mem[var]
        else:
            mem[var]=eval(exp,dic)
            return mem[var]
    elif x[0] == 'LIST':
        print("리스트입니다!")
        (_, *args) = x
        print("들어가는 args: ", args)
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
                return mem[nthList][exp]
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
                L.extend(mem[consList])
        return L
    elif x[0] == 'APPEND':
        (_, *args) = x
        appendedList = [] #들어온 리스트들을 모두 담아줄 리스트
        print("args: ", args)
        for exp in args: #args 인자들의 리스트들을 한개씩 가져오기 example : ["'", ['A', 'D']]
            print("exp: ", exp)
            dk = eval(exp, dic)
            print("dk이다: ",dk)
            for val in exp[1]: #val example : ['A', 'D']
                print("val: ", val)
                #print("exp: ", exp)
                val = eval(val, dic)
                print("eval-val: ", val)
                appendedList.append(val) # appendedList 의 결과 ex: ['A', 'D', 'F', 'D', 'G', 'D']
                print("appendedList: ", appendedList)
        resultList = ["'",]
        resultList.append(appendedList) # ["'", ['A', 'D', 'F', 'D', 'G', 'D']]
        return resultList

    # elif x[0] == 'MEMBER':
    #     (_, word, memberList) = x
    #     if memberList in mem:
    #         memberList = mem[memberList][1]
    #         startIndex = memberList.index(word)
    #         for i in range(startIndex)
            

    #     else:
    #         print("Error")
        

    #(NULL X) ;  X가 NIL일 때만 참(true)을 반환함.
    #elif x[0] == 'NULL':
    elif x[0] == 'CAR':
        (_, carList) = x
        if isList(carList)[0]: #true 이면
            if isList(carList)[1] == 0: # 직접 입력
                return carList[1][0]
            elif isList(carList)[1] == 1: #저장된 리스트
                return mem[carList][0]
    elif x[0] == 'CDR':
        (_, cdrList) = x
        if isList(cdrList)[0]: #true 이면
            if isList(cdrList)[1] == 0: # 직접 입력
                return cdrList[1][1:]
            elif isList(cdrList)[1] == 1: #저장된 리스트
                return mem[cdrList][1:]
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
                return len(mem[lengthList])
        else :
            return False
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