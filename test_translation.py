from transformers import MarianTokenizer, MarianMTModel
import json
import torch

# Check if CUDA is available and set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

# Load the articles from the JSON file
with open('international_articlesCLEANED.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

tokenizer = MarianTokenizer.from_pretrained('Helsinki-NLP/opus-mt-fr-en')
model = MarianMTModel.from_pretrained('Helsinki-NLP/opus-mt-fr-en').to(device)

# Counter variable
articles_processed = 0


# Translate each French summary to English
for article in articles:
    french_summary = article['summary']

    input_text = "translate French to English: " + french_summary
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)
    output_ids = model.generate(input_ids).to(device)
    english_summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    article['summary']= english_summary
  
        # Increment the articles_processed counter
    articles_processed += 1
    print(f"Processed article {articles_processed}/{len(articles)}")

# Save the updated articles to a new JSON file
with open('international_articles_translated.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

