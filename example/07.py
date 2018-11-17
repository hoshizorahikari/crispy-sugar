from hikari import BinaryTree

if __name__ == "__main__":
    tree = BinaryTree('KiJ#h##bG#aeF##CD##')
    # tree = BinaryTree('abcd##efg#h')
    print('→'.join(tree.inorder_list()))  # i→b→a→h→C→e→D→G→F→K→J
    print('→'.join(tree.postorder_list()))  # a→b→C→D→e→F→G→h→i→J→K
