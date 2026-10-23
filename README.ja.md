# Lunar Tear Browser Launcher

[Website](https://cloud-oc.github.io/lunar-tear-browser-launcher/?lang=ja) · [Download ZIP](https://github.com/cloud-oc/lunar-tear-browser-launcher/archive/refs/heads/main.zip)

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md)

Windows・macOS・Linux で **Lunar Tear、Android エミュレーター／端末、ブラウザー**を接続します。MuMu は必須ではありません。

Python 3.10 以降、Chrome/Edge、ADB（Android platform-tools）。変更済みグローバル版 3.7.1 APK、Android アセット、処理済み Master Data は別途必要です。

1. 展開したプロジェクトを用意し、Android エミュレーター／端末を起動して ADB を有効にします。
2. Setup を実行し、必要に応じて `config.json` を編集。`adb: "auto"` は ADB を検索、`serial: "auto"` は唯一の接続端末を選択します。複数の場合は Devices で ID を確認して指定してください。
3. Tools と Database を実行し、詳細ガイドに従ってゲームファイルを配置します。
4. Check、Play の順に実行し、ブラウザーで **「連接畫面」（画面に接続）→「啟動遊戲」（ゲーム起動）**を選択します。

| Task | Windows (PowerShell) | macOS / Linux (Terminal) |
|---|---|---|
| Setup | `.\setup.cmd` | `sh setup.sh` |
| Devices | `.\launch.cmd devices` | `sh launch.sh devices` |
| Tools | `.\launch.cmd fetch-tools` | `sh launch.sh fetch-tools` |
| Database | `.\launch.cmd init-db` | `sh launch.sh init-db` |
| Check | `.\doctor.cmd` | `sh doctor.sh` |
| Play | `.\start.cmd` | `sh start.sh` |
| Stop | `.\stop.cmd` | `sh stop.sh` |

Windows x64、macOS/Linux x64・ARM64 の上流バイナリに対応。汎用 ADB はエミュレーター ID・TCP・USB を扱います。Android 環境にはゲームの ARM64 ライブラリ、ADB reverse、scrcpy の互換性が必要です。

**Experimental:** 追加した OS／エミュレーターの組み合わせは実機未検証です。ゲームや翻訳パッチは含まれず、全編の動作も保証しません。GitHub Pages は案内とダウンロード用です。

[Detailed guide / 详细指南](docs/guide.en.md) · [Lunar Tear upstream](https://github.com/Walter-Sparrow/lunar-tear) · [Licenses](THIRD_PARTY.md)
