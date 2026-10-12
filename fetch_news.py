import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import re

# 1. 従来のAIプロンプト検索設定
prompt_urls = {
    "intern": ("インターン対策", "ChatGPT インターン 就活"),
    "es": ("ES作成・添削", "ChatGPT ES 添削 就活"),
    "interview": ("面接対策", "ChatGPT 面接 就活"),
    "gd": ("GD", "ChatGPT GD グループディスカッション 就活"),
    "research": ("企業研究", "ChatGPT 企業研究 就活"),
    "self_analysis": ("自己分析", "ChatGPT 自己分析 就活"),
    "ir_news": ("IR・企業ニュース要約", "ChatGPT IR ニュース 要約 就活"),
    "prompt": ("有用AIプロンプト", "ChatGPT プロンプト 就活")
}

# 2. 連携企業のリスト（IR情報を確実に拾うため「(決算 OR 業績 OR プレスリリース)」を追加）
companies = [
    {"name": "任天堂", "code": "7974", "query": "任天堂 (決算 OR 業績 OR プレスリリース)"},
    {"name": "ソニーグループ", "code": "6758", "query": "ソニーグループ (決算 OR 業績 OR プレスリリース)"},
    {"name": "トヨタ自動車", "code": "7203", "query": "トヨタ自動車 (決算 OR 業績 OR プレスリリース)"}
]

news_data = []
month_map = {"Jan":"01", "Feb":"02", "Mar":"03", "Apr":"04", "May":"05", "Jun":"06", "Jul":"07", "Aug":"08", "Sep":"09", "Oct":"10", "Nov":"11", "Dec":"12"}

# --- A. プロンプト記事（Web & YouTube）の取得 ---
# YouTubeの検索条件に「-広告 -PR -CM -宣伝」を追加してノイズを完全ブロック
sources = [
    {"type": "web", "query_suffix": "when:1y"},
    {"type": "youtube", "query_suffix": "when:1y site:youtube.com -広告 -PR -CM -宣伝"}
]

for src in sources:
    for category, (cat_name, keyword) in prompt_urls.items():
        try:
            search_query = f"{keyword} {src['query_suffix']}"
            url = f"https://news.google.com/rss/search?q={urllib.parse.quote(search_query)}&hl=ja&gl=JP&ceid=JP:ja"
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                root = ET.fromstring(response.read())
                for index, item in enumerate(root.findall('./channel/item')[:6]):
                    title = item.find('title').text
                    link = item.find('link').text
                    pub_date
