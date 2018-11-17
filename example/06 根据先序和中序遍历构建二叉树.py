from hikari import BinaryTree, TreeNode


def build_binary_tree(preoder, inorder):
    # 根据先序遍历和中序遍历构建二叉树,返回根结点
    assert set(preoder) == set(inorder)
    n = len(preoder)
    return __build(preoder, 0, n, inorder, 0, n)


def __build(preorder, plow, phigh, inorder, ilow, ihigh, parent=None):
    assert phigh-plow == ihigh-ilow
    if phigh-plow <= 0:  # 递归基, 序列长度为0
        return
    root_val = preorder[plow]  # 先序遍历首个为根结点
    root = TreeNode(root_val, parent)
    ipos = ilow
    while ipos < ihigh:  # 寻找中序遍历根结点位置
        if inorder[ipos] == root_val:
            break
        ipos += 1
    len_left = ipos-ilow  # 左子树元素个数
    # 左子树: preorder[plow, plow+1+len_left) + inorder[ilow, ipos)
    root.left = __build(preorder, plow+1, plow+1+len_left,
                        inorder, ilow, ipos, root)
    # 右子树: preorder[plow+1+len_left, phigh) + inorder[ipos, ihigh)
    root.right = __build(preorder, plow+1+len_left, phigh,
                         inorder, ipos+1, ihigh, root)
    return root


# def re_construct_binary_tree(pre_lst, in_lst):
#     # 转成集合判断元素是不是一致
#     if set(pre_lst) != set(in_lst):
#         return
#     if len(pre_lst) == 0:
#         return
#     root_num = pre_lst[0]  # 前序遍历第 1 个为根结点
#     root = TreeNode(root_num)
#     pos = in_lst.index(root_num)  # 寻找根结点在中序遍历的位置
#     # 对左右子树分别递归
#     root.left = re_construct_binary_tree(pre_lst[1:pos + 1], in_lst[:pos])
#     root.right = re_construct_binary_tree(pre_lst[pos + 1:], in_lst[pos + 1:])
#     return root


if __name__ == "__main__":
    preorder_lst = [44, 33, 26, 38, 41, 55, 47, 45, 52]
    inorder_lst = [26, 33, 38, 41, 44, 45, 47, 52, 55]

    root = build_binary_tree(preorder_lst, inorder_lst)
    tree = BinaryTree(root=root)
    lst = []
    tree.postorder_traverse(lambda x: lst.append(x))
    print(lst)  # [26, 41, 38, 33, 45, 52, 47, 55, 44]
