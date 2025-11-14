#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
簡化版測試腳本 - 測試代碼結構和基本功能
"""

import sys
import os

def test_imports():
    """測試模組導入"""
    print("測試模組導入...")
    try:
        from services.stock_data import StockDataService
        from services.news_service import NewsService
        from services.analysis_service import AnalysisService
        print("✓ 所有服務模組導入成功")
        return True
    except Exception as e:
        print(f"✗ 模組導入失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_flask_app():
    """測試 Flask 應用程式結構"""
    print("\n測試 Flask 應用程式...")
    try:
        import app as flask_app

        # 檢查應用程式對象
        assert hasattr(flask_app, 'app'), "Flask app 對象不存在"
        print("✓ Flask 應用程式載入成功")

        # 檢查路由
        routes = []
        for rule in flask_app.app.url_map.iter_rules():
            routes.append(str(rule))

        print(f"  已註冊 {len(routes)} 個路由:")
        for route in sorted(routes):
            print(f"    - {route}")

        return True
    except Exception as e:
        print(f"✗ Flask 應用程式測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_stock_service_basic():
    """測試股票服務基本功能"""
    print("\n測試股票資料服務基本功能...")
    try:
        from services.stock_data import StockDataService
        service = StockDataService()

        # 測試取得股票清單
        stocks = service.get_stock_list()
        assert isinstance(stocks, list), "股票清單不是列表類型"
        assert len(stocks) > 0, "股票清單為空"

        print(f"✓ 股票清單載入成功，共 {len(stocks)} 支股票")
        print(f"  範例股票: {stocks[0]['id']} - {stocks[0]['name']}")

        return True
    except Exception as e:
        print(f"✗ 股票服務測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_news_service_basic():
    """測試新聞服務基本功能"""
    print("\n測試新聞服務基本功能...")
    try:
        from services.news_service import NewsService
        service = NewsService()

        # 測試取得模擬新聞
        news = service._get_mock_news()
        assert isinstance(news, list), "新聞列表不是列表類型"
        assert len(news) > 0, "新聞列表為空"

        print(f"✓ 新聞服務基本功能正常，可產生 {len(news)} 則模擬新聞")
        print(f"  範例新聞: {news[0]['title']}")

        return True
    except Exception as e:
        print(f"✗ 新聞服務測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_analysis_service_structure():
    """測試分析服務結構"""
    print("\n測試分析服務結構...")
    try:
        from services.analysis_service import AnalysisService
        import pandas as pd
        import numpy as np

        service = AnalysisService()

        # 測試技術指標計算函數
        test_prices = pd.Series([100, 102, 101, 103, 105, 104, 106, 108, 107, 109])

        # 測試 MA 計算
        ma5 = service._calculate_ma(test_prices, 5)
        assert len(ma5) == len(test_prices), "MA 計算結果長度不正確"
        print("  ✓ MA 計算功能正常")

        # 測試 RSI 計算
        rsi = service._calculate_rsi(test_prices, 5)
        assert len(rsi) == len(test_prices), "RSI 計算結果長度不正確"
        print("  ✓ RSI 計算功能正常")

        # 測試 MACD 計算
        macd_line, signal_line, macd_hist = service._calculate_macd(test_prices)
        assert len(macd_line) == len(test_prices), "MACD 計算結果長度不正確"
        print("  ✓ MACD 計算功能正常")

        print("✓ 分析服務所有技術指標計算功能正常")

        return True
    except Exception as e:
        print(f"✗ 分析服務測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_static_files():
    """測試靜態文件存在性"""
    print("\n測試靜態文件...")
    try:
        files_to_check = [
            'static/index.html',
            'static/css/style.css',
            'static/js/app.js'
        ]

        for file_path in files_to_check:
            assert os.path.exists(file_path), f"文件不存在: {file_path}"
            print(f"  ✓ {file_path}")

        print("✓ 所有靜態文件存在")
        return True
    except Exception as e:
        print(f"✗ 靜態文件檢查失敗: {str(e)}")
        return False

def main():
    """主測試函數"""
    print("=" * 50)
    print("台灣股市分析平台 - 簡化版測試")
    print("=" * 50)
    print("\n注意: 本測試僅檢查代碼結構和基本功能")
    print("      不包含實際 API 調用測試\n")

    results = []

    # 執行測試
    results.append(("模組導入", test_imports()))
    results.append(("Flask 應用", test_flask_app()))
    results.append(("股票服務結構", test_stock_service_basic()))
    results.append(("新聞服務結構", test_news_service_basic()))
    results.append(("分析服務功能", test_analysis_service_structure()))
    results.append(("靜態文件", test_static_files()))

    # 顯示結果
    print("\n" + "=" * 50)
    print("測試結果摘要")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ 通過" if result else "✗ 失敗"
        print(f"{name}: {status}")

    print(f"\n總計: {passed}/{total} 項測試通過")

    if passed == total:
        print("\n🎉 所有測試通過！代碼結構正常。")
        print("\n下一步:")
        print("  1. 安裝 yfinance 套件以啟用實際 API 功能")
        print("  2. 執行 'python app.py' 啟動服務")
        print("  3. 在瀏覽器訪問 http://localhost:5000")
        return 0
    else:
        print("\n⚠️  部分測試失敗，請檢查相關模組。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
