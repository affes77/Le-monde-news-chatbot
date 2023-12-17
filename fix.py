import json

with open('SQUAD_TRANSLATED_dataset.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

list1 = []

for article in articles:
    if article['context'] not in list1:
        list1.append(article['context'])

print(len(list1))

with open('international_articles_translated.json', 'r', encoding='utf-8') as f:
    arts = json.load(f)
    
num_dicts = len(arts)
print(num_dicts)

for i, art in enumerate(arts):
    art['summary'] = list1[i]


with open('international_articles_translated.json', 'w', encoding='utf-8') as f:
    json.dump(arts, f, ensure_ascii=False, indent=4)