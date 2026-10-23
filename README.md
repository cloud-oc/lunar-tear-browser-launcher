# Lunar Tear Browser Launcher

**[Website](https://cloud-oc.github.io/lunar-tear-browser-launcher/) · [Download](https://github.com/cloud-oc/lunar-tear-browser-launcher/archive/refs/heads/main.zip)**

**English** · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

Play through your local browser. The game runs in an Android emulator; this launcher connects **Lunar Tear + Android + scrcpy** on your Windows PC.

## Before you start

- Windows 10/11, [Python 3.10+](https://www.python.org/downloads/windows/), Chrome or Edge.
- An ADB-enabled Android emulator. **MuMu Android 15 is tested**; other compatible emulators are untested.
- Your own **global 3.7.1 APK patched for Lunar Tear**, Android assets and patched Master Data. [Preparation guide →](docs/guide.en.md)

## First setup

1. Download and extract this project. Run **`setup.cmd`**.
2. Edit **`config.json`**: set your ADB path, emulator connection and server folder.
3. Open a terminal in the project folder and run:

   ```powershell
   .\.venv\Scripts\python.exe launcher.py fetch-tools
   .\.venv\Scripts\python.exe launcher.py init-db
   ```

4. Prepare your game files using the [guide](docs/guide.en.md), then run **`doctor.cmd`**.

## Play

Double-click **`start.cmd` → Connect screen → Launch game**. The local controls are currently labeled **「連接畫面」→「啟動遊戲」**. Use **`stop.cmd`** when finished.

**Experimental:** streaming and server connectivity are verified; a full playthrough is not. Game-language availability is not guaranteed. Game files and saves are not included. The public website is a project page, not a hosted game.

[Detailed setup & troubleshooting](docs/guide.en.md) · [Upstream Lunar Tear](https://github.com/Walter-Sparrow/lunar-tear) · [Licenses](THIRD_PARTY.md)
