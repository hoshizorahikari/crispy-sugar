#include <iostream>
using namespace std;
#define Position(T) ListNode<T> * // 列表结点的位置
typedef int Rank;

template <typename T> //简洁起见,完全开放而不过度封装
struct ListNode
{ //列表结点模板类(双向链表形式实现)
    T data;
    Position(T) prev; // 前驱
    Position(T) next; // 后继
    ListNode() {}
    ListNode(T e, Position(T) p = nullptr, Position(T) n = nullptr)
    { // 默认构造器
        this->data = e;
        this->prev = p;
        this->next = n;
    }
    Position(T) insertPrev(T const &e); //插入作为前驱
    Position(T) insertNext(T const &e); // 插入作为后继
};
template <typename T> //前插入算法(后插入算法完全对称)
Position(T) ListNode<T>::insertPrev(T const &e)
{                                                      //O(1)
    Position(T) x = new ListNode(e, this->prev, this); //创建新结点
    this->prev->next = x;
    this->prev = x; // 建立链接
    return x;       // 返回新结点位置
}

template <typename T> // 后插入算法
Position(T) ListNode<T>::insertNext(T const &e)
{
    Position(T) x = new ListNode(e, this, this->next); //创建新结点
    this->next->prev = x;
    this->next = x;
    return x;
}
template <typename T>
class List
{
  private:
    int _size;
    Position(T) header;
    Position(T) trailer; // 头部尾部哨兵
  protected:
    void init();
    void copyNodes(Position(T), int);
    void initByArray(T *arr, Rank low, Rank high)
    {
        init();
        for (Rank i = low; i < high; i++)
            append(arr[i]);
    }
    void selectionSort(Position(T) p, int n);
    Position(T) selectMax(Position(T) p, int n);
    void insertionSort(Position(T) p, int n);

  public:
    List() { init(); } //默认构造函数
    List(List<T> const &L)
    { //整体复制列表L
        copyNodes(L.first(), L.size());
    }
    List(List<T> const &L, Rank r, int n)
    { //复制列表L中自第r项起的n项
        copyNodes(L[r], n);
    }
    List(Position(T) p, int n)
    { //复制列表中自位置p起的n项
        copyNodes(p, n);
    }
    List(T *arr, Rank low, Rank high)
    {
        initByArray(arr, low, high);
    }
    List(T *arr, int length)
    {
        initByArray(arr, 0, length);
    }
    ~List()
    {                  //析构函数
        clear();       // 清空列表
        delete header; // 释放头尾哨兵
        delete trailer;
    };
    int size() const { return _size; }
    bool empty() const { return _size <= 0; }
    Position(T) first() const { return header->next; }
    Position(T) last() const { return trailer->prev; }
    bool valid(Position(T) p) { return p && (trailer != p) && (header != p); }
    T &operator[](Rank r) const;
    Position(T) find(T const &e, int n, Position(T) p) const;
    Position(T) find(T const &e) const { return find(e, _size, trailer); }
    Position(T) insertBefore(Position(T) p, T const &e);
    Position(T) insertAfter(Position(T) p, T const &e);

    Position(T) append(T const &e) { return insertBefore(trailer, e); }
    Position(T) prepend(T const &e) { return insertAfter(header, e); }
    T remove(Position(T) p);
    int clear();
    int deduplicate();
    void show() const;
    T pop() { return remove(first()); } //删除首结点
    // 、、----------------------
    int uniquify();
    Position(T) search(T const &e, int n, Position(T) p) const;
    Position(T) search(T const &e) const { return search(e, _size, trailer); }
    void sort()
    {
        // selectionSort(first(), _size);
        insertionSort(first(), _size);
    }
};

template <typename T>
void List<T>::init()
{ // 初始化, 创建列表统一调用
    header = new ListNode<T>();
    trailer = new ListNode<T>();

    header->next = trailer;
    header->prev = nullptr;
    trailer->prev = header;
    trailer->next = nullptr;
    _size = 0;
}

template <typename T> // 重载[]通过秩直接访问列表结点,效率低,慎用!
T &List<T>::operator[](Rank r) const
{ //assert: 0 <= r < _size
    Position(T) p = first();
    while (0 < r--) // 从首结点出发第r个结点
        p = p->next;
    return p->data;
}

template <typename T> // 0 <= n <= rank(p) < _size
Position(T) List<T>::find(T const &e, int n, Position(T) p) const
{                   // 顺序查找O(n)
    while (0 < n--) //从右向左逐个将p的前驱与e比较
        if (e == (p = p->prev)->data)
            return p; //直至命中或范围越界
    return nullptr;   //越出左边界,查找失败
}

template <typename T>
Position(T) List<T>::insertBefore(Position(T) p, T const &e)
{
    _size++;
    return p->insertPrev(e); //e作为p的前驱插入
}

template <typename T>
void List<T>::copyNodes(Position(T) p, int n)
{           //O(n)
    init(); //初始化,创建头尾哨兵
    while (n--)
    {
        append(p->data); // 作为末结点插入
        p = p->next;
    }
}

template <typename T>
Position(T) List<T>::insertAfter(Position(T) p, T const &e)
{
    _size++;
    return p->insertNext(e); //e作为p的后继插入
}

template <typename T>
T List<T>::remove(Position(T) p)
{                  //O(1)
    T e = p->data; //备份删除结点的数据
    p->prev->next = p->next;
    p->next->prev = p->prev;
    delete p; // 释放空间
    _size--;  // 规模减少
    return e;
}

