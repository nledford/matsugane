namespace matsugane.Lastfm;

public class Item
{
    public string Name { get; set; }
    public int TotalTracks { get; set; }
    public int TotalPlays { get; set; }
    public int TotalAlbums { get; set; }
    public double PlaysPercent { get; set; }

    public Item(string name, int totalTracks, int totalPlays, int totalAlbums, int globalPlays)
    {
        Name = name;
        TotalTracks = totalTracks;
        TotalPlays = totalPlays;
        TotalAlbums = totalAlbums;
        PlaysPercent = (double)totalPlays / globalPlays;
    }
}