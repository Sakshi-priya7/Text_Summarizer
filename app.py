# ✅ FINAL WORKING VERSION: app.py
import streamlit as st
from summarizer import (
    abstractive_summary,
    generate_bullet_points,
    get_summary_stats,
    plot_dual_wordcloud
)
from utils import read_pdf, read_docx, clean_text

# Session Setup
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'selected_summary' not in st.session_state:
    st.session_state['selected_summary'] = ""

# Page Setup
st.set_page_config(page_title="Text Summarizer", layout="wide")
st.title("📝 Text Summarizer")

# Upload Section
uploaded_file = st.file_uploader("Upload a .txt, .pdf, or .docx file", type=["txt", "pdf", "docx"])
text_input = st.text_area("Or paste your text here:", height=200)

text = ""
if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        text = read_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        text = read_docx(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
if not text and text_input:
    text = text_input

# Main UI
if text:
    st.markdown("---")
    st.markdown("🔍 **Summarization Settings:**")

    length = st.slider("Summary Length (approx. words)", 50, 500, step=10, value=150)
    tone = st.selectbox("Select Tone:", ["Neutral", "Formal", "Casual", "Simple"])

    if st.button("🚀 Generate Summary"):
        cleaned = clean_text(text)
        with st.spinner("Summarizing..."):
            summary = abstractive_summary(cleaned, word_limit=length, tone=tone.lower())
        st.session_state['selected_summary'] = summary
        st.session_state['history'].append(summary)

# Display Summary
if st.session_state['selected_summary']:
    summary = st.session_state['selected_summary']
    st.subheader("📋 Your Summary")
    st.success(summary)

    # Copy to Clipboard Styled Button
    if st.button("📋 Copy Summary to Clipboard"):
        st.code(summary, language="")
        st.toast("Copied to clipboard!")

    # Download Button
    st.download_button("📄 Download Summary", summary, file_name="summary.txt", mime="text/plain")

    # Bullet Points (Shortened)
    st.subheader("🔸 Key Bullet Points")
    bullets = generate_bullet_points(summary)
    for point in bullets:
        st.markdown(f"- {point}")

    # Stats
    st.subheader("📈 Summary Stats")
    stats = get_summary_stats(summary)
    st.write(f"📝 **Word Count:** {stats['Word Count']}")
    st.write(f"📏 **Sentence Count:** {stats['Sentence Count']}")
    st.write(f"🔑 **Top Keywords:** {', '.join(stats['Top Keywords'])}")

    # Word Clouds
    st.subheader("📊 Keyword Comparison")
    plot_dual_wordcloud(clean_text(text), summary)

# Sidebar History (Session-Persisted)
with st.sidebar:
    st.subheader("🕓 Summary History")
    if st.session_state['history']:
        selected = st.selectbox("Select a Summary:", st.session_state['history'][::-1])
        if selected != st.session_state['selected_summary']:
            st.session_state['selected_summary'] = selected
    else:
        st.info("No summaries generated yet.")

# Custom Dark CSS
st.markdown("""
<style>
body, .stApp { background-color: #0d1117; color: #c9d1d9; }
h1, h2, h3, h4, h5, h6, .stMarkdown, label, .stTextInput label {
    color: #c9d1d9 !important;
}
button { background-color: #238636 !important; color: white !important; }
.stDownloadButton { border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)
