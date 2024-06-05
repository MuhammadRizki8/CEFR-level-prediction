import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Memuat model dan vectorizer yang telah dilatih
model = joblib.load("Logistic_Regression.joblib")
vectorizer = joblib.load("tfidf_vectorizer.joblib")

# Definisikan model input data
class TextData(BaseModel):
    texts: List[str]

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

def clean_text(text):
    import re
    text = text.lower()  # Ubah ke lowercase
    text = re.sub(r'\d+', '', text)  # Hapus angka
    text = re.sub(r'[^\w\s]', '', text)  # Hapus tanda baca
    return text

# Untuk menjalankan aplikasi: uvicorn main:app --reload
