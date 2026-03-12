# KnovaIQ - AI-Powered Knowledge Platform

A Retrieval-Augmented Generation (RAG) system that transforms static documents into an intelligent conversational AI assistant.

## Features
- Study Assistant: Ask anything from the Hands-On ML book
- Tech Support: Get solutions from 1,896 resolved tickets  
- HR and Recruitment: Find best candidates from resume database
- CV Analyzer: Upload CV and get full career analysis

## Tech Stack
- LLM: Llama 3.3 70B via Groq API
- Search: TF-IDF + Cosine Similarity
- UI: Streamlit
- PDF Processing: PyPDF2

## Quick Start
1. Clone the repo
2. Create virtual environment: python -m venv venv
3. Activate: source venv/bin/activate
4. Install: pip install streamlit scikit-learn PyPDF2 pandas numpy groq
5. Add Groq API key in query_runner.py
6. Build index: python ingestion.py
7. Run: streamlit run app.py

## Author
Amina Abdelaziz Gabr Shaheen - AI Student 2026
