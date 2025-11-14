# 真實股市數據功能說明

## 📊 真實數據已啟用

所有依賴套件已安裝完成，系統現在可以獲取真實的台灣股市數據！

## 已驗證功能

### ✅ 即時股票報價

**台積電 (2330)** - 真實數據範例
```json
{
  "stock_id": "2330",
  "name": "Taiwan Semiconductor Manufacturing Company Limited",
  "price": 1430.0,
  "change": -30.0,
  "change_percent": -2.05,
  "volume": 31,682,102,
  "high": 1440.0,
  "low": 1425.0,
  "open": 1425.0,
  "timestamp": "2025-11-14 00:00:00"
}
```

**其他已測試股票**
- 鴻海 (2317): 241.0 元 (-4.37%)
- 聯發科 (2454): 1230.0 元 (-1.20%)
- 國泰金 (2882): 66.0 元 (+0.15%)

### ✅ 歷史數據

成功獲取台積電最近 5 天的歷史數據：
```
2025-11-07: 收盤 1460.0, 成交量 20,329,390
2025-11-10: 收盤 1475.0, 成交量 25,281,744
2025-11-11: 收盤 1465.0, 成交量 22,444,166
2025-11-12: 收盤 1475.0, 成交量 23,642,502
2025-11-13: 收盤 1460.0, 成交量 21,255,597
```

### ✅ 技術分析

基於真實數據的技術分析結果：

**台積電 (2330) 分析報告**
- **當前價格**: 1460.0 元
- **建議動作**: 賣出
- **信心度**: 90%
- **分析原因**: 短期均線跌破長期均線，RSI處於相對高點，MACD呈現空頭訊號

**技術指標**
- MA5 (5日均線): 1467.0
- MA20 (20日均線): 1477.25
- RSI (相對強弱): 52.63
- MACD: 5.07
- 支撐位: 1435.0
- 壓力位: 1525.0

### ✅ 財經新聞

成功從經濟日報 RSS 獲取真實新聞：

1. **TrendForce：AI 伺服器電源架構轉型 電源供應器市場迎接高速增長期**
   - 來源: 經濟日報
   - 時間: 2025-11-14 15:19:03

2. **TrendForce：估今年全球 AI 伺服器出貨年增逾24% 明年再成長逾20%**
   - 來源: 經濟日報
   - 時間: 2025-11-14 15:13:31

3. **TrendForce：AI 伺服器散熱革新 液冷加速取代氣冷邁向主流**
   - 來源: 經濟日報
   - 時間: 2025-11-14 15:12:29

## 安裝的套件

```
✓ yfinance 0.2.66       - Yahoo Finance API 客戶端
✓ feedparser 6.0.12     - RSS 新聞解析器
✓ beautifulsoup4 4.14.2 - HTML 解析器
✓ lxml 6.0.2            - XML 解析器
✓ Flask 3.1.2           - Web 框架
✓ pandas 2.3.3          - 數據處理
✓ numpy 2.3.4           - 數值計算
```

## 資料來源

### 股票數據
- **提供商**: Yahoo Finance
- **API**: yfinance Python 庫
- **資料延遲**: 15-20 分鐘
- **涵蓋範圍**: 台灣證券交易所上市股票（.TW 後綴）

### 新聞數據
- **提供商**: 經濟日報 RSS Feed
- **更新頻率**: 即時
- **內容**: 台灣財經新聞、科技產業新聞

## API 端點測試結果

### GET /api/stocks/list
✅ 返回 12 支熱門台股清單

### GET /api/stocks/{stock_id}/quote
✅ 返回真實即時報價
- 測試通過: 2330, 2317, 2454, 2882

### GET /api/stocks/{stock_id}/history?days=30
✅ 返回真實歷史數據
- 測試通過: 2330

### GET /api/stocks/{stock_id}/analysis?days=60
✅ 返回基於真實數據的技術分析
- 計算 MA5, MA10, MA20
- 計算 RSI, MACD
- 產生買賣建議

