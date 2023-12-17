from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Check if CUDA is available and set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)


tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
model = AutoModelForSeq2SeqLM.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap").to(device)


# Counter variable
articles_processed = 0

def get_question(answer, context, max_length=128):
  input_text = "answer: %s  context: %s </s>" % (answer, context)
  features = tokenizer([input_text], return_tensors='pt').to(device)

  output = model.generate(input_ids=features['input_ids'], 
               attention_mask=features['attention_mask'],
               max_length=max_length).to(device)

  return tokenizer.decode(output[0])



import json

# Load the NER dataset
with open('ner_dataset.json', 'r', encoding='utf-8') as f:
    ner_dataset = json.load(f)

# Initialize a list to store the SQuAD dataset
squad_dataset = []

# Loop through each article in the NER dataset
for article in ner_dataset:
    context = article['summary'] # Set the context to the article summary
    id = article['id'] # Get the article ID
    for ner in article['ner_texts']: # Loop through each NER entity in the article
        question = get_question(ner, context) # Generate a question based on the NER entity and context
        squad_dataset.append({
            'id': id, # Set the SQuAD ID
            'context': context,
            'question': question,
            'answer': ner, # Set the answer to the NER entity text
            "answer_start": context.find(ner)
        })
        # Increment the articles_processed counter
    articles_processed += 1
    print(f"Processed article {articles_processed}/{len(ner_dataset)}")

# Save the SQuAD dataset to a JSON file
with open('SQUAD_TRANSLATED_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(squad_dataset, f, ensure_ascii=False, indent=4)
