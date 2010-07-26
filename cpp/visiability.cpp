/**
*
* 测试C++中同一个类的对象间可以相互访问对方的私有成员
*/
#include <iostream>

using namespace std;

class A
{
    public:
    void setX(int y)
    {
        x = y;
    }

    void func(A a)
    {
        cout << a.x << endl;
        a._setX(6);
        cout << a.x << endl;
    }

    private:
    int x;
    void _setX(int y)
    {
        x = y;
    }
};

int main()
{
    A a,b;
    a.setX(3);
    b.func(a);
}
