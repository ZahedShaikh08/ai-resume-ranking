from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
import string

# Download stopwords once
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

STOP_WORDS = set(stopwords.words('english') + list(string.punctuation))

def preprocess(text):
    # Simple preprocessing: lowercase, remove stopwords/punctuation
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    words = text.split()
    return " ".join([w for w in words if w not in STOP_WORDS and len(w) > 2])

def rank_resumes(jd_text, resume_data):
    # Preprocess JD text
    jd_processed = preprocess(jd_text)
    
    # Prepare documents for ranking
    documents = [jd_processed]
    resume_texts = []
    
    for resume in resume_data:
        processed = preprocess(resume["text"])
        documents.append(processed)
        resume_texts.append(resume)
    
    # TF-IDF Similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    tfidf_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # BM25 Ranking
    tokenized_corpus = [doc.split() for doc in documents[1:]]
    bm25 = BM25Okapi(tokenized_corpus)
    bm25_scores = bm25.get_scores(documents[0].split())
    
    # Normalize scores
    bm25_scores = (bm25_scores - np.min(bm25_scores)) / (np.max(bm25_scores) - np.min(bm25_scores))
    
    # Hybrid scoring (TF-IDF 60% + BM25 40%)
    hybrid_scores = (0.6 * tfidf_scores) + (0.4 * bm25_scores)
    
    # Combine results
    results = []
    for i, resume in enumerate(resume_texts):
        results.append({
            "name": resume["name"],
            "score": round(hybrid_scores[i] * 100, 1),
            "path": resume["path"]
        })
    
    # Sort by hybrid score
    return sorted(results, key=lambda x: x["score"], reverse=True)