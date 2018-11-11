from hikari import Stack


def convert(n, base):  # 十进制n转换到base进制
    digit = '0123456789ABCDEF'
    assert 1 < base <= len(digit)
    s = Stack()
    while n > 0:
        s.push(digit[n % base])  # 将余数(对应位数)入栈
        n //= base  # n变为n除以base的商
    ret = ''
    while not s.empty():
        ret += s.pop()
    return ret


if __name__ == "__main__":
    n = 123
    print(f'{n}的16进制: {convert(n,16)}')  # 123的16进制: 7B
    print(f'{n}的5进制: {convert(n,5)}')  # 123的5进制: 443
