# Loc strings for various entity state & client-side PVS related commands

cmd-reset-ent-help = Usage: resetent <Entity UID>
cmd-reset-ent-desc = Resets an entity to the last state received from the server. This will also reset entities that were deleted in null-space.
cmd-reset-all-ents-help = Usage: resetallents
cmd-reset-all-ents-desc = Resets all entities to the last state received from the server. This only affects entities that were not deleted in null-space.
cmd-detach-ent-help = Usage: detachent <Entity UID>
cmd-detach-ent-desc = Removes an entity to null-space, as if it left the PVS range.
cmd-local-delete-help = Usage: localdelete <Entity UID>
cmd-local-delete-desc = Deletes an entity. Unlike the normal delete command, this command works on the CLIENT-SIDE. If the entity is not a client entity, this will likely cause errors.
cmd-full-state-reset-help = Usage: fullstatereset
cmd-full-state-reset-desc = Resets all entity state information and requests full state from the server.
