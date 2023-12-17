import json
import newspaper

with open('international_articlesCLEANED.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for article in data:
    url = article['link']
    try:
        article_content = newspaper.Article(url)
        article_content.download()
        article_content.parse()
        article['content'] = article_content.text
    except Exception as e:
        print(f"Error scraping article content for {url}: {e}")

with open('international_articlesCLEANED.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
