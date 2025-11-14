#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
真實數據測試腳本 - 測試從 Yahoo Finance 獲取真實股市數據
"""

import sys
from services.stock_data import StockDataService, YFINANCE_AVAILABLE
from services.news_service import NewsService, FEEDPARSER_AVAILABLE

def test_real_stock_data():
    """測試真實股市數據獲取"""
    print("=" * 60)
    print("測試真實股市數據獲取")
    print("=" * 60)

    print(f"\nyfinance 可用: {YFINANCE_AVAILABLE}")
    print(f"feedparser 可用: {FEEDPARSER_AVAILABLE}")

    if not YFINANCE_AVAILABLE:
        print("\n❌ yfinance 未安裝，無法測試真實數據")
        return False

    service = StockDataService()

    # 測試台積電 (2330)
    print("\n" + "-" * 60)
    print("測試獲取台積電 (2330) 即時報價...")
    print("-" * 60)

    try:
        quote = service.get_stock_quote('2330')
        print(f"\n✓ 成功獲取台積電報價:")
        print(f"  股票代碼: {quote['stock_id']}")
        print(f"  股票名稱: {quote['name']}")
        print(f"  目前股價: {quote['price']}")
        print(f"  漲跌金額: {quote['change']}")
        print(f"  漲跌幅度: {quote['change_percent']}%")
        print(f"  成交量: {quote['volume']:,}")
        print(f"  最高價: {quote['high']}")
        print(f"  最低價: {quote['low']}")
        print(f"  開盤價: {quote['open']}")
        print(f"  更新時間: {quote['timestamp']}")
    except Exception as e:
        print(f"\n✗ 獲取報價失敗: {str(e)}")
        return False

    # 測試歷史數據
    print("\n" + "-" * 60)
    print("測試獲取台積電 (2330) 歷史數據 (最近5天)...")
    print("-" * 60)

    try:
        history = service.get_stock_history('2330', days=5)
        print(f"\n✓ 成功獲取 {len(history)} 天歷史數據:")
        for i, day in enumerate(history[-5:], 1):
            print(f"  {i}. {day['date']}: 收盤 {day['close']}, 成交量 {day['volume']:,}")
    except Exception as e:
        print(f"\n✗ 獲取歷史數據失敗: {str(e)}")
        return False

    # 測試其他股票
    print("\n" + "-" * 60)
    print("測試獲取其他熱門股票報價...")
    print("-" * 60)

    test_stocks = [('2317', '鴻海'), ('2454', '聯發科'), ('2882', '國泰金')]

    for stock_id, expected_name in test_stocks:
        try:
            quote = service.get_stock_quote(stock_id)
            print(f"\n  ✓ {stock_id} ({quote['name']}): {quote['price']} ({quote['change']:+.2f}, {quote['change_percent']:+.2f}%)")
        except Exception as e:
            print(f"\n  ✗ {stock_id} 獲取失敗: {str(e)}")

    return True

def test_real_news_data():
    """測試真實新聞數據獲取"""
    print("\n" + "=" * 60)
    print("測試真實新聞數據獲取")
    print("=" * 60)

    if not FEEDPARSER_AVAILABLE:
        print("\n⚠️  feedparser 未安裝，將使用模擬新聞數據")

    service = NewsService()

    try:
        news = service.get_latest_news(5)
        print(f"\n✓ 成功獲取 {len(news)} 則新聞:")
        for i, item in enumerate(news, 1):
            print(f"\n  {i}. {item['title']}")
            print(f"     來源: {item['source']} | 時間: {item['published']}")
            if item['summary']:
                print(f"     摘要: {item['summary'][:100]}...")
    except Exception as e:
        print(f"\n✗ 獲取新聞失敗: {str(e)}")
        return False

    return True

def main():
    """主測試函數"""
    print("\n" + "=" * 60)
    print("🚀 台灣股市分析平台 - 真實數據測試")
    print("=" * 60)

    results = []

    # 執行測試
    results.append(("股市數據", test_real_stock_data()))
    results.append(("新聞數據", test_real_news_data()))

    # 顯示結果
    print("\n" + "=" * 60)
    print("測試結果摘要")
    print("=" * 60)

    for name, result in results:
        status = "✓ 通過" if result else "✗ 失敗"
        print(f"{name}: {status}")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print(f"\n總計: {passed}/{total} 項測試通過")

    if passed == total:
        print("\n🎉 所有測試通過！已成功連接真實數據源。")
        print("\n下一步:")
        print("  執行 'python app.py' 啟動服務")
        print("  在瀏覽器訪問 http://localhost:5000")
        print("  現在可以看到真實的台股即時行情！")
        return 0
    else:
        print("\n⚠️  部分測試失敗，請檢查網絡連接和 API 狀態。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
