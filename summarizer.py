from transformers import pipeline
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st

# Load the abstractive summarization model (only once)
summarizer = pipeline("summarization", model="t5-small")

def clean_generated_summary(text):
    text = re.sub(r'[\(\)\[\]\{\}\'\"\;\_]', '', text)
    text = re.sub(r'\s+([,.?!])', r'\1', text)
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    sentences = re.split(r'(?<=[.?!])\s+', text)
    valid_sentences = []
    
    for s in sentences:
        s_clean = s.strip()
        if re.search(r'[\'\"].*[\'\"]\s*[\'\"].*[\'\"]', s_clean) or s_clean.count('.') > 3:
            break
        if len(s_clean) > 15 and re.search(r'[a-zA-Z]', s_clean):
            valid_sentences.append(s_clean)
            
    result_text = " ".join(valid_sentences)
    
    if result_text and not result_text[-1] in ['.', '!', '?']:
        result_text += '.'
        
    return result_text

# 🔸 Summarization Function with Tone Control
def abstractive_summary(text, word_limit=100, tone="neutral"):
    tone_prompts = {
        "formal": "Summarize the text formally:\n",
        "casual": "Summarize the text casually:\n",
        "simple": "Summarize the text in simple language:\n",
        "neutral": "Summarize the text:\n"
    }

    prompt = tone_prompts.get(tone, "summarize: ")
    full_prompt = prompt + text.strip()

    # Approximate token count
    max_tokens = int(word_limit * 2.0)
    min_tokens = int(word_limit * 1.0)

    result = summarizer(full_prompt, max_length=max_tokens, min_length=min_tokens, num_beams=4, length_penalty=0.8, no_repeat_ngram_size=3,truncation=True, do_sample=False)
    raw_summary = result[0]['summary_text']
    return clean_generated_summary(raw_summary)

# 🔸 Generate Bullet Point List from Summary

def generate_bullet_points(summary):
    # 1. Split into sentences
    sentences = re.split(r'(?<=[.?!])\s+', summary.strip())

    # 2. Filter short, key phrases only
    bullet_candidates = [
        s.strip() for s in sentences 
        if len(s.strip()) > 20 and len(s.strip().split()) <= 15
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
    words = re.findall(r'\w+', text)
    sentences = re.split(r'[.!?]', text)
    keywords = Counter(words)
    most_common = keywords.most_common(5)

    return {
        "Word Count": len(words),
        "Sentence Count": len([s for s in sentences if s.strip()]),
        "Top Keywords": [word for word, _ in most_common]
    }

# 🔸 Dual Word Cloud (Original vs. Summary)
def plot_dual_wordcloud(original_text, summary_text):
    wc1 = WordCloud(
        width=800,
        height=400,
        background_color='black',
        colormap='Pastel1',
        collocations=False
    ).generate(original_text)

    wc2 = WordCloud(
        width=800,
        height=400,
        background_color='black',
        colormap='Pastel2',
        collocations=False
    ).generate(summary_text)

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
