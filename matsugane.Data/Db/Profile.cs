using System.ComponentModel.DataAnnotations.Schema;

namespace matsugane.Data.Db;

[Table("profile")]
public class Profile
{
    [Column("profile_id")]
    public required int ProfileId { get; set; }

    [Column("playlist_id")]
    public required string PlaylistId { get; set; }

    [Column("profile_title")]
    public required string ProfileTitle { get; set; }

    [Column("profile_summary")]
    public required string ProfileSummary { get; set; }

    [Column("enabled")]
    public bool Enabled { get; set; }

    [Column("profile_source")]
    public required string ProfileSource { get; set; }

    [Column("profile_source_id")]
    public string? ProfileSourceId { get; set; }

    [Column("refresh_interval")]
    public required int RefreshInterval { get; set; }

    [Column("time_limit")]
    public required int TimeLimit { get; set; }

    [Column("track_limit")]
    public required int TrackLimit { get; set; }
}