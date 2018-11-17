from hikari import Stack, Queue


class TreeNode():  # 二叉树结点
    def __init__(self, val, parent=None, left=None, right=None):
        self.val = val
        self.parent = parent
        self.left = left
        self.right = right
        self.height = 0  # 高度

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

    def succ(self):  # 获取中序遍历下该结点直接后继
        pass

    def traverse_level(self, visit):  # 以该结点为根的层次遍历
        pass

        # queue = Queue()  # 辅助队列
        # queue.enqueue(self)  # 首先根结点入队
        # while not queue.empty():
        #     x = queue.dequeue()
        #     visit(x.val)
        #     if x.left is not None:  # 左孩子入队
        #         queue.enqueue(x.left)
        #     if x.right is not None:  # 右孩子入队
        #         queue.enqueue(x.right)

    def pre_traverse(self):  # 子树前序遍历
        pass

    def in_traverse(self):  # 子树中序遍历
        pass

    def post_traverse(self):  # 子树后序遍历
        pass

    @staticmethod
    def stature(p):  # 获取结点p子树的高度
        if p is None:
            return -1
        assert isinstance(p, TreeNode)
        return p.height

    def __eq__(self, other):
        return self.val == other

    def __lt__(self, other):
        return self.val < other.val

    def __gt__(self, other):
        return self.val > other.val


class BinaryTree():  # 二叉树
    def __init__(self, root=None):
        self.__root = root
        self.__size = 0

    def build_tree(self, arr):
        """自己瞎写的，构造二叉树"""
        if not arr:
            return
        self.__root = TreeNode(arr.pop(0))
        queue = [self.__root]
        while arr:
            p = queue.pop(0)
            val = arr.pop(0)
            if val == '#':
                p.left = None
            else:
                p.left = TreeNode(val, p)
                queue.append(p.left)
            if not arr:
                return
            val = arr.pop(0)

            if val == '#':
                p.right = None
            else:
                p.right = TreeNode(val)
                queue.append(p.right)

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

    def insert_as_right_child(self, x, e):
        self.__size += 1  # 假设x存在并没有右孩子
        x.insert_as_right_child(e)
        BinaryTree.update_height_above(x)  # 祖先结点高度可以增加
        return x.right

    def preorder_traverse(self, visit):  # 先序遍历
        assert callable(visit)
        # self.__preorder_traversal(self.__root, visit)
        BinaryTree.__preorder_i2(self.__root, visit)

    @staticmethod
    def __preorder_traverse(x, visit):  # O(n)
        if x is None:
            return
        visit(x.val)  # 访问根结点元素
        # 再对左右子树分别递归
        BinaryTree.__preorder_traverse(x.left, visit)
        BinaryTree.__preorder_traverse(x.right, visit)

    @staticmethod
    def __preorder_i1(x, visit):
        s = Stack()  # 辅助栈
        if x is not None:
            s.push(x)  # 根结点入栈
        while not s.empty():
            p = s.pop()  # 弹出并访问当前结点
            visit(p.val)
            if p.right is not None:  # 右孩子先入后出
                s.push(p.right)
            if p.left is not None:  # 左孩子后入先出
                s.push(p.left)

    @staticmethod
    def __visit_along_left(x, vist, stack):
        while x is not None:
            vist(x.val)  # 访问左侧通路各个结点
            stack.push(x.right)  # 右孩子入栈
            x = x.left  # 左侧下行

    @staticmethod
    def __preorder_i2(x, visit):
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
    def __inorder_i1(x, visit):  # 中序遍历迭代版本1
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
        BinaryTree.__inorder_i1(self.__root, visit)

    def postorder_traverse(self, visit):  # 后序遍历
        assert callable(visit)
        BinaryTree.__postorder(self.__root, visit)

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
        # if self.empty():
        #     return
        assert callable(visit)
        # self.__root.traverse_level(visit)
        BinaryTree.__traverse_level(self.__root, visit)


import hikari_tool
if __name__ == "__main__":
    # arr = [x for x in range(1, 16)]
    arr = list('idlchkna#f#j#mp#beg####o#')
    tree = BinaryTree()
    tree.build_tree(arr)
    lst = []
    tree.level_order_traverse(lambda x: lst.append(x))
    print('→'.join(lst))  # i→d→l→c→h→k→n→a→f→j→m→p→b→e→g→o
