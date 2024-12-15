from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database connection URL
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/english_app"

# Database engine and session setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    cefr_results = relationship("CEFRResult", back_populates="user")
    exam_attempts = relationship("ExamAttempt", back_populates="user")

# CEFRResult model
class CEFRResult(Base):
    __tablename__ = "cefr_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    text = Column(Text, nullable=False)
    predicted_level = Column(String(50), nullable=False)
    user = relationship("User", back_populates="cefr_results")

class QuestionBatch(Base):
    __tablename__ = "question_batches"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    cefr_rank = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    questions = relationship("Question", back_populates="batch")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("question_batches.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    correct_answer = Column(String(255), nullable=False)
    explanation = Column(Text, nullable=True)
    tips = Column(Text, nullable=True)

    batch = relationship("QuestionBatch", back_populates="questions")
    choices = relationship("Choice", back_populates="question")

class Choice(Base):
    __tablename__ = "choices"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    choice_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)

    question = relationship("Question", back_populates="choices")

class ExamAttempt(Base):
    __tablename__ = "exam_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    batch_id = Column(Integer, ForeignKey("question_batches.id"), nullable=False)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)

    user = relationship("User", back_populates="exam_attempts")
    batch = relationship("QuestionBatch")


# Function to initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)
