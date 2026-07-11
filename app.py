import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
import io

# Page config
st.set_page_config(page_title="Language Translator", page_icon="🌐", layout="centered")

# Title
st.markdown("<h1 style='text-align: center;'>🌐 Language Translation Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Translate text or your voice instantly</p>", unsafe_allow_html=True)
st.write("")

# Supported languages
languages = GoogleTranslator().get_supported_languages(as_dict=True)
lang_names = list(languages.keys())

# --- Voice Input Section ---
st.markdown("### 🎙️  Speak and translate")

# Common speech recognition language codes (locale format)
speech_lang_map = {
    "english": "en-US",
    "telugu": "te-IN",
    "hindi": "hi-IN",
    "tamil": "ta-IN",
    "kannada": "kn-IN",
    "malayalam": "ml-IN",
    "urdu": "ur-IN",
    "marathi": "mr-IN",
    "bengali": "bn-IN",
    "gujarati": "gu-IN",
}

speech_lang = st.selectbox("🎤 Speaking in:", options=list(speech_lang_map.keys()), index=1)

audio_value = st.audio_input("Record your voice")

voice_text = ""
if audio_value is not None:
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_value) as source:
            audio_data = recognizer.record(source)
            voice_text = recognizer.recognize_google(audio_data, language=speech_lang_map[speech_lang])
            st.success(f"🗣️ You said: {voice_text}")
    except sr.UnknownValueError:
        st.error("❌ Could not understand the audio. Try speaking clearly.")
    except sr.RequestError:
        st.error("❌ Speech recognition service unavailable. Check your internet.")

st.markdown("### ✍️ Or Type Text")
input_text = st.text_area("Enter text to translate:", height=120, value=voice_text, placeholder="Type something...")

# Language selectors
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source Language", options=["auto"] + lang_names)
with col2:
    target_lang = st.selectbox("Target Language", options=lang_names, index=lang_names.index("telugu") if "telugu" in lang_names else 0)

# Translate button
if st.button("🔁 Translate", use_container_width=True):
    if input_text.strip() == "":
        st.warning("⚠️ Please enter some text or record your voice first.")
    else:
        try:
            translated_text = GoogleTranslator(
                source=source_lang if source_lang != "auto" else "auto",
                target=languages[target_lang]
            ).translate(input_text)

            st.success("✅ Translation:")
            st.text_area("Result", value=translated_text, height=150, label_visibility="collapsed")

            # --- Text-to-Speech ---
            tts_lang_code = languages[target_lang]
            try:
                tts = gTTS(text=translated_text, lang=tts_lang_code)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)

                st.write("🔊 Listen to translation:")
                st.audio(audio_buffer, format="audio/mp3")
            except Exception:
                st.info("🔇 Voice not available for this language.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 13px;'>Built with ❤️ using Streamlit | CodeAlpha Internship Project</p>", unsafe_allow_html=True)