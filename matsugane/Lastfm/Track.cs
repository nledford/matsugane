namespace matsugane.Lastfm;

public class Track
{
    public string TrackId => $"track|{SortTitle}|{SortArtist}|{SortAlbum}";
    public string PlayId => $"play|{PlayedAt}";
    public string Title { get; private init; }
    public string SortTitle { get; private init; }
    public string ArtistId => $"artist|{SortArtist}";
    public string Artist { get; private init; }
    public string SortArtist { get; private init; }
    public string AlbumId => $"album|{SortArtist}|{SortAlbum}";
    public string Album { get; private init; }
    public string SortAlbum { get; private init; }
    public DateTime PlayedAt { get; private init; }
    public string PlayedAtFmt => PlayedAt.ToString("T");

    public static async Task<Track> BuildTrack(string title, string artist, string album, string playedAt)
    {
        return new Track()
        {
            Title = title,
            SortTitle = await Utils.BuildSortNameAsync(title),
            Artist = artist,
            SortArtist = await Utils.BuildSortNameAsync(artist),
            Album = album,
            SortAlbum = await Utils.BuildSortNameAsync(album),
            PlayedAt = DateTimeOffset.FromUnixTimeSeconds(long.Parse(playedAt)).LocalDateTime,
        };
    }
}