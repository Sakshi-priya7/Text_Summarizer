from transformers import pipeline
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

# Load once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# 🔹 Main Abstractive Summary
def abstractive_summary(text, word_limit=150, tone="neutral"):
    tone_prompts = {
        "formal": "Summarize the text formally:\n",
        "casual": "Summarize the text casually:\n",
        "simple": "Summarize the text in simple language:\n",
        "neutral": ""
    }

    full_prompt = tone_prompts.get(tone, "") + text
    max_tokens = int(word_limit * 1.3)
    min_tokens = int(word_limit * 1.0)

    result = summarizer(full_prompt, max_length=max_tokens, min_length=min_tokens, do_sample=False)
    return result[0]['summary_text']

# 🔹 Short Key Bullet Points
def generate_bullet_points(text):
    words = re.findall(r'\b\w{5,}\b', text.lower())
    counter = Counter(words)
    top_keywords = [word for word, _ in counter.most_common(5)]
    emojis = ["💡", "🔑", "🧠", "🚀", "🎯"]
    return [f"{emojis[i]} {word.capitalize()}" for i, word in enumerate(top_keywords)]

# 🔹 Summary Stats
def get_summary_stats(text):
    words = re.findall(r'\w+', text)
    sentences = re.split(r'[.!?]', text)
    keywords = Counter(words).most_common(5)
    return {
        "Word Count": len(words),
        "Sentence Count": len([s for s in sentences if s.strip()]),
        "Top Keywords": [w for w, _ in keywords]
    }

# 🔹 Dual Word Cloud
def plot_dual_wordcloud(original_text, summary_text):
    wc1 = WordCloud(width=800, height=400, background_color='black', colormap='Pastel1').generate(original_text)
    wc2 = WordCloud(width=800, height=400, background_color='black', colormap='Pastel2').generate(summary_text)

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