from transformers import pipeline
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

# Load the abstractive summarization model (only once)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# 🔸 Summarization Function with Tone Control
def abstractive_summary(text, word_limit=150, tone="neutral"):
    tone_prompts = {
        "formal": "Summarize the text formally:\n",
        "casual": "Summarize the text casually:\n",
        "simple": "Summarize the text in simple language:\n",
        "neutral": ""
    }

    prompt = tone_prompts.get(tone, "")
    full_prompt = prompt + text

    # Approximate token count
    max_tokens = min(int(word_limit * 1.5),200)
    min_tokens = max(15, int(word_limit * 0.3))

    result = summarizer(full_prompt, max_length=max_tokens, min_length=min_tokens, truncation=True, no_repeat_ngram_size=3, do_sample=False)
    return result[0]['summary_text']

# 🔸 Generate Bullet Point List from Summary

def generate_bullet_points(summary):
    # 1. Split into sentences
    sentences = re.split(r'(?<=[.?!])\s+', summary.strip())

    # 2. Filter short, key phrases only
    bullet_candidates = [
        s.strip() for s in sentences 
        if len(s.strip()) > 15 and re.search(r'[a-zA-Z]', s)
    ]

    # 3. Add emojis
    emojis = ["💡", "🧠", "💪", "🎯", "🔍", "🚀", "📘", "📌", "✨", "📝"]
    bullets = [
        f"{emojis[i % len(emojis)]} {line}" 
        for i, line in enumerate(bullet_candidates[:5])
    ]

    return bullets or ["⚠️ No key points could be extracted."]

# 🔸 Word Count, Sentence Count, Keyword Stats
def get_summary_stats(text):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    sentences = [s for s in re.split(r'[.!?]', text) if len(s.strip()) > 5]
    keywords = Counter(words)
    most_common = keywords.most_common(5)

    return {
        "Word Count": len(words),
        "Sentence Count": len(sentences),
        "Top Keywords": [word for word, _ in most_common]
    }

# 🔸 Dual Word Cloud (Original vs. Summary)
def plot_dual_wordcloud(original_text, summary_text):
    text1 = original_text if original_text and original_text.strip() else "Empty Text"
    text2 = summary_text if summary_text and summary_text.strip() else "Empty Summary"
    wc1 = WordCloud(
        width=800,
        height=400,
        background_color='black',
        colormap='Pastel1',
        collocations=False
    ).generate(text1)

    wc2 = WordCloud(
        width=800,
        height=400,
        background_color='black',
        colormap='Pastel2',
        collocations=False
    ).generate(text2)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ☁ Word Cloud: Original Text")
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
