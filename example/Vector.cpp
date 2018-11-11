#include <iostream>
using namespace std;

typedef int Rank;          // 秩
#define DEFAULT_CAPACITY 3 // 默认初始容量(实际应用可设更大)
template <typename T>
class Vector
{ // 向量模板类
  private:
    Rank _size;    // 元素个数
    int _capacity; // 容量
    T *_elem;      // 数据区
  protected:
    // 内部函数
    void expand();
    void copyFrom(T const *A, Rank low, Rank high);
    void shrink();

  public:
    // 构造函数
    Vector(int c = DEFAULT_CAPACITY)
    {
        _elem = new T[_capacity = c]; // 申请长度为c类型为T的一段连续空间
        _size = 0;                    // 元素个数为0
    }
    Vector(T const *A, Rank low, Rank high)
    {                           // 数组区间复制
        copyFrom(A, low, high); // 需要实现
    }
    Vector(Vector<T> const &V, Rank low, Rank high)
    { // 向量区间复制
        copyFrom(V._elem, low, high);
    }
    Vector(Vector<T> const &V)
    { // 向量整体复制
        copyFrom(V._elem, 0, V._size);
    }
    // 析构函数
    ~Vector()
    { // 释放内部空间
        delete[] _elem;
    }

    // 函数声明
    T &operator[](Rank r) const;
    Rank insert(Rank r, T const &e);
    int remove(Rank low, Rank high);
    T remove(Rank r);
    Rank find(T const &e, Rank low, Rank high) const;
    int deduplicate();
    template <typename VST>
    void traverse(VST &visit);
    int disordered() const;
    int uniquify();
    Rank search(T const &e, Rank low, Rank high) const;
    //-------------------------------------------

    bool empty() const //  判空
    {
        return _size <= 0;
    }
    Rank size() const // 获取元素个数
    {
        return _size;
    }

    void show() const // 自己写的遍历
    {
        cout << "[";
        if (empty())
        {
            cout << "]" << endl;
            return;
        }
        for (int i = 0;; i++)
        {
            if (i == _size - 1)
            {
                cout << _elem[i] << "]" << endl;
                return;
            }
            cout << _elem[i] << ", ";
        }
    }
};

template <typename T> // 元素类型((T为基本类型或已重载赋值操作符=)
void Vector<T>::copyFrom(T const *A, Rank low, Rank high)
{
    _elem = new T[_capacity = 2 * (high - low)]; // 分配2倍空间
    _size = 0;
    while (low < high)
    { // 将A[low, high)元素逐一复制到_elem[0, high-low)
        _elem[_size++] = A[low++];
    }
}

template <typename T>
void Vector<T>::expand()
{ // 向量空间不足时扩容
    if (_size < _capacity)
        return;                                   // 未满不必扩容
    _capacity = max(_capacity, DEFAULT_CAPACITY); // 不低于最小容量
    T *oldElem = _elem;                           // 备份
    _elem = new T[_capacity <<= 1];               // 容量加倍
    for (int i = 0; i < _size; i++)
    { // 复制原来内容
        _elem[i] = oldElem[i];
    }
    delete[] oldElem; // 释放原来空间
}

template <typename T>
T &Vector<T>::operator[](Rank r) const
{ //重载下标操作符,返回引用:T&
    // assert 0 <= r < _size;
    return _elem[r];
}

template <typename T>
Rank Vector<T>::insert(Rank r, T const &e) // r处插入元素e, 0<=r<=_size
{
    expand();                       // 如果满了就扩容
    for (int i = _size; i > r; i--) // 自后向前,r后的元素后移一个单元
        _elem[i] = _elem[i - 1];
    _elem[r] = e; // r处插入e
    _size++;      // 更新元素个数
    return r;     // 返回秩
}

template <typename T>
void Vector<T>::shrink()
{ //装填因子过小时压缩向量所占空间
    if (_capacity < DEFAULT_CAPACITY << 1)
        return; //不会收缩到DEFAULT_CAPACITY以下
    if (_size << 2 > _capacity)
        return;                     //以25%为界,装填因子>25%不缩容
    T *oldElem = _elem;             //备份
    _elem = new T[_capacity >>= 1]; //容量减半
    for (int i = 0; i < _size; i++)
        _elem[i] = oldElem[i]; //复制原来内容
    delete[] oldElem;          //释放原空间
}

