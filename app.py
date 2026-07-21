import streamlit as st
import pyperclip
from summarizer import (
    abstractive_summary,
    generate_bullet_points,
    get_summary_stats,
    plot_dual_wordcloud
)
from utils import read_pdf, read_docx, clean_text

# Page Setup
st.set_page_config(page_title="Text Summarizer", layout="wide")
st.title("📝 Text Summarizer")

if "show_clear_modal" not in st.session_state:
    st.session_state["show_clear_modal"] = False

# Upload Section
uploaded_file = st.file_uploader("Upload a .txt, .pdf, or .docx file", type=["txt", "pdf", "docx"])

def clear_text_input():
    st.session_state["text_box"] = ""

# 🆕 Add text input + clear text button side-by-side
col1, col2 = st.columns([6, 1])

with col1:
    text_input = st.text_area("Or paste your text here:", height=200, key="text_box")

with col2:
    st.button("❌ Clear Text", on_click=clear_text_input)

text = text_input or ""

if uploaded_file:
    if uploaded_file.name.endswith(".pdf"):
        text = read_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        text = read_docx(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
elif text_input:
    text = text_input

# Initialize summary variable
summary = ""

# Main UI

st.markdown("---")
st.markdown("🔍 **Summarization Settings:**")

length = st.slider("Summary Length (approx. words)", 50, 500, step=10, value=150)
tone = st.selectbox("Select Tone:", ["Neutral", "Formal", "Casual", "Simple"])

if st.button("🚀 Generate Summary"):
    cleaned = clean_text(text)
    with st.spinner("Summarizing..."):
        summary = abstractive_summary(cleaned, word_limit=length, tone=tone.lower())
    st.session_state["summary"] = summary

# Display summary if available
if "summary" in st.session_state:
    summary = st.session_state["summary"]

    st.subheader("📋 Your Summary")
    st.success(summary)

    # Show in a read-only textarea
    st.text_area("📄 Copy from here", summary, height=150)

    # "Copy Summary" Button (works locally with pyperclip)
    if st.button("📋 Copy Summary"):
        try:
            pyperclip.copy(summary)
            st.success("✅ Summary copied to clipboard!")
        except Exception:
            st.warning("⚠️ Clipboard copy not supported in Streamlit Cloud. Please copy manually.")

    # Download Button
    st.download_button("📄 Download Summary", summary, file_name="summary.txt", mime="text/plain")

    # Bullet Points
    st.subheader("🔸 Bullet Points")
    bullets = generate_bullet_points(summary)
    bullet_html = "<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>"
    st.markdown(bullet_html, unsafe_allow_html=True)

    # Stats
    st.subheader("📈 Summary Stats")
    stats = get_summary_stats(summary)
    st.write(f"📝 Word Count: {stats['Word Count']}")
    st.write(f"📏 Sentence Count: {stats['Sentence Count']}")
    st.write(f"🔑 Top Keywords: {', '.join(stats['Top Keywords'])}")

    # Word Clouds
    st.subheader("📊 Keyword Comparison")
    plot_dual_wordcloud(clean_text(text), summary)

    # Clear All Button
    if st.button("🗑️ Clear All"):
        st.session_state["show_clear_modal"] = True

# Display modal-like confirmation
if st.session_state.get("show_clear_modal", False):
    st.markdown("### Are you sure you want to clear everything?")
    st.markdown("This will remove all uploaded files, text, and summaries.")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("✅ Yes, Clear Everything"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    with col2:
        if st.button("❌ Cancel"):
            st.session_state["show_clear_modal"] = False
            st.rerun()

# Dark Mode CSS + Custom Clear Button Style
st.markdown("""
<style>
body, .stApp {
    background-color: #0d1117;
    color: #c9d1d9;
}
h1, h2, h3, h4, h5, h6, .stMarkdown, label, .stTextInput label {
    color: #c9d1d9 !important;
}
button {
    background-color: #238636 !important;
    color: white !important;
    padding: 6px 10px !important;
    font-size: 13px !important;
}
.stDownloadButton {
    border: 1px solid #30363d;
}

/* 🔴 Custom Red Style for "Clear All" Button */
button[kind="secondary"] {
    background-color: #DA3633 !important;
    color: white !important;
    border: none;
}
</style>
""", unsafe_allow_html=True)
