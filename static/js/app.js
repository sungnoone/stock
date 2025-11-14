// API 基礎 URL
const API_BASE = '/api';

// 全域變數
let currentChart = null;
let currentStockId = null;

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    loadStockList();
    loadMarketNews();
});

// 載入股票清單
async function loadStockList() {
    try {
        const response = await fetch(`${API_BASE}/stocks/list`);
        const result = await response.json();

        if (result.success) {
            displayStockList(result.data);
        } else {
            showError('stockList', '無法載入股票清單');
        }
    } catch (error) {
        console.error('Error loading stock list:', error);
        showError('stockList', '載入股票清單時發生錯誤');
    }
}

// 顯示股票清單
function displayStockList(stocks) {
    const container = document.getElementById('stockList');
    container.innerHTML = '';

    stocks.forEach(stock => {
        const div = document.createElement('div');
        div.className = 'stock-item';
        div.innerHTML = `
            <div class="stock-item-id">${stock.id}</div>
            <div class="stock-item-name">${stock.name}</div>
        `;
        div.onclick = () => selectStock(stock.id, stock.name);
        container.appendChild(div);
    });
}

// 選擇股票
async function selectStock(stockId, stockName) {
    currentStockId = stockId;

    // 更新選中狀態
    document.querySelectorAll('.stock-item').forEach(item => {
        item.classList.remove('active');
    });
    event.currentTarget.classList.add('active');

    // 顯示股票資訊區
    document.getElementById('stockInfo').style.display = 'block';
    document.getElementById('stockTitle').textContent = `${stockName} (${stockId})`;

    // 載入資料
    await Promise.all([
        loadStockQuote(stockId),
        loadStockAnalysis(stockId),
        loadStockNews(stockId)
    ]);
}

// 載入股票報價
async function loadStockQuote(stockId) {
    const container = document.getElementById('quoteInfo');
    container.innerHTML = '<div class="loading">載入中...</div>';

    try {
        const response = await fetch(`${API_BASE}/stocks/${stockId}/quote`);
        const result = await response.json();

        if (result.success) {
            displayQuote(result.data);
        } else {
            showError('quoteInfo', '無法載入報價資訊');
        }
    } catch (error) {
        console.error('Error loading quote:', error);
        showError('quoteInfo', '載入報價時發生錯誤');
    }
}

// 顯示報價
function displayQuote(quote) {
    const container = document.getElementById('quoteInfo');
    const changeClass = quote.change > 0 ? 'up' : (quote.change < 0 ? 'down' : 'neutral');
    const changeSymbol = quote.change > 0 ? '▲' : (quote.change < 0 ? '▼' : '－');

    container.innerHTML = `
        <div class="price">${quote.price}</div>
        <div class="change ${changeClass}">
            ${changeSymbol} ${Math.abs(quote.change)} (${quote.change_percent}%)
        </div>
        <div class="detail-row">
            <span class="detail-label">開盤</span>
            <span class="detail-value">${quote.open}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">最高</span>
            <span class="detail-value">${quote.high}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">最低</span>
            <span class="detail-value">${quote.low}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">成交量</span>
            <span class="detail-value">${formatVolume(quote.volume)}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">更新時間</span>
            <span class="detail-value">${quote.timestamp}</span>
        </div>
    `;
}

// 載入技術分析
async function loadStockAnalysis(stockId) {
    const container = document.getElementById('analysisInfo');
    container.innerHTML = '<div class="loading">分析中...</div>';

    try {
        const response = await fetch(`${API_BASE}/stocks/${stockId}/analysis?days=60`);
        const result = await response.json();

        if (result.success) {
            displayAnalysis(result.data);
            displayChart(result.data.chart_data);
            displayIndicators(result.data.indicators, result.data.support, result.data.resistance);
        } else {
            showError('analysisInfo', '無法載入分析資訊');
        }
    } catch (error) {
        console.error('Error loading analysis:', error);
        showError('analysisInfo', '載入分析時發生錯誤');
    }
}

