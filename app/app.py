import streamlit as st
import sys
import os
import requests
from io import BytesIO
 


import firebase_admin
from firebase_admin import credentials, db

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.fethcing_youtube_transcript import fetching_transcript_details
from models.generate_content import gemini_content_generation


# Translating the text using MyMemory API 
def translate_text(text, target_language="es", max_chars=500):
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
            translated_chunks.append(chunk)
        start += max_chars
    return " ".join(translated_chunks)


# Creating PDF using ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

def create_pdf(summary_text, video_url, language):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=54,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name="TitleCenter", parent=styles["Heading1"], alignment=TA_CENTER)
    sub_style = ParagraphStyle(name="SubCenter", parent=styles["Normal"], alignment=TA_CENTER, spaceAfter=6)
    body_style = ParagraphStyle(name="Body", parent=styles["BodyText"], leading=14)

    story = []
    story.append(Paragraph("YouTube Video Summary", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"Language: {language}", sub_style))
    story.append(Paragraph(f"Video URL: {video_url}", sub_style))
    story.append(Spacer(1, 16))

    for raw in summary_text.splitlines():
        line = raw.strip()
        if not line:
            story.append(Spacer(1, 8))
            continue
        if line.lstrip().startswith(("-", "•", "*")):
            text = line.lstrip()[1:].strip()
            story.append(Paragraph(text, styles["Bullet"]))
        else:
            story.append(Paragraph(line, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer




# Initializing Firebase

import os, json
from dotenv import load_dotenv

'''load_dotenv()

firebase_key = os.getenv("FIREBASE_KEY")
service_account_info = json.loads(firebase_key)

# convert \\n to real newlines for PEM
service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")

if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://content-summarizer-31c3a-default-rtdb.firebaseio.com/"
    })
'''

firebase_key = st.secrets["FIREBASE_KEY"]  # only from cloud
service_account_info = json.loads(firebase_key)
service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")

if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://content-summarizer-31c3a-default-rtdb.firebaseio.com/"
    })




# Building the Streamlit App
def app():
    # Initialize session state variables if they don't exist
    if 'content_summary' not in st.session_state:
        st.session_state.content_summary = None
    if 'comments' not in st.session_state:
        st.session_state.comments = []  # Initialize comments as an empty list

    st.title("Welcome to YouTubeDigest")
    st.write("Get a quick summary of any YouTube video in your preferred language!")

    youtube_link = st.text_input("Enter YouTube video URL:")

    # Always visible comment section (independent of the summary generation)
    st.subheader("Feedback / Comments")
    feedback = st.text_area("Enter your feedback or comments here:", key="feedback_area")

    if st.button("Submit Feedback"):
        if feedback:
            ref = db.reference("feedbacks")
            ref.push({"feedback": feedback})
            st.session_state.comments.append(feedback)  # Store feedback in session state
            st.success("Thank you for your feedback!")
        else:
            st.error("Please enter some feedback before submitting")

    # Displaying comments
    st.header("Comments:")
    if st.session_state.comments:
        for comment in st.session_state.comments:
            st.write(f"- {comment}")
    else:
        ref = db.reference('feedbacks')
        comments = ref.get()

        if comments:
            for key, value in comments.items():
                st.write(f"- {value['feedback']}")
        else:
            st.write("No comments yet.")

    if youtube_link:
        video_id = youtube_link.split("=")[-1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", caption="Video Thumbnail", use_container_width=True)

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
            # Check if summary is already stored in session_state
            if st.session_state.content_summary:
                # If summary already exists, just display it
                st.markdown("### Content Summary:")
                st.write(st.session_state.content_summary)
            else:
                try:
                    transcript = fetching_transcript_details(youtube_link)

                    prompt = """You are a friendly and engaging assistant that summarizes YouTube videos in a way that feels like a conversation. Summarize the following transcript, keeping it friendly and easy to understand:
                                Start with a short introduction (3-6 sentences) that captures the key theme or problem the video addresses.
                                Use bullet points to highlight the key takeaways (4–8 points). Keep each point around 3-5 sentences and focus on the main message, examples, and any important stats or names mentioned.
                                Make it conversational by keeping the tone approachable and easy to follow. Add any humor or examples from the video that make it feel like a chat.
                                End with a short conclusion (4-8 sentences) that reinforces the main takeaway or solution from the video.
                                Make sure the summary is clear and concise, easy to skim, and captures all the important details without feeling overwhelming."""

                    if transcript:
                        content_summary = gemini_content_generation(transcript, prompt)

                        if selected_language_code != "en":
                            content_summary = translate_text(content_summary, selected_language_code)

                        st.session_state.content_summary = content_summary  # Save summary in session state

                        pdf_buffer = create_pdf(content_summary, youtube_link, language)
                        st.download_button(
                            label="📄 Download Summary as PDF",
                            data=pdf_buffer,
                            file_name="content_summary.pdf",
                            mime="application/pdf"
                        )

                        st.markdown("### Content Summary:")
                        st.write(content_summary)
                    else:
                        st.write("No transcript available.")
                except Exception as e:
                    st.write(f"Error: {str(e)}")


if __name__ == "__main__":
    app()
