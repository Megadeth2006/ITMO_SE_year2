using Microsoft.VisualBasic.FileIO;
using Analysis.Services;


const string csvPath = "movies.csv";

if (!File.Exists(csvPath))
{
    Console.WriteLine("Файл не найден");
    return;
}

CsvParser csvParser = new CsvParser();



var rawLines = csvParser.ReadAllCsvLines(csvPath);


var movies = rawLines
    .Select(ParseMovie.FromCsvFields)
    .Where(m => m != null)
    .ToList();

Console.WriteLine($"Загружено фильмов: {movies.Count}\n");
// фильмы режиссёра
string directorName = "Robert";
string directorSurname = "Zemeckis";

var zemeckisMovies = movies
    .Where(m => m != null && !string.IsNullOrEmpty(m.Director) && m.Director.Contains(directorName, StringComparison.OrdinalIgnoreCase) && m.Director.Contains(directorSurname, StringComparison.OrdinalIgnoreCase))
    .ToList();
Console.WriteLine($"Фильмы {directorName + " " + directorSurname}: {zemeckisMovies.Count}");
if (zemeckisMovies.Any())
{

    zemeckisMovies.Take(zemeckisMovies.Count).ToList().ForEach(m => Console.WriteLine($"- {m?.OriginalTitle ?? "Unknown"} ({m?.Year ?? "Unknown"})"));
}
else {
    Console.WriteLine("Фильмы не найдены.");
}

// топ 5 фильмов после 2010 по рейтингу
var top5 = movies
    .Where(m => m != null && !string.IsNullOrEmpty(m.Year) && int.TryParse(m.Year, out var y) && y > 2010 && m.AvgVote > 0)
    .OrderByDescending(m => m?.AvgVote ?? 0)
    .ThenByDescending(m => m?.Votes ?? 0)
    .Take(5)
    .ToList();

Console.WriteLine("\nтоп 5 фильмов после 2010:");
if (top5.Any())
{
    top5.ForEach(m => Console.WriteLine($"- {m?.Title ?? "Unknown"} ({m?.Year ?? "Unknown"}) — {m?.AvgVote:F1}"));
}


// статистика по жанру
string genre = "western";
var sciFyMovies = movies
    .Where(m => m != null && !string.IsNullOrEmpty(m.Genre) && m.Genre.Split(',')
                       .Any(g => g.Trim().Equals(genre, StringComparison.OrdinalIgnoreCase)))
    .ToList();

Console.WriteLine($"\nЖанр '{genre}':");
Console.WriteLine($"Количество: {sciFyMovies.Count}");
if (sciFyMovies.Any())
{
    Console.WriteLine($"Средний рейтинг: {sciFyMovies.Average(m => m?.AvgVote ?? 0):F2}");
}
else
{
    Console.WriteLine("Средний рейтинг: 0.00");
}
Console.WriteLine();

var allDirectors = movies
    .Where(m => m != null && !string.IsNullOrWhiteSpace(m.Director))
    .SelectMany(m =>
        m.Director
            .Split(',', StringSplitOptions.RemoveEmptyEntries)
            .Select(name => name.Trim())
            .Where(name => !string.IsNullOrEmpty(name))
    );

var topDirectorGroup = allDirectors
    .GroupBy(name => name, StringComparer.OrdinalIgnoreCase)
    .OrderByDescending(g => g.Count())
    .FirstOrDefault();

if (topDirectorGroup != null)
{
    Console.WriteLine($"Режиссёр с наибольшим числом фильмов: {topDirectorGroup.Key} ({topDirectorGroup.Count()} фильмов)");
}