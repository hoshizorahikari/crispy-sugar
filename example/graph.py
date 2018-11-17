class GraphError(Exception):
    """Graph错误类"""
    pass


class GraphMatrix():
    """图, 用邻接矩阵表示"""

    def __init__(self, directed=True, vertices=None, edges=None):
        self.__data = vertices  # 顶点数据list
        self.__vertex_num = len(data) if data else 0  # 顶点数
        self.__edge_num = 0  # 边数
        self.__matrix = []  # 邻接矩阵
        self.__INFINITY = '∞'  # 2**31-1
        self.__directed = directed  # 有向图or无向图
        self.__init_grapgh()

    def __init_grapgh(self):  # 初始化图
        if self.__vertex_num > 0:
            # 初始对角线为0,其他为∞
            for i in range(self.__vertex_num):
                row = [self.__INFINITY] * self.__vertex_num
                row[i] = 0
                self.__matrix.append(row)

    def get_vertex_num(self):
        """获取顶点个数"""
        return self.__vertex_num

    def __invalid(self, v):
        """顶点下标无效与否"""
        return v < 0 or v >= self.__vertex_num

    def add_vertex(self):
        """添加新顶点"""
        # 每行最后添加∞
        for i in range(self.__vertex_num):
            self.__matrix[i].append(self.__INFINITY)
        # 添加新的一行
        new_row = [self.__INFINITY] * self.__vertex_num
        new_row.append(0)
        self.__matrix.append(new_row)
        self.__vertex_num += 1  # 顶点数+1

    def insert_edge(self, u, v, weight=1):
        """给两个顶点之间添加边,权值默认1"""
        if self.__invalid(u) or self.__invalid(v):
            raise GraphError('{} or {} is not a valid vertex.'.format(u, v))
        if self.__matrix[u][v] == self.__INFINITY:
            self.__edge_num += 1  # 没边到有边,边数+1,否则视为修改权值
        self.__matrix[u][v] = weight
        if not self.__directed:  # 无向图对称
            self.__matrix[v][u] = weight

    def get_edge_weight(self, u, v):
        """获取边的权值"""
        if self.__invalid(u) or self.__invalid(v):
            raise GraphError('{} or {} is not a valid vertex.'.format(u, v))
        return self.__matrix[u][v]

    def is_edge(self, u, v):
        """判断u和v是不是邻接点,是不是边"""
        if self.__invalid(u) or self.__invalid(v):
            raise GraphError('{} or {} is not a valid vertex.'.format(u, v))
        return self.__matrix[u][v] not in (0, self.__INFINITY)

    def out_edges(self, v):
        """获取顶点v的出边和权值(邻接顶点下标,边的权值)元组组成的列表"""
        if self.__invalid(v):
            raise GraphError('{} is not a valid vertex.'.format(v))
        edges = []
        for u in range(self.__vertex_num):  # 就是获取v行权值不是0和∞的列数
            if self.is_edge(v, u):
                edges.append((u, self.__matrix[v][u]))
        return edges

    def __str__(self):
        return '\n'.join([''.join([f'{i:^8}' for i in x]) for x in self.__matrix])
        # return '[\n' + ',\n'.join(map(str, self.__matrix)) + '\n]'

    def rebuild_graph(self, data, edges, directed=True):
        """重新构造图"""
        # self.__data = data
        # self.__directed = directed
        # self.__matrix = []
        # self.__vertex_num = len(data)
        # self.__edge_num = 0
        # self.__init_grapgh()  # 全部初始化
        self.__init__(data, directed)
        for edge in edges:  # 根据给定的边信息插入边
            self.insert_edge(*edge)


if __name__ == "__main__":
    g = GraphMatrix()
    data = [chr(65+x) for x in range(4)]
    edges = ((0, 3, 8), (1, 0, 5), (2, 1, 3), (0, 2, 9))
    # edges = ((0, 4), (0, 7), (1, 2), (1, 3),
    #          (2, 4), (3, 7), (4, 5), (5, 6), (6, 7))
    g.rebuild_graph(data, edges)
    print(g)
