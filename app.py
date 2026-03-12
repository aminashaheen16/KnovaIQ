import streamlit as st
import subprocess
import os
import json
from PyPDF2 import PdfReader

st.set_page_config(page_title="KnovaIQ", page_icon="💼", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
.stApp { background: #f3f3f3; color: #181818; }
section[data-testid="stSidebar"] { background: #032d60 !important; border-right: none !important; }
section[data-testid="stSidebar"] * { color: #fff !important; }
section[data-testid="stSidebar"] .stRadio label { background: rgba(255,255,255,0.08) !important; border: none !important; border-radius: 6px !important; color: #c9d9f0 !important; padding: 0.55rem 1rem !important; margin-bottom: 2px !important; }
section[data-testid="stSidebar"] .stRadio label:hover { background: rgba(255,255,255,0.15) !important; color: #fff !important; }
.page-title { font-size: 1.75rem; font-weight: 700; color: #032d60; margin-bottom: 0.3rem; }
.page-subtitle { font-size: 0.9rem; color: #706e6b; margin-bottom: 2rem; }
.card { background: #fff; border: 1px solid #dddbda; border-radius: 8px; padding: 1.5rem 2rem; margin-bottom: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.06); }
.card-header { font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: #706e6b; margin-bottom: 1.2rem; padding-bottom: 0.8rem; border-bottom: 1px solid #f3f2f2; }
.answer-card { background: #fff; border: 1px solid #dddbda; border-radius: 8px; padding: 1.5rem 2rem; margin-top: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.06); line-height: 1.8; color: #3e3e3c; }
.answer-label { display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; padding: 0.3rem 0.8rem; border-radius: 4px; margin-bottom: 1rem; }
.label-books { background: #e8f5e9; color: #2e7d32; }
.label-support { background: #e3f2fd; color: #1565c0; }
.label-resumes { background: #fce4ec; color: #880e4f; }
.label-cv { background: #fff8e1; color: #f57f17; }
.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
.stat-card { background: #fff; border: 1px solid #dddbda; border-radius: 8px; padding: 1.2rem 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.04); }
.stat-label { font-size: 0.75rem; color: #706e6b; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
.stat-value { font-size: 1.8rem; font-weight: 700; color: #032d60; margin: 0.3rem 0; }
.stat-sub { font-size: 0.78rem; color: #00a1e0; }
.cv-item { background: #fff; border: 1px solid #dddbda; border-left: 4px solid #00a1e0; border-radius: 6px; padding: 1rem 1.2rem; margin-bottom: 0.6rem; }
.cv-item-name { font-weight: 600; color: #032d60; font-size: 0.95rem; }
.cv-item-date { font-size: 0.78rem; color: #706e6b; margin-top: 0.2rem; }
.stTextArea textarea { background: #fff !important; border: 1px solid #dddbda !important; border-radius: 6px !important; color: #181818 !important; font-size: 0.95rem !important; padding: 0.8rem 1rem !important; }
.stTextArea textarea:focus { border-color: #00a1e0 !important; box-shadow: 0 0 0 3px rgba(0,161,224,0.15) !important; }
.stButton > button { background: #0070d2 !important; color: #fff !important; border: none !important; border-radius: 4px !important; font-weight: 600 !important; font-size: 0.9rem !important; padding: 0.6rem 1.8rem !important; }
.stButton > button:hover { background: #005fb2 !important; }
.kb-item { margin: 0.3rem 0.8rem; padding: 0.6rem 0.8rem; background: rgba(255,255,255,0.06); border-radius: 6px; border-left: 3px solid #00a1e0; }
.kb-item-title { font-size: 0.78rem; font-weight: 600; color: #fff; }
.kb-item-sub { font-size: 0.72rem; color: #8aabcf; margin-top: 0.1rem; }
hr { border-color: #f3f2f2 !important; margin: 1.5rem 0 !important; }
div[data-testid="stRadio"] > div { gap: 3px !important; }
</style>
""", unsafe_allow_html=True)

CV_FOLDER = "saved_cvs"
CV_INDEX = "saved_cvs/index.json"
os.makedirs(CV_FOLDER, exist_ok=True)
if not os.path.exists(CV_INDEX):
    with open(CV_INDEX, 'w') as f:
        json.dump([], f)

def load_cv_index():
    with open(CV_INDEX, 'r') as f:
        return json.load(f)

def save_cv_to_index(name, filename, text_preview):
    from datetime import datetime
    index = load_cv_index()
    index.append({"name": name, "filename": filename, "date": datetime.now().strftime("%b %d, %Y · %H:%M"), "preview": text_preview[:200]})
    with open(CV_INDEX, 'w') as f:
        json.dump(index, f, ensure_ascii=False)

def read_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "".join([p.extract_text() or "" for p in reader.pages])

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style='padding: 1.5rem 1.2rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 1rem;'>
        <div style='font-size:1.5rem; font-weight:800; color:#fff; letter-spacing:-0.02em;'>Knova<span style='color:#00a1e0;'>IQ</span></div>
        <div style='font-size:0.7rem; color:#8aabcf; margin-top:0.2rem; letter-spacing:0.1em; text-transform:uppercase;'>AI Knowledge Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='color:#8aabcf; font-size:0.65rem; font-weight:600; text-transform:uppercase; letter-spacing:0.1em; padding: 0.5rem 1rem;'>Navigation</div>", unsafe_allow_html=True)
    mode = st.radio("", ["📚 Study Assistant", "🛠️ Tech Support", "👔 HR & Recruitment", "📄 CV Analyzer"], label_visibility="collapsed")

    st.markdown("<div style='color:#8aabcf; font-size:0.65rem; font-weight:600; text-transform:uppercase; letter-spacing:0.1em; padding: 0.5rem 1rem; margin-top:0.5rem;'>Knowledge Base</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='kb-item'><div class='kb-item-title'>📖 Books</div><div class='kb-item-sub'>Hands-On ML · 640 chunks</div></div>
    <div class='kb-item'><div class='kb-item-title'>🎫 Support Tickets</div><div class='kb-item-sub'>1,896 resolved cases</div></div>
    <div class='kb-item'><div class='kb-item-title'>👔 Resume DB</div><div class='kb-item-sub'>100 candidate profiles</div></div>
    <div class='kb-item'><div class='kb-item-title'>📄 My CVs</div><div class='kb-item-sub'>{len(load_cv_index())} saved files</div></div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    if st.button("🔄 Rebuild Index", use_container_width=True):
        with st.spinner("Building..."):
            r = subprocess.run(["python", "ingestion.py"], capture_output=True, text=True, cwd=os.getcwd())
            st.success("✅ Done!") if r.returncode == 0 else st.error(r.stderr[:200])

    st.markdown("<div style='padding:1.5rem 1rem 0; color:#8aabcf; font-size:0.7rem;'>Powered by Groq · Llama 3.3 70B</div>", unsafe_allow_html=True)


# STUDY
if "Study" in mode:
    st.markdown('<div class="page-title">Study Assistant 📚</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Ask anything from the Hands-On Machine Learning book and get instant answers.</div>', unsafe_allow_html=True)
    st.markdown("""<div class='stat-grid'>
        <div class='stat-card'><div class='stat-label'>Book Chapters</div><div class='stat-value'>19</div><div class='stat-sub'>Hands-On ML</div></div>
        <div class='stat-card'><div class='stat-label'>Text Chunks</div><div class='stat-value'>640</div><div class='stat-sub'>Indexed & searchable</div></div>
        <div class='stat-card'><div class='stat-label'>AI Model</div><div class='stat-value'>Llama</div><div class='stat-sub'>3.3 70B · Groq</div></div>
        <div class='stat-card'><div class='stat-label'>Search Method</div><div class='stat-value'>TF-IDF</div><div class='stat-sub'>+ RAG pipeline</div></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='card'><div class='card-header'>Ask a Question</div>", unsafe_allow_html=True)
    question = st.text_area("", placeholder="e.g. What is gradient descent? How does backpropagation work?", height=130, key="sq", label_visibility="collapsed")
    col1, _ = st.columns([1, 4])
    with col1:
        btn = st.button("🔍 Search & Answer", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    if btn and question.strip():
        with st.spinner("Searching the book..."):
            r = subprocess.run(["python", "query_runner.py", "books", question], capture_output=True, text=True, cwd=os.getcwd())
        if r.returncode == 0:
            st.markdown('<div class="answer-card"><span class="answer-label label-books">📖 Answer from Book</span>', unsafe_allow_html=True)
            st.markdown(r.stdout)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error(r.stderr[:400])

# SUPPORT
elif "Support" in mode:
    st.markdown('<div class="page-title">Tech Support 🛠️</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Describe your technical issue and get solutions from 1,896 resolved support cases.</div>', unsafe_allow_html=True)
    st.markdown("""<div class='stat-grid'>
        <div class='stat-card'><div class='stat-label'>Total Cases</div><div class='stat-value'>1,896</div><div class='stat-sub'>Resolved tickets</div></div>
        <div class='stat-card'><div class='stat-label'>Categories</div><div class='stat-value'>6</div><div class='stat-sub'>Issue types</div></div>
        <div class='stat-card'><div class='stat-label'>Avg Resolution</div><div class='stat-value'>74m</div><div class='stat-sub'>Response time</div></div>
        <div class='stat-card'><div class='stat-label'>Success Rate</div><div class='stat-value'>94%</div><div class='stat-sub'>Cases resolved</div></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='card'><div class='card-header'>Describe Your Issue</div>", unsafe_allow_html=True)
    issue = st.text_area("", placeholder="e.g. My WiFi keeps disconnecting every few minutes...", height=130, key="tq", label_visibility="collapsed")
    col1, _ = st.columns([1, 4])
    with col1:
        btn2 = st.button("🔧 Find Solution", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    if btn2 and issue.strip():
        with st.spinner("Searching knowledge base..."):
            r = subprocess.run(["python", "query_runner.py", "support", issue], capture_output=True, text=True, cwd=os.getcwd())
        if r.returncode == 0:
            st.markdown('<div class="answer-card"><span class="answer-label label-support">🎫 Solution from Knowledge Base</span>', unsafe_allow_html=True)
            st.markdown(r.stdout)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error(r.stderr[:400])

# HR
elif "HR" in mode:
    st.markdown('<div class="page-title">HR & Recruitment 👔</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Enter a job description and instantly find the best matching candidates.</div>', unsafe_allow_html=True)
    st.markdown("""<div class='stat-grid'>
        <div class='stat-card'><div class='stat-label'>Candidates</div><div class='stat-value'>100</div><div class='stat-sub'>Indexed profiles</div></div>
        <div class='stat-card'><div class='stat-label'>Job Categories</div><div class='stat-value'>25+</div><div class='stat-sub'>Fields covered</div></div>
        <div class='stat-card'><div class='stat-label'>Match Method</div><div class='stat-value'>RAG</div><div class='stat-sub'>Semantic search</div></div>
        <div class='stat-card'><div class='stat-label'>Analysis By</div><div class='stat-value'>AI</div><div class='stat-sub'>Llama 3.3 70B</div></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='card'><div class='card-header'>Job Description</div>", unsafe_allow_html=True)
    job = st.text_area("", placeholder="e.g. We are looking for a Senior Python Developer with 3+ years of ML experience...", height=150, key="hq", label_visibility="collapsed")
    col1, _ = st.columns([1, 4])
    with col1:
        btn3 = st.button("👔 Find Candidates", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    if btn3 and job.strip():
        with st.spinner("Analyzing candidate profiles..."):
            r = subprocess.run(["python", "query_runner.py", "resumes", job], capture_output=True, text=True, cwd=os.getcwd())
        if r.returncode == 0:
            st.markdown('<div class="answer-card"><span class="answer-label label-resumes">👔 Top Candidates</span>', unsafe_allow_html=True)
            st.markdown(r.stdout)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error(r.stderr[:400])

# CV ANALYZER
elif "CV" in mode:
    st.markdown('<div class="page-title">CV Analyzer 📄</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Upload your CV and get a full AI-powered career analysis with best job matches.</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        st.markdown("<div class='card'><div class='card-header'>Upload CV</div>", unsafe_allow_html=True)
        uploaded = st.file_uploader("", type=["pdf"], key="cu", label_visibility="collapsed")
        name_input = st.text_input("", placeholder="Your name (optional)", key="cn", label_visibility="collapsed")
        if uploaded:
            st.markdown(f"<div style='color:#0070d2; font-size:0.85rem; margin:0.5rem 0;'>✅ {uploaded.name}</div>", unsafe_allow_html=True)
            c1, c2, _ = st.columns([1, 1, 2])
            with c1:
                a_btn = st.button("🔍 Analyze", use_container_width=True)
            with c2:
                s_btn = st.button("💾 Save", use_container_width=True)
            if a_btn:
                with st.spinner("Analyzing your CV..."):
                    cv_text = read_pdf_text(uploaded)
                    cv_short = " ".join(cv_text.split()[:800])
                    r = subprocess.run(["python", "query_runner.py", "analyze_cv", cv_short], capture_output=True, text=True, cwd=os.getcwd())
                if r.returncode == 0:
                    st.markdown('<div class="answer-card"><span class="answer-label label-cv">📄 CV Analysis Report</span>', unsafe_allow_html=True)
                    st.markdown(r.stdout)
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error(r.stderr[:400])
            if s_btn:
                cv_text = read_pdf_text(uploaded)
                name = name_input.strip() or uploaded.name.replace(".pdf", "")
                with open(os.path.join(CV_FOLDER, uploaded.name), "wb") as f:
                    f.write(uploaded.getbuffer())
                save_cv_to_index(name, uploaded.name, cv_text)
                st.success(f"✅ Saved as: {name}")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        saved = load_cv_index()
        st.markdown(f"<div class='card'><div class='card-header'>Saved CVs ({len(saved)})</div>", unsafe_allow_html=True)
        if not saved:
            st.markdown("<div style='color:#706e6b; font-size:0.85rem; text-align:center; padding:2rem 0;'>No CVs saved yet.</div>", unsafe_allow_html=True)
        else:
            for cv in reversed(saved):
                st.markdown(f"""<div class='cv-item'>
                    <div class='cv-item-name'>📄 {cv['name']}</div>
                    <div class='cv-item-date'>{cv['date']}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
