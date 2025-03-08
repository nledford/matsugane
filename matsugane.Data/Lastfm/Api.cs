using Microsoft.AspNetCore.WebUtilities;
using Newtonsoft.Json.Linq;

namespace matsugane.Data.Lastfm;

public class LastfmClient : IDisposable
{
    private readonly HttpClient _client;

    public LastfmClient(HttpClient client)
    {
        client.BaseAddress = new Uri("http://ws.audioscrobbler.com/2.0/");
        _client = client;
    }

    public async Task<IEnumerable<Track>> GetRecentTracks(int limit = 1000)
    {
        var user = Environment.GetEnvironmentVariable("LASTFM_USER");
        var key = Environment.GetEnvironmentVariable("LASTFM_KEY");

        if (string.IsNullOrWhiteSpace(user))
        {
            throw new Exception("`LASTFM_USER` environment variable not found.");
        }

        if (string.IsNullOrWhiteSpace(key))
        {
            throw new Exception("`LASTFM_KEY` environment variable not found.");
        }

        var query = new Dictionary<string, string?>()
        {
            ["method"] = "User.getrecenttracks",
            ["user"] = user,
            ["limit"] = limit.ToString(),
            ["extended"] = "1",
            ["from"] = ((DateTimeOffset)DateTime.Today).ToUnixTimeSeconds().ToString(),
            ["api_key"] = key,
            ["format"] = "json"
        };

        var response = await _client.GetAsync(QueryHelpers.AddQueryString("", query));
        Console.WriteLine(response.ToString());
        Console.WriteLine(response.RequestMessage?.RequestUri);

        var json = JObject.Parse(await response.Content.ReadAsStringAsync());
        var tracks = json["recenttracks"]!["track"]!;

        var lastfmTracks = new List<Track>();
        foreach (var track in tracks)
        {
            var title = (string)track["name"]!;
            var artist = (string)track["artist"]!["name"]!;
            var album = (string)track["album"]!["#text"]!;
            var playedAt = (string)track["date"]!["uts"]!;

            var lastfmTrack = await Track.BuildTrack(title, artist, album, playedAt);
            lastfmTracks.Add(lastfmTrack);
        }

        return lastfmTracks;
    }

    public void Dispose()
    {
        _client.Dispose();
        GC.SuppressFinalize(this);
    }
}