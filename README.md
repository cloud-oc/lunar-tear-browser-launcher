# Lunar Tear Browser Launcher

Windows 上的本机浏览器启动器：用一个 `config.json` 管理 **MuMu Android 模拟器 + Lunar Tear 私服 + scrcpy 浏览器串流**。

首次准备完成后，双击 **`start.cmd` →「連接畫面」→「啟動遊戲」**。Chrome 显示画面、播放声音，并把鼠标点击和拖动传回游戏。游戏仍在本机安卓模拟器运行，不是 WebAssembly 移植版，也不是云游戏托管服务。

**状态：实验性工具。已在 Windows / MuMu Android 15 / 国际版 3.7.1 上验证标题画面、鼠标控制和本机服务请求。完整剧情与战斗尚未完成验证。控制页面是繁体中文，不代表游戏客户端包含繁体中文剧情。**

```mermaid
flowchart LR
    A[Chrome / Edge] <-->|WebSocket: H.264 + PCM + 输入| B[Python 浏览器桥接]
    B <-->|ADB + scrcpy| C[MuMu: Android 游戏]
    C <-->|ADB reverse: 127.0.0.1| D[Lunar Tear: gRPC / CDN / Auth]
    D <--> E[本地资源与 SQLite 存档]
```

## 需要准备什么

