from hikari import Stack

operators = {  # 运算符对应编号
    '+': 0,
    '-': 1,
    '*': 2,
    '/': 3,
    '^': 4,
    '!': 5,
    '(': 6,
    ')': 7,
    '\0': 8,
}

priority = [  # 运算符优先级表
    # +    -    *    /    ^    !    (    )    \0  当前运算符
    ['>', '>', '<', '<', '<', '<', '<', '>', '>'],  # +  --
    ['>', '>', '<', '<', '<', '<', '<', '>', '>'],  # -  |
    ['>', '>', '>', '>', '<', '<', '<', '>', '>'],  # *  栈
    ['>', '>', '>', '>', '<', '<', '<', '>', '>'],  # /  顶
    ['>', '>', '>', '>', '>', '<', '<', '>', '>'],  # ^  运
    ['>', '>', '>', '>', '>', '>', ' ', '>', '>'],  # !  算
    ['<', '<', '<', '<', '<', '<', '<', '=', ' '],  # (  符
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],  # )  |
    ['<', '<', '<', '<', '<', '<', '<', ' ', '='],  # \0 --
]


def evaluate(s):  # 计算中缀表达式s的值
    s += '\0'  # 末尾添加'\0'尾哨兵
    nums, optr = Stack(), Stack()  # 存放操作数和运算符的两个栈
    rpn = ''  # 逆波兰表达式
    optr.push('\0')  # 尾哨兵'\0'首先入栈
    i = 0  # 表达式当前下标
    while not optr.empty():
        if is_digit(s[i]):
            i, n = read_num(s, i)  # 读入数字可能多位
            nums.push(n)  # 操作数入栈
            rpn += f'{n} '  # 并添加到rpn末尾
        elif s[i] == ' ':  # 忽略空格
            i += 1
        else:
            pri = order_between(optr.top(), s[i])
            if pri == '<':  # 栈顶运算符优先级低
                optr.push(s[i])  # 推迟计算,当前运算符入栈
                i += 1
            elif pri == '>':  # 栈顶运算符优先级高,计算
                op = optr.pop()
                rpn += f'{op} '  # 栈顶运算符出栈,接至RPN末尾
                if op == '!':  # 一元运算符
                    nums.push(fac(nums.pop()))
                else:  # 二元运算符
                    n2 = nums.pop()
                    n1 = nums.pop()
                    nums.push(cal(n1, op, n2))  # 计算结果入栈
            elif pri == '=':  # 优先级相等(当前运算符是右括号或'\0')
                optr.pop()  # 相当于删除右括号
                i += 1
    return rpn, nums.pop()  # 返回逆波兰表达式和计算值


def is_digit(n):  # 判断单个字符是不是整数
    return n in '0123456789'


def read_num(s, index):  # 只考虑正整数
    ret = 0
    while is_digit(s[index]):  # 设置了尾哨兵, 不必判断是否出界
        ret = ret*10+int(s[index])
        index += 1
    return index, ret


def order_between(a, b):  # 根据优先级表获取两个运算符优先级
    return priority[operators[a]][operators[b]]


def fac(n):  # 阶乘
    s = 1
    while n > 0:
        s *= n
        n -= 1
    return s


def cal(n1, op, n2):  # 二元运算符
    if op == '+':
        return n1+n2
    elif op == '-':
        return n1-n2
    elif op == '*':
        return n1*n2
    elif op == '/':
        return n1/n2
    elif op == '^':
        return n1**n2


if __name__ == "__main__":
    infix = '0! + 123 + 4 * (5 * 6! + 7! / 8) / 9'
    rpn, ret = evaluate(infix)
    print(f'{rpn} = {ret}')  # 0 ! 123 + 4 5 6 ! * 7 ! 8 / + * 9 / + = 2004.0
