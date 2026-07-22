from Services.embeddingservice import searchreviews
import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

def build_prompt(question, reviews):
    context = "\n".join([f"- {r}" for r in reviews])
    prompt = f"""You are a professional customer support analyst.
Based on the following customer reviews, answer the question clearly and professionally in English.

Customer Reviews:
{context}

Question: {question}

Answer in English:"""
    return prompt

def ask_assistant(question: str):
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
    reviews = searchreviews(question)
    review_texts = reviews["review_body"].tolist()
    prompt = build_prompt(question, review_texts)
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs, max_new_tokens=150, num_beams=4, early_stopping=True)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {"answer": answer, "sources": review_texts   }
     