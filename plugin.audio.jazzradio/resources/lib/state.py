# -*- coding: utf-8 -*-
"""Small persistent state shared by the plugin and metadata service."""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import xbmc
import xbmcaddon
import xbmcvfs

ADDON_ID = "plugin.audio.jazzradio"


def _state_path():
    """Return the playback-state path inside this add-on's profile."""
    addon = xbmcaddon.Addon(ADDON_ID)
    profile = xbmcvfs.translatePath(addon.getAddonInfo("profile"))
    os.makedirs(profile, exist_ok=True)
    return Path(profile) / "playback_state.json"


def load_state():
    """Load playback state, returning an empty dict if unavailable."""
    try:
        path = _state_path()
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
    except Exception as exc:
        xbmc.log(
            f"[plugin.audio.jazzradio] unable to read playback state: {exc!r}",
            xbmc.LOGWARNING,
        )
    return {}


def save_state(data):
    """Persist playback state for the background Now Playing service."""
    path = _state_path()
    payload = dict(data or {})
    payload["updated_at"] = int(time.time())
    path.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    try:
        os.chmod(path, 0o600)
    except Exception as exc:
        xbmc.log(
            "[plugin.audio.jazzradio] unable to restrict playback state "
            f"permissions: {exc!r}",
            xbmc.LOGWARNING,
        )


def clear_state():
    """Remove stale playback state."""
    try:
        path = _state_path()
        if path.exists():
            path.unlink()
    except Exception as exc:
        xbmc.log(
            f"[plugin.audio.jazzradio] unable to clear playback state: {exc!r}",
            xbmc.LOGWARNING,
        )
