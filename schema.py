from pydantic import BaseModel
from typing import List
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
    
class AnswerSubmission(BaseModel):
    question_id: int
    choice_id: int

class ExamSubmission(BaseModel):
    user_id: int
    batch_id: int
    answers: List[AnswerSubmission]