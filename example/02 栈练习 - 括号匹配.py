from hikari import Stack


def paren(expression):  # 括号匹配
    s = Stack()
    for i in expression:  # 逐一检查字符
        if i == '(':  # 遇到左括号入栈
            s.push(i)
        elif i == ')':  # 遇到右括号,则弹出左括号
            if not s.empty():
                s.pop()
            else:  # 遇到右括号,且栈为空,不匹配
                return False
    return s.empty()  # 最终,栈为空则匹配


if __name__ == "__main__":
    expr = '((1+2)*3+4/(5-6))*7-(8-9)/10'
    print('匹配' if paren(expr) else '不匹配')  # 匹配
