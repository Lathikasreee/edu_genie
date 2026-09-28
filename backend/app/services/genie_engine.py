import requests
import json
from app.config import settings

class EduGenieEngine:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.DEFAULT_MODEL
        self.mock_fallback = settings.USE_MOCK_FALLBACK or not self.api_key

    def generate_quiz(self, topic: str, num_questions: int = 3) -> list:
        if self.mock_fallback:
            return [
                {
                    "question": f"What is a primary principle of {topic}?",
                    "options": ["A) Foundational theory", "B) Unrelated concept", "C) Random noise", "D) None of the above"],
                    "answer": "A) Foundational theory"
                },
                {
                    "question": f"Why is studying {topic} important in modern applications?",
                    "options": ["A) Drives innovation", "B) Has no practical use", "C) Decreases productivity", "D) Obsolete method"],
                    "answer": "A) Drives innovation"
                },
                {
                    "question": f"Which term best relates to advanced {topic}?",
                    "options": ["A) Optimization", "B) Decoupling", "C) Fragmentation", "D) Stagnation"],
                    "answer": "A) Optimization"
                }
            ][:num_questions]
        
        # Real LLM call if configured
        prompt = f"Generate a JSON array of {num_questions} multiple choice quiz questions on '{topic}'. Format: [{{\"question\": "...", \"options\": ["A", "B", "C", "D"], \"answer\": "A"}}]"
        response_text = self._query_llm(prompt)
        try:
            return json.loads(response_text)
        except Exception:
            return self.generate_quiz(topic, num_questions)

    def generate_flashcards(self, content: str) -> list:
        if self.mock_fallback:
            return [
                {"front": "Key Term 1", "back": f"Core insight derived from input content: '{content[:30]}...'"},
                {"front": "Important Concept", "back": "Central rule that governs system behaviors and outcomes."},
                {"front": "Summary Principle", "back": "Main takeaway to keep in mind during exam preparation."}
            ]
        
        prompt = f"Create 3 flashcards from this text in JSON format [{{\"front\": "...", \"back\": "..."}}]:\n{content}"
        response_text = self._query_llm(prompt)
        try:
            return json.loads(response_text)
        except Exception:
            return self.generate_flashcards(content)

    def ask_tutor(self, query: str, context: str = "") -> str:
        if self.mock_fallback:
            ctx_info = f" [Context: {context[:40]}...]" if context else ""
            return f"🧞 **[Edu Genie AI Tutor]**{ctx_info}

That's a great question about *"{query}"*!

Here is a simple breakdown:
1. **Core Concept:** Breakdown of the key underlying logic.
2. **Practical Example:** Real-world usage.
3. **Study Tip:** Practice this with quizzes to reinforce long-term memory!"
        
        return self._query_llm(f"You are an empathetic expert tutor. Explain concisely:\nContext: {context}\nQuestion: {query}")

    def _query_llm(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5
        }
        try:
            res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30)
            res.raise_for_status()
            return res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error connecting to AI Provider: {str(e)}"
