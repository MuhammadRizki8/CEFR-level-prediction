from pydantic import BaseModel
from typing import List, Optional
# Models for API requests/responses
class UserCreate(BaseModel):
    username: str
    fullname: str
    password: str  # REQUIRED
    interests: Optional[List[str]] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    fullname: str
    interests: List[str]

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
    category: str
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
    
class GenerateQuestionsRequest(BaseModel):
    number: Optional[str] = "anything"
    cefr_level: Optional[str] = "anything"
    interest: Optional[str] = "anything"
    subject: Optional[str] = "anything"

class BatchGetByInterest(BaseModel):
    interest: str