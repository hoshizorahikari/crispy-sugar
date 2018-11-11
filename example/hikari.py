class Stack():  # 栈
    def __init__(self):
        self.__elem = []
        self.__size = 0

    def empty(self):  # 判空
        return self.__size <= 0

    def size(self):  # 获取元素个数
        return self.__size

    def push(self, e):  # 压栈
        self.__elem.append(e)
        self.__size += 1

    def pop(self):  # 出栈
        # assert not self.empty()
        if self.empty():
            return
        self.__size -= 1
        return self.__elem.pop()

    def top(self):  # 获取栈顶元素
        # assert not self.empty()
        if self.empty():
            return
        return self.__elem[-1]

    def __len__(self):  # len()
        return len(self.__elem)

    def to_list(self):
        return [x for x in self.__elem]


class ListNode():
    def __init__(self, val=None, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

    def insert_prev(self, e):  # 前插入算法
        x = ListNode(e, self.prev, self)
        self.prev.next = x
        self.prev = x
        return x

    def insert_next(self, e):  # 后插入算法
        x = ListNode(e, self, self.next)
        self.next.prev = x
        self.next = x
        return x

    def __lt__(self, other):
        return self.val < other.val


class List():  # 基于双向链表
    def __init__(self, arr=None):  # 初始化
        self.__header = ListNode()
        self.__trailer = ListNode()
        self.__header.next = self.__trailer  # 首尾相连
        self.__trailer.prev = self.__header
        self.__size = 0
        if arr is not None:
            try:
                for i in arr:
                    self.append(i)
            except Exception as e:
                print(e)

    def size(self):
        return self.__size

    def __len__(self):
        return self.__size

    def empty(self):
        return self.__size <= 0

    def first(self):  # 首结点位置
        return self.__header.next

    def last(self):  # 末结点位置
        return self.__trailer.prev

    def valid(self, p):  # 判断位置p是否有效
        return p and self.__trailer != p and self.__header != p

    def __find(self, e, n, p):
        while n > 0:  # 从右向左逐个将p的n个真前驱与e比较
            p = p.prev
            if e == p.val:
                return p
            n -= 1

    def find(self, e):
        return self.__find(e, self.__size, self.__trailer)

    def insert_before(self, p, e):  # 前插法
        # if self.valid(p):
        self.__size += 1
        return p.insert_prev(e)  # e作为p的前驱插入

    def insert_after(self, p, e):  # 后插法
        # if self.valid(p):
        self.__size += 1
        return p.insert_next(e)

    def append(self, e):
        return self.insert_before(self.__trailer, e)

    def prepend(self, e):
        return self.insert_after(self.__header, e)

    def remove(self, p):  # 删除元素
        p.prev.next = p.next
        p.next.prev = p.prev
        self.__size -= 1
        return p.val

    def clear(self):
        while not self.empty():
            self.remove(self.first())  # 反复删除首结点

    def deduplicate(self):
        if self.__size < 2:  # <1个结点自然不重复
            return 0
        old_size = self.__size
        p = self.first().next  # 初始第2个结点
        r = 1  # 初始第2个结点只有1个前驱
        while p != self.__trailer:
            q = self.__find(p.val, r, p)  # 在p的r个真前驱寻找相同者
            if q is None:  # q重复则删除,否则后移1位
                r += 1
            else:
                self.remove(q)
            p = p.next
        return old_size-self.__size

    def to_list(self):
        lst = []
        if not self.empty():
            p = self.first()
            while p != self.__trailer:
                lst.append(p.val)
                p = p.next
        return lst

    def show(self):
        print(self.to_list())

    def traverse(self, f):
        assert callable(f)
        if not self.empty():
            p = self.first()
            while p != self.__trailer:
                p.val = f(p.val)

    def pop(self):  # 删除首结点
        return self.remove(self.first())

    def uniquify(self):
        if self.__size < 2:  # <1个结点自然不重复
            return 0
        old_size = self.__size
        p = self.first()  # p初始为第1个结点
        q = p.next  # q一直是p的直接后继
        while q != self.__trailer:
            if p.val != q.val:  # 若不等,转向下一个区段
                p = q
            else:  # 若相同,删除后者
                self.remove(q)
            q = p.next
        return old_size-self.__size

    def __search(self, e, n, p):
        # 在有序列表结点p的n个真前驱中找到不大于e的最后者
        while n >= 0:  # 对于p的最近n个前驱,从右向左逐个比较
            p = p.prev
            if p.val and p.val <= e:
                break
            n -= 1
        return p

    def search(self, e):
        return self.__search(e, self.__size, self.__trailer)

    def sort(self):
        self.__insertion_sort(self.first(), self.__size)

    def __insertion_sort(self, p, n):  # 起始于p的连续n个结点做插入排序
        for r in range(n):
            # 从p的r个前驱寻找合适位置,插入,r即有序前缀长度
            self.insert_after(self.__search(p.val, r, p), p.val)
            p = p.next  # 转向下一个结点,无序的首结点
            self.remove(p.prev)  # 插入是复制元素再插入,故前一个结点已无用


class Queue(List):  # 队列
    def enqueue(self, e):  # 入队,尾部删除
        self.append(e)

    def dequeue(self):  # 出队,首部删除
        return self.pop()

    def front(self):
        return self.first().val

    def rear(self):
        return self.last().val
