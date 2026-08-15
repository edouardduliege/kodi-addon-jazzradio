# -*- coding: utf-8 -*-
"""Background service that refreshes linear-stream Now Playing metadata."""
from __future__ import annotations

import xbmc
import xbmcaddon
import xbmcgui

from resources.lib.client import AudioAddictClient, AudioAddictError
from resources.lib.helpers import image_url
from resources.lib.state import load_state, save_state

ADDON_ID = "plugin.audio.jazzradio"
ADDON = xbmcaddon.Addon(ADDON_ID)


class DIFMPlayer(xbmc.Player):
    def __init__(self):
        super().__init__()


def update_linear_metadata(client, player, state):
    channel = state.get("channel_key")
    if not channel or state.get("mode") != "linear":
        return

    current = client.current_track(channel)
    if not isinstance(current, dict) or not current.get("id"):
        return

    if current.get("id") == state.get("track_id"):
        return

    title = (
        current.get("display_title")
        or current.get("title")
        or channel
    )
    artist = current.get("display_artist") or "JazzRadio"
    album = f"JazzRadio — {state.get('channel_name') or channel}"

    # Work on Kodi's actual current ListItem. This gives artwork updates
    # the best chance of propagating not only to Estuary but also to
    # JSON-RPC clients such as the web interface and Kore.
    try:
        item = player.getPlayingItem()
    except Exception:
        item = xbmcgui.ListItem()
        try:
            item.setPath(player.getPlayingFile())
        except Exception:
            pass

    tag = item.getMusicInfoTag()
    tag.setTitle(str(title))
    tag.setArtist(str(artist))
    tag.setAlbum(str(album))

    thumb = image_url(
        current.get("asset_url")
        or (
            (current.get("images") or {}).get("default")
            if isinstance(current.get("images"), dict)
            else ""
        )
    )

    art = {}
    if thumb or state.get("channel_art"):
        art["thumb"] = thumb or state.get("channel_art")
        art["icon"] = thumb or state.get("channel_art")
    if state.get("channel_fanart") or state.get("channel_art"):
        art["fanart"] = (
            state.get("channel_fanart")
            or state.get("channel_art")
        )

    if art:
        item.setArt(art)

    # updateInfoTag pushes the modified playing item back to Kodi's
    # Now Playing state after mutating title/artist/artwork above.
    player.updateInfoTag(item)

    state["track_id"] = current.get("id")
    state["title"] = title
    state["artist"] = artist
    state["track_art"] = thumb or ""
    save_state(state)

    xbmc.log(
        "[plugin.audio.jazzradio] Now Playing updated: "
        f"track_id={current.get('id')}, art={'yes' if thumb else 'no'}",
        xbmc.LOGDEBUG,
    )


def main():
    monitor = xbmc.Monitor()
    player = DIFMPlayer()
    client = None

    while not monitor.abortRequested():
        if monitor.waitForAbort(10):
            break

        try:
            state = load_state()

            if state.get("mode") != "linear":
                continue
            if not player.isPlayingAudio():
                continue

            if client is None:
                client = AudioAddictClient()

            update_linear_metadata(client, player, state)

        except AudioAddictError as exc:
            xbmc.log(
                f"[plugin.audio.jazzradio] metadata service API error: {exc}",
                xbmc.LOGDEBUG,
            )
        except Exception as exc:
            xbmc.log(
                f"[plugin.audio.jazzradio] metadata service error: {exc!r}",
                xbmc.LOGDEBUG,
            )


if __name__ == "__main__":
    main()
