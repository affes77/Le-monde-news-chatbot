import json

with open('output.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

international_articles = []
for article in articles:
    if article['category'] == 'international':
        international_articles.append(article)

# Write the filtered articles to a new JSON file
with open('international_articles.json', 'w', encoding='utf-8') as f: 
    json.dump(international_articles, f, ensure_ascii=False, indent=4)
