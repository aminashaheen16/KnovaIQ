import sys
import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def search(query, index_name, top_k=5):
    with open(f"{index_name}_chunks.pkl", 'rb') as f:
        data = pickle.load(f)
    chunks, sources = data['chunks'], data['sources']
    vectorizer = TfidfVectorizer(max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(chunks)
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, tfidf_matrix)[0]
    top_indices = np.argsort(scores)[-top_k:][::-1]
    return [(chunks[i], sources[i]) for i in top_indices]

mode = sys.argv[1]
query = sys.argv[2]

if mode == "books":
    results = search(query, "books_index")
    context = "\n\n".join([f"[Source: {s}]\n{c}" for c, s in results])
    prompt = f"You are a study assistant for Hands-On Machine Learning book. Answer clearly and concisely:\n\nCONTENT:\n{context}\n\nQUESTION: {query}\n\nANSWER:"

elif mode == "support":
    results = search(query, "support_index")
    context = "\n\n".join([f"[{s}]\n{c}" for c, s in results])
    prompt = f"You are a tech support assistant. Give a clear step-by-step solution:\n\nPAST CASES:\n{context}\n\nCUSTOMER ISSUE: {query}\n\nSOLUTION:"

elif mode == "resumes":
    results = search(query, "resumes_index")
    context = "\n\n".join([f"[Candidate: {s}]\n{c}" for c, s in results])
    prompt = f"You are an expert HR recruiter. Analyze these candidates and rank them:\n\nJOB DESCRIPTION:\n{query}\n\nCANDIDATES:\n{context}\n\nANALYSIS:"

elif mode == "analyze_cv":
    prompt = f"""You are an expert career coach. Analyze this CV and provide:

1. 📋 SUMMARY: Brief overview of the candidate
2. 💪 KEY SKILLS: Top technical and soft skills
3. 🎯 BEST JOB MATCHES: Top 5 job roles this person is suited for
4. ⭐ STRENGTHS: What makes this candidate stand out
5. 📈 IMPROVEMENT AREAS: Skills to develop
6. 💡 CAREER ADVICE: Specific actionable advice

CV CONTENT:
{query}

ANALYSIS:"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1024
)
print(response.choices[0].message.content)
