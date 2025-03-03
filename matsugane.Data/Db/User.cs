using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;

namespace matsugane.Data.Db;

[Table("startpage_user")]
public class User
{

    [Column("id")]
    public required string Id { get; set; }

    [Column("username")]
    [Required]
    public required string Username { get; set; }

    [Column("password")]
    [Required]
    public required string Password { get; set; }
}