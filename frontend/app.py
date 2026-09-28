import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/api/v1/genie"

st.set_page_config(page_title="Edu Genie - AI Study Buddy", page_icon="🧞", layout="wide")

st.title("🧞 Edu Genie - AI Study Assistant")
st.caption("Your intelligent study companion for generating quizzes, flashcards, and interactive tutoring.")

tab1, tab2, tab3 = st.tabs(["💬 AI Tutor Chat", "📝 Quiz Generator", "🎴 Flashcard Maker"])

# TAB 1: AI TUTOR
with tab1:
    st.header("Ask Edu Genie")
    context_text = st.text_area("Optional Study Notes / Context:", placeholder="Paste text or study notes here...")
    user_query = st.text_input("What would you like explained?", placeholder="e.g., How does photosynthesis work?")
    
    if st.button("Ask Tutor"):
        if user_query:
            with st.spinner("Edu Genie is thinking..."):
                try:
                    res = requests.post(f"{BACKEND_URL}/chat", json={"prompt": user_query, "context": context_text})
                    if res.status_code == 200:
                        st.markdown(res.json()["response"])
                    else:
                        st.error("Failed to get response from backend API.")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")

# TAB 2: QUIZ GENERATOR
with tab2:
    st.header("Generate Practice Quiz")
    topic = st.text_input("Quiz Topic:", value="Machine Learning Basics")
    num_q = st.slider("Number of Questions:", 1, 5, 3)
    
    if st.button("Generate Quiz"):
        with st.spinner("Crafting quiz questions..."):
            try:
                res = requests.post(f"{BACKEND_URL}/quiz", json={"topic": topic, "num_questions": num_q})
                if res.status_code == 200:
                    quiz_data = res.json()["quiz"]
                    st.session_state["current_quiz"] = quiz_data
                else:
                    st.error("Error generating quiz.")
            except Exception as e:
                st.error(f"Error connecting to server: {e}")

    if "current_quiz" in st.session_state:
        for idx, q in enumerate(st.session_state["current_quiz"]):
            st.subheader(f"Q{idx+1}: {q['question']}")
            user_choice = st.radio(f"Select option for Q{idx+1}:", q["options"], key=f"q_{idx}")
            if st.button(f"Submit Answer for Q{idx+1}", key=f"btn_{idx}"):
                if user_choice == q["answer"]:
                    st.success("Correct! 🎉")
                else:
                    st.info(f"Answer: {q['answer']}")

# TAB 3: FLASHCARDS
with tab3:
    st.header("Flashcard Generator")
    study_material = st.text_area("Paste material to convert into flashcards:", height=150)
    
    if st.button("Create Flashcards"):
        if study_material:
            with st.spinner("Extracting key flashcards..."):
                try:
                    res = requests.post(f"{BACKEND_URL}/flashcards", json={"content": study_material})
                    if res.status_code == 200:
                        cards = res.json()["flashcards"]
                        col1, col2, col3 = st.columns(3)
                        cols = [col1, col2, col3]
                        for idx, card in enumerate(cards):
                            with cols[idx % 3]:
                                with st.expander(f"📌 {card['front']}", expanded=True):
                                    st.write(card["back"])
                    else:
                        st.error("Could not generate flashcards.")
                except Exception as e:
                    st.error(f"Error: {e}")
