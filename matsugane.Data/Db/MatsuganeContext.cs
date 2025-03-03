using Microsoft.EntityFrameworkCore;

namespace matsugane.Data.Db;

public class MatsuganeContext(DbContextOptions<MatsuganeContext> options) : DbContext(options)
{
    public DbSet<User> Users { get; set; }
}