using Microsoft.VisualBasic.FileIO;

List<string[]> ReadAllCsvLines(string filePath)
{
    var result = new List<string[]>();

    using (var parser = new TextFieldParser(filePath))
    {
        parser.TextFieldType = FieldType.Delimited;
        parser.SetDelimiters(",");
        parser.HasFieldsEnclosedInQuotes = true;

        while (!parser.EndOfData)
        {
            string[] fields = parser.ReadFields();
            result.Add(fields);
        }
    }

    return result;
}



// 1. Преобразовать в класс Movie (нужно создать класс) - Select
// Над списком из Movie 
// 2. Найти все фильмы режисёра (на выбор, например Nolan) - Where
// 3. 5 самый высокооценённых фильма выпущенных после 2010 
// 4. Получить список фильмов (их количество и средний рейтинг) жанра (на выбор, например Drama) 
// 5. Режисёр у которого больше всего фильмов
// Не учитывать регистр