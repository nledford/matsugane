using Newtonsoft.Json.Linq;
using RestSharp;

namespace matsugane.Data.Lastfm;

interface ILastfmClient
{
    Task<IEnumerable<Track>> GetRecentTracks(int limit = 1000);
}

public class LastfmClient : ILastfmClient, IDisposable
{
    private readonly RestClient _client;

    public LastfmClient()
    {
        var options = new RestClientOptions("http://ws.audioscrobbler.com/2.0/");
        _client = new RestClient(options);
    }

    public async Task<IEnumerable<Track>> GetRecentTracks(int limit = 1000)
    {
        var req = new RestRequest();
        req.AddQueryParameter("method", "User.getrecenttracks");
        req.AddQueryParameter("user", Environment.GetEnvironmentVariable("LASTFM_USER"));
        req.AddQueryParameter("limit", limit);
        req.AddQueryParameter("extended", 1);
        req.AddQueryParameter("from", ((DateTimeOffset)DateTime.Today).ToUnixTimeSeconds());
        req.AddQueryParameter("api_key", Environment.GetEnvironmentVariable("LASTFM_KEY"));
        req.AddQueryParameter("format", "json");

        var response = await _client.GetAsync(req);
        var json = JObject.Parse(response.Content!);
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
        _client?.Dispose();
        GC.SuppressFinalize(this);
    }
}