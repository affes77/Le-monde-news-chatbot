from sentence_transformers import SentenceTransformer, util
import json
import pickle
import torch

# Set device to use CUDA if available
device = "cuda" if torch.cuda.is_available() else "cpu"


# Load model
model = SentenceTransformer('sentence-transformers/multi-qa-distilbert-cos-v1', device=device)

# Load docs
with open("docs_Q&A.json", "r", encoding='utf-8') as f:
    docs = json.load(f)

with open("doc_emb.pickle", "rb") as f:
    doc_emb = pickle.load(f)

while True:
    # Get user input
    query = input("Enter a question or 'stop' to exit: ")

    # Check if user wants to stop
    if query.lower() == "stop":
        break

    # Encode query
    query_emb = model.encode(query)

    # Compute dot score between query and all document embeddings
    scores = util.dot_score(query_emb, doc_emb)[0].tolist()

    # Combine docs, scores, and answers
    doc_score_pairs = list(zip(docs, scores))
    doc_score_answer_triplets = [(doc, score, answer) for (doc, answer), score in doc_score_pairs]

    # Sort by decreasing score
    doc_score_answer_triplets = sorted(doc_score_answer_triplets, key=lambda x: x[1], reverse=True)

    # Get answer to top-scoring question
    top_question, top_score, top_answer = doc_score_answer_triplets[0]

    # Output top-scoring question, score, and answer
    print("Top question: ", top_question)
    print("Score: ", top_score)
    print("Answer: ", top_answer)
