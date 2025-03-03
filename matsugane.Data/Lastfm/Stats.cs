using matsugane.Data.Utils;

namespace matsugane.Data.Lastfm;

public class Stats(List<int> items)
{
    private int Total => items.Count;
    public double Mean => items.Mean();

    public double Median => items.OrderBy(item => item)
        .Skip((items.Count - 1) / 2)
        .Take(2 - items.Count % 2)
        .ToList()
        .Mean();

    public double Mode => items.GroupBy(item => item)
        .OrderByDescending(group => group.Count())
        .First().Key;

    public double Variance => items.Variance();
    public double StandardDeviation => items.StandardDeviation();

    public double LowerLimit
    {
        get
        {
            if (Total <= 0)
            {
                return 1.0;
            }

            var result = Mean - (2 * StandardDeviation);
            return result < 1.0 ? 1.0 : result;
        }
    }

    public double UpperLimit
    {
        get
        {
            if (Total <= 0)
            {
                return 1.0;
            }

            var result = Mean + (2 * StandardDeviation);
            return result < 1.0 ? 1.0 : result;
        }
    }

    public int ItemsExceedingUpperLimit
    {
        get { return items.Count(i => i > UpperLimit); }
    }
}