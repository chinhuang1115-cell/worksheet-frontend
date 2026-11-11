# CLAUDE.md

易數教室學習單的**前端**（單頁 HTML，GitHub Pages 部署）。給資源班學生使用的數學學習單；教材設計以「視覺化、結構化、生活化、簡單易懂」為原則。實際的 PDF／Word 生成在後端 repo（`worksheet-backend`，FastAPI，部署於 Railway）。

## 文件索引

| 想找什麼 | 去哪裡 |
|---|---|
| **題型設計決策**：題型命名與康軒對照、填空留白規則、難度層次、各題型的教學設計意圖、**提示漸退版型**（完整提示→淡化提示→無提示→**逐題漸退淡化提示**：同一份學單提示逐題淡化，計算格先退、算式列後退，最後一題兩者皆無） | [`docs/題型設計決策.md`](docs/題型設計決策.md) |
| **教材設計規範**：使用對象與設計原則、版面規格、量詞、答案合理範圍、主題與位數對應、時鐘、錢幣配色（互動頁） | [`docs/教材設計規範.md`](docs/教材設計規範.md) |
| **互動頁規格資料**（`dashboard/` 只留資料與腳本，網頁介面已於 2026-10-14 捨棄）：`hint-profile.json`＝強／弱／無提示設定檔（權威）、`spec.json`＝提示規格表資料、`catalog.json`＝互動頁清單（總覽頁用）；`check_catalog.py <後端路徑>` 檢查漏列端點。**新增／修改互動頁時，同一個 commit 更新 catalog／spec** | [`dashboard/`](dashboard/)；規格說明與盤點結論：[`docs/互動版提示規格.md`](docs/互動版提示規格.md) |
| **互動學習單總覽**（名稱「互動學習單」，GitHub Pages 的 `/interactive/`：左側導覽樹＋縮圖三欄、頂端小次類篩選、搜尋；連結一律帶 `lv=2&mode=faded`＝從這裡進去是弱提示；**跨頁切換用左側邊緣直式標籤**：總覽→易數教室、首頁→互動學習單；**遊戲（catalog 的 `kind:'game'`）不進導覽樹；入口是橘色直式標籤「互動遊戲」→ 互動遊戲導覽頁 `games/`**（使用者 2026-11-10，原本每個遊戲一個標籤）；⚠️ 總覽的 `load()` 每 2 分鐘重跑一次（抓最新 catalog），**在 `load()` 裡往頁面加東西要先清掉舊的**，否則會一直疊加（2026-11-09 遊戲標籤疊成好幾個）；階層配色與細節見後端 repo `docs/guide/interactive-web.md`「互動學習單入口、版面與切換」）。資料與儀表板共用 `dashboard/catalog.json`；**新增／改版互動頁後，除了更新 catalog，還要重產縮圖**：`python dashboard/make_thumbs.py <後端路徑> [id…]`（重產後 `catalog.json` 的 `thumbsV` 會自動更新，縮圖網址帶 `?v=` 才不會被快取沿用舊圖；`params` 含 `calc=1` 的直式計算題縮圖是靜態畫的計算格特寫，標籤是 `index.html` 的 `rgTag`） | [`interactive/`](interactive/)、[`dashboard/make_thumbs.py`](dashboard/make_thumbs.py) |
| **互動遊戲導覽頁**（GitHub Pages 的 `/games/`，使用者 2026-11-10 選模擬圖 C「商店街」：每個遊戲一間店、右側欄選關卡＋強／弱／無提示，預設弱、記在 `localStorage.ys_game_lv`；遊戲另開分頁）。入口：首頁與互動學習單總覽左側的橘色「互動遊戲」標籤。**資料讀 `dashboard/catalog.json` 的 `kind:'game'` 項目**：`shop`（店名）、`tag`、`desc`、`stages:[{n,name,sub}]`；**新增遊戲＝加一筆 catalog＋`make_thumbs.py` 重產縮圖**，不用改頁面；街尾固定一間灰色「敬請期待」 | [`games/index.html`](games/index.html)；模擬圖 `docs/mock-game-hub/`（`make.py` 重產） |
| 認識錢幣「半自由／完全自由排列」與錢幣外觀改版的**後端交接說明**（要做什麼、演算法、驗收清單）| [`docs/後端交接_錢幣自由排列與外觀.md`](docs/後端交接_錢幣自由排列與外觀.md)；視覺依據 `docs/mock-coin-free/` |
| 認識錢幣自由排列的**後端實作順序清單**（決策 → 外觀 → 共用模組 → 試水 → 擴充 → 收尾，含每步驗收）| [`docs/後端實作順序清單.md`](docs/後端實作順序清單.md)（規則細節在上一列的交接說明）；可直接貼給後端 session 的簡短提示：[`docs/後端提示_錢幣自由排列.md`](docs/後端提示_錢幣自由排列.md) |
| **錢幣配色（互動頁）**：1 元咖啡銅、5／10 元銀灰、50 元黃銅（2026-11-09 定案方案 A；Word／PDF 不變） | 規範：[`docs/教材設計規範.md`](docs/教材設計規範.md) 第 8 節；mockup `docs/mock-coin-color/`；後端交接（已完成）[`docs/後端提示_錢幣顏色.md`](docs/後端提示_錢幣顏色.md) |
| **早餐店購物遊戲**（顧客／店員輪流、綜合四則與錢幣；2026-11-08 規劃中）的定案事項、流程、關卡、實作步驟 | [`docs/早餐店購物遊戲_規劃.md`](docs/早餐店購物遊戲_規劃.md)；模擬圖 `docs/mock-breakfast-shop/` |
| **麵包店購物遊戲**（2026-11-10；與早餐店**同一份程式換主題**，多第 5 關「哪袋划算」：紅袋藍袋比單價、價錢天平；**每個店家的裝潢都要不同**，角色色橘／藍不換）的定案、菜單、第 5 關設計 | [`docs/麵包店購物遊戲_規劃.md`](docs/麵包店購物遊戲_規劃.md)；菜單草案 `docs/mock-bakery-shop/`；實作在後端 `game_shop.SHOPS`＋`docs/guide/game-shop.md`「多家店」 |
| **生圖流程**（使用者 2026-11-11 定案：需要圖一律「Claude Code 寫指令 → 使用者轉貼 Cowork 在 Gemini 生圖、上傳雲端硬碟『遊戲素材／待處理』→ Claude Code 用 Google Drive 下載、去背、對齊」）：指令格式、提示詞寫法、去背坑 | [`docs/生圖流程.md`](docs/生圖流程.md)；去背工具 [`tools/cutout.py`](tools/cutout.py) |
| 直式加減乘的**計算格設計規範**（尺寸、欄數、進退位、鷹架層級）| [`docs/輔助計算格規範.md`](docs/輔助計算格規範.md)；視覺依據 `docs/calc-grid-mock.html`／`.png` |
| 計算格的**後端實作**、版面驗收、踩坑、各題型產生器 | 後端 repo：`CLAUDE.md`（核心規則）與 `docs/guide/`（詳細筆記） |
| 題型清單、圖片處理等**技術開發規範** | 後端 repo：`toolkit/RULES.md`（題型清單在第 9 節） |
| 可重複執行的標準流程（**Skill**），例如 `/bake`：擷取範本正確內容壓成圖片 | 後端 repo：`.claude/skills/`（索引見後端 `CLAUDE.md`；只適用後端範本，前端工作用不到） |
| 網站介面的設計系統（顏色、字型、間距 token 與元件樣式） | `_ds/design-system-*/`：`tokens/`、`styles.css`、`_ds_bundle.js` 由 `index.html` **實際載入，不可刪**。⚠️ 其 `readme.md` 的產品與對象描述（國中生 App、教師儀表板、影片平台等）是產生設計系統時的推測，與本專案（資源班學習單的產生與銷售網站）不符，**只參考 tokens 與元件樣式，不要當作專案定位** |

