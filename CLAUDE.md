# CLAUDE.md

易數教室學習單的**前端**（單頁 HTML，GitHub Pages 部署）。給資源班學生使用的數學學習單；教材設計以「視覺化、結構化、生活化、簡單易懂」為原則。實際的 PDF／Word 生成在後端 repo（`worksheet-backend`，FastAPI，部署於 Railway）。

## 文件索引

| 想找什麼 | 去哪裡 |
|---|---|
| **題型設計決策**：題型命名與康軒對照、填空留白規則、難度層次、各題型的教學設計意圖 | [`docs/題型設計決策.md`](docs/題型設計決策.md) |
| **教材設計規範**：使用對象與設計原則、版面規格、量詞、答案合理範圍、主題與位數對應、時鐘 | [`docs/教材設計規範.md`](docs/教材設計規範.md) |
| 認識錢幣「半自由／完全自由排列」與錢幣外觀改版的**後端交接說明**（要做什麼、演算法、驗收清單）| [`docs/後端交接_錢幣自由排列與外觀.md`](docs/後端交接_錢幣自由排列與外觀.md)；視覺依據 `docs/mock-coin-free/` |
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
