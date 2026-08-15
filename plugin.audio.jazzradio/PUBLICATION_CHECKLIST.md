# Kodi publication checklist

## Already addressed

- [x] Python 3 add-on
- [x] V1 feature scope frozen around linear playback
- [x] interactive prototype code removed from V1 client
- [x] native Kodi player UI only
- [x] `LICENSE.txt` included
- [x] icon and fanart declared in `addon.xml`
- [x] English and French localisation
- [x] API/network errors presented to users are localised
- [x] add-on state stored in its own Kodi profile directory
- [x] XML validation
- [x] Python syntax compilation
- [x] no compiled Python files included
- [x] no analytics
- [x] no direct Kodi database access
- [x] no forced skin view
- [x] session re-login logic on HTTP 401/403
- [x] dynamic Now Playing tested in Kodi, web UI and Kore

## Before the V1 public submission

- [ ] choose the public maintainer/provider name for `addon.xml`
- [ ] create the public source repository and add its URL to `<source>`
- [ ] decide whether to expose a public maintainer email
- [ ] confirm branding/logo/API expectations with JazzRadio
- [ ] ask JazzRadio whether higher-resolution TV/desktop channel artwork exists
- [ ] add final screenshots to addon metadata if desired
- [ ] run the official Kodi addon-checker against the final source tree
- [ ] perform one final clean-install test from the release ZIP
- [ ] submit to the appropriate official Kodi repository branch

## Deferred to V2

- [ ] per-track progress bar
- [ ] live application of a changed stream-quality setting
- [ ] optional interactive controls, only if justified by actual user demand
- [ ] sleep timer
- [ ] graceful recovery testing after temporary network loss
