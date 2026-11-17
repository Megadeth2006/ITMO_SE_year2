using Microsoft.VisualBasic.FileIO;

namespace Analysis.Services;


public class CsvParser
{


    public List<string[]> ReadAllCsvLines(string filePath)
    {

        var result = new List<string[]>();
        using var parser = new TextFieldParser(filePath);
        parser.TextFieldType = FieldType.Delimited;
        parser.SetDelimiters(",");
        parser.HasFieldsEnclosedInQuotes = true;

        
        parser.ReadFields(); 

            while (!parser.EndOfData)
            {
                try
                {
                    string[]? fields = parser.ReadFields();
                    if (fields != null)
                    {
                        result.Add(fields);
                    }
                }
                catch (MalformedLineException)
                {
                    continue;
                }
            }
        return result;
    }


    
}