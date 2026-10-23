# Detailed setup

[Quick start](../README.md) · [简体中文](guide.zh-CN.md)

## Configuration

Run `setup.cmd` with Python 3.10+ installed. Edit the generated `config.json`; keep every field from the template. Relative paths resolve from the configuration file's directory.

| Field | What to enter |
|---|---|
| `adb` | Path to your emulator's `adb.exe` |
| `emulator_manager` | MuMu's `MuMuManager.exe`; set to `""` for another emulator and start it yourself |
| `emulator_index` | MuMu instance number, default `0` |
| `serial` | Local ADB address, e.g. `127.0.0.1:16384`; confirm your instance's actual port |
| `server_dir` | Prepared Lunar Tear v1.0.2 directory, or keep the default for a new installation |
| `scrcpy_server` | Keep the default; `fetch-tools` downloads it |
| `patched_apk` | Path to your patched and signed APK |
| `asset_archive` | Optional path to your Android `.7z` archive |
| `asset_sha1` | Expected archive SHA-1 from your source, recommended when importing |
| `seven_zip` | Path to `7z.exe`, needed for archive import |

MuMu is not mandatory. Alternatives must run the game's ARM64 libraries (directly or through compatible translation), support ADB reverse and run scrcpy. Only MuMu Android 15 has been tested. This launcher accepts local TCP ADB addresses, not USB device IDs.

## Tools and database

From a terminal in the project directory:

```powershell
.\.venv\Scripts\python.exe launcher.py fetch-tools
.\.venv\Scripts\python.exe launcher.py init-db
```

Official releases of Lunar Tear v1.0.2 and scrcpy v3.3.4 are checked against fixed SHA-256 hashes. Existing server folders and databases are preserved. Database upgrades are not performed.

## Game files

Use the [upstream guide](https://github.com/Walter-Sparrow/lunar-tear) and [patching scripts](https://gitlab.com/walter-sparrow-group/lunar-scripts) to prepare your global 3.7.1 APK and Master Data. This project does not download, patch or sign game files. An unmodified official APK will not connect to the local server.

The patched client must target addresses matching `config.json`:

| Service | Default address |
|---|---|
| gRPC | `127.0.0.1:18003` |
| CDN / HTTP | `127.0.0.1:18080` |
| Auth | `127.0.0.1:13000` |

Changing these ports requires matching client changes. `start.cmd` creates ADB reverse mappings automatically.

```text
<server_dir>/
  bin/dev.exe
  db/game.db
  assets/
    release/*.bin.e          # patched Master Data
    revisions/0/
      list.bin
      assetbundle/...
      resources/...
```

`list.bin`, `assetbundle/` and `resources/` may alternatively be inside `revisions/0/android/`. Retain any other revisions included in the archive.

For a local `.7z` whose root is `revisions/`, set `asset_archive`, `seven_zip` and preferably `asset_sha1`, then run:

```powershell
.\.venv\Scripts\python.exe launcher.py import-assets
```

Import checks paths, optional SHA-1 and the extraction result. It refuses to overwrite an existing `assets/revisions/`. Inspect partial data after an interrupted import. The website's resource indicator checks layout, not every file's completeness. Allow space for the archive, extracted files and emulator game data.

Start the emulator, fill in `patched_apk`, then install:

```powershell
.\.venv\Scripts\python.exe launcher.py install-apk
```

A different signing key can cause installation to fail. The launcher will not uninstall an existing app or delete its data. Complete in-game agreements and age prompts yourself.

## Daily use and troubleshooting

Run `doctor.cmd`, resolve `FAIL` items and prepare missing resources. Use `start.cmd`, then **「連接畫面」(Connect screen)** and **「啟動遊戲」(Launch game)**. Click and drag to interact. Audio requires a user gesture. Only one streaming connection is accepted per bridge instance.

`stop.cmd` stops only services started and recorded by this launcher. It leaves MuMu and pre-existing services running. Exit the game before stopping. Closing the web page disconnects streaming but leaves services running.

- Browser: `http://127.0.0.1:18765` by default.
- Logs: `runtime/bridge.log`, `runtime/server.log`, `runtime/scrcpy.log`.
- Save: `<server_dir>/db/game.db`. Backups before a new server start: `runtime/backups/`. Backups are not automatically pruned. Stop the server before restoring.
- Video: `video.max_size`, `video.max_fps`, `video.bit_rate`.
- Alternative config: `launcher.py --config config.other.local.json start`.

| Symptom | Check |
|---|---|
| Loading never finishes | Complete assets, patched Master Data, client endpoints, logs |
| No language option | Website language does not change game text; no translation patch is included |
| Port occupied | Identify the program; port changes may require patching the client again |
| Emulator unavailable | Android boot completed, ADB enabled, correct `serial` |
| Launch disabled | Missing resources or no active streaming connection |
| Python too old | Install 3.10+, or run `setup.ps1 -Python "C:\Path\To\python.exe"` |

The bridge is localhost-only and not designed for public hosting. GitHub Pages hosts project information only.

## Development

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

`ci/windows-tests.yml` is an optional Actions template, not an enabled workflow. Tests do not run a full game session. [Third-party notices](../THIRD_PARTY.md).
