import streamlit as st
from summarizer import (
    abstractive_summary,
    generate_bullet_points,
    get_summary_stats,
    plot_dual_wordcloud
)
from utils import read_pdf, read_docx, clean_text

# Initialize session state
if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'history_display' not in st.session_state:
    st.session_state['history_display'] = ""

# App config
st.set_page_config(page_title="Text Summarizer", layout="wide")
st.title("📝 Text Summarizer")

# --- File Upload & Text Input ---
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
elif text_input:
    text = text_input

# --- Main Summarization UI ---
if text:
    st.markdown("---")
    st.markdown("🔍 **Summarization Settings:**")
    length = st.slider("Summary Length (approx. words)", 50, 500, step=10, value=150)
    tone = st.selectbox("Select Tone: ", ["Neutral", "Formal", "Casual", "Simple"])

    st.markdown("### 🧠 Ready to Summarize?")
    if st.button("🚀 Generate Summary"):
        cleaned = clean_text(text)
        with st.spinner("Summarizing..."):
            summary = abstractive_summary(cleaned, word_limit=length, tone=tone.lower())

        st.session_state['history'].append(summary)
        st.session_state['history_display'] = summary

# --- Summary Output ---
if st.session_state['history_display']:
    summary = st.session_state['history_display']

    st.subheader("📋 Your Summary")
    st.markdown(f"<div id='summary-text'>{summary}</div>", unsafe_allow_html=True)

    # Copy button
    st.markdown(
        f"""
        <button onclick="navigator.clipboard.writeText(document.getElementById('summary-text').innerText)"
                style="background-color:#00ffae;color:black;padding:10px 20px;
                       border:none;border-radius:10px;font-weight:bold;
                       margin-top:10px;cursor:pointer;">
            📋 Copy Summary to Clipboard
        </button>
        """,
        unsafe_allow_html=True
    )

    # Download summary
    st.download_button("📄 Download Summary as .txt", data=summary, file_name="summary.txt", mime="text/plain")

    # Bullet points
    st.subheader("🔸 Bullet Points")
    bullets = generate_bullet_points(summary)
    bullet_html = "<ul>" + "".join([f"<li>{b}</li>" for b in bullets]) + "</ul>"
    st.markdown(bullet_html, unsafe_allow_html=True)

    # Stats
    st.subheader("📈 Summary Stats")
    stats = get_summary_stats(summary)
    st.write(f"📝 **Word Count:** {stats['Word Count']}")
    st.write(f"📏 **Sentence Count:** {stats['Sentence Count']}")
    st.write(f"🔑 **Top Keywords:** {', '.join(stats['Top Keywords'])}")

    # Word Cloud
    st.subheader("📊 Keyword Comparison")
    plot_dual_wordcloud(clean_text(text), summary)

# --- Sidebar History ---
with st.sidebar:
    st.subheader("🕓 Summary History")
    if st.session_state['history']:
        selected = st.selectbox("📚 Select Previous Summary", options=st.session_state['history'][::-1])
        if selected:
            st.session_state['history_display'] = selected
    else:
        st.info("No summaries generated yet.")

# --- Dark Mode Styling ---
dark_css = """
<style>
body {
    background-color: #0d1117;
    color: #c9d1d9;
}
.stApp {
    background-color: #0d1117;
}
h1, h2, h3, h4, h5, h6, .stMarkdown, .stTextInput label, .stSelectbox label, .stRadio label, .stSlider label {
    color: #c9d1d9 !important;
}
button {
    background-color: #238636 !important;
    color: white !important;
}
.stDownloadButton {
    border: 1px solid #30363d;
}
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)
