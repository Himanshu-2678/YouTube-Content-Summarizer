import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.fethcing_youtube_transcript import fetching_transcript_details  
from models.generate_content import gemini_content_generation

## Defining the Streamlit app
def app():
    st.title("YouTube Video Content Summarizer")

    st.write("This app allows you to enter the YouTube video URL and get the summary of the entire video using Gemini-1.5-flash.")

    ## Input field for YouTube URL
    youtube_link = st.text_input("Enter YouTube video URL:")

    ## to Display video thumbnail if link is entered
    if youtube_link:
        video_id = youtube_link.split("=")[-1]
        print(video_id)
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", caption="Video Thumbnail", use_container_width=True)

    ## Button to trigger summarization.
    if st.button("Generate Content"):
        if youtube_link:
            try:
                ## Fetching the transcript using your existing function
                transcript = fetching_transcript_details(youtube_link)

                ## Defining the prompt for summarization
                prompt = """You are a highly knowledgeable assistant that summarizes YouTube videos in a detailed and engaging way.

                            Summarize the following transcript in a structured and comprehensive format:
                            1. Start with a 3–5 sentence introduction that sets the context of the video.
                            2. Provide 8–12 bullet points, each with 2–4 sentences explaining the key ideas, examples, and important details.
                            3. Include any relevant statistics, facts, or names mentioned in the video.
                            4. End with a 2–3 sentence conclusion that wraps up the main takeaways.
                            5. Make the summary long enough to cover all major points and easy to read.

                            Ensure the output is detailed, explanatory, and fully covers the content of the video transcript."""

                if transcript:
                    ## Generating content summary using your existing function
                    content_summary = gemini_content_generation(transcript, prompt)
                    st.markdown("### Content Summary:")
                    st.write(content_summary)
                else:
                    st.write("No transcript available.")
            except Exception as e:
                st.write(f"Error: {str(e)}")

if __name__ == "__main__":
    app()
