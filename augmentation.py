from transformers import AutoModelWithLMHead, AutoTokenizer
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics import f1_score
import pandas as pd

# Load the original dataset
squad_df = pd.read_json("SQUAD_TRANSLATED_dataset.json")

# Choose 50 random questions from the original dataset
sampled_df = squad_df.sample(n=300, random_state=42)

tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-small-finetuned-quora-for-paraphrasing")
model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-small-finetuned-quora-for-paraphrasing")

def paraphrase(text, max_length=128):
    input_ids = tokenizer.encode(text, return_tensors="pt", add_special_tokens=True)
    generated_ids = model.generate(input_ids=input_ids, num_return_sequences=5, num_beams=5, max_length=max_length, no_repeat_ngram_size=2, repetition_penalty=3.5, length_penalty=1.0, early_stopping=True)
    preds = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]
    return preds

# Define the number of augmented questions to generate
num_aug = 5

# Augment the selected questions
augmented_questions = []
true_labels = []
for _, row in sampled_df.iterrows():
    for i in range(num_aug):
        # Generate paraphrases
        paraphrases = paraphrase(row['question'])
        # Add original question to the list of paraphrases
        paraphrases.append(row['question'])
        # Append all paraphrases with their original question to the list
        augmented_questions.extend([(p, row['question']) for p in paraphrases])
        # Append true labels (1 for correct, 0 for incorrect)
        true_labels.extend([1] * (len(paraphrases) - 1) + [0])

# Load the sentence transformer model
model = SentenceTransformer('sentence-transformers/multi-qa-distilbert-cos-v1')

# Encode all questions in the original dataset
question_embeddings = model.encode(list(squad_df['question']))

# Define a function to retrieve the closest question
def retrieve_closest_question(query, embeddings, original_questions):
    query_embedding = model.encode(query)
    scores = util.dot_score(query_embedding, embeddings)[0].tolist()
    idx = scores.index(max(scores))
    return original_questions[idx]

# Evaluate the model on the augmented questions
correct = 0
for augmented_question, original_question in augmented_questions:
    closest_question = retrieve_closest_question(augmented_question, question_embeddings, list(squad_df['question']))
    if closest_question == original_question:
        correct += 1

# Compute the accuracy
accuracy = correct / len(augmented_questions)
print(f"Accuracy: {accuracy}")

# Compute the F1 score
f1 = f1_score(true_labels, [1] * correct + [0] * (len(augmented_questions) - correct))
print(f"F1 Score: {f1}")
