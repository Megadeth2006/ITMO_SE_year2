using System.Runtime.InteropServices;
 
[DllImport("my_lib.dll", CallingConvention = CallingConvention.Cdecl)]
static extern long fib_rec(int n);
 
[DllImport("point_lib.dll", CallingConvention = CallingConvention.Cdecl)]
static extern void process_point(ref Point p);
 
[DllImport("point_lib.dll", CallingConvention = CallingConvention.Cdecl)]
static extern void process_points([In, Out] Point[] p, [In] int count);
 
[DllImport("point_lib.dll", CallingConvention = CallingConvention.Cdecl)]
static extern int func(int a, map f);
 
// TODO:
// 1. Взять файл с точками с прошлого занятия (либо заново сгенерировать)
// 2. Прочитать из C# этот файл в массив Point[]
// 3. На C написать функцию filter(), которая принимает
// 3.1 Массив точек
// 3.2 Их количество
// 3.3 Массив точек для хранения результата
// 3.4 Функцию фильтрации
// Функция записывает в результат(3.3) отфильтрованные точки 
// Функции задаются в C#
// 4. Применить функцию разложить точки на координатные четверти
 
 
static int MyFunc(int a)
{
    return a;
}
 
var res = fib_rec(35);
Console.WriteLine($"result = {res}");
 
var p = new Point
{
    x = 10,
    y = 10
};
process_point(ref p);
Console.WriteLine($"p.x = {p.x} p.y = {p.y}");
 
var array_points = new Point[]
{
    p,
    new Point
    {
        x = 1,
        y = 2
    }
};
process_points(array_points, array_points.Length);
for (int i = 0; i < array_points.Length; i++)
{
    Console.WriteLine($"array_points.x = {array_points[i].x} array_points.y = {array_points[i].y}");
}
 
map bar = x => x * 3;
bar = MyFunc;
bar(3);
 
res = func(10, x => x * 2);
Console.WriteLine($"result = {res}");
 
[StructLayout(LayoutKind.Sequential)]
struct Point
{
    public int x;
    public int y;
}
 
public delegate int map(int a);
 
 