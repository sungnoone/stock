from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta
import os
from services.stock_data import StockDataService
from services.news_service import NewsService
from services.analysis_service import AnalysisService

app = Flask(__name__, static_folder='static')
CORS(app)

# 初始化服務
stock_service = StockDataService()
news_service = NewsService()
analysis_service = AnalysisService()

@app.route('/')
def index():
    """首頁"""
    return send_from_directory('static', 'index.html')

@app.route('/api/stocks/list', methods=['GET'])
def get_stock_list():
    """取得台股清單"""
    try:
        stocks = stock_service.get_stock_list()
        return jsonify({
            'success': True,
            'data': stocks
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stocks/<stock_id>/quote', methods=['GET'])
def get_stock_quote(stock_id):
    """取得即時報價"""
    try:
        quote = stock_service.get_stock_quote(stock_id)
        return jsonify({
            'success': True,
            'data': quote
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stocks/<stock_id>/history', methods=['GET'])
def get_stock_history(stock_id):
    """取得歷史資料"""
    try:
        days = request.args.get('days', default=30, type=int)
        history = stock_service.get_stock_history(stock_id, days)
        return jsonify({
            'success': True,
            'data': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stocks/<stock_id>/analysis', methods=['GET'])
def get_stock_analysis(stock_id):
    """取得技術分析"""
    try:
        days = request.args.get('days', default=60, type=int)
        analysis = analysis_service.analyze_stock(stock_id, days)
        return jsonify({
            'success': True,
            'data': analysis
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/news', methods=['GET'])
def get_news():
    """取得財經新聞"""
    try:
        limit = request.args.get('limit', default=20, type=int)
        news = news_service.get_latest_news(limit)
        return jsonify({
            'success': True,
            'data': news
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/news/stock/<stock_id>', methods=['GET'])
def get_stock_news(stock_id):
    """取得特定股票新聞"""
    try:
        limit = request.args.get('limit', default=10, type=int)
        news = news_service.get_stock_news(stock_id, limit)
        return jsonify({
            'success': True,
            'data': news
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # 確保靜態資料夾存在
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
