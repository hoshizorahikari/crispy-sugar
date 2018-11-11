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
    Rank bubble(Rank low, Rank high);
    void bubbleSort(Rank low, Rank high);
    void swap(T &a, T &b);
    void mergeSort(Rank low, Rank high);
    void merge(Rank low, Rank mid, Rank high);
    void selectionSort(Rank low, Rank high);

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
    // void sort(Rank low, Rank high);
    void sort();

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
// ----------------------------------
// template <typename T>
// void Vector<T>::sort(Rank low, Rank high)
// { // 区间[low, high)
//     switch (rand() % 5)
//     { // 视具体情况灵活选取或扩充
//     case 1:
//         bubbleSort(low, high);
//         break;
//     case 2:
//         selectionSort(low, high);
//         break;
//     case 3:
//         mergeSort(low, high);
//         break;
//     case 4:
//         heapSort(low, high);
//         break;
//     default:
//         quickSort(low, high);
//         break;
//     }
// } // 在此统一接口下,具体算法不同实现,见后续

template <typename T>
void Vector<T>::bubbleSort(Rank low, Rank high)
{
    // while (!bubloe(low, hi--))
    while (low < (high = bubble(low, high)))
        ; // 逐趟扫描交换,直至全部有序
}

template <typename T>
void Vector<T>::swap(T &a, T &b)
{
    T tmp = a;
    a = b;
    b = tmp;
}

template <typename T>
Rank Vector<T>::bubble(Rank low, Rank high)
{                    // 一趟扫描交换
    Rank last = low; //最右侧的逆序对初始化为[low-1, low]
    for (int i = low + 1; i < high; i++)
    {
        if (_elem[i - 1] > _elem[i])
        {             // 存在逆序
            last = i; //更新最右侧逆序对的位置
            swap(_elem[i - 1], _elem[i]);
        }
    }
    return last; // 逻辑标志sorted改为秩last
}

template <typename T>
void Vector<T>::sort()
{
    // mergeSort(0, _size);
    selectionSort(0, _size);
}

template <typename T>
void Vector<T>::mergeSort(Rank low, Rank high)
{ //[low, high)
    if (high - low < 2)
        return;                   //单个元素自然有序
    Rank mid = (low + high) >> 1; //一分为二
    mergeSort(low, mid);
    mergeSort(mid, high);  // 对两部分归并排序
    merge(low, mid, high); // 归并
}

template <typename T>
void Vector<T>::merge(Rank low, Rank mid, Rank high)
{
    T *A = _elem + low; //合并后的向量A[0, high-low)=_elem[low, high)
    int lsize = mid - low;
    T *B = new T[lsize]; //前子向量B[0, lsize)=_elem[low, mid)
    for (Rank i = 0; i < lsize; i++)
        B[i] = A[i]; //复制前子向量B
    int rsize = high - mid;
    T *C = _elem + mid; // 后子向量C[0, rsize)=_elem[mid, high)
    for (Rank i = 0, lp = 0, rp = 0; lp < lsize;)
    {
        // B已全部归并,或B大于C, C接至A末尾
        if ((rp < rsize) && (C[rp] < B[lp]))
            A[i++] = C[rp++];
        // C已全部归并,或C不小于B, B接至A末尾
        if (rsize <= rp || (B[lp] <= C[rp]))
            A[i++] = B[lp++];
    }           // 交换两句次序,删除冗余逻辑
    delete[] B; //释放临时空间B
}

template <typename T>
void Vector<T>::selectionSort(Rank low, Rank high)
{
    for (Rank i = low; i < high - 1; i++)
    {
        Rank min_index = i;
        for (Rank j = i + 1; j < high; j++)
        {
            if (_elem[j] < _elem[min_index])
                min_index = j;
        }
        swap(_elem[i], _elem[min_index]);
    }
}

// -----------------------------------

int main(int argc, char const *argv[])
{

    int arr[] = {23, 12, 43, 32, 78, 98, 75, 57};
    int length = sizeof(arr) / sizeof(int);
    Vector<int> myvector(arr, 0, length);
    myvector.show();
    myvector.sort();
    myvector.show();

    return 0;
}
