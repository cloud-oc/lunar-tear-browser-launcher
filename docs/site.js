'use strict';
const translations = {
  "zh-CN": {
    "skip": "跳至正文",
    "navSetup": "使用指南",
    "language": "语言",
    "title": "在本机，\n重访牢笼。",
    "intro": "安卓游戏，在 Windows、macOS 或 Linux 上运行。用通用 ADB 连接 Lunar Tear、安卓模拟器或设备与浏览器，不绑定模拟器品牌。",
    "download": "下载启动器",
    "start": "阅读简明指南",
    "downloadNote": "工程 ZIP · Windows / macOS / Linux · 游戏文件自备",
    "diagramCaption": "本机运行，浏览器呈现。",
    "status": "实验性项目",
    "statusText": "已实现跨平台代码适配，新增系统／模拟器组合未实测。",
    "setupTitle": "开始之前。",
    "setupIntro": "首次准备好环境，以后从一个文件启动。",
    "system": "系统",
    "android": "安卓环境",
    "androidText": "开启 ADB、兼容游戏 ARM64 库的模拟器或设备。不限定品牌；新增组合未实测。",
    "gameFiles": "游戏文件",
    "gameFilesText": "连接私服的国际版 3.7.1 修改版 APK、Android 资源和处理后的 Master Data。工程不包含这些文件。",
    "fullGuide": "完整准备指南 ↗",
    "step1": "安装启动器环境",
    "step1Text": "解压工程，运行下方对应系统的初始化命令。Python 依赖安装在工程目录内。",
    "step2": "连接你的运行环境",
    "step2Text": "编辑 config.json，填写 ADB 路径、模拟器地址和服务端目录。然后在工程目录运行以下命令。",
    "copy": "复制命令",
    "copied": "已复制",
    "copyFailed": "复制失败，请手动选择命令复制。",
    "step3": "准备游戏文件",
    "step3Text": "按完整指南安装修改版 APK，放好资源与 Master Data，再运行下方检查命令。",
    "step4": "打开本机游戏窗口",
    "step4Text": "运行下方启动命令，点击「連接畫面」和「啟動遊戲」。结束后 Windows 用 stop.cmd，macOS/Linux 用 sh stop.sh。",
    "notesTitle": "还有几件事。",
    "faq1": "必须使用 MuMu 吗？",
    "faq1Text": "不必须。可通过 ADB 接入 Android Studio AVD、品牌模拟器或兼容安卓设备。emulator_start 为空表示手动启动，也可填启动参数数组；serial 支持 auto、模拟器编号、TCP 和 USB。仍需兼容游戏 ARM64 库、ADB reverse 与 scrcpy；新增组合未实测。",
    "faq2": "可以直接在这个网站游玩吗？",
    "faq2Text": "这个网站提供工程下载和说明。游戏运行在你电脑的安卓模拟器里，由本机浏览器页面显示和控制，不提供云端游戏服务。",
    "faq3": "切换语言会翻译游戏吗？",
    "faq3Text": "语言选项只切换本网站。游戏文本取决于客户端和资源。繁体中文剧情尚未验证，工程不包含汉化补丁。",
    "disclaimer": "非官方社区工具，与游戏发行商及上游项目无隶属关系。",
    "source": "源代码",
    "upstream": "上游 Lunar Tear",
    "licenses": "授权信息",
    "hostLabel": "选择系统"
  },
  "zh-TW": {
    "skip": "跳至主要內容",
    "navSetup": "使用指南",
    "language": "語言",
    "title": "在本機，\n重訪牢籠。",
    "intro": "Android 遊戲，在 Windows、macOS 或 Linux 上執行。透過通用 ADB 連接 Lunar Tear、Android 模擬器或裝置與瀏覽器，不限定模擬器品牌。",
    "download": "下載啟動器",
    "start": "閱讀簡明指南",
    "downloadNote": "專案 ZIP · Windows / macOS / Linux · 遊戲檔案自備",
    "diagramCaption": "本機執行，瀏覽器呈現。",
    "status": "實驗性專案",
    "statusText": "已實作跨平台程式碼，新增系統／模擬器組合尚未實測。",
    "setupTitle": "開始之前。",
    "setupIntro": "首次備妥環境，之後從一個檔案啟動。",
    "system": "系統",
    "android": "Android 環境",
    "androidText": "開啟 ADB、相容遊戲 ARM64 程式庫的模擬器或裝置。不限定品牌；新增組合未實測。",
    "gameFiles": "遊戲檔案",
    "gameFilesText": "連接私服的國際版 3.7.1 修改版 APK、Android 資源與處理後的 Master Data。專案不包含這些檔案。",
    "fullGuide": "完整準備指南（英文）↗",
    "step1": "安裝啟動器環境",
    "step1Text": "解壓縮專案，執行下方對應系統的初始化命令。Python 相依套件安裝在專案目錄內。",
    "step2": "連接你的執行環境",
    "step2Text": "編輯 config.json，填入 ADB 路徑、模擬器位址及伺服器目錄。接著在專案目錄執行以下命令。",
    "copy": "複製命令",
    "copied": "已複製",
    "copyFailed": "複製失敗，請手動選取命令複製。",
    "step3": "準備遊戲檔案",
    "step3Text": "依完整指南安裝修改版 APK，放妥資源與 Master Data，再執行下方檢查命令。",
    "step4": "開啟本機遊戲視窗",
    "step4Text": "執行下方啟動命令，點選「連接畫面」與「啟動遊戲」。結束後 Windows 用 stop.cmd，macOS/Linux 用 sh stop.sh。",
    "notesTitle": "還有幾件事。",
    "faq1": "一定要使用 MuMu 嗎？",
    "faq1Text": "不一定。可透過 ADB 接入 Android Studio AVD、品牌模擬器或相容 Android 裝置。emulator_start 為空表示手動啟動，也可填入啟動參數陣列；serial 支援 auto、模擬器編號、TCP 與 USB。仍需相容遊戲 ARM64 程式庫、ADB reverse 與 scrcpy；新增組合未實測。",
    "faq2": "可以直接在這個網站遊玩嗎？",
    "faq2Text": "這個網站提供專案下載及說明。遊戲在你電腦的 Android 模擬器中執行，由本機瀏覽器頁面顯示與控制，不提供雲端遊戲服務。",
    "faq3": "切換語言會翻譯遊戲嗎？",
    "faq3Text": "語言選項只切換本網站。遊戲文字取決於用戶端及資源。繁體中文劇情尚未驗證，專案不包含翻譯修補檔。",
    "disclaimer": "非官方社群工具，與遊戲發行商及上游專案無隸屬關係。",
    "source": "原始碼",
    "upstream": "上游 Lunar Tear",
    "licenses": "授權資訊",
    "hostLabel": "選擇系統"
  },
  "ja": {
    "skip": "本文へ移動",
    "navSetup": "使い方",
    "language": "言語",
    "title": "「檻」への、\n小さな窓。",
    "intro": "Android ゲームを Windows・macOS・Linux のブラウザーで。汎用 ADB で Lunar Tear とエミュレーターや端末を接続します。特定のブランドは不要です。",
    "download": "ランチャーをダウンロード",
    "start": "使い方を読む",
    "downloadNote": "ソース ZIP · Windows / macOS / Linux · ゲームは別途必要",
    "diagramCaption": "PC で実行。ブラウザーで操作。",
    "status": "実験的なプロジェクト",
    "statusText": "クロスプラットフォーム対応コードを実装。追加の OS／エミュレーターは実機未検証です。",
    "setupTitle": "始める前に。",
    "setupIntro": "最初に環境を準備すれば、次回からはファイルひとつで起動できます。",
    "system": "システム",
    "android": "Android 環境",
    "androidText": "ADB が有効でゲームの ARM64 ライブラリに対応するエミュレーターまたは端末。ブランド指定なし。追加の組み合わせは未検証です。",
    "gameFiles": "ゲームファイル",
    "gameFilesText": "接続先を変更したグローバル版 3.7.1 APK、Android アセット、処理済み Master Data。いずれも付属しません。",
    "fullGuide": "詳しい準備ガイド（英語）↗",
    "step1": "ランチャーを準備",
    "step1Text": "ZIP を展開し、下の OS 別セットアップコマンドを実行。Python の依存パッケージはプロジェクト内に配置されます。",
    "step2": "実行環境を接続",
    "step2Text": "config.json に ADB のパス、エミュレーターの接続先、サーバーフォルダーを設定。その後、プロジェクトフォルダーで次のコマンドを実行します。",
    "copy": "コピー",
    "copied": "コピーしました",
    "copyFailed": "コピーできませんでした。コマンドを選択して手動でコピーしてください。",
    "step3": "ゲームファイルを配置",
    "step3Text": "詳細ガイドに従って変更済み APK、アセット、Master Data を準備し、下の確認コマンドを実行します。",
    "step4": "ローカルのゲーム画面へ",
    "step4Text": "下の起動コマンドを実行し、「連接畫面」「啟動遊戲」を選択。終了時は Windows なら stop.cmd、macOS/Linux なら sh stop.sh を実行します。",
    "notesTitle": "知っておきたいこと。",
    "faq1": "MuMu は必須ですか？",
    "faq1Text": "必須ではありません。Android Studio AVD、他社エミュレーター、互換 Android 端末を ADB で接続できます。emulator_start を空にして手動起動するか、起動引数の配列を設定します。serial は auto・エミュレーター ID・TCP・USB に対応。ゲームの ARM64 ライブラリ、ADB reverse、scrcpy への対応が必要で、追加環境は未検証です。",
    "faq2": "このサイトで直接プレイできますか？",
    "faq2Text": "ここはダウンロードと説明のためのサイトです。ゲームは PC の Android エミュレーターで動作し、ローカルのブラウザーページで表示・操作します。クラウドゲームサービスではありません。",
    "faq3": "言語を変えるとゲームも翻訳されますか？",
    "faq3Text": "言語選択はこのサイトの表示だけを変更します。ゲーム内のテキストはクライアントとアセットによります。繁体字中国語でのプレイは未検証で、翻訳パッチも付属しません。",
    "disclaimer": "非公式のコミュニティツールです。ゲームの発売元や上流プロジェクトとは関係ありません。",
    "source": "ソースコード",
    "upstream": "Lunar Tear 本体",
    "licenses": "ライセンス",
    "hostLabel": "OS を選択"
  }
};
const nodes = [...document.querySelectorAll('[data-i18n]')];
translations.en = Object.fromEntries(nodes.map(el => [el.dataset.i18n, el.textContent]));
translations.en.title = 'A local window\ninto the Cage.';
translations.en.copied = 'Copied';
translations.en.copyFailed = 'Copy failed. Select and copy the commands manually.';
const select = document.querySelector('#language');
let activeLanguage = 'en';
function chooseLanguage(lang) {
  if (!Object.hasOwn(translations, lang)) lang = 'en';
  activeLanguage = lang;
  const strings = translations[lang];
  nodes.forEach(el => {
    const value = strings[el.dataset.i18n] ?? translations.en[el.dataset.i18n];
    el.replaceChildren();
    value.split('\n').forEach((line, index) => { if(index) el.append(document.createElement('br')); el.append(document.createTextNode(line)); });
  });
  document.documentElement.lang = lang;
  document.title = 'Lunar Tear — ' + ({en:'Browser Launcher','zh-CN':'浏览器启动器','zh-TW':'瀏覽器啟動器',ja:'ブラウザーランチャー'}[lang]);
  document.querySelector('nav').setAttribute('aria-label',strings.navSetup);
  document.querySelector('.guide-link').href = 'https://github.com/cloud-oc/lunar-tear-browser-launcher/blob/main/docs/guide.'+(lang === 'zh-CN' ? 'zh-CN' : 'en')+'.md';
  document.querySelector('#diagram-title').textContent = strings.diagramCaption;
  document.querySelector('#copy-status').textContent = '';
  select.value = lang;
  try {localStorage.setItem('lunar-language',lang);} catch {}
}
let preference;
try {preference = localStorage.getItem('lunar-language');} catch {}
const browserLanguage = navigator.language || 'en';
const fallback = /^zh-(TW|HK|Hant)/i.test(browserLanguage) ? 'zh-TW' : /^zh/i.test(browserLanguage) ? 'zh-CN' : /^ja/i.test(browserLanguage) ? 'ja' : 'en';

