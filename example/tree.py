class TreeNode():  # 二叉树结点
    def __init__(self, val, parent=None, left=None, right=None):
        self.val = val
        self.parent = parent
        self.left = left
        self.right = right
        self.height = 0  # 高度
        # self.size = 0  # 子树规模

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

    def traverse_level(self):  # 子树层序遍历
        pass

    def pre_traverse(self):  # 子树前序遍历
        pass

    def in_traverse(self):  # 子树中序遍历
        pass

    def post_traverse(self):  # 子树后序遍历
        pass


class BinaryTree():  # 二叉树
    def __init__(self, root=None):
        self.__root = root
        self.__size = 0

    @staticmethod
    def stature(p):
        if p is None:
            return -1
        assert isinstance(p, TreeNode)
        return p.height

    @staticmethod
    def update_height(x):  # 更新结点x的高度,具体规则因树不同而异
        if x is None:
            return -1
        assert isinstance(x, TreeNode)
        # stature(p)=p.height is p else -1
        # x的高度为左右子树高度较大者+1, O(1)
        x.height = 1 + max(BinaryTree.stature(x.left),
                           BinaryTree.stature(x.right))
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
        # if x is None:
        #     return
        # assert isinstance(x, TreeNode)
        self.__size += 1  # 假设x存在并没有右孩子
        x.insert_as_right_child(e)
        BinaryTree.update_height_above(x)  # 祖先结点高度可以增加
        return x.right
