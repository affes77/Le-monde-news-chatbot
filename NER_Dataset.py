import json
import spacy

# load the NER model
nlp = spacy.load("en_core_web_sm")

# read the articles from the JSON file
with open("international_articles_translated.json", 'r', encoding='utf-8') as f:
    articles = json.load(f)

# article processed 
articles_processed = 0
# initialize counter
counter = 1  

# create a list to hold the NER results for each article
ner_results = []

# loop through each article and extract its summary
for article in articles:
    summary = article["summary"]
    
    # apply NER on the summary using the loaded NER model
    doc = nlp(summary)
    
    # extract the NER labels and their text
    ner_texts = [ent.text for ent in doc.ents]
    
    # create a dictionary to hold the article's NER results
    article_ner = {
        "id": counter,
        "summary": summary,
        "ner_texts": ner_texts
    }
    counter += 1  # increment counter
    # append the article's NER results to the list
    ner_results.append(article_ner)
            # Increment the articles_processed counter
    articles_processed += 1
    print(f"Processed article {articles_processed}/{len(articles)}")

# write the NER results to a JSON file
with open("ner_dataset.json", 'w', encoding='utf-8') as f:
    json.dump(ner_results, f, ensure_ascii=False, indent=4)
