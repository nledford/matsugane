namespace matsugane.Data.Utils;

public static class StatsExtensions
{
    public static double Mean(this List<int> values)
    {
        return values.Count == 0 ? 0 : values.Mean(0, values.Count);
    }

    public static double Mean(this List<int> values, int start, int end)
    {
        double s = 0;

        for (var i = start; i < end; i++)
        {
            s += values[i];
        }

        return s / (end - start);
    }

    public static double Variance(this List<int> values)
    {
        return values.Variance(values.Mean(), 0, values.Count);
    }

    public static double Variance(this List<int> values, double mean)
    {
        return values.Variance(mean, 0, values.Count);
    }

    public static double Variance(this List<int> values, double mean, int start, int end)
    {
        double variance = 0;

        for (var i = start; i < end; i++)
        {
            variance += Math.Pow((values[i] - mean), 2);
        }

        var n = end - start;
        if (start > 0) n -= 1;

        return variance / (n);
    }

    public static double StandardDeviation(this List<int> values)
    {
        return values.Count == 0 ? 0 : values.StandardDeviation(0, values.Count);
    }

    public static double StandardDeviation(this List<int> values, int start, int end)
    {
        var mean = values.Mean(start, end);
        var variance = values.Variance(mean, start, end);

        return Math.Sqrt(variance);
    }
}