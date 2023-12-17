import json

# Load the NER dataset
with open('ner_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

ner =[]

for article in dataset:
    for text in article["ner_texts"]:
        if text not in ner:
            ner.append(text)
    article["ner_texts"] = ner
    ner = []

# write the NER results to a JSON file
with open("ner_dataset.json", 'w', encoding='utf-8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=4)