- Windows 10/11 x64；Python **3.10+**（推荐 3.12，[官网下载](https://www.python.org/downloads/windows/)）。
- 已安装 MuMu，创建 **Android 15** 实例并开启 ADB；其他模拟器未验证。可把 `emulator_manager` 设为空字符串，自行启动兼容的本机模拟器。
- Chrome 或 Edge，支持 WebCodecs；网页通过 `http://127.0.0.1` 打开。
- 自行准备国际版 3.7.1 客户端、对应 Android 资源和已按上游指南处理的 Master Data；解压资源时需要 [7-Zip](https://www.7-zip.org/)。
- 足够的磁盘空间容纳资源压缩包、解压后的资源和模拟器内部游戏数据；本机使用的资源包约 15 GB，完整环境需要更多空间。

仓库不包含 APK、游戏资源、Master Data、个人存档或签名密钥。不要把这些文件提交到 GitHub。

## 第一次使用

### 1. 初始化环境

下载此仓库，双击 `setup.cmd`。它仅创建项目内 `.venv`、安装 Python 依赖、复制配置模板，不修改系统 Python。随后编辑生成的 `config.json`。

已有可用私服时，通常只需要修改：

```json
{
  "adb": "D:/MuMuPlayer/nx_main/adb.exe",
  "emulator_manager": "D:/MuMuPlayer/nx_main/MuMuManager.exe",
  "serial": "127.0.0.1:16384",
  "server_dir": "D:/Games/LunarTear/server"
}
```

这是需要修改的字段示例，**不要用这段替换整个配置文件**。保留模板的其他字段。路径可以包含空格；相对路径以配置文件所在文件夹为基准。MuMu 的 ADB 端口随实例而变，请以你的实例设置为准。

已有指定 Python，可用：

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1 -Python "C:\Path\To\python.exe"
```

### 2. 准备开源工具与新服务端

在工程目录打开终端：

```powershell
.\.venv\Scripts\python.exe launcher.py fetch-tools
.\.venv\Scripts\python.exe launcher.py init-db
```

`fetch-tools` 从官方 GitHub Release 下载 **Lunar Tear v1.0.2 Windows amd64** 与 **scrcpy-server v3.3.4**，检查固定 SHA-256。已有服务端目录会被保留；请自行确认它是兼容版本。`init-db` 只创建新库，已有 `db/game.db` 不会被覆盖或升级。

### 3. 准备游戏资源与客户端（只需一次）

遵循 [Lunar Tear 项目指南](https://github.com/Walter-Sparrow/lunar-tear) 和 [lunar-scripts](https://gitlab.com/walter-sparrow-group/lunar-scripts)。本项目不从第三方站点下载游戏文件，也不自动修改或签名 APK。**未修改的官方 APK 不能直接连接本机私服。**

将处理后的 Master Data `*.bin.e` 放入 `<server_dir>/assets/release/`。Android 资源支持两种目录：

```text
server_dir/
  bin/dev.exe
  db/game.db
  assets/
    release/*.bin.e
    revisions/0/
      list.bin
      assetbundle/...
      resources/...
```

或将 `list.bin`、`assetbundle`、`resources` 放在 `revisions/0/android/` 下。保留归档的其他 revisions。

对于根目录为 `revisions/` 的本地 `.7z`，可填写 `asset_archive`、`seven_zip`，并建议填写来源公布的 `asset_sha1`，然后运行：

```powershell
.\.venv\Scripts\python.exe launcher.py import-assets
```

该命令检查归档路径、可选 SHA-1 和解压退出码；为保护已有数据，如果 `assets/revisions/` 已存在，会拒绝再次导入。中断后的部分目录需自行检查处理。网页的“资源就绪”只检查目录和目录文件存在，不等同于完整性校验。

修改 APK 时必须使用与配置一致的地址，默认：

| 客户端用途 | 默认目标 |
|---|---|
| 游戏 gRPC | `127.0.0.1:18003` |
| CDN / HTTP | `127.0.0.1:18080` |
| Auth | `127.0.0.1:13000` |

将已修改并签名的 APK 路径填入 `patched_apk`，在模拟器已启动并连接 ADB 的情况下运行：

```powershell
.\.venv\Scripts\python.exe launcher.py install-apk
```

安装使用 `adb install -r`。若已有不同签名的同包名应用，安装可能失败；工具不会自动卸载它，以免删除数据。游戏内协议、年龄确认等应由使用者自己完成。

### 4. 启动

双击 `doctor.cmd` 检查文件。解决 `FAIL`，准备完成后双击 `start.cmd`。启动器会：

1. 检查配置、端口占用及已有服务身份。
2. 启动指定 MuMu 实例，等待 Android 完成开机。
3. 设置三条 ADB reverse，将模拟器回环地址映射到 Windows 服务。
4. 为新启动的服务备份 SQLite 存档，并启动 gRPC / CDN / Auth。
5. 启动浏览器桥接，打开 `http://127.0.0.1:18765`。

点击「連接畫面」后，可直接用鼠标操作画面；声音需要浏览器用户手势开启。点击「斷開連接」后可以重新连接。串流每个桥接实例仅允许一个连接。

## 配置与维护

| 配置 | 说明 |
|---|---|
| `emulator_index` | MuMu 实例编号，默认 0 |
| `ports.web` | 浏览器入口端口，默认 18765 |
| `ports.stream` | scrcpy ADB 转发端口，默认 27183 |
| `ports.grpc/cdn/auth` | 必须与已修改客户端中的端口相同；修改后通常需要重新修改 APK |
| `video.max_size` | 画面最大边，默认 1280 |
| `video.max_fps` | 帧率上限，默认 30 |
| `video.bit_rate` | 视频码率，默认 5000000 |

`stop.cmd` 只停止本工程记录并核对过进程 ID、创建时间和程序路径的服务。它不会关闭 MuMu，也不会停止启动前已经运行的服务。退出游戏再停止服务，避免中断正在进行的请求。关闭网页会断开串流，但服务继续运行。

- 日志：`runtime/bridge.log`、`runtime/server.log`、`runtime/scrcpy.log`。
- 自动备份：`runtime/backups/`；当前游戏存档：`<server_dir>/db/game.db`。
- 备份不会自动清理；定期自行归档。手动恢复存档前先停服。
- CLI：`launcher.py --help`；指定其他配置：`launcher.py --config config.other.local.json start`。
- 仅绑定 `127.0.0.1`，检查 Host 与 WebSocket Origin。不提供公网访问、远程登录或多用户隔离，**不要反向代理到公网**。

## 常见问题

- **停在加载页面**：检查资源是否完整、Master Data 是否已处理、三个服务日志、APK 地址与端口是否一致。
- **标题正常但没中文**：浏览器 UI 的语言与游戏文本不同，本工程不提供汉化补丁，也未验证国际版 3.7.1 的繁体中文剧情支持。
- **端口占用**：启动器会拒绝未知程序占用的端口；先确认该程序用途。不要随意终止不认识的进程。
- **模拟器无响应**：确认 Android 15 实例启动、ADB 开启、`serial` 正确。浏览器不能代替安卓运行环境。
- **资源显示 WAIT 仍能连接画面**：串流可用于检查模拟器，但「啟動遊戲」会被禁用。
- **Python 版本太旧**：安装 3.10+，或用 `setup.ps1 -Python` 明确选择新版本。

## 开发与验证

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

测试覆盖配置路径与端口限制、新建数据库及保留已有存档、服务端网页的 Host/Origin 限制。`ci/windows-tests.yml` 是可选 GitHub Actions 模板，目前未启用；拥有工作流写入权限后，可将它复制到 `.github/workflows/test.yml`。这些测试不包含游戏文件，不执行完整游戏流程。

代码采用 MIT；`vendor/migrations` 来自 Lunar Tear v1.0.2，保留上游 MIT 许可。scrcpy 由使用者下载，采用 Apache-2.0。详见 [THIRD_PARTY.md](THIRD_PARTY.md)。本项目与游戏发行商及上述上游项目无隶属关系。
