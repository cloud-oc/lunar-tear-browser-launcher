# Lunar Tear 浏览器启动器

[Website](https://cloud-oc.github.io/lunar-tear-browser-launcher/?lang=zh-CN) · [Download ZIP](https://github.com/cloud-oc/lunar-tear-browser-launcher/archive/refs/heads/main.zip)

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

在 Windows、macOS 或 Linux 上连接 **Lunar Tear、安卓模拟器／设备和浏览器**。不强制使用 MuMu。

Python 3.10+、Chrome/Edge、ADB（Android platform-tools），以及自备的国际版 3.7.1 修改版 APK、Android 资源和处理后的 Master Data。

1. 解压工程，启动安卓模拟器／设备并开启 ADB。
2. 执行 Setup，按需编辑 `config.json`。`adb: "auto"` 自动查找 ADB；`serial: "auto"` 选择唯一设备。多设备时用 Devices 查看并填写准确编号。
3. 执行 Tools 和 Database，再按详细指南准备游戏文件。
4. 执行 Check，再执行 Play，在浏览器点击 **「連接畫面」→「啟動遊戲」**。

| Task | Windows (PowerShell) | macOS / Linux (Terminal) |
|---|---|---|
| Setup | `.\setup.cmd` | `sh setup.sh` |
| Devices | `.\launch.cmd devices` | `sh launch.sh devices` |
| Tools | `.\launch.cmd fetch-tools` | `sh launch.sh fetch-tools` |
| Database | `.\launch.cmd init-db` | `sh launch.sh init-db` |
| Check | `.\doctor.cmd` | `sh doctor.sh` |
| Play | `.\start.cmd` | `sh start.sh` |
| Stop | `.\stop.cmd` | `sh stop.sh` |

支持 Windows x64、macOS/Linux x64 与 ARM64，对应上游预编译包。通用 ADB 接受模拟器编号、TCP 和 USB 设备；安卓环境仍须能运行游戏的 ARM64 库，并支持 ADB reverse 与 scrcpy。

**Experimental:** 新增平台／模拟器组合未实测。不含游戏文件或汉化补丁，也不保证完整流程可玩。GitHub Pages 仅提供说明与下载。

[Detailed guide / 详细指南](docs/guide.zh-CN.md) · [Lunar Tear upstream](https://github.com/Walter-Sparrow/lunar-tear) · [Licenses](THIRD_PARTY.md)
