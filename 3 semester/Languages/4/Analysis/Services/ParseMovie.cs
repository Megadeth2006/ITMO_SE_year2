using System.Globalization;
using Analysis.Model;

namespace Analysis.Services;

public static class ParseMovie
{
    public static Movie? FromCsvFields(string[] fields)
    {
        if (fields == null || fields.Length < 22)
            return null;

        static float ParseFloat(string s) =>
            float.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out var f) ? f : 0f;

        static int ParseInt(string s) =>
            int.TryParse(s, out var i) ? i : 0;

        DateOnly? datePublished = null;
        if (DateOnly.TryParse(fields[4], out var date))
            datePublished = date;

        var actorNames = new List<string>();
        if (!string.IsNullOrWhiteSpace(fields[12]))
        {
            var parts = fields[12].Split(',');
            foreach (var part in parts)
                actorNames.Add(part.Trim());
        }

        return new Movie
        {
            ImdbTitleId = fields[0],
            Title = fields[1],
            OriginalTitle = fields[2],
            Year = fields[3],
            DatePublished = datePublished,
            Genre = fields[5],
            Duration = ParseInt(fields[6]),
            Country = fields[7],
            Language = fields[8],
            Director = fields[9],
            Writer = fields[10],
            ProductionCompany = fields[11],
            Actors = new Actors(actorNames),
            Description = fields[13],
            AvgVote = ParseFloat(fields[14]),
            Votes = ParseInt(fields[15]),
            Budget = fields[16],
            UsaGrossIncome = fields[17],
            WorldwideGrossIncome = fields[18],
            Metascore = ParseFloat(fields[19]),
            ReviewsFromUsers = ParseFloat(fields[20]),
            ReviewsFromCritics = ParseFloat(fields[21])
        };
    }
}