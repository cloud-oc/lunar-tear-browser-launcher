# Setup and compatibility

[Quick start](../README.md) · [简体中文](guide.zh-CN.md)

## Host platforms

The launcher implements Windows x64, macOS x64/Apple Silicon, and Linux x64/ARM64. `fetch-tools` selects the pinned Lunar Tear v1.0.2 release for the OS/CPU and verifies SHA-256. No upstream Windows ARM64 binary is pinned; unsupported architectures fail with a clear error. This is implementation support, not an end-to-end certification: the expanded platform/emulator matrix has not been tested.

Install Python 3.10+ and [Android SDK platform-tools](https://developer.android.com/tools/releases/platform-tools). Use Chrome/Edge with WebCodecs. Linux may require a separate Python venv package. On macOS, handle any system approval for downloaded tools yourself; the launcher does not remove quarantine or change system security settings.

| Operation | Windows PowerShell | macOS / Linux terminal |
|---|---|---|
| Setup | `.\setup.cmd` | `sh setup.sh` |
| Run a command | `.\launch.cmd COMMAND` | `sh launch.sh COMMAND` |
| Start / stop | `.\start.cmd` / `.\stop.cmd` | `sh start.sh` / `sh stop.sh` |
| Check | `.\doctor.cmd` | `sh doctor.sh` |

On macOS, `setup.command` and `start.command` are optional double-click wrappers; `sh` works even if a downloaded ZIP did not preserve executable permissions. To choose Python: `PYTHON=/path/to/python3 sh setup.sh` (Unix), or `setup.ps1 -Python "C:\Path\python.exe"` (Windows).

## Any compatible ADB environment

Start your Android environment, enable debugging and authorize the connection when prompted. Run `launch.cmd devices` or `sh launch.sh devices`. The launcher uses standard ADB commands, not vendor-specific streaming APIs.

| Environment | Connection/configuration |
|---|---|
| Android Studio Emulator / AVD | Use an ID such as `emulator-5554`, or `auto`; optional `emulator_start` can run the SDK emulator with `-avd YOUR_AVD` |
| MuMu | Its local ADB address or discovered ID; optional MuMuManager command. Older `emulator_manager` / `emulator_index` configurations remain accepted |
| BlueStacks, LDPlayer, Nox | Enable that product's ADB/debugging feature; use its actual ADB executable and device ID/TCP endpoint |
| Genymotion | Use its configured ADB installation and the ID/address reported by `adb devices` |
| Waydroid / Android-x86 | Use a reachable ADB TCP endpoint from the running Android environment |
| Physical Android device | USB debugging and the serial from `adb devices`, or a previously configured TCP debugging endpoint |

These are integration routes, not claims that every product/version runs this game. Emulator availability varies by host OS. The Android environment must support the game's ARM64 native libraries (natively or via compatible translation), `adb reverse`, a usable H.264 encoder and scrcpy input control. An x86-only Android image without compatible ARM translation will not run the game. Android 15 is the previously used environment; do not assume any newer image works. Audio capture requires a compatible Android version/device; set `audio` to `false` for video-only streaming ([scrcpy audio documentation](https://github.com/Genymobile/scrcpy/blob/v3.3.4/doc/audio.md)).

## Configuration

`setup` creates `config.json` without overwriting an existing configuration. Relative paths resolve from its directory. `~` is expanded for tool paths. Bare tool names are resolved through PATH.

| Field | Meaning |
|---|---|
| `adb` | `auto`: search PATH, ANDROID_HOME/ANDROID_SDK_ROOT and common SDK locations; or set an explicit path |
| `serial` | `auto`: select exactly one connected device. Or specify `emulator-5554`, a USB serial, `host:port` or `[IPv6]:port`. Multiple devices require explicit selection |
| `emulator_start` | Optional argument array, e.g. `["emulator", "-avd", "LunarTear"]`; `[]` means start Android yourself. No shell interpolation |
| `boot_timeout` | Seconds to wait for Android boot, default 180 |
| `server_dir` | Local server folder; default `tools/lunar-tear-server` |
| `scrcpy_server` | Pinned scrcpy server file, downloaded by `fetch-tools` |
| `patched_apk` | Your modified and signed global 3.7.1 APK |
| `asset_archive` / `asset_sha1` | Optional Android .7z and expected SHA-1 |
| `seven_zip` | `auto`, a PATH command (`7zz`/`7z`) or explicit executable path |
| `audio` | true / false |

Copy one complete [example config](../examples/) into the project root as `config.json`, then edit paths/IDs. Do not run example device addresses blindly. The default generic config does not require a particular emulator. Configure remote ADB only for your own trusted device; the web bridge and game services still bind to localhost. USB/TCP devices access them through ADB reverse.

## Prepare the server and game

Run `fetch-tools`, then `init-db` using your platform's command wrapper. Server binaries and scrcpy are downloaded from official releases with pinned hashes. `init-db` only creates a new database; existing saves are preserved, not migrated.

Use the [upstream guide](https://github.com/Walter-Sparrow/lunar-tear) and [patching scripts](https://gitlab.com/walter-sparrow-group/lunar-scripts) for your APK and Master Data. The launcher does not supply, patch or sign game files. An official unmodified APK cannot connect to this private server.

| Client service | Default target |
|---|---|
| gRPC | `127.0.0.1:18003` |
| CDN / HTTP | `127.0.0.1:18080` |
| Auth | `127.0.0.1:13000` |

These must match `ports` in your config. Put prepared files in:

```text
<server_dir>/
  bin/dev[.exe]
  db/game.db
  assets/
    release/*.bin.e
    revisions/0/
      list.bin
      assetbundle/...
      resources/...
```

`revisions/0/android/` is also accepted. Retain any other revisions. With `asset_archive` and 7-Zip configured, run `import-assets`. Existing `assets/revisions/` is never overwritten. An interrupted extraction needs manual inspection; the browser's readiness indicator checks layout, not full asset integrity. Start Android and run `install-apk` after setting `patched_apk`. Different app signing keys may prevent an upgrade; this tool never uninstalls existing game data.

## Operation

Run `doctor`, resolve missing files and device warnings, then `start`. Use the local browser controls 「連接畫面」and「啟動遊戲」. Stop with `stop` after leaving the game. Only processes recorded by this configuration are stopped; the emulator is left running. Unknown pre-existing servers on the same ports are rejected rather than adopted. When upgrading from the initial launcher, stop its services first; manually started services may need manual shutdown.

Logs and backups are under `runtime/` (separate subdirectories for named configs). Saves: `<server_dir>/db/game.db`. Automatic SQLite backups precede a newly started server; backups are not pruned. Stop before restoring. The bridge accepts one viewer and is not intended for public hosting.

Use `video.max_size`, `video.max_fps`, `video.bit_rate` to tune video. For a custom config: `sh launch.sh --config config.other.local.json start` or `.\launch.cmd --config config.other.local.json start`.

If loading stalls, check assets, Master Data and client endpoints. If Android is offline/unauthorized, resolve ADB first. `audio: false` can isolate audio-capture incompatibilities. A working ADB connection does not prove game ABI compatibility. Game languages depend on the client, not the website language.

## Verification scope

Only offline unit checks are used for this expansion. No macOS/Linux installation, alternate emulator or game session was run. `ci/windows-tests.yml` contains an optional three-OS test matrix, not an enabled workflow. Tests mock ADB and validate host selection, extraction safety and configuration; they do not certify gameplay.
