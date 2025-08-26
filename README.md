# YouTubeDigest 

**Quick and friendly summaries of any YouTube video — delivered as easy-to-read text or PDF!**

---

## Demo Video

[Click to watch a short walkthrough.](https://www.youtube.com/watch?v=Zl2JTqAB68E)

---

## Project Overview

YouTubeDigest is a Streamlit-based web app that converts YouTube video transcripts into concise, conversational summaries. Users can:

- Generate bullet-point summaries of videos.
- Translate summaries into multiple languages (English, Spanish, French, German, Hindi, Chinese, Japanese).
- Download summaries as PDF for easy sharing.

---

## Features

- **Transcript Fetching:** Automatically retrieves YouTube video transcripts (if available).
- **LLM Summarization:** Uses a friendly, easy-to-read summarization prompt for key points and conclusions.
- **Multilingual Support:** Translate summaries into your preferred language.
- **PDF Export:** Generate professional-looking PDFs with video title, URL, and bullet-point summary.
- **Interactive Frontend:** Streamlit interface with video thumbnail previews and language selection.

---

## Tech Stack

- **Python Version:** 3.12  
- **Frontend:** Streamlit  
- **Backend:** Python 3.x  
- **APIs / Libraries:**
  - `youtube-transcript-api` for transcript fetching  
  - `reportlab` for PDF generation  
  - `requests` for translation API calls  
  - `google-generativeai` (Gemini) for summary generation  
- **Deployment:** Render / Local machine  

---

## Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/Himanshu-2678/YouTube_Content_Summarizer.git
cd YouTube_Content_Summarizer
pip install --upgrade pip
pip install -r requirements.txt
```


Run locally:
```
streamlit run app/app.py
```

### Steps:

- Enter a YouTube video URL.
- Select your preferred language.
- Click “Generate Summary”.

View summary in the app and optionally download as PDF.

## Folder Structure
YouTube_Content_Summarizer/
├─ app/
│   └─ app.py                  # Main Streamlit app
├─ models/
│   ├─ fetching_youtube_transcript.py
│   └─ generate_content.py
├─ .devcontainer/
├─ .env
├─ .gitignore
├─ README.md
└─ requirements
