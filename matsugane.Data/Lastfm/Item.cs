namespace matsugane.Data.Lastfm;

public interface IItemBuilder
{
    public ItemBuilder Name(string name);
    public ItemBuilder TotalTracks(int totalTracks);
    public ItemBuilder TotalPlays(int totalPlays);
    public ItemBuilder TotalAlbums(int totalAlbums);
    public ItemBuilder PlaysPercent(double playsPercent);
    public ItemBuilder CumulativeTotal(int cumulativeTotal);
    public ItemBuilder CumulativePercent(double cumulativePercent);
    public Item Build();
    public Task<Item> BuildAsync();
}

public class ItemBuilder : IItemBuilder
{
    private readonly Item _item = new();

    public ItemBuilder Name(string name)
    {
        _item.Name = name;
        return this;
    }

    public ItemBuilder TotalTracks(int totalTracks)
    {
        _item.TotalTracks = totalTracks;
        return this;
    }

    public ItemBuilder TotalPlays(int totalPlays)
    {
        _item.TotalPlays = totalPlays;
        return this;
    }

    public ItemBuilder TotalAlbums(int totalAlbums)
    {
        _item.TotalAlbums = totalAlbums;
        return this;
    }

    public ItemBuilder PlaysPercent(double playsPercent)
    {
        _item.PlaysPercent = playsPercent;
        return this;
    }

    public ItemBuilder CumulativeTotal(int cumulativeTotal)
    {
        _item.CumulativeTotal = cumulativeTotal;
        return this;
    }

    public ItemBuilder CumulativePercent(double cumulativePercent)
    {
        _item.CumulativePercent = cumulativePercent;
        return this;
    }

    public Item Build()
    {
        return _item;
    }

    public async Task<Item> BuildAsync()
    {
        if (!string.IsNullOrWhiteSpace(_item.Name))
        {
            _item.SortName = await Utils.BuildSortNameAsync(_item.Name);
        }

        return _item;
    }
}

public class Item
{
    private const int FmtRound = 8;

    public string Name { get; set; } = string.Empty;
    public string SortName { get; set; } = string.Empty;
    public int TotalTracks { get; set; }
    public int TotalPlays { get; set; }
    public int TotalAlbums { get; set; }
    public double PlaysPercent { get; set; }
    public string PlaysPercentFmt => $"{Math.Round(PlaysPercent * 100.0, FmtRound)}%";
    public int CumulativeTotal { get; set; }
    public double CumulativePercent { get; set; }
    public string CumulativePercentFmt => $"{Math.Round(CumulativePercent * 100.0, FmtRound)}%";

    public static async Task<Item> Build(string name, int totalTracks, int totalPlays, int totalAlbums, int globalPlays)
    {
        return await new ItemBuilder()
            .Name(name)
            .TotalTracks(totalTracks)
            .TotalPlays(totalPlays)
            .TotalAlbums(totalAlbums)
            .PlaysPercent((double)totalPlays / globalPlays)
            .BuildAsync();
    }
}