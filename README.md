# JazzRadio for Kodi — pre-V1

Unofficial community JazzRadio / AudioAddict music add-on for Kodi.

## V1 scope

The V1 deliberately provides a simple linear-radio experience using Kodi's
native player:

- AudioAddict account login with cached/reused sessions
- current JazzRadio channel list and style filters
- Popular and New views
- favourites synchronised with the AudioAddict account
- Premium stream quality selection
- multiple stream-server fallback
- dynamic title, artist and track-cover updates
- channel artwork exposed as Kodi fanart
- English and French localisation
- no custom player UI

The JazzRadio channel directory is fetched from AudioAddict when its Kodi view is opened;
the add-on does not maintain a local channel catalogue cache.

## Architecture

`default.py`
: Kodi plugin entry point. Builds directories and resolves a selected station
  to a linear Premium stream.

`service.py`
: Lightweight background service. While a JazzRadio stream is playing, it polls
  Now Playing metadata and updates Kodi's actual playing `ListItem`, allowing
  title/artist/cover changes to propagate to Estuary, the Kodi web interface
  and remote controls such as Kore.

`resources/lib/client.py`
: AudioAddict network client. Handles authentication/session renewal, channel
  metadata, favourites and Premium PLS stream resolution.

`resources/lib/helpers.py`
: Image URL normalisation and Kodi `ListItem` helpers.

`resources/lib/state.py`
: Small state file stored only inside this add-on's Kodi profile directory.

## Authentication and session handling

The user's AudioAddict email/password remain Kodi settings. A successful
AudioAddict session is cached in the add-on profile and reused across restarts.
If the server rejects that session with HTTP 401/403, the add-on deletes the
cached session and performs one fresh login automatically.

## Premium quality mapping

- Medium → `premium_medium` → AAC-HE 64 kb/s
- High → `premium` → AAC 128 kb/s
- Ultra → `premium_high` → MP3 320 kb/s

Changing this setting affects the next time a stream is opened. V1 does not
interrupt/restart an already playing stream when the quality setting changes.

## V2 candidates

- per-track progress using a track-by-track playback engine
- apply a quality change without manually stopping/restarting playback
- optional interactive JazzRadio functions (Like / Dislike / Next) only if there
  is enough user value to justify the additional Kodi UI complexity
- sleep timer
- improved behaviour/recovery after a temporary network loss
- higher-resolution official channel fanart if JazzRadio can provide suitable
  TV/desktop assets

## Publication status

The code has been cleaned toward Kodi repository submission, but two metadata
fields must be chosen before submission and are deliberately not invented:

1. public maintainer/provider name
2. public source repository URL

JazzRadio branding/API permission and availability of higher-resolution official
channel artwork should also be clarified with JazzRadio / AudioAddict before public release.

GPL-3.0-or-later.
Unofficial; not affiliated with JazzRadio or AudioAddict.


## 0.6.1 settings fix

- Restores the JazzRadio/AudioAddict account e-mail field in Kodi settings.
- The configured e-mail remains visible so the active account can be identified.
- The password remains masked.
- Existing stored values are preserved by keeping the same setting IDs (`email`, `password`).


## 0.6.2 settings schema fix

Kodi's v2 add-on settings format requires empty editable string fields to use
a self-closing `<default/>` and `<constraints><allowempty>true</allowempty></constraints>`.
This restores the visible JazzRadio/AudioAddict e-mail field and masked
password field while preserving the existing setting IDs.

## 0.6.3 stability and maintenance update

* Reduces unnecessary AudioAddict API calls during Now Playing updates.
* Reuses the current session directly and only re-authenticates after HTTP 401/403.
* Fetches detailed track metadata only when the current track changes.
* Improves favourites error handling so API failures are no longer treated as an empty favourites list.
* Refreshes the Kodi directory after adding or removing a favourite.
* Improves user-facing error handling while keeping technical details in the Kodi log.
* Opens add-on settings and exits cleanly when account credentials are missing.
* Uses the add-on version dynamically in the HTTP User-Agent.
* Removes unused interactive/V2 localisation strings and redundant player code.
* Adds additional logging for previously silent file/state errors.

