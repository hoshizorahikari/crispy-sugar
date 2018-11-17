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

    # def set_head(self, head):  #
    #     assert isinstance(head, ListNode)
    #     self.__size = 1
    #     while head.next:
    #         self.__header.next = head
    #         head.prev = self.__header
    #         head = head.next
    #         self.__size += 1
    #     self.__trailer.pre = head
    #     head.next = self.__trailer

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


class TreeNode():  # 二叉树结点
    def __init__(self, val, parent=None, left=None, right=None):
        self.val = val
        self.parent = parent
        self.left = left
        self.right = right
        # self.height = 0  # 高度

    def insert_as_left_child(self, e):  # 作为左孩子插入
        self.left = TreeNode(e, self)
        return self.left

    def insert_as_right_child(self, e):
        self.right = TreeNode(e, self)
        return self.right

    def size(self):  # 后代总数,子树规模, O(n)
        s = 1  # 包括本身
        # 左右子树递归
        s += self.left.size() if self.left is not None else 0
        s += self.right.size() if self.right is not None else 0
        return s

    def __eq__(self, other):
        return self.val == other

    def __lt__(self, other):
        return self.val < other.val

    def __gt__(self, other):
        return self.val > other.val

    def has_left_child(self):
        return self.left is not None

    def has_right_child(self):
        return self.right is not None

    def is_leaf(self):
        return self.left is None and self.right is None

    def has_no_children(self):
        return self.is_leaf()

    def has_both_left_right(self):
        return self.left is not None and self.right is not None

    def has_child_x(self, x):
        return self.left == x or self.right == x

    @staticmethod
    def stature(p):  # 获取结点p子树的高度
        if p is None:
            return -1
        assert isinstance(p, TreeNode)
        return p.height


