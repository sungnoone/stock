import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from services.stock_data import StockDataService

class AnalysisService:
    """股價技術分析服務"""

    def __init__(self):
        self.stock_service = StockDataService()

    def analyze_stock(self, stock_id, days=60):
        """進行股票技術分析"""
        try:
            # 取得歷史資料
            history = self.stock_service.get_stock_history(stock_id, days)

            if not history or len(history) < 20:
                raise Exception("歷史資料不足，無法進行分析")

            # 轉換為 DataFrame
            df = pd.DataFrame(history)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')

            # 計算技術指標
            ma5 = self._calculate_ma(df['close'], 5)
            ma10 = self._calculate_ma(df['close'], 10)
            ma20 = self._calculate_ma(df['close'], 20)
            rsi = self._calculate_rsi(df['close'], 14)
            macd_line, signal_line, macd_hist = self._calculate_macd(df['close'])

            # 產生買賣建議
            recommendation = self._generate_recommendation(
                df['close'].iloc[-1],
                ma5[-1] if len(ma5) > 0 else None,
                ma20[-1] if len(ma20) > 0 else None,
                rsi[-1] if len(rsi) > 0 else None,
                macd_hist[-1] if len(macd_hist) > 0 else None
            )

            # 計算支撐壓力
            support, resistance = self._calculate_support_resistance(df['close'], df['low'], df['high'])

            # 準備回傳資料
            analysis_data = {
                'stock_id': stock_id,
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'current_price': float(df['close'].iloc[-1]),
                'indicators': {
                    'ma5': round(float(ma5[-1]), 2) if len(ma5) > 0 and not np.isnan(ma5[-1]) else None,
                    'ma10': round(float(ma10[-1]), 2) if len(ma10) > 0 and not np.isnan(ma10[-1]) else None,
                    'ma20': round(float(ma20[-1]), 2) if len(ma20) > 0 and not np.isnan(ma20[-1]) else None,
                    'rsi': round(float(rsi[-1]), 2) if len(rsi) > 0 and not np.isnan(rsi[-1]) else None,
                    'macd': round(float(macd_line[-1]), 2) if len(macd_line) > 0 and not np.isnan(macd_line[-1]) else None,
                    'signal': round(float(signal_line[-1]), 2) if len(signal_line) > 0 and not np.isnan(signal_line[-1]) else None,
                    'macd_hist': round(float(macd_hist[-1]), 2) if len(macd_hist) > 0 and not np.isnan(macd_hist[-1]) else None,
                },
                'support': round(float(support), 2) if support else None,
                'resistance': round(float(resistance), 2) if resistance else None,
                'recommendation': recommendation,
                'chart_data': {
                    'dates': df['date'].dt.strftime('%Y-%m-%d').tolist(),
                    'prices': df['close'].round(2).tolist(),
                    'volumes': df['volume'].tolist(),
                    'ma5': [round(float(x), 2) if not np.isnan(x) else None for x in ma5],
                    'ma10': [round(float(x), 2) if not np.isnan(x) else None for x in ma10],
                    'ma20': [round(float(x), 2) if not np.isnan(x) else None for x in ma20],
                }
            }

            return analysis_data

        except Exception as e:
            print(f"Error analyzing stock {stock_id}: {str(e)}")
            raise Exception(f"分析失敗: {str(e)}")

    def _calculate_ma(self, prices, period):
        """計算移動平均線"""
        return prices.rolling(window=period).mean().fillna(0).values

    def _calculate_rsi(self, prices, period=14):
        """計算相對強弱指標 (RSI)"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.fillna(50).values

    def _calculate_macd(self, prices, fast=12, slow=26, signal=9):
        """計算 MACD 指標"""
        exp1 = prices.ewm(span=fast, adjust=False).mean()
        exp2 = prices.ewm(span=slow, adjust=False).mean()

        macd_line = exp1 - exp2
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        macd_hist = macd_line - signal_line

        return macd_line.fillna(0).values, signal_line.fillna(0).values, macd_hist.fillna(0).values

    def _calculate_support_resistance(self, prices, lows, highs):
        """計算支撐與壓力"""
        recent_prices = prices.tail(20)
        recent_lows = lows.tail(20)
        recent_highs = highs.tail(20)

        support = recent_lows.min()
        resistance = recent_highs.max()

        return support, resistance

    def _generate_recommendation(self, current_price, ma5, ma20, rsi, macd_hist):
        """產生買賣建議"""
        buy_signals = 0
        sell_signals = 0

        # MA 訊號
        if ma5 and ma20:
            if ma5 > ma20:
                buy_signals += 1
            else:
                sell_signals += 1

        # RSI 訊號
        if rsi:
            if rsi < 30:
                buy_signals += 2  # 超賣，強烈買入訊號
            elif rsi > 70:
                sell_signals += 2  # 超買，強烈賣出訊號
            elif rsi < 50:
                buy_signals += 1
            else:
                sell_signals += 1

        # MACD 訊號
        if macd_hist:
            if macd_hist > 0:
                buy_signals += 1
            else:
                sell_signals += 1

        # 產生建議
        if buy_signals > sell_signals + 1:
            action = "買進"
            confidence = min(90, 60 + (buy_signals - sell_signals) * 10)
            reason = self._get_buy_reason(ma5, ma20, rsi, macd_hist)
        elif sell_signals > buy_signals + 1:
            action = "賣出"
            confidence = min(90, 60 + (sell_signals - buy_signals) * 10)
            reason = self._get_sell_reason(ma5, ma20, rsi, macd_hist)
        else:
            action = "持有"
            confidence = 50
            reason = "目前技術指標呈現中性，建議觀望"

        return {
            'action': action,
            'confidence': confidence,
            'reason': reason
        }

    def _get_buy_reason(self, ma5, ma20, rsi, macd_hist):
        """取得買入理由"""
        reasons = []

        if ma5 and ma20 and ma5 > ma20:
            reasons.append("短期均線突破長期均線")

        if rsi and rsi < 30:
            reasons.append("RSI顯示超賣")
        elif rsi and rsi < 50:
            reasons.append("RSI處於相對低點")

        if macd_hist and macd_hist > 0:
            reasons.append("MACD呈現多頭訊號")

        return "，".join(reasons) if reasons else "技術指標偏多"

    def _get_sell_reason(self, ma5, ma20, rsi, macd_hist):
        """取得賣出理由"""
        reasons = []

        if ma5 and ma20 and ma5 < ma20:
            reasons.append("短期均線跌破長期均線")

        if rsi and rsi > 70:
            reasons.append("RSI顯示超買")
        elif rsi and rsi > 50:
            reasons.append("RSI處於相對高點")

        if macd_hist and macd_hist < 0:
            reasons.append("MACD呈現空頭訊號")

        return "，".join(reasons) if reasons else "技術指標偏空"
