import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json

# 検索するキーワードの設定
urls = {
    "es": ("ES作成・添削", "ChatGPT ES 就活"),
    "interview": ("面接対策", "ChatGPT 面接 就活"),
    "research": ("企業研究・自己分析", "ChatGPT 自己分析 就活")
}

news_data = []

for category, (cat_name, keyword) in urls.items():
    try:
        # Googleニュースからキーワードで検索して取得
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ja&gl=JP&ceid=JP:ja"
        
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            # 各カテゴリ最新の5件だけ取得
            for item in root.findall('./channel/item')[:5]:
                title = item.find('title').text
                link = item.find('link').text
                pub_date = item.find('pubDate').text
                
                news_data.append({
                    "title": title,
                    "category": category,
                    "categoryName": cat_name,
                    "date": pub_date[5:16], # 日付部分を切り取る
                    "url": link
                })
    except Exception as e:
        print(f"エラー: {e}")

# 集めたデータを「news_data.json」として保存する
with open('news_data.json', 'w', encoding='utf-8') as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)

print("記事の取得が完了しました！")
