namespace matsugane.Lastfm;

public class Item
{
    public string Name { get; set; }
    public string SortName { get; set; }
    public int TotalTracks { get; set; }
    public int TotalPlays { get; set; }
    public int TotalAlbums { get; set; }
    public double PlaysPercent { get; set; }
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