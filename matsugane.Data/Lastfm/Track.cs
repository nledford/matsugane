// ReSharper disable MemberCanBePrivate.Global

// ReSharper disable UnusedMember.Global

// ReSharper disable UnusedAutoPropertyAccessor.Global

namespace matsugane.Data.Lastfm;

public class Track
{
    public string TrackId => $"track|{SortTitle}|{SortArtist}|{SortAlbum}";
    public string PlayId => $"play|{PlayedAt}";
    public string Title { get; private init; } = string.Empty;
    public string SortTitle { get; private init; } = string.Empty;
    public string ArtistId => $"artist|{SortArtist}";
    public string Artist { get; private init; } = string.Empty;
    public string SortArtist { get; private init; } = string.Empty;
    public string AlbumId => $"album|{SortArtist}|{SortAlbum}";
    public string Album { get; private init; } = string.Empty;
    public string SortAlbum { get; private init; } = string.Empty;
    public DateTime PlayedAt { get; private init; }
    public string PlayedAtFmt => PlayedAt.ToString("HH:mm:ss");

    public static async Task<Track> BuildTrack(string title, string artist, string album, string playedAt)
    {
        return new Track
        {
            Title = title,
            SortTitle = await Utils.BuildSortNameAsync(title),
            Artist = artist,
            SortArtist = await Utils.BuildSortNameAsync(artist),
            Album = album,
            SortAlbum = await Utils.BuildSortNameAsync(album),
            PlayedAt = DateTimeOffset.FromUnixTimeSeconds(long.Parse(playedAt)).LocalDateTime
        };
    }
}