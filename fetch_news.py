import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json

# 指定された8つのタグに合わせた検索キーワードの設定
urls = {
    "intern": ("インターン対策", "ChatGPT インターン 就活"),
    "es": ("ES作成・添削", "ChatGPT ES 添削 就活"),
    "interview": ("面接対策", "ChatGPT 面接 就活"),
    "gd": ("GD", "ChatGPT GD グループディスカッション 就活"),
    "research": ("企業研究", "ChatGPT 企業研究 就活"),
    "self_analysis": ("自己分析", "ChatGPT 自己分析 就活"),
    "ir_news": ("IR・企業ニュース要約", "ChatGPT IR ニュース 要約 就活"),
    "prompt": ("有用AIプロンプト", "ChatGPT プロンプト 就活")
}

news_data = []

for category, (cat_name, keyword) in urls.items():
    try:
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ja&gl=JP&ceid=JP:ja"
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            # 各カテゴリ最新の4件を取得
            for item in root.findall('./channel/item')[:4]:
                title = item.find('title').text
                link = item.find('link').text
                pub_date = item.find('pubDate').text
                
                news_data.append({
                    "title": title,
                    "category": category,
                    "categoryName": cat_name,
                    "date": pub_date[5:16],
                    "url": link
                })
    except Exception as e:
        print(f"エラー ({category}): {e}")

# 集めたデータを保存する
with open('news_data.json', 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)

print("8カテゴリの記事取得が完了しました！")
