import re
import functools


def checkInput(formula):
    """检测输入合法与否,是否包含字母等非法字符"""
    return not re.search("[^0-9+\-*/.()^\s]",formula)

def formatInput(formula):
    """标准化输入表达式，去除多余空格等"""
    formula = formula.replace(' ','')
    formula = formula.replace('++', '+')
    formula = formula.replace('+-', '-')
    formula = formula.replace('-+', '-')
    formula = formula.replace('--', '+')
    return formula

def facOperation(s):
    """幂运算"""
    s = formatInput(s)
    sub_str = re.search('(\d+\.?\d*\^-?\d+\.?\d*)', s)
    while sub_str:
        sub_str = sub_str.group()
        l_num, r_num = sub_str.split('^')
        s = s.replace(sub_str, str(pow(float(l_num),float(r_num))))
        #print(s)
        s = formatInput(s)
        sub_str = re.search('(\d+\.?\d*\^\d+\.?\d*)', s)

    return s
def mul_divOperation(s):
    """乘法除法运算"""
    s = formatInput(s)
    sub_str = re.search('(\d+\.?\d*[*/]-?\d+\.?\d*)', s)
    while sub_str:
        sub_str = sub_str.group()
        if sub_str.count('*'):
            l_num, r_num = sub_str.split('*')
            s = s.replace(sub_str, str(float(l_num)*float(r_num)))
        else:
            l_num, r_num = sub_str.split('/')
            s = s.replace(sub_str, str(float(l_num) / float(r_num)))
        #print(s)
        s = formatInput(s)
        sub_str = re.search('(\d+\.?\d*[*/]\d+\.?\d*)', s)

    return s


def add_minusOperation(s):
    """加法减法运算
    思路：在最前面加上+号，然后正则匹配累加
    """
    s = formatInput(s)
    s = '+' + s
    #print(s)
    tmp = re.findall('[+\-]\d+\.?\d*', s)
    s = str(functools.reduce(lambda x, y:float(x)+float(y), tmp))
    #print(tmp)
    return s

def compute(formula):
    """无括号表达式解析"""
    #ret = formula[1:-1]
    ret = formatInput(formula)
    ret = facOperation(ret)
    ret = mul_divOperation(ret)
    ret = add_minusOperation(ret)
    return ret


def calc(formula):
    """计算程序入口"""
    has_parenthesise = formula.count('(')
    if checkInput(formula):
        formula = formatInput(formula)
        while has_parenthesise:
            sub_parenthesise = re.search('\([^()]*\)', formula) #匹配最内层括号
            if sub_parenthesise:
                #print(formula+"...before")
                formula = formula.replace(sub_parenthesise.group(), compute(sub_parenthesise.group()[1:-1]))
                #print(formula+'...after')
            else:
                has_parenthesise = False

        ret = compute(formula)
        return  '结果为：'+ret

    else:
        return("输入有误！")