// 顯示分析建議
function displayAnalysis(data) {
    const container = document.getElementById('analysisInfo');
    const rec = data.recommendation;
    const actionClass = rec.action === '買進' ? 'buy' : (rec.action === '賣出' ? 'sell' : 'hold');

    container.innerHTML = `
        <div class="recommendation ${actionClass}">${rec.action}</div>
        <div style="margin: 15px 0;">
            <strong>信心度：</strong>${rec.confidence}%
        </div>
        <div style="color: #666; line-height: 1.6;">
            <strong>分析：</strong>${rec.reason}
        </div>
        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #ddd; font-size: 0.9em; color: #999;">
            分析時間：${data.analysis_date}
        </div>
    `;
}

// 顯示圖表
function displayChart(chartData) {
    const ctx = document.getElementById('priceChart').getContext('2d');

    // 銷毀舊圖表
    if (currentChart) {
        currentChart.destroy();
    }

    // 建立新圖表
    currentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.dates,
            datasets: [
                {
                    label: '收盤價',
                    data: chartData.prices,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    tension: 0.1
                },
                {
                    label: 'MA5',
                    data: chartData.ma5,
                    borderColor: '#e74c3c',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false
                },
                {
                    label: 'MA10',
                    data: chartData.ma10,
                    borderColor: '#f39c12',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false
                },
                {
                    label: 'MA20',
                    data: chartData.ma20,
                    borderColor: '#27ae60',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

// 顯示技術指標
function displayIndicators(indicators, support, resistance) {
    const container = document.getElementById('indicators');
    container.innerHTML = '';

    const indicatorData = [
        { label: 'MA5', value: indicators.ma5 },
        { label: 'MA10', value: indicators.ma10 },
        { label: 'MA20', value: indicators.ma20 },
        { label: 'RSI', value: indicators.rsi },
        { label: 'MACD', value: indicators.macd },
        { label: 'Signal', value: indicators.signal },
        { label: '支撐價', value: support },
        { label: '壓力價', value: resistance }
    ];

    indicatorData.forEach(item => {
        const div = document.createElement('div');
        div.className = 'indicator-item';
        div.innerHTML = `
            <div class="indicator-label">${item.label}</div>
            <div class="indicator-value">${item.value !== null ? item.value : 'N/A'}</div>
        `;
        container.appendChild(div);
    });
}

// 載入股票新聞
async function loadStockNews(stockId) {
    const container = document.getElementById('stockNews');
    container.innerHTML = '<div class="loading">載入中...</div>';

    try {
        const response = await fetch(`${API_BASE}/news/stock/${stockId}?limit=5`);
        const result = await response.json();

        if (result.success) {
            displayNews(result.data, 'stockNews');
        } else {
            showError('stockNews', '無法載入新聞');
        }
    } catch (error) {
        console.error('Error loading stock news:', error);
        showError('stockNews', '載入新聞時發生錯誤');
    }
}

// 載入市場新聞
async function loadMarketNews() {
    const container = document.getElementById('marketNews');
    container.innerHTML = '<div class="loading">載入中...</div>';

    try {
        const response = await fetch(`${API_BASE}/news?limit=10`);
        const result = await response.json();

        if (result.success) {
            displayNews(result.data, 'marketNews');
        } else {
            showError('marketNews', '無法載入新聞');
        }
    } catch (error) {
        console.error('Error loading market news:', error);
        showError('marketNews', '載入新聞時發生錯誤');
    }
}

// 顯示新聞
function displayNews(newsItems, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    if (newsItems.length === 0) {
        container.innerHTML = '<div class="loading">暫無新聞</div>';
        return;
    }

    newsItems.forEach(news => {
        const div = document.createElement('div');
        div.className = 'news-item';
        div.innerHTML = `
            <div class="news-title">
                <a href="${news.link}" target="_blank">${news.title}</a>
            </div>
            <div class="news-meta">
                ${news.source} · ${news.published}
            </div>
            ${news.summary ? `<div class="news-summary">${news.summary}</div>` : ''}
        `;
        container.appendChild(div);
    });
}

// 格式化成交量
function formatVolume(volume) {
    if (volume >= 100000000) {
        return (volume / 100000000).toFixed(2) + '億';
    } else if (volume >= 10000) {
        return (volume / 10000).toFixed(2) + '萬';
    }
    return volume.toString();
}

// 顯示錯誤
function showError(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `<div class="loading" style="color: #e74c3c;">${message}</div>`;
}
