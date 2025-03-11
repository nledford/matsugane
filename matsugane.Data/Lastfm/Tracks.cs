namespace matsugane.Data.Lastfm;

public class Tracks
{
    private readonly LastfmClient _client;

    public Tracks(HttpClient client)
    {
        _client = new LastfmClient(client);
    }

    public IEnumerable<Item> Artists { get; private set; } = new List<Item>();
    public IEnumerable<Item> Albums { get; private set; } = new List<Item>();

    public static async Task<Tracks> Build(HttpClient client, bool fetchTracks = false)
    {
        var tracks = new Tracks(client);

        if (!fetchTracks) return tracks;

        await tracks.RefreshTracks();
        await tracks.BuildArtists();
        await tracks.BuildAlbums();

        return tracks;
    }

    private async Task RefreshTracks()
    {
        RecentlyPlayedTracks = (await _client.GetRecentTracks()).ToList();
    }

    public List<Track> RecentlyPlayedTracks { get; private set; } = [];

    public int TotalArtists
    {
        get { return RecentlyPlayedTracks.DistinctBy(t => t.ArtistId).Count(); }
    }

    public int TotalAlbums
    {
        get { return RecentlyPlayedTracks.DistinctBy(t => t.AlbumId).Count(); }
    }

    public int TotalTracks
    {
        get { return RecentlyPlayedTracks.DistinctBy(t => t.TrackId).Count(); }
    }

    public int TotalPlays
    {
        get { return RecentlyPlayedTracks.DistinctBy(t => t.PlayId).Count(); }
    }

    private async Task BuildArtists()
    {
        var artists = RecentlyPlayedTracks
            .Select(t => new { id = t.SortArtist, artist = t.Artist })
            .DistinctBy(a => a.id);

        var result = new List<Item>();
        foreach (var artist in artists)
        {
            var allTracks = RecentlyPlayedTracks.Where(t => t.SortArtist == artist.id).ToList();
            var totalTracks = allTracks.DistinctBy(t => t.TrackId).Count();
            var totalPlays = allTracks.DistinctBy(t => t.PlayId).Count();
            var totalAlbums = allTracks.DistinctBy(t => t.AlbumId).Count();

            var item = await new ItemBuilder()
                .Name(artist.artist)
                .TotalTracks(totalTracks)
                .TotalPlays(totalPlays)
                .TotalAlbums(totalAlbums)
                .PlaysPercent((double)totalPlays / TotalPlays)
                .BuildAsync();

            result.Add(item);
        }

        result = result.OrderByDescending(x => x.TotalPlays)
            .ThenByDescending(x => x.TotalTracks)
            .ThenByDescending(x => x.TotalAlbums)
            .ThenBy(x => x.SortName)
            .ToList();

        var cumulativePlays = 0;
        foreach (var item in result)
        {
            cumulativePlays += item.TotalPlays;

            item.CumulativeTotal = cumulativePlays;
            item.CumulativePercent = (double)cumulativePlays / TotalPlays;
        }

        Artists = result;
    }

    private async Task BuildAlbums()
    {
        var albums = RecentlyPlayedTracks
            .Select(t => new { id = t.SortAlbum, album = t.Album })
            .DistinctBy(a => a.id);


        var result = new List<Item>();
        foreach (var album in albums)
        {
            var allTracks = RecentlyPlayedTracks.Where(t => t.SortAlbum == album.id).ToList();
            var totalTracks = allTracks.DistinctBy(t => t.TrackId).Count();
            var totalPlays = allTracks.DistinctBy(t => t.PlayId).Count();
            result.Add(await Item.Build(album.album, totalTracks, totalPlays, 0, TotalPlays));
        }

        Albums = result;
    }

    public Stats PlaysPerArtistStats => new(Artists.Select(a => a.TotalPlays).ToList());
    public Stats AlbumsPerArtistStats => new(Artists.Select(a => a.TotalAlbums).ToList());

    public IEnumerable<Item> TopArtists
    {
        get { return Artists.OrderBy(i => i.CumulativePercent).ThenBy(i => i.SortName); }
    }

    public IEnumerable<PlaysByHour> PlaysByHours
    {
        get
        {
            return RecentlyPlayedTracks
                .GroupBy(t => t.PlayedAt.Hour)
                .Select(grp => new
                {
                    hour = grp.Key,
                    plays = grp.Count()
                })
                .Select(hour => new PlaysByHour(hour.hour, hour.plays, TotalPlays))
                .OrderByDescending(h => h.Plays)
                .ThenBy(h => h.Hour);
        }
    }

    public double AvgPlaysPerHour => PlaysByHours.Select(x => x.Plays).Average();
}