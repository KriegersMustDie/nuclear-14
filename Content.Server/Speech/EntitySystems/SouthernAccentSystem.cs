using System.Text.RegularExpressions;
using Content.Server.Speech.Components;

namespace Content.Server.Speech.EntitySystems;

public sealed class SouthernAccentSystem : EntitySystem
{
    private static readonly Regex RegexIng = new(@"ing\b");
    private static readonly Regex RegexAnd = new(@"\band\b");
    private static readonly Regex RegexDve = new("d've");

    // Regex replacements for whole words with case handling
    private static readonly Regex RegexGood = new(@"(?<!\w)(good)(?!\w)", RegexOptions.IgnoreCase);
    private static readonly Regex RegexThank = new(@"(?<!\w)(thanks)(?!\w)", RegexOptions.IgnoreCase);
    private static readonly Regex RegexHello = new(@"(?<!\w)(hello)(?!\w)", RegexOptions.IgnoreCase);
    private static readonly Regex RegexGoodbye = new(@"(?<!\w)(goodbye|bye)(?!\w)", RegexOptions.IgnoreCase);
    private static readonly Regex RegexHim = new(@"(?<!\w)(him)(?!\w)", RegexOptions.IgnoreCase);
    private static readonly Regex RegexThis = new(@"(?<!\w)(this)(?!\w)", RegexOptions.IgnoreCase);
    private static readonly Regex RegexWhat = new(@"(?<!\w)(what)(?!\w)", RegexOptions.IgnoreCase);

    // Regex replacements for letter groups with case handling
    private static readonly Regex RegexReplaceR = new(@"r", RegexOptions.IgnoreCase);
    private static readonly Regex RegexReplaceSh = new(@"sh", RegexOptions.IgnoreCase);
    private static readonly Regex RegexReplaceY = new(@"y", RegexOptions.IgnoreCase);
    private static readonly Regex RegexReplaceCh = new(@"ch", RegexOptions.IgnoreCase);
    private static readonly Regex RegexReplaceF = new(@"f", RegexOptions.IgnoreCase);
    private static readonly Regex RegexReplaceTsa = new(@"ts\b", RegexOptions.IgnoreCase);

    [Dependency] private readonly ReplacementAccentSystem _replacement = default!;

    public override void Initialize()
    {
        base.Initialize();
        SubscribeLocalEvent<SouthernAccentComponent, AccentGetEvent>(OnAccent);
    }

    private void OnAccent(EntityUid uid, SouthernAccentComponent component, AccentGetEvent args)
    {
        var message = args.Message;

        // Apply replacement rules
        message = _replacement.ApplyReplacements(message, "southern");

        //They shoulda started runnin' an' hidin' from me!
        message = RegexIng.Replace(message, "in'");
        message = RegexAnd.Replace(message, "an'");
        message = RegexDve.Replace(message, "da");
        // Apply specific word replacements with case preservation
        message = RegexGood.Replace(message, match => PreserveCase(match.Value, "hao"));
        message = RegexThank.Replace(message, match => PreserveCase(match.Value, "xie xie"));
        message = RegexHello.Replace(message, match => PreserveCase(match.Value, "ni hao"));
        message = RegexGoodbye.Replace(message, match => PreserveCase(match.Value, "zai jian"));
        message = RegexHim.Replace(message, match => PreserveCase(match.Value, "heem"));
        message = RegexThis.Replace(message, match => PreserveCase(match.Value, "dis"));
        message = RegexWhat.Replace(message, match => PreserveCase(match.Value, "wut"));

        // Apply character replacements with case preservation
        message = RegexReplaceR.Replace(message, match => ReplaceWithCase(match.Value, "l"));
        message = RegexReplaceSh.Replace(message, match => ReplaceWithCase(match.Value, "s"));
        message = RegexReplaceY.Replace(message, match => ReplaceWithCase(match.Value, "i"));
        message = RegexReplaceCh.Replace(message, match => ReplaceWithCase(match.Value, "ts"));
        message = RegexReplaceF.Replace(message, match => ReplaceWithCase(match.Value, "v"));
        message = RegexReplaceTsa.Replace(message, match => ReplaceWithCase(match.Value, "tsa"));

        args.Message = message;
    }

    private string PreserveCase(string original, string replacement)
    {
        return original.ToUpper() == original
            ? replacement.ToUpper()
            : original.ToLower() == original
                ? replacement.ToLower()
                : replacement;
    }

    private string ReplaceWithCase(string original, string replacement)
    {
        return original.ToUpper() == original
            ? replacement.ToUpper()
            : original.ToLower() == original
                ? replacement.ToLower()
                : replacement;
    }
}
