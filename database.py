from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database connection URL
# DATABASE_URL = "mysql+mysqlconnector://root:@localhost/english_app"
# DATABASE_URL = "mysql+mysqlconnector://root:@34.50.68.65/english_app"

# Database engine and session setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Association table for many-to-many relationship
user_interests = Table(
    "user_interests",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("interest_id", Integer, ForeignKey("interests.id"), primary_key=True)
)

# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    fullname = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    interests = relationship("Interest", secondary=user_interests, back_populates="users")
    cefr_results = relationship("CEFRResult", back_populates="user")
    exam_attempts = relationship("ExamAttempt", back_populates="user")

# Interest model
class Interest(Base):
    __tablename__ = "interests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    users = relationship("User", secondary=user_interests, back_populates="interests")

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
    category = Column(String(255), nullable=True)
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

    # Relationships
    user = relationship("User")
    batch = relationship("QuestionBatch")
    submission_details = relationship("ExamSubmissionDetail", back_populates="attempt")

class ExamSubmissionDetail(Base):
    __tablename__ = "exam_submission_details"
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("exam_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    choice_id = Column(Integer, ForeignKey("choices.id"), nullable=False)
    is_correct = Column(Boolean, nullable=False)

    # Relationships
    attempt = relationship("ExamAttempt", back_populates="submission_details")
    question = relationship("Question")
    choice = relationship("Choice")
# Function to initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)
