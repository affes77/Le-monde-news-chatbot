import json
from sentence_transformers import SentenceTransformer
import pickle

with open("SQUAD_TRANSLATED_dataset.json", "r", encoding='utf-8') as f:
    dataset = json.load(f)

docs = []
for i, data in enumerate(dataset):
    question = data["question"]
    answer = data["answer"]
    docs.append((question, answer))

#Load the model
model = SentenceTransformer('sentence-transformers/multi-qa-distilbert-cos-v1')

doc_emb = model.encode(docs)

with open("doc_emb.pickle", "wb") as f:
    pickle.dump(doc_emb, f)

with open('docs_Q&A.json', 'w', encoding='utf-8') as f:
    json.dump(docs, f, ensure_ascii=False, indent=4)

