# Lunar Tear Browser Launcher

**[プロジェクトサイト](https://cloud-oc.github.io/lunar-tear-browser-launcher/?lang=ja) · [ダウンロード](https://github.com/cloud-oc/lunar-tear-browser-launcher/archive/refs/heads/main.zip)**

[English](README.md) · [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md) · **日本語**

Windows のブラウザーから、同じ PC の Android ゲームを操作するツールです。**Lunar Tear サーバー・Android エミュレーター・scrcpy** を接続します。

## 必要なもの

- Windows 10/11、[Python 3.10 以降](https://www.python.org/downloads/windows/)、Chrome または Edge。
- ADB が有効な Android エミュレーター。**MuMu Android 15 で動作確認済み**。ほかの互換エミュレーターは未検証です。
- ご自身で用意した、**Lunar Tear 接続用に変更済みのグローバル版 3.7.1 APK**、Android アセット、処理済み Master Data。[準備ガイド（英語）→](docs/guide.en.md)

## 初回設定

1. プロジェクトをダウンロードして展開し、**`setup.cmd`** を実行。
2. **`config.json`** に ADB のパス、エミュレーターの接続先、サーバーフォルダーを設定。
3. プロジェクトフォルダーでターミナルを開き、次を実行：

   ```powershell
   .\.venv\Scripts\python.exe launcher.py fetch-tools
   .\.venv\Scripts\python.exe launcher.py init-db
   ```

4. [詳細ガイド（英語）](docs/guide.en.md)に従ってゲームファイルを配置し、**`doctor.cmd`** で確認。

## 起動

**`start.cmd` →「連接畫面」（画面に接続）→「啟動遊戲」（ゲーム起動）**。終了時は **`stop.cmd`** を実行します。

**実験的なプロジェクトです。** 映像配信とサーバー接続は確認済みですが、全編のプレイとゲーム内の対応言語は未検証です。ゲームファイルやセーブデータは含まれません。公開サイトは紹介・ダウンロード用で、ゲームを直接実行するものではありません。

[詳細ガイド（英語）](docs/guide.en.md) · [Lunar Tear 本体](https://github.com/Walter-Sparrow/lunar-tear) · [ライセンス](THIRD_PARTY.md)
