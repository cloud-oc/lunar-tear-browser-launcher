# Lunar Tear Browser Launcher

[Website](https://cloud-oc.github.io/lunar-tear-browser-launcher/?lang=en) · [Download ZIP](https://github.com/cloud-oc/lunar-tear-browser-launcher/archive/refs/heads/main.zip)

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

Connect **Lunar Tear + an Android emulator/device + your browser** on Windows, macOS or Linux. MuMu is optional.

Python 3.10+, Chrome/Edge, ADB (Android platform-tools), and your own patched global 3.7.1 APK, Android assets and patched Master Data.

1. Extract this project. Start your Android emulator/device and enable ADB.
2. Run Setup. Edit `config.json` if needed: `adb: "auto"` finds ADB; `serial: "auto"` selects the only connected device. With multiple devices, use Devices below and set the exact ID.
3. Run Tools and Database below; prepare game files using the detailed guide.
4. Run Check, then Play. In the browser choose **「連接畫面」(Connect screen) →「啟動遊戲」(Launch game)**.

| Task | Windows (PowerShell) | macOS / Linux (Terminal) |
|---|---|---|
| Setup | `.\setup.cmd` | `sh setup.sh` |
| Devices | `.\launch.cmd devices` | `sh launch.sh devices` |
| Tools | `.\launch.cmd fetch-tools` | `sh launch.sh fetch-tools` |
| Database | `.\launch.cmd init-db` | `sh launch.sh init-db` |
| Check | `.\doctor.cmd` | `sh doctor.sh` |
| Play | `.\start.cmd` | `sh start.sh` |
| Stop | `.\stop.cmd` | `sh stop.sh` |

Windows x64; macOS/Linux x64 and ARM64, matching upstream binaries. Generic ADB accepts emulator IDs, TCP and USB devices. Android must support the game’s ARM64 libraries, ADB reverse and scrcpy.

**Experimental:** The additional platform/emulator combinations have not been tested. No game files or translation patches are included; full gameplay is not guaranteed. GitHub Pages hosts project information only.

[Detailed guide / 详细指南](docs/guide.en.md) · [Lunar Tear upstream](https://github.com/Walter-Sparrow/lunar-tear) · [Licenses](THIRD_PARTY.md)
