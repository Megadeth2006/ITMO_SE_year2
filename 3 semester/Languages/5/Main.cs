// Пул потоков
// Заранее выделенные потоки dotnet

using System.Diagnostics;

var st = Stopwatch.StartNew();

// async await

Console.WriteLine(Environment.CurrentManagedThreadId);

// Task.Run(() =>
// {
//     var lines = File.ReadAllText("C:\\Users\\professor\\Documents\\task4\\movies.csv");
//     Console.WriteLine(lines.Length);
//     Console.WriteLine(Environment.CurrentManagedThreadId);
// });

// Task.Run(() =>
// {
//     var lines2 = File.ReadAllText("C:\\Users\\professor\\Documents\\task4\\movies.csv");
//     Console.WriteLine(lines2.Length);
//     Console.WriteLine(Environment.CurrentManagedThreadId);
// });

// var task3 = Task.Run(() =>
// {
//     var lines3 = File.ReadAllText("C:\\Users\\professor\\Documents\\task4\\movies.csv").Order().ToList();
//     Console.WriteLine(lines3.Count);
//     Console.WriteLine(Environment.CurrentManagedThreadId);
// });

// TODO
// Написать программу которая берёт три имени файла
// Считает количество слов в каждом файле
// Подсчёт должен происходить в отдельной таске
// Все таски должны работать паралельно.
// Как только расчёт в таске закончен выводит в консоль.

string file1 = "1.txt";
string file2 = "2.txt";
string file3 = "3.txt";

var task1 = CountWordsInFileAsync(file1);
var task2 = CountWordsInFileAsync(file2);
var task3 = CountWordsInFileAsync(file3);

await Task.WhenAll(task1, task2, task3);

Console.WriteLine(st.Elapsed);

static async Task CountWordsInFileAsync(string fileName)
{
    try
    {
        await Task.Delay(5000);
        var content = await File.ReadAllTextAsync(fileName);
        var words = content.Split(new[] { ' ', '\t', '\n', '\r' }, 
            StringSplitOptions.RemoveEmptyEntries);
        int wordCount = words.Length;
        
        Console.WriteLine($"файл: {fileName}, количество слов: {wordCount}");
    }
    catch (Exception ex)
    {
        Console.WriteLine($"ошибка при чтении файла '{fileName}': {ex.Message}");
    }
}