using Microsoft.EntityFrameworkCore;

namespace matsugane.Data.Db;

public class MatsuganeContext(DbContextOptions<MatsuganeContext> options) : DbContext(options)
{
    public virtual DbSet<Profile> Profiles { get; set; }
    public virtual DbSet<VProfile> VProfiles { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        if (!optionsBuilder.IsConfigured)
        {
            optionsBuilder.UseNpgsql(Conn.BuildConnection());
        }
    }
}