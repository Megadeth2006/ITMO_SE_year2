using System.Collections.Generic;

namespace Analysis.Model;

public class Actors
{
    public List<string> Names { get; set; } = new();

    public Actors() { }

    public Actors(List<string> names)
    {
        Names = names ?? new List<string>();
    }
}