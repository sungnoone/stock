import requests
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import time

class StockDataService:
    """台灣股市資料服務"""

    def __init__(self):
        self.twse_url = "https://www.twse.com.tw/exchangeReport"
        self.popular_stocks = [
            {'id': '2330', 'name': '台積電'},
            {'id': '2317', 'name': '鴻海'},
            {'id': '2454', 'name': '聯發科'},
            {'id': '2882', 'name': '國泰金'},
            {'id': '2881', 'name': '富邦金'},
            {'id': '2886', 'name': '兆豐金'},
            {'id': '2303', 'name': '聯電'},
            {'id': '2412', 'name': '中華電'},
            {'id': '1301', 'name': '台塑'},
            {'id': '1303', 'name': '南亞'},
            {'id': '2002', 'name': '中鋼'},
            {'id': '2308', 'name': '台達電'},
        ]

    def get_stock_list(self):
        """取得熱門股票清單"""
        return self.popular_stocks

    def get_stock_quote(self, stock_id):
        """取得即時報價 - 使用 Yahoo Finance"""
        try:
            # 台股代碼需要加上 .TW 後綴
            ticker = f"{stock_id}.TW"
            stock = yf.Ticker(ticker)

            # 取得最新資訊
            info = stock.info
            hist = stock.history(period='2d')

            if hist.empty:
                raise Exception(f"無法取得股票 {stock_id} 的資料")

            latest = hist.iloc[-1]
            prev = hist.iloc[-2] if len(hist) > 1 else latest

            # 計算漲跌
            change = latest['Close'] - prev['Close']
            change_percent = (change / prev['Close']) * 100 if prev['Close'] != 0 else 0

            return {
                'stock_id': stock_id,
                'name': info.get('longName', stock_id),
                'price': round(float(latest['Close']), 2),
                'change': round(float(change), 2),
                'change_percent': round(float(change_percent), 2),
                'volume': int(latest['Volume']),
                'high': round(float(latest['High']), 2),
                'low': round(float(latest['Low']), 2),
                'open': round(float(latest['Open']), 2),
                'timestamp': latest.name.strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            print(f"Error getting quote for {stock_id}: {str(e)}")
            raise Exception(f"無法取得股票報價: {str(e)}")

    def get_stock_history(self, stock_id, days=30):
        """取得歷史資料"""
        try:
            ticker = f"{stock_id}.TW"
            stock = yf.Ticker(ticker)

            # 取得歷史資料
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days+10)  # 多抓一些以防假日

            hist = stock.history(start=start_date, end=end_date)

            if hist.empty:
                raise Exception(f"無法取得股票 {stock_id} 的歷史資料")

            # 轉換為列表格式
            history_list = []
            for index, row in hist.iterrows():
                history_list.append({
                    'date': index.strftime('%Y-%m-%d'),
                    'open': round(float(row['Open']), 2),
                    'high': round(float(row['High']), 2),
                    'low': round(float(row['Low']), 2),
                    'close': round(float(row['Close']), 2),
                    'volume': int(row['Volume'])
                })

            # 只回傳最近 days 天的資料
            return history_list[-days:] if len(history_list) > days else history_list

        except Exception as e:
            print(f"Error getting history for {stock_id}: {str(e)}")
            raise Exception(f"無法取得歷史資料: {str(e)}")

    def get_twse_market_data(self, date=None):
        """取得證交所大盤資料（備用方法）"""
        if date is None:
            date = datetime.now().strftime('%Y%m%d')

        try:
            url = f"{self.twse_url}/MI_INDEX"
            params = {
                'response': 'json',
                'date': date,
                'type': 'ALLBUT0999'
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            return data

        except Exception as e:
            print(f"Error getting TWSE data: {str(e)}")
            return None