template <typename T>
int List<T>::clear() //清空列表,O(n)
{
    int oldSize = _size;
    while (0 < _size)
        remove(header->next); //反复删除首结点
    return oldSize;
}
template <typename T>
int List<T>::deduplicate()
{
    if (_size < 2) //一个结点自然不重复
        return 0;
    int oldSize = _size; //记录原规模
    Rank r = 1;
    for (Position(T) p = (first()->next); p != trailer; p = p->next)
    {
        Position(T) q = find(p->data, r, p); //在p的r个真前驱寻找相同者
        q ? remove(q) : r++;
    } //循环过程中,p的所有前驱互不相同
    return oldSize - _size;
}
// template <typename T>
// T *List<T>::toArray() const
// {
//     T *arr = new T[_size];
//     for (Rank i = 0, Position(T) p = first(); i < _size; i++, p = p->next)
//         arr[i] = p->data;
//     return arr;
// }

template <typename T>
void List<T>::show() const
{
    if (empty())
    {
        cout << "[]" << endl;
        return;
    }

    cout << "[";
    for (Position(T) p = first();; p = p->next)
    {
        if (p->next == trailer)
        {
            cout << p->data << "]" << endl;
            return;
        }
        cout << p->data << ", ";
    }
}

template <typename T>
int List<T>::uniquify()
{                  //有序列表删除重复元素,只需遍历列表一次,O(n)
    if (_size < 2) //一个结点自然不重复
        return 0;
    int oldSize = _size;
    Position(T) p = first();
    // Position(T) q = p->next;
    for (Position(T) q = p->next; q != trailer; q = p->next)
    { // p为各区段起点,q为p的后继
        if (p->data != q->data)
            p = q; //若不等,转向下一个区段
        else
            remove(q); //若相同,删除后者
    }
    return oldSize - _size;
}

template <typename T> // 在有序列表结点p的n个真前驱中找到不大于e的最后者
Position(T) List<T>::search(T const &e, int n, Position(T) p) const
{ //对于p的最近n个前驱,从右向左逐个比较
    while (0 <= n--)
    {
        if (((p = p->prev)->data) <= e)
            break;
    }
    return p; //直至命中,数值越界或范围越界,返回查找终止的位置
}

template <typename T> //起始于p的连续n个结点做选择排序
void List<T>::selectionSort(Position(T) p, int n)
{
    Position(T) head = p->prev; // 待排序区间(head,tail)
    Position(T) tail = p;
    for (int i = 0; i < n; i++) // 寻找到正确tail位置,可能是尾哨兵
        tail = tail->next;
    while (1 < n)
    {
        Position(T) pmax = selectMax(head->next, n); // 找到最大者
        insertBefore(tail, remove(pmax));            //将其删除并移至有序区间最前
        tail = tail->prev;                           // 有序区间范围扩大
        n--;                                         // 待排区间减小
    }
}
template <typename T> // 从起始于p的n个结点查找最大者
Position(T) List<T>::selectMax(Position(T) p, int n)
{
    Position(T) pmax = p;
    for (Position(T) cur = p->next; 1 < n; n--, cur = cur->next)
    {
        if (!lt(cur->data, pmax->data)) //当前元素>=pmax则更新位置
                                        // if (cur->data>= pmax->data)
            pmax = cur;                 //多个相同元素选取靠后的移动,为了稳定性
    }
    return pmax;
}

template <typename T> //起始于p的连续n个结点做插入排序
void List<T>::insertionSort(Position(T) p, int n)
{ // valid(p) && rank(p) + n <= size
    for (int r = 0; r < n; r++)
    {
        // 从p的r个前驱寻找合适位置,插入,r即有序前缀长度
        insertAfter(search(p->data, r, p), p->data);
        p = p->next;     //转向下一个结点,无序的首结点
        remove(p->prev); // 插入是复制元素再插入,故前一个结点已无用
    }                    // n次迭代,每次O(r+1)
} // O(1)辅助空间,属于就地算法

int main(int argc, char const *argv[])
{
    // List<int> ll;
    // int arr[] = {3, 4, 5, 1, 2, 4, 5, 6, 1};
    int arr[] = {6, 1, 2, 4, 2, 1, 3, 2, 4, 5, 1};
    int length = sizeof(arr) / sizeof(int);
    // for (int i = 0; i < length; i++)
    // {
    //     if (i % 3 == 1)
    //         ll.append(arr[i]);
    //     else
    //         ll.prepend(arr[i]);
    // }
    List<int> ll(arr, length);
    ll.show();                             // [1, 5, 4, 1, 5, 3, 4, 2, 6]
    cout << "size: " << ll.size() << endl; // size: 9
    ll.sort();
    ll.show();
    ll.uniquify();
    ll.show();                             // [1, 5, 3, 4, 2, 6]
    cout << "size: " << ll.size() << endl; // size: 6
    ll.insertAfter(ll.search(3), 23);
    ll.show();                            // [1, 5, 3, 23, 4, 2, 6]
    cout << "fisrt:" << ll.pop() << endl; // fisrt:1
    ll.show();                            // [5, 3, 23, 4, 2, 6]
    ll.clear();
    ll.show();                             // []
    cout << "size: " << ll.size() << endl; // size: 0

    return 0;
}
