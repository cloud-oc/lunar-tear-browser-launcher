# Lunar Tear 浏览器启动器

**[项目网站](https://cloud-oc.github.io/lunar-tear-browser-launcher/?lang=zh-CN) · [下载工程](https://github.com/cloud-oc/lunar-tear-browser-launcher/archive/refs/heads/main.zip)**

[English](README.md) · **简体中文** · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

在 Windows 浏览器中操作本机安卓游戏。启动器连接 **Lunar Tear 私服、安卓模拟器和 scrcpy 串流**。

## 准备

- Windows 10/11、[Python 3.10+](https://www.python.org/downloads/windows/)、Chrome 或 Edge。
- 开启 ADB 的安卓模拟器；已测试 **MuMu Android 15**，其他兼容模拟器尚未验证。
- 自备**连接 Lunar Tear 的国际版 3.7.1 修改版 APK**、Android 资源和处理后的 Master Data。[准备指南 →](docs/guide.zh-CN.md)

## 首次配置

1. 下载解压工程，双击 **`setup.cmd`**。
2. 编辑 **`config.json`**，填写 ADB 路径、模拟器连接地址和服务端目录。
3. 在工程目录打开终端，运行：

   ```powershell
   .\.venv\Scripts\python.exe launcher.py fetch-tools
   .\.venv\Scripts\python.exe launcher.py init-db
   ```

4. 按[详细指南](docs/guide.zh-CN.md)放好游戏文件，运行 **`doctor.cmd`** 检查。

## 开始游玩

双击 **`start.cmd` →「連接畫面」→「啟動遊戲」**。结束后运行 **`stop.cmd`**。

**实验性项目：**已验证串流和服务连接，完整流程及游戏中文支持尚未验证。仓库不含游戏文件或存档。项目网站提供介绍与下载，不能直接在线运行游戏。

[详细配置与排错](docs/guide.zh-CN.md) · [上游 Lunar Tear](https://github.com/Walter-Sparrow/lunar-tear) · [许可证](THIRD_PARTY.md)
