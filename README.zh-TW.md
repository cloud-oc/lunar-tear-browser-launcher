# Lunar Tear 瀏覽器啟動器

**[專案網站](https://cloud-oc.github.io/lunar-tear-browser-launcher/?lang=zh-TW) · [下載專案](https://github.com/cloud-oc/lunar-tear-browser-launcher/archive/refs/heads/main.zip)**

[English](README.md) · [简体中文](README.zh-CN.md) · **繁體中文** · [日本語](README.ja.md)

透過 Windows 瀏覽器操作本機 Android 遊戲。啟動器連接 **Lunar Tear 私服、Android 模擬器與 scrcpy 串流**。

## 準備

- Windows 10/11、[Python 3.10+](https://www.python.org/downloads/windows/)、Chrome 或 Edge。
- 已開啟 ADB 的 Android 模擬器；已測試 **MuMu Android 15**，其他相容模擬器尚未驗證。
- 自備**連接 Lunar Tear 的國際版 3.7.1 修改版 APK**、Android 資源及處理後的 Master Data。[準備指南（英文）→](docs/guide.en.md)

## 首次設定

1. 下載並解壓縮專案，執行 **`setup.cmd`**。
2. 編輯 **`config.json`**，填入 ADB 路徑、模擬器連線位址及伺服器目錄。
3. 在專案目錄開啟終端機，執行：

   ```powershell
   .\.venv\Scripts\python.exe launcher.py fetch-tools
   .\.venv\Scripts\python.exe launcher.py init-db
   ```

4. 依[詳細指南（英文）](docs/guide.en.md)放妥遊戲檔案，再執行 **`doctor.cmd`** 檢查。

## 開始遊玩

按兩下 **`start.cmd` →「連接畫面」→「啟動遊戲」**。結束後執行 **`stop.cmd`**。

**實驗性專案：**已驗證串流與伺服器連線，完整流程及繁體中文內容尚未驗證。儲存庫不含遊戲檔案或存檔。專案網站提供介紹與下載，無法直接在線上執行遊戲。

[詳細指南（英文）](docs/guide.en.md) · [上游 Lunar Tear](https://github.com/Walter-Sparrow/lunar-tear) · [授權資訊](THIRD_PARTY.md)
