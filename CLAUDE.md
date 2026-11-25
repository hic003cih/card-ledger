# card-ledger：卡牌收藏帳本

- 一律用繁體中文回覆。
- 卡牌收藏帳本：在美國代買的寶可夢／NBA／Lorcana 卡盒收據。這是一個獨立的 GitHub Pages 網站：
  - `cards.json`：資料（記帳只改這個）。
  - `index.html`／`cards.js`／`cards.css`／`icon.svg`：網站畫面。要改版面就改這幾個檔，改完用 `python3 -m http.server` 開起來看過再推。
- 哥哥的「家的旅程」網站也會**讀這裡的 `cards.json`**（用它自己那份畫面程式，不載入這裡的 js）。所以 `cards.json` 的欄位**只能增加、不要改名或刪掉**，不然他那邊會壞；真的要改格式先跟使用者確認。
- 推上 `main` 後幾分鐘，兩邊網站都會更新。
- 這個 repo 是**公開的**：只寫品名、金額、稅、店名、日期。**不要寫**姓名、信用卡號或末四碼、會員號、電話、地址、訂單編號。收據照片不要 commit。

## 使用者傳收據時怎麼記

使用者傳收據照片或說「記一筆」時，**不用問、直接記**，推上 `main` 後用一兩句話說記了什麼、哪些欄位還不確定。

1. 一張收據＝`receipts` 陣列裡的一個物件，**新的放最前面**：
   - `id`：店家縮寫＋日期，例 `bn-1112`（Barnes & Noble）、`tg-1112`（Target）、`wm-1112`（Walmart）；同一天同一家第二張加 `-2`。不能跟現有的重複。
   - `date`：`YYYY-MM-DD`；收據沒拍到日期就填 `null`，並在 `ref` 寫收據上的交易號（例 `"交易 #4551"`）。
   - `store`：店名＋分店，例 `"Barnes & Noble Shady Ave"`。
   - `ref`（可省略）：交易號、「抽籤」之類的補充。
2. 每個品項放進 `items`：
   - `name`：商品名，盡量寫完整的正式名稱（收據縮寫要查出全名，查不到就照收據寫並在 `note` 說明）。
   - `cat`：`pokemon`／`nba`／`lorcana`／`misc`（袋子費、運費這類雜支）。新的卡牌種類先問使用者。
   - `kind`（決定網站上的示意圖，圖在 `cards.js` 的 `ART`）：`etb`（Elite Trainer Box）、`exbox`（ex Box）、`upc`（Ultra-Premium Collection）、`bundle`（多盒組合）、`poster`（Poster Collection）、`tin`（鐵盒）、`display`（補充包整盒）、`collection`（其他收藏盒）、`blaster`（運動卡 Blaster）、`trove`（Lorcana Trove）。都不像就用 `collection`（要新增 kind 就在 `ART` 畫一張自己畫的 SVG，不放網路照片、不畫角色或商標，並加進 `check.py` 的 `KINDS`）。
   - `paid`：稅前實付（有會員折扣就是折後價），`tax`：這個品項的稅。整張收據只有一個稅額時，按各品項金額比例分攤，並在 `note` 寫「稅是整張 $X 按金額分的」。各品項 `paid＋tax` 加總要等於收據總額。
   - `msrp`：官方原價（美元）。查 Pokémon Center 官網、ICv2 等可靠來源；查不到填 `null`，`note` 寫「原價還沒查」。數量 >1 時 `msrp` 填**總原價**並加 `qty`。
   - `market`：二手市場參考價（TCGplayer、Pokemon Wizard 等），查不到填 `null`；`market_src` 寫來源和日期（沒標日期就寫「日期未標」）。有好幾個來源時用**最低值**，並把其他範圍寫在 `market_src`。
   - `note`：其他要記的事（會員折多少、收據哪裡看不清楚、推論了什麼）。
   - `qty`（可省略，預設 1）。
3. **不用填「原價／貴／超過上限」**：網站依 `rule` 自動算（寶可夢 ETB 上限 $80，其他原價 +25%；非寶可夢只比原價）。
4. 改完執行 `python3 check.py` 確認格式和每張收據的加總，沒問題才 commit、push。
5. 哥哥請 Claude 記帳時：推完這裡後，把同一份 `cards.json` 複製到他的私有庫一起推（11/25 起；他的 Token 讀不到這個私人 repo，家的旅程收藏分頁實際讀那份副本）。弟弟自己記帳時碰不到那個庫，不用做，跟哥哥說一聲即可。

## 預算（匯給弟弟的錢）

`funds` 是匯給弟弟買卡的錢，網站總覽會用它算「預算還剩多少」的進度條。使用者說又匯了一筆（例如「再匯 2 萬」）時，在 `funds` 加一筆：`amount`（數字）、`cur`（`TWD` 或 `USD`）、`date`（`YYYY-MM-DD`，不知道就 `null`）、`note`。不要寫帳號、轉帳序號。

## 補資料

使用者說查到原價或行情、或要改哪一筆時，找到那筆直接改 `msrp`／`market`／`market_src`／`note`，跑 `check.py` 後推上去。不要改 `rule`，除非使用者明確說規則要改。
