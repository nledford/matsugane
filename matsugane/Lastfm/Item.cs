namespace matsugane.Lastfm;

public class Item
{
    public string Name { get; private init; } = string.Empty;
    public string SortName { get; private init; } = string.Empty;
    public int TotalTracks { get; private init; }
    public int TotalPlays { get; private init; }
    public int TotalAlbums { get; private init; }
    public double PlaysPercent { get; private init; }
    public string PlaysPercentFmt => $"{PlaysPercent * 100.0}%";

    public static async Task<Item> Build(string name, int totalTracks, int totalPlays, int totalAlbums, int globalPlays)
    {
        return new Item
        {
            Name = name,
            SortName = await Utils.BuildSortNameAsync(name),
            TotalTracks = totalTracks,
            TotalPlays = totalPlays,
            TotalAlbums = totalAlbums,
            PlaysPercent = (double)totalPlays / globalPlays
        };
    }
}