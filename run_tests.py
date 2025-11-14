#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
簡單的測試腳本，用於驗證各個模組是否正常運作
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
        return False

def test_stock_service():
    """測試股票資料服務"""
    print("\n測試股票資料服務...")
    try:
        from services.stock_data import StockDataService
        service = StockDataService()

        # 測試取得股票清單
        stocks = service.get_stock_list()
        print(f"✓ 股票清單載入成功，共 {len(stocks)} 支股票")

        # 測試取得報價（使用台積電）
        print("  嘗試取得台積電 (2330) 報價...")
        quote = service.get_stock_quote('2330')
        print(f"  ✓ 台積電股價: {quote['price']}")

        return True
    except Exception as e:
        print(f"✗ 股票服務測試失敗: {str(e)}")
        return False

def test_news_service():
    """測試新聞服務"""
    print("\n測試新聞服務...")
    try:
        from services.news_service import NewsService
        service = NewsService()

        news = service.get_latest_news(5)
        print(f"✓ 新聞載入成功，共 {len(news)} 則新聞")

        return True
    except Exception as e:
        print(f"✗ 新聞服務測試失敗: {str(e)}")
        return False

def test_analysis_service():
    """測試分析服務"""
    print("\n測試分析服務...")
    try:
        from services.analysis_service import AnalysisService
        service = AnalysisService()

        print("  嘗試分析台積電 (2330)...")
        analysis = service.analyze_stock('2330', 30)
        print(f"  ✓ 分析完成")
        print(f"  建議動作: {analysis['recommendation']['action']}")
        print(f"  信心度: {analysis['recommendation']['confidence']}%")

        return True
    except Exception as e:
        print(f"✗ 分析服務測試失敗: {str(e)}")
        return False

def main():
    """主測試函數"""
    print("=" * 50)
    print("台灣股市分析平台 - 測試腳本")
    print("=" * 50)

    results = []

    # 執行測試
    results.append(("模組導入", test_imports()))
    results.append(("股票服務", test_stock_service()))
    results.append(("新聞服務", test_news_service()))
    results.append(("分析服務", test_analysis_service()))

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
        print("\n🎉 所有測試通過！系統運作正常。")
        return 0
    else:
        print("\n⚠️  部分測試失敗，請檢查相關模組。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
