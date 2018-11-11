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

// -----------------------------------
// 以向量为基类,派生出栈模板类
template <typename T>
class Stack : public Vector<T>
{ // 向量末尾作为栈顶
  public:
    void push(T const &e)
    { // 入栈, 末尾添加元素
        insert(size(), e);
    }
    T pop()
    { //出栈,删除末尾元素
        return remove(size() - 1);
    }
    T &top()
    { //取顶,返末尾元素回
        return (*this)[size() - 1];
    }
};

// -----------------------------------

int main(int argc, char const *argv[])
{

    int arr[] = {23, 12, 43, 32, 78, 98, 75, 57};
    int length = sizeof(arr) / sizeof(int);
    return 0;
}