template <typename T> //删除区间[low, high)
int Vector<T>::remove(Rank low, Rank high)
{
    if (low == high)
        return 0;
    while (high < _size) // [high,_size)元素向前向后,往前移动high-low位
        _elem[low++] = _elem[high++];
    _size = low;       // 循环结束时low就是新的元素个数
    shrink();          // 如有必要则缩容
    return high - low; // 返回删除元素个数
}

template <typename T> //删除秩为r的元素
T Vector<T>::remove(Rank r)
{
    T e = _elem[r];   // 记录删除元素
    remove(r, r + 1); // 调用区间删除
    return e;         // 返回被删除元素
}

template <typename T> // 无序向量的逆序查找:返回元素e的最后位置,不存在返回low-1
Rank Vector<T>::find(T const &e, Rank low, Rank high) const
{
    while ((--high >= low) && (e != _elem[high])) // 从后向前
        ;
    return high; // 返回high是元素的秩(索引),如果元素不存在则high=low-1
}

template <typename T> // 删除无序向量中重复元素
int Vector<T>::deduplicate()
{
    int oldSize = _size; // 记录原来元素个数
    Rank i = 1;          // 从_elem[1]开始查重
    while (i < _size)    // 从前向后考察每个元素
    {
        if (find(_elem[i], 0, i) < 0) // 该元素在前面有没有出现(至多一个)
            i++;                      // 没有重复,指针向后移
        else
            remove(i); // 有重复,删除该位置元素
    }
    return oldSize - _size; // 返回被删除元素个数
}

// template <typename T>
// void Vector<T>::traverse(void (*visit)(T &)) //函数指针
// {
//     for (int i = 0; i < _size; i++)
//         visit(_elem[i]);
// }

template <typename T>
template <typename VST>
void Vector<T>::traverse(VST &visit) //函数对象
{
    for (int i = 0; i < _size; i++)
        visit(_elem[i]);
}
template <typename T>
int Vector<T>::disordered() const
{
    int cnt = 0; //计数器
    for (int i = 1; i < _size; i++)
    {
        if (_elem[i - 1] > _elem[i]) // 逆序计数器+1
            cnt++;
    }
    // 返回相邻逆序对总数,如果只是判断是否有序,首次遇到逆序对即可结束
    return cnt;
}

// template <typename T>
// int Vector<T>::uniquify()
// {
//     int oldSize = _size; // 记录原来元素个数
//     for (int i = 0; i < _size - 1;)
//     { // 从前往后逐一比对相邻元素
//         if (_elem[i] == _elem[i + 1])
//             remove(i + 1); // 若相等,删除后者
//         else
//             i++;
//     }
//     // 返回删除元素个数;_size的变化由remove()完成
//     return oldSize - _size;
// }

template <typename T>
int Vector<T>::uniquify()
{
    Rank i = 0, j = 0;
    while (++j < _size)
    { // 逐一扫描直至末尾
        if (_elem[i] != _elem[j])
            _elem[++i] = _elem[j]; // 与i位第一个不同元素,移到i+1处
    }
    _size = ++i; // 直接截断尾部多余元素
    shrink();
    return j - i; // 删除元素个数
}

template <typename T> //  查找算法统一接口, 0<=low<high<=_size
Rank Vector<T>::search(T const &e, Rank low, Rank high) const
{ // 50%概率随机选取: 二分查找 or 斐波那契查找
    return (rand() % 2) ? binSearch(_elem, e, low, high)
                        : fibSearch(_elem, e, low, high);
}

template <typename T> // 有序向量区间[low, high)二分查找
static Rank binSearch(T *A, T const &e, Rank low, Rank high)
{
    cout << "binary search..."<<endl;
    while (low < high)
    {
        Rank mid = (low + high) >> 1; // 轴点为中点
        if (e < A[mid])
            high = mid;      // 前半段[low, mid)查找
        else if (e > A[mid]) // 建议写成:A[mid] < e
            low = mid + 1;   // 后半段(mid, high)查找
        else
            return mid;
    }
    return -1; // 查找失败, 返回-1是不够的
}