const platformSelect = document.querySelector('#platform');
const commandSets = {
  windows: {setup:'.\\setup.cmd', doctor:'.\\doctor.cmd', start:'.\\start.cmd',tools:'.\\launch.cmd fetch-tools\n.\\launch.cmd init-db'},
  macos: {setup:'sh setup.sh',doctor:'sh doctor.sh',start:'sh start.sh',tools:'sh launch.sh fetch-tools\nsh launch.sh init-db'},
  linux: {setup:'sh setup.sh',doctor:'sh doctor.sh',start:'sh start.sh',tools:'sh launch.sh fetch-tools\nsh launch.sh init-db'}
};
function choosePlatform(value) {
  if(!Object.hasOwn(commandSets,value)) value='windows';
  platformSelect.value=value;
  document.querySelectorAll('[data-command]').forEach(el=>{el.textContent=commandSets[value][el.dataset.command];});
  document.querySelector('.command-block code').textContent=commandSets[value].tools;
  document.querySelector('#copy').textContent=translations[activeLanguage].copy;
  document.querySelector('#copy-status').textContent='';
}
const host=navigator.userAgentData?.platform || navigator.platform || '';
choosePlatform(new URLSearchParams(location.search).get('os') || (/mac/i.test(host)?'macos':/linux/i.test(host)?'linux':'windows'));
platformSelect.addEventListener('change',()=>choosePlatform(platformSelect.value));

chooseLanguage(new URLSearchParams(location.search).get('lang') || preference || fallback);
select.addEventListener('change',() => {
  chooseLanguage(select.value);
  const url = new URL(location.href); url.searchParams.set('lang',select.value);
  history.replaceState(null,'',url);
});
document.querySelector('#copy').addEventListener('click',async event => {
  const button = event.currentTarget;
  const text = document.querySelector('.command-block code').textContent;
  try {
    await navigator.clipboard.writeText(text);
    button.textContent = translations[activeLanguage].copied;
    document.querySelector('#copy-status').textContent = translations[activeLanguage].copied;
  } catch {
    document.querySelector('#copy-status').classList.remove('sr-only');
    document.querySelector('#copy-status').textContent = translations[activeLanguage].copyFailed;
  }
});
