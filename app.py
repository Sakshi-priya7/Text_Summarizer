import streamlit as st
import io
from summarizer import abstractive_summary
from utils import read_pdf, read_docx, clean_text

st.set_page_config(page_title="Text Summarizer", layout="wide")
st.title("Text Summarizer 📝")

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

if text:
    st.markdown("---")
    st.markdown("🔍 **Summarization:**")
    length = st.slider("Summary Length (approx. words)", min_value=50, max_value=500, step=10, value=150)

    tone = st.selectbox("Select Tone: ", ["Neutral", "Formal", "Casual", "Simple"])

    if st.button("🚀 Generate Summary"):
        cleaned = clean_text(text)
        with st.spinner("Summarizing..."):
            summary = abstractive_summary(cleaned, word_limit=length, tone=tone.lower())
        st.subheader("📋 Your Summary")
        st.success(summary)
        # Download as TXT
        st.download_button(
            label="📄 Download Summary as .txt",
            data=summary,
            file_name="summary.txt",
            mime="text/plain"
        )

# Custom dark theme CSS
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
