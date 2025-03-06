namespace matsugane.Utils;

public static class Time
{
    public static DateTime RoundUp(TimeSpan d)
    {
        return DateTime.Now.RoundUp(d);
    }

    // SOURCE: https://stackoverflow.com/a/7029464
    public static DateTime RoundUp(this DateTime dt, TimeSpan d)
    {
        return new DateTime((dt.Ticks + d.Ticks - 1) / d.Ticks * d.Ticks, dt.Kind);
    }
}