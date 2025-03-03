namespace matsugane.Data.Lastfm;

public class PlaysByHour(int hour, int plays, int globalPlays)
{
    public int Hour { get; } = hour;
    public string HourFmt => $"{Hour:D2}:00";
    public int Plays { get; } = plays;
    public string PlaysFmt => $"{Plays} play{(Plays == 1 ? "" : "s")}";
    public double Percent { get; } = (double)plays / globalPlays;
    public string PercentFmt => $"{Percent * 100.0}%";
}