**規範與實作的分工**：教材長什麼樣子、為什麼這樣設計，以本 repo `docs/` 的設計規範為準；怎麼畫出來、怎麼在 Word／LibreOffice 兩邊都正確，以後端 repo 為準。

**哪些檔案在這裡改、哪些不要改**：
- `index.html`（前端 UI 本體）：**直接在本 repo 編輯**，這裡就是唯一來源。
- `registry.js`、`gallery.js`：是**拷貝**。題型資料的權威來源是後端 repo 的 `shared/registry.js`，由後端 `python toolkit/sync_registry.py`（或手動 `cp`）同步過來，**不要直接在這裡改**，否則下次同步會被蓋掉。

## 工作原則（全域指示）

前後端 repo 共用同一套流程。**本節為精簡版；後端 repo `CLAUDE.md`「任務難度分級與模型選擇」是完整版（含模型組合表）。修改時兩邊一併更新，避免漂移。**

### 1. 先判斷難度，再選作法

- 接到任務先用一兩句話說明難度與作法。
- **先規劃、再執行（使用者 2026-10-28 指示）**：接到需求後一律先由 **Opus 5 規劃**（讀相關檔案、釐清需求、盤點要改的檔案與風險、產出含驗收方式的步驟計畫；規劃階段不動程式碼），計畫定案後交由 **Sonnet 執行**（實作、驗收、commit／push／合併 `main`）。涉及新設計或跨多檔的需求，計畫先給使用者確認再動手；小修改可直接接著做。交棒方式與例外見後端完整版。
- 預設由主對話直接做；多數工作（改版面、改 registry、寫文件）在 Sonnet 5.5 中等強度就夠。
- **升級**：同一個問題修了兩三輪還不對，主動告訴使用者「建議切到 Opus／Fable + 高強度」，由使用者切換；不要在同一方向上微調第四輪。
- **派 sub-agent 要先問**：子代理每次都要重新讀背景，成本不低。只有使用者明確要求，或任務明確屬於大量簡單搜尋／逐份比對時才派（可選 haiku／sonnet／opus／fable）。使用者明確指定模型或作法時，以當下指示為準。
- 要確認目前是哪個模型，用 session 資訊查（`get_session`），不要憑感覺回答。

