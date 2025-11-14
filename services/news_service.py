import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

class NewsService:
    """財經新聞服務"""

    def __init__(self):
        # 台灣財經新聞 RSS 來源
        self.news_sources = [
            {
                'name': '鉅亨網',
                'url': 'https://news.cnyes.com/news/cat/tw_stock?exp=a',
                'type': 'web'
            },
            {
                'name': '經濟日報',
                'url': 'https://money.udn.com/rssfeed/news/1001/5591/0?ch=news',
                'type': 'rss'
            }
        ]

    def get_latest_news(self, limit=20):
        """取得最新財經新聞"""
        all_news = []

        # 從各個來源收集新聞
        for source in self.news_sources:
            try:
                if source['type'] == 'rss':
                    news = self._parse_rss_feed(source['url'], source['name'])
                    all_news.extend(news)
                elif source['type'] == 'web':
                    # 對於網頁爬蟲，這裡簡化處理
                    pass
            except Exception as e:
                print(f"Error fetching news from {source['name']}: {str(e)}")

        # 如果沒有從 RSS 取得新聞，回傳模擬資料
        if not all_news:
            all_news = self._get_mock_news()

        # 按時間排序並限制數量
        all_news.sort(key=lambda x: x.get('published', ''), reverse=True)
        return all_news[:limit]

    def get_stock_news(self, stock_id, limit=10):
        """取得特定股票相關新聞"""
        # 取得股票名稱
        stock_names = {
            '2330': '台積電',
            '2317': '鴻海',
            '2454': '聯發科',
            '2882': '國泰金',
            '2881': '富邦金',
            '2886': '兆豐金',
            '2303': '聯電',
            '2412': '中華電',
            '1301': '台塑',
            '1303': '南亞',
            '2002': '中鋼',
            '2308': '台達電',
        }

        stock_name = stock_names.get(stock_id, stock_id)

        # 從所有新聞中過濾包含該股票的新聞
        all_news = self.get_latest_news(100)
        stock_news = [
            news for news in all_news
            if stock_name in news.get('title', '') or stock_id in news.get('title', '')
        ]

        return stock_news[:limit] if stock_news else self._get_mock_stock_news(stock_name)[:limit]

    def _parse_rss_feed(self, url, source_name):
        """解析 RSS Feed"""
        try:
            feed = feedparser.parse(url)
            news_list = []

            for entry in feed.entries[:20]:
                news_item = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', '')[:200] + '...' if entry.get('summary') else '',
                    'source': source_name
                }
                news_list.append(news_item)

            return news_list
        except Exception as e:
            print(f"Error parsing RSS feed: {str(e)}")
            return []

    def _get_mock_news(self):
        """取得模擬新聞資料（當無法取得真實資料時使用）"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return [
            {
                'title': '台股今日收盤上漲50點，電子股領漲',
                'link': '#',
                'published': now,
                'summary': '台灣股市今日表現強勁，加權指數收盤上漲50點，電子類股表現亮眼，台積電領漲...',
                'source': '財經新聞'
            },
            {
                'title': '台積電宣布新製程技術突破',
                'link': '#',
                'published': now,
                'summary': '台積電今日宣布在3奈米製程技術上取得重大突破，預計將提升晶片效能...',
                'source': '科技新聞'
            },
            {
                'title': '聯發科發布最新5G晶片',
                'link': '#',
                'published': now,
                'summary': '聯發科推出新一代5G旗艦晶片，效能提升顯著，預計將搶攻高階手機市場...',
                'source': '科技新聞'
            },
            {
                'title': '金融股受惠升息循環',
                'link': '#',
                'published': now,
                'summary': '在升息環境下，金融股獲利成長，國泰金、富邦金等龍頭股價穩健上揚...',
                'source': '金融新聞'
            },
            {
                'title': '外資連續買超台股',
                'link': '#',
                'published': now,
                'summary': '外資近期持續看好台股，連續多日買超，顯示對台灣市場信心增強...',
                'source': '財經新聞'
            }
        ]

    def _get_mock_stock_news(self, stock_name):
        """取得模擬的個股新聞"""
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return [
            {
                'title': f'{stock_name}法說會釋出利多消息',
                'link': '#',
                'published': now,
                'summary': f'{stock_name}在最新法說會中釋出多項利多消息，市場反應正面...',
                'source': '財經新聞'
            },
            {
                'title': f'外資調升{stock_name}目標價',
                'link': '#',
                'published': now,
                'summary': f'國際投資機構看好{stock_name}前景，調升目標價至新高...',
                'source': '投資研究'
            },
            {
                'title': f'{stock_name}業績優於預期',
                'link': '#',
                'published': now,
                'summary': f'{stock_name}公布最新財報，營收與獲利均優於市場預期...',
                'source': '財報新聞'
            }
        ]
