using System;

namespace Analysis.Model;

public class Movie
{
    public string ImdbTitleId { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
    public string OriginalTitle { get; set; } = string.Empty;
    public string Year { get; set; } = string.Empty;
    public DateOnly? DatePublished { get; set; }
    public string Genre { get; set; } = string.Empty;
    public int Duration { get; set; }
    public string Country { get; set; } = string.Empty;
    public string Language { get; set; } = string.Empty;
    public string Director { get; set; } = string.Empty;
    public string Writer { get; set; } = string.Empty;
    public string ProductionCompany { get; set; } = string.Empty;
    public Actors Actors { get; set; } = new();
    public string Description { get; set; } = string.Empty;
    public float AvgVote { get; set; }
    public int Votes { get; set; }
    public string Budget { get; set; } = string.Empty;
    public string UsaGrossIncome { get; set; } = string.Empty;
    public string WorldwideGrossIncome { get; set; } = string.Empty;
    public float Metascore { get; set; }
    public float ReviewsFromUsers { get; set; }
    public float ReviewsFromCritics { get; set; }
}