class Fib
{ //Fibonacci数列类
  private:
    int f, g; //f = fib(k - 1), g = fib(k)。均为int型，很快就会数值溢出
  public:
    Fib(int n)
    { //初始化为不小于n的最小Fibonacci项
        f = 1;
        g = 0;
        while (g < n)
            next();
    } //fib(-1), fib(0)，O(logn)时间
    int get()
    { //获取当前Fibonacci项，O(1)时间
        return g;
    }
    int next()
    { //转至下一Fibonacci项，O(1)时间
        g += f; // 下一个fib
        f = g - f; // 原来的g
        return g;
    }
    int prev()
    { //转至上一Fibonacci项，O(1)时间
        f = g - f; // 前两个fib
        g -= f; // 原来的f, 前一个fib
        return g;
    }
};

template <typename T> // 有序向量区间[low, high)fibonacci查找
static Rank fibSearch(T *A, T const &e, Rank low, Rank high)
{
    cout << "fibonacci search..."<<endl;
    Fib fib(high - low); // 用O(logn)时间创建Fib数列
    while (low < high)
    {
        while (high - low < fib.get())
            fib.prev();
        Rank mid = low + fib.get() - 1; // 按黄金比例切分
        if (e < A[mid])
            high = mid; // 深入前半段[low, mid)
        else if (A[mid] < e)
            low = mid + 1; // 深入后半段(mid, high)
        else
            return mid;
    }
    return -1;
}

// -----------------------------------

template <typename T> // 假设T可直接递增或已重载操作符++
struct Increase       // 简化起见使用struct
{                     // 函数对象,通过重载操作符"()"实现,行为上类似于函数
    virtual void operator()(T &e) { e++; }
};

template <typename T>
void increase(Vector<T> &v)
{
    v.traverse(Increase<T>());
}

int main(int argc, char const *argv[])
{

    // int arr[] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    // Vector<int> myvector(arr, 0, 5); // 选取前5个
    // myvector.show();                 // [1, 2, 3, 4, 5]
    // int a = myvector[1];             // 右值
    // cout << "a = " << a << endl;     //a = 2
    // myvector[2] = 33;                // 左值,因为返回引用,可以修改元素的值
    // myvector.show();                 //[1, 2, 33, 4, 5]
    // // 接着上面继续测试
    // myvector.insert(2, 99);                                               // 2号位插入99
    // myvector.show();                                                      // [1, 2, 99, 33, 4, 5]
    // cout << "size = " << myvector.size() << endl;                         // 打印元素个数
    // myvector.remove(2, 4);                                                // 删除[2, 4)元素
    // myvector.show();                                                      // [1, 2, 4, 5]
    // cout << "size = " << myvector.size() << endl;                         // size = 4
    // cout << "rank(2) = " << myvector.find(2, 0, myvector.size()) << endl; // rank(2) = 1
    // // ...
    // myvector.show();                                      // [1, 2, 4, 5]
    // cout << "逆序对 = " << myvector.disordered() << endl; // 逆序对 = 0
    // myvector.insert(0, 99);
    // myvector.show();                                      // [99, 1, 2, 4, 5]
    // cout << "逆序对 = " << myvector.disordered() << endl; // 逆序对 = 1

    // int arr[] = {3, 3, 3, 3, 5, 5, 5, 5, 5, 8, 8, 8, 13, 13, 13, 13};
    // Vector<int> myvector(arr, 0, (sizeof arr) / (sizeof(int)) - 1); 
    // myvector.show();                                                // [3, 3, 3, 3, 5, 5, 5, 5, 5, 8, 8, 8, 13, 13, 13]
    // cout << (myvector.disordered() ? "无序" : "有序") << endl;      // 逆序对 = 0
    // myvector.uniquify();
    // myvector.show(); // [3, 5, 8, 13]

    return 0;
}
