namespace Content.Shared._Misfits.Warcry;

/// <summary>
/// Temporary movement-speed buff applied by a warcry.
/// </summary>
[RegisterComponent]
public sealed partial class WarcryBuffComponent : Component
{
    /// <summary>
    /// Flat fractional movement bonus while the buff is active.
    /// For example, 0.15 grants a 15% walk and sprint speed increase.
    /// </summary>
    [DataField]
    public float SpeedBonus = 0.15f;

    /// <summary>
    /// When the buff expires.
    /// </summary>
    [DataField]
    public TimeSpan ExpiresAt;
}