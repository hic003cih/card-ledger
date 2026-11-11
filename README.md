# 卡牌收藏帳本

在美國代買的卡盒收據帳本，是一個 GitHub Pages 網站（`index.html`），資料在 `cards.json`。

開網站：Settings → Pages → Source 選「Deploy from a branch」、Branch 選 `main`、資料夾 `/ (root)`，存檔後幾分鐘就有網址。

## 怎麼更新

最簡單：在 Claude（Claude Code，連到這個 repo）傳收據照片，說「記一筆」。Claude 會照 `CLAUDE.md` 的規則寫進 `cards.json` 並推上來，幾分鐘後網站就會更新。

要自己改也可以直接在 GitHub 網頁上編輯 `cards.json`，欄位說明都在 `CLAUDE.md`。

## 注意

這個 repo 是公開的：只寫品名、金額、店名、日期，不要放姓名、卡號、會員號、地址或收據照片。