class BinaryTree():  # 二叉树
    def __init__(self, arr=None, root=None):
        self.__root = root
        self.__size = 0
        if arr is not None:
            self.build_tree(arr)

    def build_tree(self, arr=None):
        """自己瞎写的，构造二叉树"""
        arr = [] if arr is None else list(arr)
        n = len(arr)
        if n == 0:
            return
        self.__root = TreeNode(arr[0])
        queue = Queue()
        queue.enqueue(self.__root)
        index = 1
        self.__size = 1
        while index < n:  # 结束条件为arr元素全部添加到树
            # 取出队首结点, 将arr后2个元素作为该结点左右孩子并将孩子入队
            p = queue.dequeue()
            val = arr[index]
            index += 1
            if val == '#':
                p.left = None
            else:
                p.left = TreeNode(val, p)
                queue.enqueue(p.left)
                self.__size += 1
            if index >= n:
                return
            val = arr[index]
            index += 1
            if val == '#':
                p.right = None
            else:
                p.right = TreeNode(val, p)
                queue.enqueue(p.right)
                self.__size += 1

    @staticmethod
    def update_height(x):  # 更新结点x的高度,具体规则因树不同而异
        if x is None:
            return -1
        assert isinstance(x, TreeNode)
        # stature(p)=p.height is p else -1
        # x的高度为左右子树高度较大者+1, O(1)
        x.height = 1 + max(TreeNode.stature(x.left),
                           TreeNode.stature(x.right))
        return x.height

    @staticmethod
    def update_height_above(x):  # 更新结点x及祖先的高度
        if x is None:
            return
        assert isinstance(x, TreeNode)
        while x is not None:  # 可优化,一旦高度未变,即可终止
            BinaryTree.update_height(x)
            x = x.parent  # O(depth(x))

    def size(self):  # 规模
        return self.__size

    def empty(self):  # 判空
        return self.__root is None

    def root(self):  # 树根
        return self.__root

    def reset(self, root):  # 重设树根
        assert isinstance(root, TreeNode)
        self.__root = root
        self.__size = self.__root.size()

    def insert_as_right_child(self, x, e):
        self.__size += 1  # 假设x存在并没有右孩子
        x.insert_as_right_child(e)
        BinaryTree.update_height_above(x)  # 祖先结点高度可以增加
        return x.right

    def preorder_traverse(self, visit):  # 先序遍历
        assert callable(visit)
        BinaryTree.__preorder(self.__root, visit)

    @staticmethod
    def __visit_along_left(x, vist, stack):
        while x is not None:
            vist(x.val)  # 访问左侧通路各个结点
            stack.push(x.right)  # 右孩子入栈
            x = x.left  # 左侧下行

    @staticmethod
    def __preorder(x, visit):
        s = Stack()  # 辅助栈
        while True:
            # 访问子树x的左侧通路,右子树入栈缓冲
            BinaryTree.__visit_along_left(x, visit, s)
            if s.empty():
                break
            x = s.pop()  # 弹出下一子树的根

    @staticmethod
    def __go_along_left(x, stack):
        while x is not None:
            stack.push(x)  # 反复将左侧通路结点入栈
            x = x.left

    @staticmethod
    def __inorder(x, visit):  # 中序遍历迭代版本1
        s = Stack()  # 辅助栈
        while True:
            BinaryTree.__go_along_left(x, s)
            if s.empty():
                break
            x = s.pop()  # 取出最左侧的结点
            visit(x.val)  # 访问之
            x = x.right  # 转向右子树

    def inorder_traverse(self, visit):  # 中序遍历
        assert callable(visit)
        BinaryTree.__inorder(self.__root, visit)

    def postorder_traverse(self, visit):  # 后序遍历
        assert callable(visit)
        # BinaryTree.__postorder_i2(self.__root, visit)
        BinaryTree.__postorder_iter(self.__root, visit)

    @staticmethod
    def __postorder(x, visit):
        if x is None:
            return
        BinaryTree.__postorder(x.left, visit)
        BinaryTree.__postorder(x.right, visit)
        visit(x.val)

    @staticmethod
    def __traverse_level(x, visit):  # 以该结点为根的层次遍历
        if x is None:
            return
        queue = Queue()  # 辅助队列
        queue.enqueue(x)  # 首先根结点入队
        while not queue.empty():
            x = queue.dequeue()
            visit(x.val)
            if x.left is not None:  # 左孩子入队
                queue.enqueue(x.left)
            if x.right is not None:  # 右孩子入队
                queue.enqueue(x.right)

    def level_order_traverse(self, visit):  # 层次遍历
        assert callable(visit)
        BinaryTree.__traverse_level(self.__root, visit)

    def preorder_list(self):
        lst = []
        self.preorder_traverse(lambda x: lst.append(x))
        return lst

    def inorder_list(self):
        lst = []
        self.inorder_traverse(lambda x: lst.append(x))
        return lst

    def postorder_list(self):
        lst = []
        self.postorder_traverse(lambda x: lst.append(x))
        return lst

    def level_order_list(self):
        lst = []
        self.level_order_traverse(lambda x: lst.append(x))
        return lst

    @staticmethod
    def __go_to_HLVFL(stack):
        # 在以栈顶结点为根的子树中，找到最高左侧可见叶结点
        x = stack.top()
        while x is not None:  # 沿途结点依次入栈
            if x.left is not None:
                if x.right is not None:  # 右孩子先入后出
                    stack.push(x.right)
                stack.push(x.left)
            else:
                stack.push(x.right)  # 没有左孩子,转向右
            x = stack.top()  # 转到下一个结点
        stack.pop()  # 删除空结点

    @staticmethod
    def __postorder_iter(x, visit):  # 后序遍历迭代版本
        # print('后序遍历迭代版本')
        s = Stack()
        if x is not None:
            s.push(x)  # 根结点入栈
        while not s.empty():
            # 若栈顶不是当前结点父结点,必是其右兄弟,需要在以
            # 右兄弟为根的子树中找到HLVFL(深入其中)
            if s.top() != x.parent:
                BinaryTree.__go_to_HLVFL(s)
            x = s.pop()
            visit(x.val)

    @staticmethod
    def __postorder_i2(x, visit):
        if x is None:
            return
        pre = None  # 记录上一次访问结点
        s = Stack()
        s.push(x)
        while not s.empty():
            x = s.top()
            # 如果当前结点是叶结点或孩子结点刚被访问过
            if x.is_leaf() or (pre is not None and (x.has_child_x(pre))):
                visit(x.val)  # 访问之
                pre = s.pop()  # 弹出并更新记录
            else:  # 左右孩子入栈,如果有右孩子,则先入(后出)
                if x.has_right_child():
                    s.push(x.right)
                if x.has_left_child():
                    s.push(x.left)
