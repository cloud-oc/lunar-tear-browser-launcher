# 配置与兼容性

[快速开始](../README.zh-CN.md) · [English](guide.en.md)

## 支持的主机

启动器已实现 Windows x64、macOS x64/Apple Silicon、Linux x64/ARM64 的代码适配。`fetch-tools` 自动选择 Lunar Tear v1.0.2 对应系统／CPU 的发行包，并校验固定 SHA-256。上游没有对应的 Windows ARM64 固定包，不支持的架构会明确报错。

这里的“支持”指代码适配，不是完整游玩认证。此次扩展未进行各平台或其他模拟器实机测试。

安装 Python 3.10+、[Android platform-tools](https://developer.android.com/tools/releases/platform-tools)，使用支持 WebCodecs 的 Chrome/Edge。Linux 可能需要另外安装 Python venv 包。macOS 如出现下载程序的系统授权提示，请自行处理；启动器不会关闭系统安全保护或删除隔离标记。

| 操作 | Windows PowerShell | macOS / Linux 终端 |
|---|---|---|
| 初始化 | `.\setup.cmd` | `sh setup.sh` |
| 执行命令 | `.\launch.cmd 命令` | `sh launch.sh 命令` |
| 启动／停止 | `.\start.cmd` / `.\stop.cmd` | `sh start.sh` / `sh stop.sh` |
| 检查 | `.\doctor.cmd` | `sh doctor.sh` |

macOS 另有 `setup.command`、`start.command` 双击入口；若 ZIP 未保留执行权限，使用 `sh` 命令即可。指定 Python：Unix 使用 `PYTHON=/path/to/python3 sh setup.sh`；Windows 使用 `setup.ps1 -Python "C:\Path\python.exe"`。

## 不绑定模拟器品牌

启动安卓环境，开启 ADB／调试，并自行确认调试授权。用 `launch.cmd devices` 或 `sh launch.sh devices` 查看设备。

| 安卓环境 | 接入方式 |
|---|---|
| Android Studio Emulator / AVD | 使用 `emulator-5554` 一类编号或 `auto`；可配置 SDK emulator 的 `-avd` 启动命令 |
| MuMu | 使用该实例真实 ADB 地址／编号；可选 MuMuManager 启动命令。旧配置的 `emulator_manager` / `emulator_index` 仍兼容 |
| BlueStacks、雷电、夜神 | 开启产品的 ADB／调试功能，配置实际的 ADB 程序与设备编号／TCP 地址 |
| Genymotion | 使用其配置的 ADB 安装及 `adb devices` 显示的设备 |
| Waydroid / Android-x86 | 使用运行中安卓环境可访问的 ADB TCP 地址 |
| 安卓真机 | USB 调试编号，或已配置好的 TCP 调试地址 |

以上是接入方式，不代表每个品牌、版本都能运行游戏，各品牌也并非在所有系统都有版本。安卓环境仍须支持游戏 ARM64 原生库（原生支持或兼容转译）、`adb reverse`、可用 H.264 编码器和 scrcpy 输入控制。纯 x86 且没有兼容 ARM 转译的镜像不能运行游戏。之前使用的是 Android 15，不要默认最新镜像一定可用。声音取决于安卓版本和设备支持；可设 `audio: false` 仅串流画面（[scrcpy 声音说明](https://github.com/Genymobile/scrcpy/blob/v3.3.4/doc/audio.md)）。

## 配置文件

初始化会生成 `config.json`，不会覆盖已有配置。相对路径基于配置文件所在目录；工具路径支持 `~`，裸命令名称从 PATH 查找。

| 字段 | 说明 |
|---|---|
| `adb` | 默认 `auto`，查找 PATH、ANDROID_HOME/ANDROID_SDK_ROOT、常见 SDK 路径；也可填完整路径 |
| `serial` | 默认 `auto`，只自动选择唯一设备。支持 `emulator-5554`、USB 编号、`host:port`、`[IPv6]:port`；多设备必须明确指定 |
| `emulator_start` | 可选参数数组，例如 `["emulator", "-avd", "LunarTear"]`；空数组表示自行启动。不经过 shell 展开 |
| `boot_timeout` | 等待安卓开机的秒数，默认 180 |
| `server_dir` | 默认 `tools/lunar-tear-server` |
| `scrcpy_server` | 固定版本 scrcpy 文件，由 fetch-tools 下载 |
| `patched_apk` | 已修改并签名的国际版 3.7.1 APK |
| `asset_archive` / `asset_sha1` | 可选本地 Android .7z 和预期 SHA-1 |
| `seven_zip` | 默认 `auto`；可填 `7zz`、`7z` 或完整路径 |
| `audio` | true／false |

可把一个完整的[配置示例](../examples/)复制到工程根目录，命名为 `config.json`，再修改路径和编号。示例地址不是所有模拟器的固定地址。默认通用配置没有 MuMu 依赖。远程 ADB 只应连接你自己的可信设备；网页和游戏服务仍只监听本机，通过 ADB reverse 供 USB／TCP 设备访问。

## 游戏准备

使用对应平台的命令入口执行 `fetch-tools`、`init-db`。工具从官方发行页下载并校验；数据库只新建，不覆盖或升级旧存档。

使用[上游指南](https://github.com/Walter-Sparrow/lunar-tear)和[修改脚本](https://gitlab.com/walter-sparrow-group/lunar-scripts)处理 APK 与 Master Data。本工程不提供、修改或签名游戏文件，原版 APK 无法直接连接私服。

| 客户端用途 | 默认目标 |
|---|---|
| gRPC | `127.0.0.1:18003` |
| CDN / HTTP | `127.0.0.1:18080` |
| Auth | `127.0.0.1:13000` |

地址必须与配置中的 `ports` 一致。资源布局：

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

也支持 `revisions/0/android/`，保留其他 revisions。配置本地 .7z 与 7-Zip 后执行 `import-assets`；已有 `assets/revisions/` 不会被覆盖。中断后需自行检查部分解压数据。网页就绪状态仅检查布局，不代表全部资源完整。

启动安卓环境、填写 `patched_apk` 后执行 `install-apk`。如果原应用签名不同，覆盖安装可能失败；启动器不会自动卸载应用或删除数据。

## 日常使用与升级

先执行 `doctor`，处理缺失文件和设备提示，再执行 `start`，在浏览器点击「連接畫面」和「啟動遊戲」。退出游戏后执行 `stop`，仅停止本配置记录的服务，不关闭模拟器。未知来源的同端口服务会被拒绝复用。

从初版升级前，先停止旧版服务。手动启动或旧版未记录的服务可能需手动关闭。日志、备份保存在 `runtime/`；不同名称的配置使用不同子目录。存档为 `<server_dir>/db/game.db`，每次新启动服务前自动备份，但不会自动清理备份。恢复前先停服。

画质字段：`video.max_size`、`video.max_fps`、`video.bit_rate`。指定其他配置：`sh launch.sh --config config.other.local.json start` 或 `.\launch.cmd --config config.other.local.json start`。

卡在加载页时检查资源、Master Data 和 APK 地址；设备离线／未授权时先解决 ADB；声音异常可暂设 `audio: false`。ADB 接通不代表游戏 ABI 兼容。网页语言不改变游戏文本。此工程不是公网多人服务。

## 验证范围

此次只做离线单元检查，没有实际安装 macOS/Linux 环境、启动其他模拟器或进入游戏。`ci/windows-tests.yml` 已包含三个系统的可选测试矩阵，但未启用云端工作流。离线测试验证平台选择、归档安全和模拟设备选择，不认证实际游戏兼容性。
