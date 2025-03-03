using Kawazu;
using WanaKanaShaapu;

namespace matsugane.Translation;

public static class Japanese
{
    public static async Task<string> ConvertJapaneseToRomaji(string name)
    {
        if (!WanaKana.IsJapanese(name)) return name;

        if (WanaKana.IsKanji(name))
        {
            var converter = new KawazuConverter();
            name = await converter.Convert(name, To.Romaji);
        }

        name = WanaKana.ToRomaji(name);

        return name;
    }
}