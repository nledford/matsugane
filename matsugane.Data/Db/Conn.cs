using Npgsql;

namespace matsugane.Data.Db;

public static class Conn
{
    public static NpgsqlConnection BuildConnection()
    {
        var server = Environment.GetEnvironmentVariable("PG_SERVER");
        var port = Environment.GetEnvironmentVariable("PG_PORT");
        var db = Environment.GetEnvironmentVariable("PG_DB");
        var user = Environment.GetEnvironmentVariable("PG_USER");
        var password = Environment.GetEnvironmentVariable("PG_PASSWORD");

        return new NpgsqlConnection(
            connectionString: $"Server={server};Port={port};User Id={user};Password={password};Database={db}");
    }
}