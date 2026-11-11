"""檢查 cards.json 的格式。用法：python3 check.py（只用標準函式庫）"""
import json, re, sys

CATS = {"pokemon", "nba", "lorcana", "misc"}
KINDS = {"etb", "exbox", "upc", "bundle", "poster", "tin", "display", "collection", "blaster", "trove"}
errs, warns = [], []

d = json.load(open("cards.json", encoding="utf-8"))
for k in ("updated", "rule", "receipts"):
    if k not in d: errs.append(f"少了最上層欄位 {k}")

ids = set()
for r in d.get("receipts", []):
    rid = r.get("id", "?")
    if rid in ids: errs.append(f"{rid}：id 重複")
    ids.add(rid)
    if r.get("date") is not None and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r["date"])):
        errs.append(f"{rid}：date 要是 YYYY-MM-DD 或 null")
    if r.get("date") is None and not r.get("ref"):
        warns.append(f"{rid}：沒有日期，最好在 ref 寫交易號")
    if not r.get("store"): errs.append(f"{rid}：少了 store")
    total = 0
    for i, it in enumerate(r.get("items", [])):
        tag = f"{rid} 第 {i + 1} 項（{it.get('name', '?')}）"
        if not it.get("name"): errs.append(f"{tag}：少了 name")
        if it.get("cat") not in CATS: errs.append(f"{tag}：cat 要是 {sorted(CATS)}")
        if it.get("cat") != "misc" and it.get("kind") not in KINDS: errs.append(f"{tag}：kind 要是 {sorted(KINDS)}")
        for f in ("paid", "tax"):
            if not isinstance(it.get(f), (int, float)): errs.append(f"{tag}：{f} 要是數字")
        for f in ("msrp", "market"):
            if f in it and it[f] is not None and not isinstance(it[f], (int, float)): errs.append(f"{tag}：{f} 要是數字或 null")
        if it.get("cat") != "misc" and it.get("msrp") is None: warns.append(f"{tag}：原價還沒查")
        total += round((it.get("paid") or 0) * 100) + round((it.get("tax") or 0) * 100)
    print(f"{rid:10} {r.get('date') or '日期待補':10} {r.get('store', ''):30} ${total / 100:,.2f}")

for w in warns: print("提醒：" + w)
for e in errs: print("錯誤：" + e)
print("通過 ✓" if not errs else f"有 {len(errs)} 個錯誤")
sys.exit(1 if errs else 0)