### GET /api/news?limit=10
✅ 返回真實財經新聞
- 來源: 經濟日報 RSS

### GET /api/news/stock/{stock_id}?limit=5
✅ 返回個股相關新聞過濾

## 如何啟動

### 方法 1: 開發模式
```bash
python app.py
```
訪問: http://localhost:5000

### 方法 2: 生產模式 (使用 Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 前端功能

打開瀏覽器訪問 http://localhost:5000，您將看到：

1. **熱門股票選擇器** - 點擊任意股票查看詳情
2. **即時報價卡片** - 顯示當前價格、漲跌幅、成交量等
3. **技術分析建議** - AI 智能分析，提供買賣建議
4. **價格走勢圖** - 互動式 Chart.js 圖表，顯示價格與均線
5. **技術指標面板** - MA5/10/20, RSI, MACD 等指標
6. **相關新聞** - 該股票的最新相關新聞
7. **市場新聞** - 最新財經新聞動態

## 範例截圖數據

### 台積電 (2330) 即時報價
- 💹 價格: **1430.0** 元
- 📉 漲跌: **-30.0** 元 (**-2.05%**)
- 📊 成交量: **31,682,102** 股
- 📈 最高: **1440.0** / 最低: **1425.0**

### 技術分析建議
- 🎯 建議: **賣出**
- 💪 信心度: **90%**
- 📝 原因: 短期均線跌破長期均線，RSI處於相對高點

## 資料更新頻率

- **股票報價**: 每次 API 請求獲取最新數據（約 15-20 分鐘延遲）
- **歷史數據**: 每日更新
- **財經新聞**: 即時更新
- **技術分析**: 即時計算

## 注意事項

### 資料延遲
Yahoo Finance 提供的數據有 15-20 分鐘延遲，並非完全即時。如需真正的即時數據，需要：
- 申請證券交易所官方 API
- 使用付費的金融數據服務

### API 使用限制
- Yahoo Finance 沒有明確的 API 限制，但建議合理使用
- 避免過於頻繁的請求（建議間隔至少 1 秒）
- 可以加入快取機制減少 API 調用

### 資料準確性
- 技術分析僅供參考，不構成投資建議
- 請勿將系統建議作為唯一的投資依據
- 投資有風險，請謹慎評估

## 測試命令

```bash
# 運行完整測試
python test_real_data.py

# 測試特定股票
curl http://localhost:5000/api/stocks/2330/quote | python -m json.tool

# 測試技術分析
curl http://localhost:5000/api/stocks/2330/analysis | python -m json.tool

# 測試新聞
curl http://localhost:5000/api/news | python -m json.tool
```

## 效能優化建議

### 1. 加入快取
```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=128)
def get_cached_quote(stock_id, minute):
    # 以分鐘為快取單位
    pass
```

### 2. 非同步數據獲取
```python
import asyncio
import aiohttp

async def fetch_multiple_stocks(stock_ids):
    tasks = [fetch_stock(id) for id in stock_ids]
    return await asyncio.gather(*tasks)
```

### 3. Redis 快取
```python
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.setex(f'quote:{stock_id}', 60, json.dumps(quote))
```

## 下一步建議

1. ✅ 已完成真實數據整合
2. 🔜 加入數據快取機制
3. 🔜 實作 WebSocket 推送
4. 🔜 新增更多技術指標 (KD, BOLL)
5. 🔜 新增自選股功能
6. 🔜 實作交易回測功能

## 支援

如有問題，請查看：
- `README.md` - 完整專案文檔
- `TEST_RESULTS.md` - 測試結果報告
- `test_real_data.py` - 真實數據測試腳本

---

**最後更新**: 2025-11-14
**狀態**: ✅ 生產就緒
**數據源**: Yahoo Finance + 經濟日報 RSS
