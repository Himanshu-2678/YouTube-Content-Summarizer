import streamlit as st
import sys
import os
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.fethcing_youtube_transcript import fetching_transcript_details  
from models.generate_content import gemini_content_generation

## Function to translate using MyMemory API
def translate_text(text, target_language="es", max_chars=500):
    """
    Translate text using MyMemory API by splitting it into chunks of max_chars.
    """
    translated_chunks = []
    start = 0

    while start < len(text):
        chunk = text[start:start+max_chars]
        url = f"https://api.mymemory.translated.net/get?q={chunk}&langpair=en|{target_language}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            translated_chunks.append(result['responseData']['translatedText'])
        except requests.exceptions.RequestException as e:
            print(f"Translation request failed: {e}")
            translated_chunks.append(chunk)  # fallback: original chunk
        start += max_chars

    return " ".join(translated_chunks)


## Streamlit app
def app():
    st.title("YouTube Video Content Summarizer")

    st.write("This app allows you to enter the YouTube video URL and get the summary of the entire video using Gemini-1.5-flash.")

    youtube_link = st.text_input("Enter YouTube video URL:")

    if youtube_link:
        video_id = youtube_link.split("=")[-1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", caption="Video Thumbnail", use_container_width=True)

    ## Language selection
    language = st.selectbox("Select your preferred Language:", ["English", "Spanish", "French", "German", "Hindi", "Chinese", "Japanese"])

    language_code = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Hindi": "hi",
        "Chinese": "zh",
        "Japanese": "ja"
    }
    selected_language_code = language_code.get(language, "en")

    if st.button("Generate Content"):
        if youtube_link:
            try:
                transcript = fetching_transcript_details(youtube_link)

                prompt = """You are a friendly and engaging assistant that summarizes YouTube videos in a way that feels like a conversation. Summarize the following transcript, keeping it friendly and easy to understand:
                            Start with a short introduction (2–3 sentences) that captures the key theme or problem the video addresses.
                            Use bullet points to highlight the key takeaways (4–8 points). Keep each point around 2–3 sentences and focus on the main message, examples, and any important stats or names mentioned.
                            Make it conversational by keeping the tone approachable and easy to follow. Add any humor or examples from the video that make it feel like a chat.
                            End with a short conclusion (2–3 sentences) that reinforces the main takeaway or solution from the video.
                            Make sure the summary is clear and concise, easy to skim, and captures all the important details without feeling overwhelming."""

                if transcript:
                    content_summary = gemini_content_generation(transcript, prompt)

                    ## Translate summary if selected language is not English
                    if selected_language_code != "en":
                        content_summary = translate_text(content_summary, selected_language_code)

                    st.markdown("### Content Summary:")
                    st.write(content_summary)
                else:
                    st.write("No transcript available.")
            except Exception as e:
                st.write(f"Error: {str(e)}")

if __name__ == "__main__":
    app()
