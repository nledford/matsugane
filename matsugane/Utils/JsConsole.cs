using Microsoft.JSInterop;

namespace matsugane.Utils;

public class JsConsole(IJSRuntime jsRuntime)
{
    public async Task LogAsync(object message)
    {
        await jsRuntime.InvokeVoidAsync("console.log", message);
    }
}