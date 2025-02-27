namespace matsugane.Lastfm;

public class Track
{
    private readonly string _playedAt;

    public Track(string title, string artist, string album, string playedAt)
    {
        Title = title;
        Artist = artist;
        Album = album;
        _playedAt = playedAt;
    }

    public string TrackId => $"track|{SortTitle}|{SortArtist}|{SortAlbum}";
    public string PlayId => $"play|{PlayedAt}";
    public string Title { get; set; }
    public string SortTitle => Utils.BuildSortName(Title);
    public string ArtistId => $"artist|{SortArtist}";
    public string Artist { get; set; }
    public string SortArtist => Utils.BuildSortName(Artist);
    public string AlbumId => $"album|{SortArtist}|{SortAlbum}";
    public string Album { get; set; }
    public string SortAlbum => Utils.BuildSortName(Album);
    public DateTime PlayedAt => DateTimeOffset.FromUnixTimeSeconds(long.Parse(_playedAt)).LocalDateTime;
    public string PlayedAtFmt => PlayedAt.ToString("T");
}