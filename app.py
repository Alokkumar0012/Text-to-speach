import streamlit as st
import edge_tts
import asyncio
import os

# --- Page Config ---
st.set_page_config(page_title="Text to Speech Converter", page_icon="🎙️")

st.title("🗣️ Text to Speech Converter")
st.write("Apna text likho, awaaz select karo aur audio download karo! (No API Key Required)")

# --- Settings ---
text_input = st.text_area("Yahan apna text enter karein:", height=150, placeholder="Hello, how are you doing today?")

# Voice Options (Male & Female)
# Shortlist of high quality voices
voice_options = {
    "Female (US - Aria)": "en-US-AriaNeural",
    "Male (US - Guy)": "en-US-GuyNeural",
    "Female (UK - Sonia)": "en-GB-SoniaNeural",
    "Male (UK - Ryan)": "en-GB-RyanNeural",
    "Female (Hindi - Swara)": "hi-IN-SwaraNeural",
    "Male (Hindi - Madhur)": "hi-IN-MadhurNeural"
}

selected_voice_name = st.selectbox("Voice select karein (Male/Female):", list(voice_options.keys()))
selected_voice_code = voice_options[selected_voice_name]

# --- Function to Generate Audio ---
async def generate_audio(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

# --- Main Logic ---
if st.button("🔊 Convert to Speech"):
    if text_input.strip() == "":
        st.warning("Kripya pehle kuch text likhein!")
    else:
        output_file = "generated_audio.mp3"
        
        with st.spinner("Generating Audio..."):
            try:
                # Async loop chalana padega kyunki edge-tts async hai
                asyncio.run(generate_audio(text_input, selected_voice_code, output_file))
                
                # Success Message
                st.success("Audio ban gaya hai! Niche se play ya download karein.")
                
                # Audio Player
                audio_file = open(output_file, 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
                
                # Download Button
                st.download_button(
                    label="📥 Download MP3",
                    data=audio_bytes,
                    file_name="my_speech.mp3",
                    mime="audio/mp3"
                )
                
                audio_file.close()
                
            except Exception as e:
                st.error(f"Error aaya: {e}")

# Footer
st.markdown("---")
st.caption("Built with Python & Streamlit | No API Key Required")