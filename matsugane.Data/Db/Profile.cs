using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace matsugane.Data.Db;

[Table("profile")]
public class Profile
{
    [Key] [Column("profile_id")] public required int ProfileId { get; set; }

    [Column("playlist_id")] public required string PlaylistId { get; set; }

    [Column("profile_title")] public required string ProfileTitle { get; set; }

    [Column("profile_summary")] public required string ProfileSummary { get; set; }

    [Column("enabled")] public bool Enabled { get; set; }

    [Column("profile_source")] public required string ProfileSource { get; set; }

    [Column("profile_source_id")] public string? ProfileSourceId { get; set; }

    [Column("refresh_interval")] public required int RefreshInterval { get; set; }

    [Column("time_limit")] public required int TimeLimit { get; set; }

    [Column("track_limit")] public required int TrackLimit { get; set; }

}

[Table("v_profile")]
public class VProfile : Profile
{
    [Column("num_sections")] public required int NumSections { get; set; }

    [Column("has_max_sections")] public required bool HasMaxSections { get; set; }

    [Column("refreshes_per_hour")] public required int RefreshesPerHour { get; set; }

    [Column("last_refresh")] public required DateTime LastRefresh { get; set; }

    [Column("next_refresh")] public required DateTime NextRefresh { get; set; }

    [Column("eligible_for_refresh")] public required bool EligibleForRefresh { get; set; }
}

// [Table("profile_section")]
// public class ProfileSection
// {
//
//     [Key] [Column("profile_section_id")] public required int ProfileSectionId { get; set; }
//
//     [Column("profile_id")]
//     [ForeignKey("Profile")]
//     public required int ProfileId { get; set; }
//
//     public virtual required Profile Profile { get; set; }
//
//     [Column("section_type")] public required string SectionType { get; set; }
//
//     [Column("enabled")] public bool Required { get; set; }
//
//     [Column("deduplicate_tracks_by_guid")] public bool DeduplicateTracksByGuid { get; set; }
//
//     [Column("deduplicate_tracks_by_title_and_artist")]
//     public bool DeduplicateTracksByTitleAndArtist { get; set; }
//
//     [Column("maximum_tracks_by_artists")] public int MaximumTracksByArtists { get; set; }
//
//     [Column("minimum_track_rating")] public int MinimumTrackRating { get; set; }
//
//     [Column("randomize_tracks")] public bool RandomizeTracks { get; set; }
//
//     [Column("sorting")] public required string Sorting { get; set; }
// }