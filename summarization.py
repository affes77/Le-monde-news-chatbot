from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import json

# Check if CUDA is available and set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

# Load the pre-trained T5 model and tokenizer
model_name = "plguillou/t5-base-fr-sum-cnndm"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name).to(device)


# Load articles from output.json
with open('international_articlesCLEANED.json', "r" ,  encoding='utf-8') as f:
    data = json.load(f)
# Counter variable
articles_processed = 0
# Loop through each article and generate a summary
for article in data:
    # Extract the article text from the JSON data
    input_text = article["content"]

    # Encode the input text and generate a summary
    inputs = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=512, padding='max_length', truncation=True).to(device)
    summary_ids = model.generate(inputs,
                                    num_beams=int(2),
                                    no_repeat_ngram_size=3,
                                    length_penalty=2.0,
                                    min_length=250,
                                    max_length=500,
                                    early_stopping=True)
    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    
    # Replace the summary in the JSON data with the generated summary
    article["summary"] = output

    # Increment the articles_processed counter
    articles_processed += 1
    print(f"Processed article {articles_processed}/{len(data)}")
# Save the updated data to the same file
with open('international_articlesCLEANED.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

