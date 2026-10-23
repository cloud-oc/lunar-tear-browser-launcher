# Lunar Tear 瀏覽器啟動器

[Website](https://cloud-oc.github.io/lunar-tear-browser-launcher/?lang=zh-TW) · [Download ZIP](https://github.com/cloud-oc/lunar-tear-browser-launcher/archive/refs/heads/main.zip)

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

在 Windows、macOS 或 Linux 上連接 **Lunar Tear、Android 模擬器／裝置與瀏覽器**。MuMu 並非必要。

Python 3.10+、Chrome/Edge、ADB（Android platform-tools），以及自備的國際版 3.7.1 修改版 APK、Android 資源與處理後的 Master Data。

1. 解壓縮專案，啟動 Android 模擬器／裝置並開啟 ADB。
2. 執行 Setup，依需要編輯 `config.json`。`adb: "auto"` 自動尋找 ADB；`serial: "auto"` 選擇唯一裝置。多裝置時用 Devices 查看並填入正確編號。
3. 執行 Tools 與 Database，再依詳細指南準備遊戲檔案。
4. 執行 Check，再執行 Play，在瀏覽器點選 **「連接畫面」→「啟動遊戲」**。

| Task | Windows (PowerShell) | macOS / Linux (Terminal) |
|---|---|---|
| Setup | `.\setup.cmd` | `sh setup.sh` |
| Devices | `.\launch.cmd devices` | `sh launch.sh devices` |
| Tools | `.\launch.cmd fetch-tools` | `sh launch.sh fetch-tools` |
| Database | `.\launch.cmd init-db` | `sh launch.sh init-db` |
| Check | `.\doctor.cmd` | `sh doctor.sh` |
| Play | `.\start.cmd` | `sh start.sh` |
| Stop | `.\stop.cmd` | `sh stop.sh` |

支援 Windows x64、macOS/Linux x64 與 ARM64，對應上游預編譯套件。通用 ADB 接受模擬器編號、TCP 與 USB 裝置；Android 環境仍須能執行遊戲的 ARM64 程式庫，並支援 ADB reverse 與 scrcpy。

**Experimental:** 新增平台／模擬器組合尚未實測。不含遊戲檔案或翻譯修補檔，也不保證完整流程可玩。GitHub Pages 僅提供說明與下載。

[Detailed guide / 详细指南](docs/guide.en.md) · [Lunar Tear upstream](https://github.com/Walter-Sparrow/lunar-tear) · [Licenses](THIRD_PARTY.md)
