from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import joblib
import re
import nltk
from database import SessionLocal, init_db, User, CEFRResult, QuestionBatch, Question, Choice

# Initialize database
init_db()

app = FastAPI()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Models for API requests/responses
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class UserCEFRCheck(BaseModel):
    user_id: int
    text: str

class ChoiceCreate(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionCreate(BaseModel):
    question_text: str
    correct_answer: str
    explanation: str
    tips: str
    choices: List[ChoiceCreate]

class QuestionBatchCreate(BaseModel):
    title: str
    cefr_rank: str
    description: str
    questions: List[QuestionCreate]

@app.get("/", tags=["General"])
async def read_root():
    return {"message": "Welcome to the CEFR prediction API"}

# Load model and vectorizer
model = joblib.load("Logistic_Regression.joblib")
vectorizer = joblib.load("tfidf_vectorizer.joblib")

# Utility functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/users/register", response_model=UserResponse, tags=["Users"])
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/users/login", tags=["Users"])
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    return {"message": "Login successful", "user_id": db_user.id}

@app.get("/users/", response_model=List[UserResponse], tags=["Users"])
async def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.post("/predict/cefr-level", tags=["CEFR Check"])
async def predict_cefr(texts: List[str]):
    cleaned_texts = [clean_text(text) for text in texts]
    X_tfidf = vectorizer.transform(cleaned_texts)
    predictions = model.predict(X_tfidf)
    return {"predictions": predictions.tolist()}

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

nltk.download('punkt')

@app.post("/users/cefr-check", tags=["CEFR Check"])
async def user_cefr_check(data: UserCEFRCheck, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cleaned_text = clean_text(data.text)
    X_tfidf = vectorizer.transform([cleaned_text])
    predicted_level = model.predict(X_tfidf)[0]

    cefr_result = CEFRResult(
        user_id=data.user_id,
        text=data.text,
        predicted_level=predicted_level
    )
    db.add(cefr_result)
    db.commit()
    db.refresh(cefr_result)

    return {"user_id": cefr_result.user_id, "text": cefr_result.text, "predicted_level": cefr_result.predicted_level}



@app.post("/batches/")
def create_question_batch(batch: QuestionBatchCreate, db: Session = Depends(get_db)):
    # Create a new question batch
    db_batch = QuestionBatch(
        title=batch.title,
        cefr_rank=batch.cefr_rank,
        description=batch.description
    )
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)

    # Add questions and choices
    for question in batch.questions:
        db_question = Question(
            batch_id=db_batch.id,
            question_text=question.question_text,
            correct_answer=question.correct_answer,
            explanation=question.explanation,
            tips=question.tips
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        for choice in question.choices:
            db_choice = Choice(
                question_id=db_question.id,
                choice_text=choice.choice_text,
                is_correct=choice.is_correct
            )
            db.add(db_choice)
        db.commit()

    return {"message": "Question batch created successfully", "batch_id": db_batch.id}