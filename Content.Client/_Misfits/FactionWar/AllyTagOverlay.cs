// #Misfits Add - Screen-space overlay that draws [ALLY] and [ENEMY] tags above in-world entities
// when the local player's faction is engaged in an active war.
// Pattern mirrors AdminNameOverlay (Content.Client/Administration/AdminNameOverlay.cs).
// All faction membership checks route through NpcFactionSystem.IsMember to satisfy RA0002
// (NpcFactionMemberComponent.Factions is access-restricted to NpcFactionSystem).

using System.Numerics;
using Content.Shared._Misfits.FactionWar;
using Content.Shared.NPC.Components;
using Content.Shared.NPC.Systems;
using Robust.Client.GameObjects;
using Robust.Client.Graphics;
using Robust.Client.Player;
using Robust.Client.ResourceManagement;
using Robust.Shared.Enums;
using Robust.Shared.Maths;

namespace Content.Client._Misfits.FactionWar;

/// <summary>
/// Draws green <c>[ALLY]</c> or red <c>[ENEMY]</c> tags above entities whose faction is relevant
/// to the current war state. Active only while the local player is involved in at least one war.
/// </summary>
internal sealed class AllyTagOverlay : Overlay
{
    // All NPC faction IDs that can resolve to a war faction (including aliases like Rangers → NCR).
    private static readonly string[] WarFactionIds =
    {
        "NCR", "Rangers", "BrotherhoodOfSteel", "CaesarLegion",
        "Townsfolk", "PlayerRaider",
    };

    private readonly FactionWarClientSystem _warSystem;
    private readonly IEntityManager         _entityManager;
    private readonly IPlayerManager         _playerManager;
    private readonly NpcFactionSystem        _npcFaction;
    private readonly IEyeManager            _eyeManager;
    private readonly EntityLookupSystem     _entityLookup;
    private readonly Font                   _font;

    public override OverlaySpace Space => OverlaySpace.ScreenSpace;

    public AllyTagOverlay(
        FactionWarClientSystem warSystem,
        IEntityManager         entityManager,
        IPlayerManager         playerManager,
        NpcFactionSystem       npcFaction,
        IEyeManager            eyeManager,
        IResourceCache         resourceCache,
        EntityLookupSystem     entityLookup)
    {
        _warSystem     = warSystem;
        _entityManager = entityManager;
        _playerManager = playerManager;
        _npcFaction    = npcFaction;
        _eyeManager    = eyeManager;
        _entityLookup  = entityLookup;

        ZIndex = 195; // just below AdminNameOverlay (200) so admin tags render on top
        _font = new VectorFont(
            resourceCache.GetResource<FontResource>("/Fonts/NotoSans/NotoSans-Regular.ttf"), 10);
    }

    protected override void Draw(in OverlayDrawArgs args)
    {
        var localEntity = _playerManager.LocalSession?.AttachedEntity;
        if (localEntity == null)
            return;

        var activeWars = _warSystem.ActiveWars;
        if (activeWars.Count == 0)
            return;

        // Find the local player's war-capable faction from server-communicated data.
        // NpcFactionMemberComponent.Factions is not synced to clients, so we rely on
        // FactionWarClientSystem.LocalFactionId which is set by FactionWarPanelDataEvent.
        var myFactionId = _warSystem.LocalFactionId;

        if (myFactionId == null)
            return;

        // Build the enemy faction list from active wars involving the local player's faction.
        var enemyFactions = new List<string>(2);
        foreach (var war in activeWars)
        {
            if (war.AggressorFaction == myFactionId)
                enemyFactions.Add(war.TargetFaction);
            else if (war.TargetFaction == myFactionId)
                enemyFactions.Add(war.AggressorFaction);
        }

        // Build sets of all NPC faction IDs that map to our canonical war faction and to each enemy.
        // e.g. if myFactionId = "NCR", allyNpcFactions = { "NCR", "Rangers" }.
        var allyNpcFactions = new HashSet<string> { myFactionId };
        foreach (var (raw, canonical) in FactionWarConfig.FactionAliases)
        {
            if (canonical == myFactionId)
                allyNpcFactions.Add(raw);
        }

        var enemyNpcFactions = new HashSet<string>(enemyFactions);
        foreach (var ef in enemyFactions)
        {
            foreach (var (raw, canonical) in FactionWarConfig.FactionAliases)
            {
                if (canonical == ef)
                    enemyNpcFactions.Add(raw);
            }
        }

        var viewport = args.WorldAABB;

        // Iterate all entities that have faction membership and a visible sprite.
        var query = _entityManager.AllEntityQueryEnumerator<NpcFactionMemberComponent, SpriteComponent>();
        while (query.MoveNext(out var uid, out _, out _))
        {
            // Skip the local player's own entity.
            if (uid == localEntity.Value)
                continue;

            // Skip entities on a different map.
            if (_entityManager.GetComponent<TransformComponent>(uid).MapID != _eyeManager.CurrentMap)
                continue;

            // Skip if not in the viewport.
            var aabb = _entityLookup.GetWorldAABB(uid);
            if (!aabb.Intersects(viewport))
                continue;

            // Determine the tag. Check all NPC faction IDs that resolve to our war faction or enemies.
            string tag;
            Color  tagColor;

            var isAlly = false;
            foreach (var af in allyNpcFactions)
            {
                if (_npcFaction.IsMember(uid, af))
                {
                    isAlly = true;
                    break;
                }
            }

            if (isAlly)
            {
                tag      = "[ALLY]";
                tagColor = Color.LimeGreen;
            }
            else
            {
                var isEnemy = false;
                foreach (var ef in enemyNpcFactions)
                {
                    if (_npcFaction.IsMember(uid, ef))
                    {
                        isEnemy = true;
                        break;
                    }
                }

                if (!isEnemy)
                    continue;

                tag      = "[ENEMY]";
                tagColor = new Color(1f, 0.3f, 0.3f);
            }

            // Position above the entity's top-right corner — mirrors AdminNameOverlay placement.
            var screenCoords = _eyeManager.WorldToScreen(
                aabb.Center + new Angle(-_eyeManager.CurrentEye.Rotation)
                    .RotateVec(aabb.TopRight - aabb.Center)) + new Vector2(1f, 7f);

            args.ScreenHandle.DrawString(_font, screenCoords, tag, tagColor);
        }
    }
}
