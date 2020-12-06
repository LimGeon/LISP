#interpreter
import math
import operator as op
from functools import reduce
from parser1 import expression_parser

#### 기본적인 연산들 (ex. 사칙연산) 을 위한 딕셔너리 ####
lisp_to_python_dic = {
    '+':lambda *x: reduce(op.add, *x), '-':lambda *x: reduce(op.sub, *x),
    '*':lambda *x: reduce(op.mul, *x), '/':lambda *x: reduce(op.truediv, *x),
    '>':lambda *x: reduce(op.gt, *x), '<':lambda *x: reduce(op.lt, *x),
    '>=':lambda *x: reduce(op.ge, *x), '<=':lambda *x: reduce(op.le, *x),
    '=':lambda *x: reduce(op.eq, *x),
    ########### 밑으로 다 주석처리 해도되지않을까???##############33
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

dic_new2 = {} #lambda식을 위한 딕셔너리

mem = {} #SETQ를 통한 변수 저장을 위한 딕셔너리

def CAR_procedure(carList, dic):
    if isList(eval(carList,dic))[0]: #true 이면
        if isList(eval(carList,dic))[1] == 0: # 직접 입력
            return eval(carList,dic)[1][0] #리스트의 첫번째 원소 return (원소)
        elif isList(eval(carList,dic))[1] == 1: #저장된 리스트
            return mem[eval(carList,dic)][1][0] #리스트의 첫번째 원소 return (원소)

def CDR_procedure(cdrList, dic):
    if isList(eval(cdrList,dic))[0]: #true 이면
        if isList(eval(cdrList,dic))[1] == 0: # 직접 입력
            T = ["'"] # 리스트임을 나타내기 위한 quote
            T.append(eval(cdrList,dic)[1][1:]) #리스트의 두번째 원소부터 return (리스트 형식)
            return T # 리스트 return
        elif isList(eval(cdrList,dic))[1] == 1: #저장된 리스트
            T = ["'"] # 리스트임을 나타내기 위한 quote
            T.append(mem[eval(cdrList,dic)][1][1:]) #리스트의 두번째 원소부터 return (리스트 형식)
            return T #리스트 return

# def addQuote(vlist):
#     reList = ["'",]
#     reList.append(vlist)
#     return reList

def isList(vlist): #리스트인지 확인하기 위한 함수 -> 리스트 형식이고 첫번째 원소 값이 '인 경우에 -> 심볼인지 리스트인지
    if isinstance(vlist, list): #리스트 형식이면 
        if vlist[0] == "'":
            if isinstance(vlist[1], list):
                return [True,0] #직접 list 입력
    elif isinstance(vlist, str): #str 형식이면 -> mem에 저장된 변수인지 확인 -> 저장되어있다면 그에 맞는 value값 list형인지 확인
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
    #print("args 제대로 출력: ", args)
    for k in args: #차례로 받아오기
        L.append(eval(k,lisp_to_python_dic))
    T.append(L)
    return T

def numberp_procedure(var):
    if isinstance(var,int) or isinstance(var,float):
        return True
    elif isinstance(var,str):
        if var in mem:
            if isinstance(mem[var],int) or isinstance(mem[var],float):
                return True
    return False

def zerop_procedure(var): # var이 0인지 판별
    #int나 float 형일때는 그 자체를 0과 비교
    if isinstance(var,int): 
        if var == 0:
            return True
    elif isinstance(var,float):
        if var == 0:
            return True
    elif isinstance(var,str):  #str 형식이면 -> mem에 저장된 변수인지 확인 -> 저장되어있다면 그의 value값 0인지 check
        if var in mem:
            if mem[var] == 0:
                return True
    else: #숫자 및 스트링이 아닐 때.. 사실 나중에 Error 처리 해줘야하는데 일단 False로
        return False        

########################### eval 함수 - 핵심 ###########################################
def eval(x, dic):
    if isinstance(x, str):
        if x in mem:
            return mem[x]
        elif x in lisp_to_python_dic:
            return lisp_to_python_dic[x]
        else: #quote가 붙여져 있지도 않고, mem에 저장도 안된것..
            return "ERROR : 저장된 변수가 아닙니다..ㅠ"
    elif not isinstance(x, list):
        return x
    elif x[0] == "'": # ["'" , "X"]
        if not isinstance(x[1],list):
            (_, exp) = x
            return exp
        else:
            return x
    elif x[0] == '+':
        (_, *args) = x
        tmp = 0
        for i in args:
            if not (isinstance(i,int) or isinstance(i,float)): #int도 아니고 float도 아닐때.. ->ex. 스트링?
                if i in mem:
                    if isinstance(mem[i],int) or isinstance(mem[i],float):
                        tmp = tmp + mem[i]
                else:
                    return "ERROR : 올바르지 않은 자료형!"
            else:
                tmp = tmp + i
        return tmp
    elif x[0] == '-':
        (_, *args) = x
        tmp = 0
        for i in args:
            if not (isinstance(i,int) or isinstance(i,float)): #int도 아니고 float도 아닐때.. ->ex. 스트링?
                if i in mem:
                    if isinstance(mem[i],int) or isinstance(mem[i],float):
                        if i == args[0] : #첫번째 원소일 때
                            tmp = tmp + mem[i]
                        else:
                            tmp = tmp - mem[i]
                else:
                    return "ERROR : 올바르지 않은 자료형!"
            else:
                if i == args[0] :
                    tmp = tmp + i
                else:
                    tmp = tmp - i
        return tmp   
    elif x[0] == '*':
        (_, *args) = x
        tmp = 0
        for i in args:
            if not (isinstance(i,int) or isinstance(i,float)): #int도 아니고 float도 아닐때.. ->ex. 스트링?
                if i in mem:
                    if isinstance(mem[i],int) or isinstance(mem[i],float):
                        if i == args[0] : #첫번째 원소일 때
                            tmp = tmp + mem[i]
                        else:
                            tmp = tmp * mem[i]
                else:
                    return "ERROR : 올바르지 않은 자료형!"
            else:
                if i == args[0] :
                    tmp = tmp + i
                else:
                    tmp = tmp * i
        return tmp           
    elif x[0] == '/':
        (_, *args) = x
        tmp = 0
        for i in args:
            if not (isinstance(i,int) or isinstance(i,float)): #int도 아니고 float도 아닐때.. ->ex. 스트링?
                if i in mem:
                    if isinstance(mem[i],int) or isinstance(mem[i],float):
                        if i == args[0] : #첫번째 원소일 때
                            tmp = tmp + mem[i]
                        else:
                            if mem[i] == 0: #0으로 나누려 하면 에러처리
                                return "ERROR : 0으로 나눌 순 없어용"
                            else:
                                tmp = tmp / mem[i]
                else:
                    return "ERROR : 올바르지 않은 자료형!"
            else:
                if i == args[0] :
                    tmp = tmp + i
                else:
                    if i == 0: #0으로 나누려 하면 에러처리
                        return "ERROR : 0으로 나눌 순 없어용"
                    else:
                        tmp = tmp / i
        return tmp 

    ##################수정요망####################
    elif x[0] == 'IF': ################ IF return 값 수정해줘야함 #############
        (_, test, conseq, *alt) = x 
        if len(alt)>=2 : #alt 2개 이상이면 에러처리
            return "ERROR : 입력값이 너무 많아요 ㅠㅠ"
        if eval(test, dic):
            exp = eval(conseq, dic)
        elif alt is None: # alt 가 없을때
            return False ###################이거 왜 해준거라했지 건아..? #################
        else:
            exp = eval(alt[0], dic)
        return eval(exp, dic)
    
    elif x[0] == 'COND':
        (_, *ifexp) = x
        for exp in ifexp:
            test = exp[0]
            conseq = exp[1]
            if eval(test, dic):
                return eval(conseq, dic)

    elif x[0] == 'PRINT':
        (_, val) = x
        val = eval(val, dic)
        print(val)

    elif x[0] == 'define':
        (_, var, exp) = x
        dic[var] = eval(exp, dic)
    
    
    elif x[0] == 'SETQ': # argument 2개 아니면 error
        
        #입력값 2개 아니면 에러 처리
        (_, *inputcheck) = x
        if len(inputcheck) < 2:
            return "ERROR : 입력값이 너무 적어요 ㅠㅠ"
        elif len(inputcheck) > 2:
            return "ERROR : 입력값이 너무 많아요 ㅠㅠ"
        
        (_, var, exp) = x
        
        if not isinstance(var,str): #스트링이 아니면 에러처리
            return "ERROR : 입력값이 잘못됐어요.. (변수)"

        if isinstance(eval(exp,dic), list):
            mem[var] = eval(exp,dic)
            return mem[var]
        else:
            mem[var]=eval(exp,dic)
            return mem[var]


    elif x[0] == 'LIST':
        (_, *args) = x
        return list_procedure(*args)
   

    elif x[0] == 'REVERSE':
        (_, reverseList) = x
        L = ["'"]
        exp = eval(reverseList, dic)
        if isList(exp)[0]:
            exp[1].reverse()
            L.append(exp[1])
            return L

    elif x[0] == 'ATOM':
        (_, exp) = x
        exp = eval(exp, dic)
        if isinstance(exp, list):
            return False
        elif isinstance(exp, int) or isinstance(exp, float):
            return True
        elif isinstance(exp,str):
            return True

    elif x[0] == 'NTH':
        (_, exp, nthList) = x
        if isList(eval(nthList, dic))[0]:  # true 이면
            if isList(eval(nthList, dic))[1] == 0:  # 직접 입력
                return eval(nthList, dic)[1][eval(exp, dic)]
            elif isList(eval(nthList, dic))[1] == 1:  # 저장된 리스트
                return mem[eval(nthList, dic)][eval(exp, dic)]
    elif x[0]=='CONS':
        (_, var, consList) = x
        T=["'"]
        L=[]
        var = eval(var, dic)
        consList = eval(consList, dic)
        print(var)
        if isinstance(var,int) or isinstance(var,float):
            L.append(var)
        elif isinstance(var, str):
            if var in mem:
                L.append(mem[var])
            L.append(var)
        elif isinstance(var, list):
            L.append(var)
            
        if isinstance(consList, str):
            if consList in mem:
                if mem[consList][0] == "'":
                    if isinstance(mem[consList][1], list):
                        L.extend(mem[consList][1])
                elif isinstance(mem[consList],int) or isinstance(mem[consList],float):
                    L.extend(mem[consList])
        elif isList(consList)[0]:  # true 이면
            if isList(consList)[1] == 0:  # 직접 입력
                L.extend(consList[1])
            elif isList(consList)[1] == 1:  # 저장된 리스트
                L.extend(mem[consList][1])
        T.append(L)
        return T

    elif x[0] == 'MEMBER':
        (_, word, memberList) = x
        T = ["'"]
        if memberList in mem:
            memberList = mem[memberList][1]
            startIndex = memberList.index(word[1])
            T.append(memberList[startIndex:])
            return T
    
    elif x[0]=='REMOVE':
        (_, var, exp)=x
        L = ["'"]
        word=eval(var,dic)
        removeList=eval(exp,dic)
        while(True):
            try:
                removeList[1].remove(word)
            except ValueError:
                L.append(removeList[1])
                return L
    
    elif x[0] == 'ASSOC':
        (_, key, assocList) = x 
        # assocList 예시 ["'", [["'", ['ONE', 1]], ["'", ['TWO', 2]], ["'", ['THREE', 3]]]]
        key = eval(key, dic)
        #assocTuple 예시 [["'", ['ONE', 1]]
        for assocTuple in assocList[1]:
            if key == assocTuple[1][0]:
                return assocTuple[1][1]
    
    elif x[0] == 'SUBST':
        (_, word, word_sub, substList) = x
        word = eval(word, dic)
        word_sub = eval(word_sub, dic)
        sub_idx = substList[1].index(word_sub)
        substList[1][sub_idx] = word
        return substList
    #     else:
    #         print("Error")
    
    
    elif x[0] == 'CAR':
        (_, carList) = x
        return CAR_procedure(carList, dic)
    
    elif x[0] == 'CDR':
        (_, cdrList) = x
        return CDR_procedure(cdrList, dic)

    elif x[0] == 'CADDR':
        (_, caddrList) = x
        return CAR_procedure(CDR_procedure(CDR_procedure ( caddrList, dic) , dic), dic)

    elif x[0] == 'REVERSE':
        (_, reverseList) = x
        L = ["'"]
        exp = eval(reverseList, dic)
        if isList(exp)[0]:
            exp[1].reverse()
            L.append(exp[1])
            return L
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
     ########## Predicate 함수 ############

    elif x[0] == 'NULL':
        (_, exp) = x
        if exp=='':
            return True
        L=eval(exp,dic)
        if isList(L)[0]:
            return L[1]==[]
        else:
            return False
    elif x[0] == 'MINUSP':
        (_, exp) = x
        exp = eval(exp, dic)
        if numberp_procedure(exp) == True:
            if exp < 0:
                return True
            else:
                return False
        else:
            print("Error")
    
    elif x[0] == 'EQUAL':
        (_, var1, var2)=x
        try:
            return eval(var1,dic)==eval(var2,dic)
        except TypeError:
            return False

    elif x[0] == '<':
        (_, var1, var2)=x
        try:
            return eval(var1,dic)<eval(var2,dic)
        except TypeError:
            return False
    
    elif x[0] == '=':
        (_, var1, var2)=x
        try:
            return eval(var1,dic) == eval(var2,dic)
        except TypeError:
            return False

    elif x[0] == '>=':
        (_, var1, var2)=x
        try:
            return eval(var1,dic)>=eval(var2,dic)
        except TypeError:
            return False
        
            
    elif x[0] == 'lambda':
        (_, parms, body, *args) = x
        return lambda_procedure(parms, body, args)

    elif x[0] == 'STRINGP':
        (_,var)=x
        if isinstance(eval(x,dic),str):
            return True
        else:
            return False

    else:
        proc = eval(x[0], dic)
        args = [eval(exp, dic) for exp in x[1:]]
        try: return proc(args)
        except TypeError:
            args=[eval(exp,dic) for exp in x[0:]]
            return args

def printlist(l):
    if l[0] == "'" and isinstance(l[1],list):
        tmp = "("
        for i in l[1]:
            if not isinstance(i,list): #리스트가 아닌 경우
                if isinstance(i, str):
                    if not i == l[1][0] :
                        tmp = tmp + " " + i
                    else:
                        tmp = tmp + i
                else:
                    if not i == l[1][0]:
                        tmp = tmp + " " + str(i)
                    else:
                        tmp = tmp + str(i)
            else: #리스트인 경우
                if not i == l[1][0] : 
                    tmp = tmp +" "+ printlist(i)
                else :
                    tmp = tmp +printlist(i)

                
        
        tmp = tmp + ")"
        return tmp

def main():
    while(True):
        userInput = input("> ")
        rv = eval(expression_parser(userInput).pop(0), lisp_to_python_dic)
        if isinstance(rv, list): # 리스트면
            print(printlist(rv))
        else: # 리스트가 아니면
            print(rv)

if __name__ == "__main__":
    main()