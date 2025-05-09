import streamlit as st
import pandas as pd
import os
import json
from PIL import Image
from typing import Dict
import google.generativeai as genai

# -------------------------
# GitaGeminiBot Definition
# -------------------------

class GitaGeminiBot:
    def __init__(self, api_key: str):
        genai.configure(api_key="AIzaSyDJNmx7PKmb92aHcrwBK7L5IKHipNzjVck")
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.verses_db = self.load_gita_database()

    def load_gita_database(self) -> Dict:
        path = "bhagavad_gita_verses.csv"
        verses_df = pd.read_csv(path)
        verses_db = {}
        for _, row in verses_df.iterrows():
            chapter = f"chapter_{row['chapter_number']}"
            if chapter not in verses_db:
                verses_db[chapter] = {
                    "title": row['chapter_title'],
                    "verses": {}
                }
            verse_num = str(row['chapter_verse'])
            verses_db[chapter]["verses"][verse_num] = {
                "translation": row['translation']
            }
        return verses_db

    def format_response(self, raw_text: str) -> Dict:
        try:
            try:
                return json.loads(raw_text)
            except json.JSONDecodeError:
                pass

            if '{' in raw_text and '}' in raw_text:
                json_str = raw_text[raw_text.find('{'):raw_text.rfind('}') + 1]
                return json.loads(json_str)

            response = {
                "verse_reference": "",
                "sanskrit": "",
                "translation": "",
                "explanation": "",
                "application": ""
            }

            lines = raw_text.split('\n')
            current = None
            for line in lines:
                line = line.strip()
                if "Chapter" in line and "Verse" in line:
                    response["verse_reference"] = line
                elif line.startswith("Sanskrit:"):
                    response["sanskrit"] = line.replace("Sanskrit:", "").strip()
                elif line.startswith("Translation:"):
                    response["translation"] = line.replace("Translation:", "").strip()
                elif line.startswith("Explanation:"):
                    current = "explanation"
                    response["explanation"] = line.replace("Explanation:", "").strip()
                elif line.startswith("Application:"):
                    current = "application"
                    response["application"] = line.replace("Application:", "").strip()
                elif current:
                    response[current] += " " + line

            return response

        except Exception as e:
            return {
                "verse_reference": "Error",
                "sanskrit": "",
                "translation": str(e),
                "explanation": "Please try again.",
                "application": ""
            }

    def get_response(self, emotion: str, question: str) -> Dict:
        try:
            prompt = f"""
            You are a spiritual guide rooted in the teachings of the Bhagavad Gita.

Input:

User Emotion: {emotion}

User Question: {question}

Instructions:
Respond with authentic wisdom from the Bhagavad Gita. Do not generate or fabricate verses. Only use real verses from the Bhagavad Gita, including their correct chapter and verse number, original Sanskrit, and accurate English translation. If no relevant verse is available, respond gently and say that.

Respond in the following format:

Chapter X, Verse Y
Sanskrit: [Only real Sanskrit verse from Bhagavad Gita]
Translation: [Faithful English translation]
Explanation: [Traditional, concise explanation of the verse]
Application: [Speak to the user's emotional state using soft, friendly, and simple words. Help them connect the verse to their inner life—what they're feeling or struggling with. Use clear, everyday language to offer comfort and direction. Do not use abstract or vague ideas.]
            """
            response = self.model.generate_content(prompt)
            return self.format_response(response.text or "")
        except Exception as e:
            return {
                "verse_reference": "Error",
                "translation": f"Error: {e}",
                "explanation": "Please try again.",
                "application": ""
            }


# -------------------------
# Initialize State
# -------------------------

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'bot' not in st.session_state:
        # Try to get API key from Streamlit secrets or use environment variable as fallback
        api_key = ("GEMINI_API_KEY", "AIzaSyDJNmx7PKmb92aHcrwBK7L5IKHipNzjVck")
        st.session_state.bot = GitaGeminiBot(api_key)

# -------------------------
# Main App
# -------------------------

def main():
    st.set_page_config(
        page_title="Bhagavad Gita Wisdom Weaver",
        page_icon="🕉️",
        layout="wide"
    )

    image_path = "WhatsApp Image 2024-11-18 at 11.40.34_076eab8e.jpg"  
    try:
        if os.path.exists(image_path):  # Check if file exists locally
            image = Image.open(image_path)
            max_width = 800
            aspect_ratio = image.height / image.width
            resized_image = image.resize((max_width, int(max_width * aspect_ratio)))
            st.image(resized_image, caption="Bhagavad Gita - Eternal Wisdom")
        else:
            st.info("Header image not found. The app will continue without it.")
    except Exception as e:
        st.info(f"Could not load header image: {e}")

    initialize_session_state()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.title("🕉️ Gita Wisdom with Emotion")
        st.markdown("Select your emotion and ask a question for guidance from the Gita.")

        # Manual emotion selection
        emotion_options = ["neutral", "happy", "sad", "angry", "fear", "surprise", "disgust"]
        selected_emotion = st.selectbox("Select your emotion:", emotion_options)

        question = st.text_input("Ask your question:")
        
        if st.button("Ask for Wisdom"):
            if not question:
                st.error("Please enter a question before proceeding.")
            else:
                emotion = selected_emotion

                with st.spinner(f"Reflecting based on your {emotion} emotion..."):
                    response = st.session_state.bot.get_response(emotion, question)
                    st.session_state.messages.append({"role": "user", "content": f"{question} (Feeling: {emotion})"})
                    st.session_state.messages.append({"role": "assistant", **response})
                    st.rerun()

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.markdown(message["content"])
                else:
                    st.markdown(f"**{message['verse_reference']}**")
                    if message.get("sanskrit"):
                        st.markdown(f"*{message['sanskrit']}*")
                    if message.get("translation"):
                        st.markdown(message["translation"])
                    if message.get("explanation"):
                        st.markdown("**Understanding:** " + message["explanation"])
                    if message.get("application"):
                        st.markdown("**Modern Application:** " + message["application"])

    with col2:
        st.sidebar.title("📜 Browse Gita Chapters")
        if hasattr(st.session_state, 'bot') and hasattr(st.session_state.bot, 'verses_db') and st.session_state.bot.verses_db:
            chapters = list(st.session_state.bot.verses_db.keys())
            selected = st.sidebar.selectbox("Chapter", chapters, format_func=lambda c: f"{c}: {st.session_state.bot.verses_db[c]['title']}")
            for vnum, vdata in st.session_state.bot.verses_db[selected]["verses"].items():
                with st.sidebar.expander(f"Verse {vnum}"):
                    st.markdown(vdata["translation"])
        else:
            st.sidebar.warning("Verses database not loaded properly.")

    st.markdown("---")
    st.markdown("🧘‍♂️ This tool combines your emotions and the Gita's guidance to offer spiritual clarity.")

if __name__ == "__main__":
    main()
