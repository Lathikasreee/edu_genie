from fastapi import APIRouter, HTTPException
from app.schemas import QuizRequest, QuizResponse, FlashcardRequest, FlashcardResponse, ChatRequest
from app.services.genie_engine import EduGenieEngine

router = APIRouter(prefix="/api/v1/genie", tags=["Edu Genie AI Services"])
engine = EduGenieEngine()

@router.post("/quiz", response_model=QuizResponse)
async def create_quiz(req: QuizRequest):
    try:
        quiz_data = engine.generate_quiz(req.topic, req.num_questions)
        return QuizResponse(topic=req.topic, quiz=quiz_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/flashcards", response_model=FlashcardResponse)
async def create_flashcards(req: FlashcardRequest):
    try:
        cards = engine.generate_flashcards(req.content)
        return FlashcardResponse(flashcards=cards)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def tutor_chat(req: ChatRequest):
    try:
        reply = engine.ask_tutor(req.prompt, req.context or "")
        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
