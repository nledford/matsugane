namespace matsugane.Lastfm;

public class Tracks
{
    private readonly LastfmClient _client = new();

    public static async Task<Tracks> Build(bool fetchTracks = false)
    {
        var tracks = new Tracks();

        if (fetchTracks)
        {
            await tracks.RefreshTracks();
        }

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

    public IEnumerable<Item> Artists
    {
        get
        {
            var artists = RecentlyPlayedTracks
                .Select(t => new { id = t.SortArtist, artist = t.Artist })
                .DistinctBy(a => a.id);

            return from artist in artists
                let allTracks = RecentlyPlayedTracks.Where(t => t.SortArtist == artist.id).ToList()
                let totalTracks = allTracks.DistinctBy(t => t.TrackId).Count()
                let totalPlays = allTracks.DistinctBy(t => t.PlayId).Count()
                let totalAlbums = allTracks.DistinctBy(t => t.AlbumId).Count()
                select new Item(artist.artist, totalTracks, totalPlays, totalAlbums, TotalPlays);
        }
    }

    public IEnumerable<Item> Albums
    {
        get
        {
            var albums = RecentlyPlayedTracks
                .Select(t => new { id = t.SortAlbum, album = t.Album })
                .DistinctBy(a => a.id);

            return from album in albums
                let allTracks = RecentlyPlayedTracks.Where(t => t.SortAlbum == album.id).ToList()
                let totalTracks = allTracks.DistinctBy(t => t.TrackId).Count()
                let totalPlays = allTracks.DistinctBy(t => t.PlayId).Count()
                let totalAlbums = 0
                select new Item(album.album, totalTracks, totalPlays, totalAlbums, TotalPlays);
        }
    }

    public Stats PlaysPerArtistStats => new(Artists.Select(a => a.TotalPlays).ToList());
    public Stats AlbumsPerArtistStats => new(Artists.Select(a => a.TotalAlbums).ToList());
}