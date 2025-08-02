from transformers import pipeline
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

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

def extractive_summary(text, sentence_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return ' '.join(str(sentence) for sentence in summary)
