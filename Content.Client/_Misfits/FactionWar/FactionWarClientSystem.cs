// #Misfits Add - Client-side faction war system.
// Receives war state syncs from the server and manages the AllyTagOverlay lifecycle.
// Registers the /war client console command that opens the FactionWarWindow GUI.
// All faction detection is done server-side (NpcFactionMemberComponent.Factions is not
// synced to clients); the server sends pre-computed panel data via FactionWarPanelDataEvent.

using System.Linq;
using Content.Client._Misfits.FactionWar.UI;
using Content.Shared._Misfits.FactionWar;
using Content.Shared.NPC.Systems;
using Robust.Client.Console;
using Robust.Client.Graphics;
using Robust.Client.Player;
using Robust.Client.ResourceManagement;
using Robust.Client.UserInterface;
using Robust.Shared.Console;

namespace Content.Client._Misfits.FactionWar;

/// <summary>
/// Manages the <see cref="AllyTagOverlay"/> and the <see cref="FactionWarWindow"/> GUI.
/// The /war client command opens the GUI panel; all game-logic validation stays server-side.
/// </summary>
public sealed class FactionWarClientSystem : EntitySystem
{
    [Dependency] private readonly IOverlayManager     _overlayManager = default!;
    [Dependency] private readonly IPlayerManager      _playerManager  = default!;
    [Dependency] private readonly IEyeManager         _eyeManager     = default!;
    [Dependency] private readonly IResourceCache      _resourceCache  = default!;
    [Dependency] private readonly EntityLookupSystem  _entityLookup   = default!;
    [Dependency] private readonly NpcFactionSystem    _npcFaction     = default!;
    [Dependency] private readonly IClientConsoleHost  _conHost        = default!;
    [Dependency] private readonly IUserInterfaceManager _uiManager    = default!;

    /// <summary>Current active wars. Read by <see cref="AllyTagOverlay"/> each frame.</summary>
    public IReadOnlyList<FactionWarEntry> ActiveWars => _activeWars;

    /// <summary>
    /// Local player's war-capable faction ID as determined by the server.
    /// Used by the overlay to avoid client-side IsMember which doesn't work
    /// (NpcFactionMemberComponent.Factions is not synced to clients).
    /// </summary>
    public string? LocalFactionId { get; private set; }

    private List<FactionWarEntry> _activeWars = new();
    private AllyTagOverlay?    _overlay;
    private FactionWarWindow?  _window;

    public override void Initialize()
    {
        base.Initialize();

        SubscribeNetworkEvent<FactionWarStateUpdatedEvent>(OnWarStateUpdated);
        SubscribeNetworkEvent<FactionWarPanelDataEvent>(OnPanelData);
        SubscribeNetworkEvent<FactionWarCommandResultEvent>(OnCommandResult);

        _conHost.RegisterCommand(
            "war",
            Loc.GetString("faction-war-cmd-desc"),
            "war",
            OpenWarPanel);
    }

    public override void Shutdown()
    {
        base.Shutdown();
        _window?.Close();
        _window = null;
        RemoveOverlay();
    }

    // ── Network event handlers ─────────────────────────────────────────────

    private void OnWarStateUpdated(FactionWarStateUpdatedEvent msg)
    {
        _activeWars = msg.ActiveWars;
        UpdateOverlayVisibility();
    }

    private void OnPanelData(FactionWarPanelDataEvent msg)
    {
        // Cache faction ID for overlay use.
        LocalFactionId = msg.MyFactionId;
        _activeWars    = msg.ActiveWars;

        UpdateOverlayVisibility();

        if (_window == null)
            return;

        var eligibleTargets = msg.EligibleTargets
            .Select(t => (t.DisplayName, t.Id))
            .ToList();

        var ceasefireTargets = msg.CeasefireTargets
            .Select(t => (t.DisplayName, t.Id))
            .ToList();

        _window.UpdateState(
            msg.MyFactionId,
            msg.MyFactionDisplay,
            msg.ActiveWars,
            eligibleTargets,
            ceasefireTargets);

        if (msg.StatusMessage != null)
            _window.ShowResult(false, msg.StatusMessage);
    }

    private void OnCommandResult(FactionWarCommandResultEvent msg)
    {
        _window?.ShowResult(msg.Success, msg.Message);
    }

    // ── /war client command ────────────────────────────────────────────────

    private void OpenWarPanel(IConsoleShell shell, string argStr, string[] args)
    {
        EnsureWindow();
        _window!.OpenCentered();

        // Ask server for fresh panel data (faction detection must happen server-side).
        RaiseNetworkEvent(new FactionWarOpenPanelRequestEvent());
    }

    // ── Window lifecycle ───────────────────────────────────────────────────

    private void EnsureWindow()
    {
        if (_window != null)
            return;

        _window = new FactionWarWindow();
        _window.OnClose += () => _window = null;

        _window.OnDeclareWar += (targetId, casusBelli) =>
        {
            RaiseNetworkEvent(new FactionWarDeclareRequestEvent
            {
                TargetFaction = targetId,
                CasusBelli    = casusBelli,
            });
        };

        _window.OnCeasefire += targetId =>
        {
            RaiseNetworkEvent(new FactionWarCeasefireRequestEvent
            {
                TargetFaction = targetId,
            });
        };
    }

    // ── Overlay lifecycle ──────────────────────────────────────────────────

    private void UpdateOverlayVisibility()
    {
        // Use server-communicated LocalFactionId instead of client-side IsMember
        // (factions are not synced to the client).
        if (LocalFactionId == null || _activeWars.Count == 0)
        {
            RemoveOverlay();
            return;
        }

        var involved = _activeWars.Any(w =>
            w.AggressorFaction == LocalFactionId ||
            w.TargetFaction    == LocalFactionId);

        if (involved)
            EnsureOverlay();
        else
            RemoveOverlay();
    }

    private void EnsureOverlay()
    {
        if (_overlay != null)
            return;

        _overlay = new AllyTagOverlay(
            this,
            EntityManager,
            _playerManager,
            _npcFaction,
            _eyeManager,
            _resourceCache,
            _entityLookup);

        _overlayManager.AddOverlay(_overlay);
    }

    private void RemoveOverlay()
    {
        if (_overlay == null)
            return;

        _overlayManager.RemoveOverlay<AllyTagOverlay>();
        _overlay = null;
    }
}
