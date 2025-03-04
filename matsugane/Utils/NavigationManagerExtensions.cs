using Microsoft.AspNetCore.Components;

namespace matsugane.Utils;

public static class NavigationManagerExtensions
{
    public static string Page(this NavigationManager navigation)
    {
        return navigation.Uri[(navigation.BaseUri.Length - 1)..];
    }
}