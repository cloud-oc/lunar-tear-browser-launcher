'use strict';
const translations = {
  'zh-CN': {
    skip:'跳至正文',navSetup:'使用指南',language:'语言',title:'在本机，\n重访牢笼。',
    intro:'安卓游戏，在你的 Windows 电脑上运行。用一个启动器连接 Lunar Tear、模拟器与 scrcpy，从浏览器窗口开始操作。',
    download:'下载启动器',start:'阅读简明指南',downloadNote:'工程 ZIP · Windows · 游戏文件需自行准备',
    diagramCaption:'本机运行，浏览器呈现。',status:'实验性项目',statusText:'已验证串流和服务连接，完整游戏流程尚未验证。',
    setupTitle:'开始之前。',setupIntro:'首次准备好环境，以后从一个文件启动。',system:'系统',android:'安卓环境',
    androidText:'开启 ADB 的模拟器。已测试 MuMu Android 15，其他兼容方案尚未验证。',gameFiles:'游戏文件',
    gameFilesText:'连接私服的国际版 3.7.1 修改版 APK、Android 资源和处理后的 Master Data。工程不包含这些文件。',fullGuide:'完整准备指南 ↗',
    step1:'安装启动器环境',step1Text:'解压下载的工程，运行 setup.cmd。Python 依赖会安装在工程目录内。',
    step2:'连接你的运行环境',step2Text:'编辑 config.json，填写 ADB 路径、模拟器地址和服务端目录。然后在工程目录运行以下命令。',copy:'复制命令',copied:'已复制',copyFailed:'复制失败，请手动选择命令复制。',
    step3:'准备游戏文件',step3Text:'按照完整指南安装修改版 APK，放好资源和 Master Data，再运行 doctor.cmd 检查。',
    step4:'打开本机游戏窗口',step4Text:'运行 start.cmd，再依次点击「連接畫面」和「啟動遊戲」。结束后使用 stop.cmd 停止服务。',
    notesTitle:'还有几件事。',faq1:'必须使用 MuMu 吗？',faq1Text:'不必须。其他模拟器需要支持游戏的 ARM64 原生库、ADB reverse 和 scrcpy。将 emulator_manager 设为空字符串，配置 adb 和 serial，并自行启动模拟器。目前仅验证了 MuMu Android 15。',
    faq2:'可以直接在这个网站游玩吗？',faq2Text:'这个网站提供工程下载和说明。游戏运行在你电脑的安卓模拟器里，由本机浏览器页面显示和控制，不提供云端游戏服务。',
    faq3:'切换语言会翻译游戏吗？',faq3Text:'语言选项只切换本网站。游戏文本取决于客户端和资源。繁体中文剧情尚未验证，工程不包含汉化补丁。',
    disclaimer:'非官方社区工具，与游戏发行商及上游项目无隶属关系。',source:'源代码',upstream:'上游 Lunar Tear',licenses:'授权信息'
  },
  'zh-TW': {
    skip:'跳至主要內容',navSetup:'使用指南',language:'語言',title:'在本機，\n重訪牢籠。',
    intro:'Android 遊戲，在你的 Windows 電腦上執行。用一個啟動器連接 Lunar Tear、模擬器與 scrcpy，透過瀏覽器視窗操作。',
    download:'下載啟動器',start:'閱讀簡明指南',downloadNote:'專案 ZIP · Windows · 遊戲檔案需自行準備',
    diagramCaption:'本機執行，瀏覽器呈現。',status:'實驗性專案',statusText:'已驗證串流與伺服器連線，完整遊戲流程尚未驗證。',
    setupTitle:'開始之前。',setupIntro:'首次備妥環境，之後從一個檔案啟動。',system:'系統',android:'Android 環境',
    androidText:'已開啟 ADB 的模擬器。已測試 MuMu Android 15，其他相容方案尚未驗證。',gameFiles:'遊戲檔案',
    gameFilesText:'連接私服的國際版 3.7.1 修改版 APK、Android 資源與處理後的 Master Data。專案不包含這些檔案。',fullGuide:'完整準備指南（英文）↗',
    step1:'安裝啟動器環境',step1Text:'解壓縮下載的專案，執行 setup.cmd。Python 相依套件會安裝在專案目錄內。',
    step2:'連接你的執行環境',step2Text:'編輯 config.json，填入 ADB 路徑、模擬器位址及伺服器目錄。接著在專案目錄執行以下命令。',copy:'複製命令',copied:'已複製',copyFailed:'複製失敗，請手動選取命令複製。',
    step3:'準備遊戲檔案',step3Text:'依完整指南安裝修改版 APK，放妥資源與 Master Data，再執行 doctor.cmd 檢查。',
    step4:'開啟本機遊戲視窗',step4Text:'執行 start.cmd，再依序點選「連接畫面」與「啟動遊戲」。結束後使用 stop.cmd 停止服務。',
    notesTitle:'還有幾件事。',faq1:'一定要使用 MuMu 嗎？',faq1Text:'不一定。其他模擬器需支援遊戲的 ARM64 原生程式庫、ADB reverse 與 scrcpy。將 emulator_manager 設為空字串，設定 adb 與 serial，並自行啟動模擬器。目前僅驗證了 MuMu Android 15。',
    faq2:'可以直接在這個網站遊玩嗎？',faq2Text:'這個網站提供專案下載及說明。遊戲在你電腦的 Android 模擬器中執行，由本機瀏覽器頁面顯示與控制，不提供雲端遊戲服務。',
    faq3:'切換語言會翻譯遊戲嗎？',faq3Text:'語言選項只切換本網站。遊戲文字取決於用戶端及資源。繁體中文劇情尚未驗證，專案不包含翻譯修補檔。',
    disclaimer:'非官方社群工具，與遊戲發行商及上游專案無隸屬關係。',source:'原始碼',upstream:'上游 Lunar Tear',licenses:'授權資訊'
  },
  ja: {
    skip:'本文へ移動',navSetup:'使い方',language:'言語',title:'「檻」への、\n小さな窓。',
    intro:'Android のゲームを、Windows PC のブラウザーで。Lunar Tear、エミュレーター、scrcpy をひとつのランチャーで接続します。',
    download:'ランチャーをダウンロード',start:'使い方を読む',downloadNote:'ソース ZIP · Windows · ゲームファイルは別途必要',
    diagramCaption:'PC で実行。ブラウザーで操作。',status:'実験的なプロジェクト',statusText:'映像配信とサーバー接続は確認済み。全編のプレイは未検証です。',
    setupTitle:'始める前に。',setupIntro:'最初に環境を準備すれば、次回からはファイルひとつで起動できます。',system:'システム',android:'Android 環境',
    androidText:'ADB が有効なエミュレーター。MuMu Android 15 で確認済み。ほかの互換環境は未検証です。',gameFiles:'ゲームファイル',
    gameFilesText:'接続先を変更したグローバル版 3.7.1 APK、Android アセット、処理済み Master Data。いずれも付属しません。',fullGuide:'詳しい準備ガイド（英語）↗',
    step1:'ランチャーを準備',step1Text:'ダウンロードした ZIP を展開し、setup.cmd を実行します。Python の依存パッケージはプロジェクト内にインストールされます。',
    step2:'実行環境を接続',step2Text:'config.json に ADB のパス、エミュレーターの接続先、サーバーフォルダーを設定。その後、プロジェクトフォルダーで次のコマンドを実行します。',copy:'コピー',copied:'コピーしました',copyFailed:'コピーできませんでした。コマンドを選択して手動でコピーしてください。',
    step3:'ゲームファイルを配置',step3Text:'詳細ガイドに従い、変更済み APK をインストールしてアセットと Master Data を配置。doctor.cmd で設定を確認します。',
    step4:'ローカルのゲーム画面へ',step4Text:'start.cmd を実行し、「連接畫面」（画面に接続）、「啟動遊戲」（ゲーム起動）の順に選択。終了時は stop.cmd を実行します。',
    notesTitle:'知っておきたいこと。',faq1:'MuMu は必須ですか？',faq1Text:'必須ではありません。代替環境にはゲームの ARM64 ライブラリ、ADB reverse、scrcpy への対応が必要です。emulator_manager を空文字列にし、adb と serial を設定してエミュレーターを手動起動してください。確認済み環境は MuMu Android 15 のみです。',
    faq2:'このサイトで直接プレイできますか？',faq2Text:'ここはダウンロードと説明のためのサイトです。ゲームは PC の Android エミュレーターで動作し、ローカルのブラウザーページで表示・操作します。クラウドゲームサービスではありません。',
    faq3:'言語を変えるとゲームも翻訳されますか？',faq3Text:'言語選択はこのサイトの表示だけを変更します。ゲーム内のテキストはクライアントとアセットによります。繁体字中国語でのプレイは未検証で、翻訳パッチも付属しません。',
    disclaimer:'非公式のコミュニティツールです。ゲームの発売元や上流プロジェクトとは関係ありません。',source:'ソースコード',upstream:'Lunar Tear 本体',licenses:'ライセンス'
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
