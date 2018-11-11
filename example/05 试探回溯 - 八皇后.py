import random


def conflict(lst, cur_row, cur_col):
    # cur_row为当前行数,也是前面的总行数
    for row in range(cur_row):
        # 列数相等,或列数之差对于行数之差,即对角线,为冲突
        if abs(cur_col-lst[row]) in [0, cur_row-row]:
            return True
    return False


def queen(n):  # n皇后问题,利用栈,非递归
    solution = []  # list模拟栈结构
    row, col = 0, 0
    while row > 0 or col < n:  # 这个条件怎么确定?
        if row >= n or col >= n:  # 如果出界,回溯到上一行,继续试探下一列
            row, col = row-1, solution.pop()+1
        else:  # 试探下一行,一直冲突就不断下一列,寻找可以摆放的列
            while col < n and conflict(solution, row, col):
                col += 1
            if n > col:  # 出了循环,col可能还会越界
                solution.append(col)  # 存在就放入
                row, col = row+1, 0  # 转入下一行第一列开始试探
                if row == n:  # 如果摆放到最后一行, 将结果yield
                    yield [x for x in solution]


def pretty_print(A):
     # □ ■
    print(A)
    for i in A:
        lst = ['■'] * len(A)
        lst[i] = '□'
        print(''.join(lst))
    print('-'*20)


def queen2(n, pre=()):  # 生成器+递归
    for col in range(n):
        if not conflict(pre, len(pre), col):
            if len(pre) == n-1:
                yield (col,)
            else:  # 后面的tuple层层向上传递, 组成新的tuple, 直到最开始调用
                for ret in queen2(n, pre+(col,)):
                    yield (col,)+ret


queen3_lst = []


def queen3(A, row=0):  # 从第0行开始
    if row == len(A):
        queen3_lst.append([x for x in A])
        return
    for col in range(len(A)):
        A[row] = col  # 每列逐一尝试,如果不冲突则递归下一行
        if not conflict(A, row, col):  # 冲突什么也不做,直接尝试下一列
            queen3(A, row+1)


if __name__ == "__main__":
    n = 8
    ret = list(queen(n))
    print(f'{n}皇后问题总共{len(ret)}种方法\n随机挑选一种方法:')
    pretty_print(random.choice(ret))

    print(len(list(queen2(n))))
    queen3([None for x in range(n)])
    print(len(queen3_lst))
