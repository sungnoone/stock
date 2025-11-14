# 台灣股市分析平台 📈

一個功能完整的台灣股市即時行情、技術分析與財經新聞整合平台。

## 功能特色

### 📊 即時股市行情
- 熱門台股即時報價
- 開高低收、成交量等完整資訊
- 漲跌幅即時顯示

### 📈 技術分析
- **移動平均線 (MA)**：MA5、MA10、MA20
- **相對強弱指標 (RSI)**：超買超賣判斷
- **MACD 指標**：趨勢方向判斷
- **支撐壓力位**：關鍵價位分析
- **買賣建議**：基於技術指標的智能建議

### 📰 財經新聞
- 最新財經新聞彙整
- 個股相關新聞推送
- 多來源新聞整合

### 📉 視覺化圖表
- 互動式價格走勢圖
- 均線疊加顯示
- Chart.js 圖表引擎

## 技術架構

### 後端
- **Python 3.x**
- **Flask**：Web 框架
- **pandas**：資料處理
- **yfinance**：Yahoo Finance API 資料獲取
- **numpy**：數值計算
- **feedparser**：RSS 新聞解析

### 前端
- **HTML5 / CSS3**
- **JavaScript (ES6+)**
- **Chart.js**：圖表視覺化
- 響應式設計

### 資料來源
- **Yahoo Finance API**：股票即時與歷史資料
- **RSS Feed**：財經新聞來源

## 安裝步驟

### 1. 克隆專案
```bash
git clone <repository-url>
cd stock
```

### 2. 建立虛擬環境（建議）
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 安裝相依套件
```bash
pip install -r requirements.txt
```

### 4. 啟動應用程式
```bash
python app.py
```

### 5. 開啟瀏覽器
訪問 `http://localhost:5000`

## API 端點

### 股票相關
- `GET /api/stocks/list` - 取得熱門股票清單
- `GET /api/stocks/<stock_id>/quote` - 取得即時報價
- `GET /api/stocks/<stock_id>/history?days=30` - 取得歷史資料
- `GET /api/stocks/<stock_id>/analysis?days=60` - 取得技術分析

### 新聞相關
- `GET /api/news?limit=20` - 取得財經新聞
- `GET /api/news/stock/<stock_id>?limit=10` - 取得個股新聞

## 專案結構

```
stock/
├── app.py                  # Flask 主應用程式
├── requirements.txt        # Python 相依套件
├── .gitignore             # Git 忽略檔案
├── README.md              # 專案說明文件
├── services/              # 服務模組
│   ├── __init__.py
│   ├── stock_data.py      # 股票資料服務
│   ├── news_service.py    # 新聞服務
│   └── analysis_service.py # 分析服務
└── static/                # 靜態檔案
    ├── index.html         # 主頁面
    ├── css/
    │   └── style.css      # 樣式表
    └── js/
        └── app.js         # 前端邏輯
```

## 使用說明

### 查看股票資訊
1. 在「熱門股票」區域選擇想要查看的股票
2. 系統會自動載入該股票的即時報價、技術分析和相關新聞
3. 查看價格走勢圖和技術指標

### 技術分析解讀
- **買進建議**：技術指標偏多，適合考慮進場
- **賣出建議**：技術指標偏空，建議考慮出場
- **持有建議**：指標中性，建議觀望

### 信心度說明
- **70% 以上**：強烈訊號
- **60-70%**：中等訊號
- **50-60%**：弱訊號

## 技術指標說明

### 移動平均線 (MA)
- MA5 > MA20：短期趨勢向上
- MA5 < MA20：短期趨勢向下

### RSI (相對強弱指標)
- RSI > 70：超買區，可能回調
- RSI < 30：超賣區，可能反彈
- 50 附近：中性區域

### MACD
- MACD > 0：多頭訊號
- MACD < 0：空頭訊號
- MACD 柱狀圖由負轉正：買入訊號

## 熱門股票清單

目前支援以下台股：
- 2330 台積電
- 2317 鴻海
- 2454 聯發科
- 2882 國泰金
- 2881 富邦金
- 2886 兆豐金
- 2303 聯電
- 2412 中華電
- 1301 台塑
- 1303 南亞
- 2002 中鋼
- 2308 台達電

## 注意事項

⚠️ **重要聲明**
1. 本平台提供的資訊僅供參考，不構成投資建議
2. 技術分析有其侷限性，不保證預測準確性
3. 投資有風險，請謹慎評估自身風險承受能力
4. 建議搭配基本面分析和專業財務顧問意見

## 常見問題

### Q: 資料更新頻率？
A: 使用 Yahoo Finance API，資料會有 15-20 分鐘延遲。

### Q: 可以查詢更多股票嗎？
A: 可以修改 `services/stock_data.py` 中的 `popular_stocks` 清單來新增更多股票。

### Q: 如何自訂技術指標參數？
A: 可以修改 `services/analysis_service.py` 中的參數設定。

## 部署建議

### 開發環境
```bash
python app.py
```

### 生產環境（使用 Gunicorn）
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker 部署
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 未來改進方向

- [ ] 新增更多技術指標（KD、布林通道等）
- [ ] 整合更多新聞來源
- [ ] 加入用戶自選股功能
- [ ] 新增股票比較功能
- [ ] 歷史回測功能
- [ ] 即時推播通知
- [ ] 行動版 APP

## 授權

本專案採用 MIT 授權條款。

## 聯絡方式

如有問題或建議，歡迎提出 Issue 或 Pull Request。

---

**免責聲明**：本平台僅供學習與研究使用，所有資訊不構成任何投資建議。投資有風險，請謹慎評估。
