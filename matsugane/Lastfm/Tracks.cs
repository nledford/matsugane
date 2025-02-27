namespace matsugane.Lastfm;

public class Tracks
{
    private readonly LastfmClient _client = new();

    public IEnumerable<Item> Artists { get; private set; } = new List<Item>();
    public IEnumerable<Item> Albums { get; private set; } = new List<Item>();

    public static async Task<Tracks> Build(bool fetchTracks = false)
    {
        var tracks = new Tracks();

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
            result.Add(await Item.Build(artist.artist, totalTracks, totalPlays, totalAlbums, TotalPlays));
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
        get
        {
            return Artists
                .OrderByDescending(t => t.TotalPlays)
                .ThenByDescending(t => t.TotalTracks)
                .ThenByDescending(t => t.TotalAlbums)
                .ThenByDescending(t => t.SortName);
        }
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
                .Select(hour => new PlaysByHour(hour.hour, hour.plays, TotalPlays));
        }
    }
}