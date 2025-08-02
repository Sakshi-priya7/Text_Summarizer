from transformers import pipeline
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

def plot_dual_wordcloud(original_text, summary_text):
    wc1 = WordCloud(width=800, height=400, background_color='black', colormap='Pastel1', collocations=False).generate(original_text)
    wc2 = WordCloud(width=800, height=400, background_color='black', colormap='Pastel2', collocations=False).generate(summary_text)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ☁️ Word Cloud: Original Text")
        fig1, ax1 = plt.subplots(figsize=(5, 3))
        ax1.imshow(wc1, interpolation='bilinear')
        ax1.axis("off")
        st.pyplot(fig1)

    with col2:
        st.markdown("### 🤖 Word Cloud: AI Summary")
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        ax2.imshow(wc2, interpolation='bilinear')
        ax2.axis("off")
        st.pyplot(fig2)


summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def abstractive_summary(text, word_limit=150, tone="neutral"):
    # Tone prompt
    if tone == "formal":
        prompt = "Summarize the text formally:\n"
    elif tone == "casual":
        prompt = "Summarize the text casually:\n"
    elif tone == "simple":
        prompt = "Summarize the text in simple language:\n"
    else:
        prompt = ""

    full_prompt = prompt + text

    # Approximate token count (word_limit * 1.3)
    max_tokens = int(word_limit * 1.3)
    min_tokens = int(word_limit * 1.0)

    summary = summarizer(full_prompt, max_length=max_tokens, min_length=min_tokens, do_sample=False)
    return summary[0]['summary_text']

def generate_bullet_points(summary):
    import re
    # Break into sentence-like segments (for readability)
    sentences = re.split(r'(?<=[.?!])\s+', summary.strip())
    bullets = [f"• {s}" for s in sentences if len(s.strip()) > 0]
    return '\n'.join(bullets)

def get_summary_stats(text):
    words = re.findall(r'\w+', text)
    sentences = re.split(r'[.!?]', text)
    keywords = Counter(words)
    most_common = keywords.most_common(5)

    return {
        "Word Count": len(words),
        "Sentence Count": len([s for s in sentences if s.strip()]),
        "Top Keywords": [word for word, _ in most_common]
    }
