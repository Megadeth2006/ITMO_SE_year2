using System.Runtime.InteropServices;

[DllImport("filter.dll", CallingConvention = CallingConvention.Cdecl)]
static extern int filter([In] Point[] points, int count, [Out] Point[] result, FilterFunc filter_func);



var points = ReadPointsFromFile("points.txt");
Console.WriteLine($"прочитано точек: {points.Length}\n");

Console.WriteLine("фильтрация точек по координатным четвертям:\n");

// 1 четверть x > 0, y > 0
var quadrant1 = new Point[points.Length];
int count1 = filter(points, points.Length, quadrant1, p => (p.x > 0 && p.y > 0) ? 1 : 0);
Console.WriteLine($"1 четверть (x > 0, y > 0): {count1} точек");
PrintSamplePoints(quadrant1, count1, 5);

// 2 четверть x < 0, y > 0
var quadrant2 = new Point[points.Length];
int count2 = filter(points, points.Length, quadrant2, p => (p.x < 0 && p.y > 0) ? 1 : 0);
Console.WriteLine($"\n2 четверть (x < 0, y > 0): {count2} точек");
PrintSamplePoints(quadrant2, count2, 5);

// 3 четверть: x < 0, y < 0
var quadrant3 = new Point[points.Length];
int count3 = filter(points, points.Length, quadrant3, p => (p.x < 0 && p.y < 0) ? 1 : 0);
Console.WriteLine($"\n3 четверть (x < 0, y < 0): {count3} точек");
PrintSamplePoints(quadrant3, count3, 5);

// 4 четверть: x > 0, y < 0
var quadrant4 = new Point[points.Length];
int count4 = filter(points, points.Length, quadrant4, p => (p.x > 0 && p.y < 0) ? 1 : 0);
Console.WriteLine($"\n4 четверть (x > 0, y < 0): {count4} точек");
PrintSamplePoints(quadrant4, count4, 5);


static Point[] ReadPointsFromFile(string filename)
{
    var lines = File.ReadAllLines(filename);
    var pointsList = new List<Point>();
    
    foreach (var line in lines)
    {
        if (string.IsNullOrWhiteSpace(line))
            continue;
            
        var parts = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
        
        foreach (var part in parts)
        {
            var coords = part.Split(',');
            if (coords.Length == 2)
            {
                if (int.TryParse(coords[0], out int x) && int.TryParse(coords[1], out int y))
                {
                    pointsList.Add(new Point { x = x, y = y });
                }
            }
        }
    }
    
    return pointsList.ToArray();
}


static void PrintSamplePoints(Point[] points, int count, int maxSamples)
{
    int samples = Math.Min(count, maxSamples);
    Console.Write("  Примеры: ");
    for (int i = 0; i < samples; i++)
    {
        Console.Write($"({points[i].x}, {points[i].y})");
        if (i < samples - 1)
            Console.Write(", ");
    }
    if (count > maxSamples)
        Console.Write($" ... и еще {count - maxSamples}");
    Console.WriteLine();
}

[StructLayout(LayoutKind.Sequential)]
public struct Point
{
    public int x;
    public int y;
}

// Делегат для функции фильтрации точек
public delegate int FilterFunc(Point p);

