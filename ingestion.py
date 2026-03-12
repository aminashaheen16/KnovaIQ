import os
import pickle
import pandas as pd
from PyPDF2 import PdfReader

def read_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def build_books_index(folder_path="data/books", index_name="books_index"):
    all_chunks = []
    all_sources = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if filename.endswith(".pdf"):
            print(f"Reading {filename}...")
            text = read_pdf(filepath)
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
            all_sources.extend([filename] * len(chunks))
    if not all_chunks:
        print("No PDF found!")
        return
    with open(f"{index_name}_chunks.pkl", 'wb') as f:
        pickle.dump({'chunks': all_chunks, 'sources': all_sources}, f)
    print(f"✅ Books index saved! ({len(all_chunks)} chunks)")

def build_support_index(filepath="data/support/tech_support_dataset.csv", index_name="support_index"):
    df = pd.read_csv(filepath)
    records, sources = [], []
    for _, row in df.iterrows():
        text = f"Issue: {row['Customer_Issue']}\nSolution: {row['Tech_Response']}\nCategory: {row['Issue_Category']}"
        records.append(text)
        sources.append(f"{row['Issue_Category']} - {row['Conversation_ID']}")
    with open(f"{index_name}_chunks.pkl", 'wb') as f:
        pickle.dump({'chunks': records, 'sources': sources}, f)
    print(f"✅ Support index saved! ({len(records)} records)")

def build_resumes_index(filepath="data/resumes/Resume.csv", index_name="resumes_index"):
    df = pd.read_csv(filepath).head(100)
    records, sources = [], []
    text_col = 'Resume_str' if 'Resume_str' in df.columns else df.columns[0]
    for i, row in df.iterrows():
        words = str(row[text_col]).split()[:200]
        text = " ".join(words)
        category = str(row.get('Category', f'Resume_{i}'))
        records.append(text)
        sources.append(f"{category}_{i}")
    with open(f"{index_name}_chunks.pkl", 'wb') as f:
        pickle.dump({'chunks': records, 'sources': sources}, f)
    print(f"✅ Resumes index saved! ({len(records)} records)")

build_books_index()
build_support_index()
build_resumes_index()
