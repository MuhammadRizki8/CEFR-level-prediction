import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from transformers import pipeline

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Memuat model dan vectorizer yang telah dilatih
model = joblib.load("Logistic_Regression.joblib")
vectorizer = joblib.load("tfidf_vectorizer.joblib")

# Definisikan model input data untuk prediksi CEFR
class TextData(BaseModel):
    texts: List[str]

# Definisikan model input data untuk pembuatan pertanyaan
class ArticleData(BaseModel):
    article: str
    num_questions: int = 5

# Endpoint root
@app.get("/")
def read_root():
    return {"message": "Welcome to the CEFR prediction API"}

# Namespace dan tag untuk prediksi
@app.post("/predict/cefr-level", tags=["Prediction"])
def predict_cefr(data: TextData):
    # Preprocess text data
    cleaned_texts = [clean_text(text) for text in data.texts]
    X_tfidf = vectorizer.transform(cleaned_texts)
    
    # Prediksi CEFR
    predictions = model.predict(X_tfidf)
    
    return {"predictions": predictions.tolist()}

# Fungsi untuk membersihkan teks
def clean_text(text):
    import re
    text = text.lower()  # Ubah ke lowercase
    text = re.sub(r'\d+', '', text)  # Hapus angka
    text = re.sub(r'[^\w\s]', '', text)  # Hapus tanda baca
    return text

# Mengunduh dataset yang diperlukan
nltk.download('punkt')

# Load pre-trained model for NER dari HuggingFace
ner_pipeline = pipeline('ner', grouped_entities=True)

def get_named_entities(text):
    ner_results = ner_pipeline(text)
    entities = [result['word'] for result in ner_results]
    return entities

def generate_questions(article, num_questions=5):
    sentences = sent_tokenize(article)
    word_tokens = word_tokenize(article)
    
    # Menggunakan model transformer untuk NER
    named_entities = get_named_entities(article)
    keywords = named_entities if named_entities else [word for word, freq in nltk.FreqDist(word_tokens).most_common(10)]
    
    questions = []
    used_keywords = set()

    for keyword in keywords:
        if len(questions) >= num_questions:
            break
        if keyword in used_keywords:
            continue

        for sentence in sentences:
            if keyword in sentence:
                question = sentence.replace(keyword, '_____')
                used_keywords.add(keyword)
                
                question_data = {
                    'question': question,
                    'answer': keyword
                }
                questions.append(question_data)
                break
    
    return questions, keywords

# Endpoint untuk pembuatan pertanyaan
@app.post("/generate/questions", tags=["Question Generation"])
def question_generation(data: ArticleData):
    questions, keywords = generate_questions(data.article, data.num_questions)
    
    return {"questions": questions, "keywords": keywords}
# Untuk menjalankan aplikasi: uvicorn main:app --reload
