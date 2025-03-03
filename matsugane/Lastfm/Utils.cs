using Kawazu;
using matsugane.Translation;
using WanaKanaShaapu;

namespace matsugane.Lastfm;

public static class Utils
{
    public static async Task<string> BuildSortNameAsync(string name)
    {
        var sortName = await Japanese.ConvertJapaneseToRomaji(name);
        sortName = RemoveArticles(sortName);
        return sortName.ToLowerInvariant();
    }

    private static string RemoveArticles(string name)
    {
        if (string.IsNullOrWhiteSpace(name))
        {
            return name;
        }

        var split = name.Split(' ');

        if (split.Length == 1)
        {
            return name;
        }

        var articles = new List<string> { "the", "a", "an" };
        var first = split[0];
        if (articles.Contains(first.ToLowerInvariant()))
        {
            name = name.Replace(first, "").Trim();
        }

        return name;
    }
}