### 2. 完成後直接合併回 `main`

修改完成、自我驗證通過後，直接把工作分支合併回 `main` 並推送，**不開 pull request、也不必再詢問**。

1. 在工作分支上完成修改，commit 並 push。
2. `git fetch origin main`，把工作分支合併進最新的 `main`（有衝突先解掉，避免蓋掉別人的 commit），再 `git push origin main`。
3. 合併後切回工作分支。

**例外**：自我驗證沒過，就停在 push，把問題講清楚，不要把壞掉的東西合進 `main`。（`main` 就是 GitHub Pages 的線上版本。）

### 3. 主動把經驗寫進文件

一次修正涉及多份學習單，或根因會在其他份重複出現時，完成後主動把經驗寫進文件，不必等使用者開口：優先寫成通則（根因、判斷訊號、修法），並記下「試過但無效的做法」。教材設計規範寫在本 repo `docs/`；版面實作的坑寫在後端 repo `docs/guide/`。

## sample PDF 預算圖（2026-10-07）

`assets/img/` 是由後端 repo `toolkit/make_sample_images.py` 產生的每頁 WebP 與 `manifest.json`，前端優先載圖、沒有才用 pdf.js。**換 `assets/*.pdf` 時必須一併更新 `assets/img/` 並 bump `SAMPLE_VER`**（`python <後端>/toolkit/make_sample_images.py assets`）。

## 題型詳情頁的「題型管理工具」（管理端，2026-10-21）

`index.html` 題型詳情頁（`ADMIN-ONLY-START` 區塊，`isAdmin` 才顯示）展開後是**兩張 1:1 等寬卡片並排**：「各版型售價一覽」＋「範本與檔案」（範本管理、檢視用下載）。**管理員檢核表已移除**，QA 標記改走管理導覽列的 QA 頁。改這塊時：

- 兩卡外層 grid 用 `minmax(0,1fr) minmax(0,1fr)`，卡片樣式（accent-50 底、warning-500 框、12px 14px 內距、標題下距 8px）保持一致；改完量測兩欄寬、上緣 y、欄距（2026-10-21 實測 544px／同 y／16px）。
- 管理模式本機預覽：`localStorage.ys_admin_mode='1'`、`ys_welcome_seen='1'`，開 `#screen=home&item=<題型id>` 後點「題型管理工具」展開。
- 「定價與購買設定」頁（`isScreenConfig` 區塊）另有一份管理員檢核表，尚未比照移除。

## 推送前先同步 main 的踩坑（2026-10-21）

本機前端 repo 的 `main` 可能落後遠端數百個 commit（別的 session 先推了 sample 圖與 `index.html`），`git fetch` 後才看得出。`git rebase` 會因「未追蹤的 `assets/img/*`、`assets/*_sample.pdf` 與遠端已收錄的檔案同名」而中止。做法：先把這些未追蹤檔移到暫存區備份（不要刪），再 `git rebase --autostash origin/main`（本機未提交的 `registry.js` 等用 autostash 帶過），推送前 `grep` 確認自己的改動仍在。`git fetch`／`push` 偶爾超過 120 秒，用 `timeout` 包起來。

## 推上 `main` 但線上沒更新：先查 Pages 部署（2026-11-10）

使用者回報「總覽頁只看得到早餐店」，但 `main` 的 `catalog.json` 已有麵包店、本機開 `games/` 也正常。原因是 GitHub Pages 的「pages build and deployment」**build 成功、deploy 步驟在 GitHub 那邊逾時失敗**（卡 10 分鐘後 failure），線上停在上一版。判斷：GitHub Actions 該次 run 的 `deploy` job 是 failure。修法：再推一個實際的 commit 觸發重新部署（不要推空 commit）。推完 `main` 後順手看一下最新一次 Pages run 是否 success。
