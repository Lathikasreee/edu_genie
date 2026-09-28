from pydantic import BaseModel
from typing import List, Optional

class QuizRequest(BaseModel):
    topic: str
    num_questions: Optional[int] = 3

class QuestionItem(BaseModel):
    question: str
    options: List[str]
    answer: str

class QuizResponse(BaseModel):
    topic: str
    quiz: List[QuestionItem]

class FlashcardRequest(BaseModel):
    content: str

class FlashcardItem(BaseModel):
    front: str
    back: str

class FlashcardResponse(BaseModel):
    flashcards: List[FlashcardItem]

class ChatRequest(BaseModel):
    prompt: str
    context: Optional[str] = None
