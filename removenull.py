import json

with open('international_articles.json', 'r' , encoding='utf-8') as f:
    data = json.load(f)

data = [article for article in data if article['summary'] is not None]

with open('international_articlesCLEANED.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)






