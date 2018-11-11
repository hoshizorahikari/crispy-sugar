from hikari import Stack


def stack_permutation(A, B):
    # A是如<1, 2, 3, ..., n]的输入序列,B是待甄别的序列
    assert len(A) == len(B)
    n = len(A)
    S = Stack()
    ia = 0  # 序列A的下标
    for i in B:
        while S.empty() or i != S.top():  # 只要B当前元素未出现在S栈顶
            if ia >= n:  # 说明B当前元素在栈S中间,弹不出来...
                return False
            S.push(A[ia])  # 反复从A中取出顶元素,压入S
            ia += 1
        S.pop()  # S栈顶出现相同元素, 弹出,B移到下一个元素
    return True  # 感觉能出循环肯定S为空,B是栈混洗


if __name__ == "__main__":
    A = [1, 2, 3, 4, 5]
    B = [2, 4, 5, 3, 1]
    print(f'B{"" if stack_permutation(A,B) else "不"}是A的栈混洗')
