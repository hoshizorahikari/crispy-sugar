#include <iostream>
#include <cmath>
#include <ctime>
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

// template <typename T> // 有序向量区间[low, high)二分查找
// static Rank binSearch(T *A, T const &e, Rank low, Rank high)
// {
//     cout << "binary search..." << endl;
//     while (low < high)
//     {
//         Rank mid = (low + high) >> 1; // 轴点为中点
//         if (e < A[mid])
//             high = mid;      // 前半段[low, mid)查找
//         else if (e > A[mid]) // 建议写成:A[mid] < e
//             low = mid + 1;   // 后半段(mid, high)查找
//         else
//             return mid;
//     }
//     return -1; // 查找失败, 返回-1是不够的
// }

// template <typename T> // 有序向量区间[low, high)二分查找改进版
// static Rank binSearch(T *A, T const &e, Rank low, Rank high)
// {
//     cout << "binary search..." << endl;
//     while (1 < high - low)
//     {                                 // 有效查找区间宽度缩减到1时,退出循环
//         Rank mid = (low + high) >> 1; // 轴点为中点
//         if (e < A[mid])
//             high = mid; // 前半段[low, mid)查找
//         else
//             low = mid; // 后半段[mid, high)查找
//     }
//     // 循环结束,high=low+1,查找区间只有一个元素A[low]
//     return (e == A[low]) ? low : -1;
// }

template <typename T> // 有序向量区间[low, high)二分查找终极版
static Rank binSearch(T *A, T const &e, Rank low, Rank high)
{
    cout << "binary search..." << endl;
    while (low < high)
    {
        Rank mid = (low + high) >> 1; // 轴点为中点
        if (e < A[mid])
            high = mid; // 前半段[low, mid)查找
        else
            low = mid + 1; // 后半段(mid, high)查找
    }
    // 循环结束,low=high,A[low]为大于e的最小元素
    return low - 1; //low-1是不大于e的元素最大秩
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
    {              //转至下一Fibonacci项，O(1)时间
        g += f;    // 下一个fib
        f = g - f; // 原来的g
        return g;
    }
    int prev()
    {              //转至上一Fibonacci项，O(1)时间
        f = g - f; // 前两个fib
        g -= f;    // 原来的f, 前一个fib
        return g;
    }
};

template <typename T> // 有序向量区间[low, high)fibonacci查找
static Rank fibSearch(T *A, T const &e, Rank low, Rank high)
{
    cout << "fibonacci search..." << endl;
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





template <typename T> //  查找算法统一接口, 0<=low<high<=_size
Rank Vector<T>::search(T const &e, Rank low, Rank high) const
{ // 50%概率随机选取: 二分查找 or 斐波那契查找
    return (rand() % 2) ? binSearch(_elem, e, low, high)
                        : fibSearch(_elem, e, low, high);
}

// -----------------------------------

int main(int argc, char const *argv[])
{
    time_t t = time(0);
    srand((unsigned)t);
    int arr[] = {2, 5, 6, 8, 11, 14, 23, 34, 56, 67, 85};
    int length = sizeof(arr) / sizeof(int);
    Vector<int> myvector(arr, 0, length);
    myvector.show();
    int e = 11;
    int index = myvector.search(e, 0, length);
    if (myvector[index] == e)
        cout << e << "存在,index=" << index << endl;
    else
        cout << e << "不存在";

    return 0;
}
