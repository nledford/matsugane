using Kawazu;
using WanaKanaShaapu;

namespace matsugane.Lastfm;

public static class Utils
{
    public static string BuildSortName(string name)
    {
        // name = await ConvertJapaneseToRomaji(name);
        name = Task.Run(async () => await ConvertJapaneseToRomaji(name)).Result;
        name = RemoveArticles(name);
        return name.ToLowerInvariant();
    }

    public static async Task<string> BuildSortNameAsync(string name)
    {
        name = await ConvertJapaneseToRomaji(name);
        name = RemoveArticles(name);
        return name.ToLowerInvariant();
    }

    private static async Task<string> ConvertJapaneseToRomaji(string name)
    {
        var converter = new KawazuConverter();

        if (!WanaKana.IsJapanese(name)) return name;

        if (WanaKana.IsKanji(name))
        {
            name = await converter.Convert(name, To.Romaji);
        }
        else
        {
            name = WanaKana.ToRomaji(name);
        }

        return name;
    }

    private static string RemoveArticles(string name)
    {
        var split = name.Split(' ');

        if (split.Length == 1)
        {
            return name;
        }

        var articles = new List<string> { "the", "a", "an" };
        var first = split[0];
        if (articles.Contains(first.ToLowerInvariant()))
        {
            name = name.Replace(first, "");
        }

        return name;
    }
}