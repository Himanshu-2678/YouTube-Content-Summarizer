"""
This file contains a function to generate content from gemeni pro based on the transcript provided.
"""

## required imorts

from dotenv import load_dotenv
import os
import google.generativeai as genai  

## loading the variables from .env file
load_dotenv()

## Fetch the key
api_key = os.getenv("GOOGLE_API_KEY")

## Configure genai
genai.configure(api_key=api_key)

prompt = """You are a friendly and engaging assistant that summarizes YouTube videos in a way that feels like a conversation. Summarize the following transcript, keeping it friendly and easy to understand:
            Start with a short introduction (2–3 sentences) that captures the key theme or problem the video addresses.
            Use bullet points to highlight the key takeaways (4–8 points). Keep each point around 2–3 sentences and focus on the main message, examples, and any important stats or names mentioned.
            Make it conversational by keeping the tone approachable and easy to follow. Add any humor or examples from the video that make it feel like a chat.
            End with a short conclusion (2–3 sentences) that reinforces the main takeaway or solution from the video.
            Make sure the summary is clear and concise, easy to skim, and captures all the important details without feeling overwhelming."""

def gemini_content_generation(youtube_transcript, prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt + youtube_transcript, 
                                        generation_config=genai.types.GenerationConfig(
                                            temperature=0.7, max_output_tokens=2048))
        
        return response.text
        

    except Exception as e:
        raise e



"""
This file contains a function to generate content from GPT-4o based on the transcript provided.
"""

"""
This file contains a function to generate content from Hugging Face based on the transcript provided.
"""

'''## required imports
from dotenv import load_dotenv
import os
from transformers import pipeline  

## loading the variables from .env file
load_dotenv()

## (Optional) if you want to use a Hugging Face API key
hf_key = os.getenv("HF_TOKEN")

## initializing the Hugging Face summarizer pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

prompt = "You are a summarizer app. Take the transcript of the given YouTube video and create a detailed structured summary with key points, examples, and steps. Organize it into sections (Introduction, Key Concepts, Roadmaps, Tools, Suggestions if required)."

def hf_content_generation(youtube_transcript, prompt):
    try:
        # Combine prompt with transcript
        text = prompt + "\n\nTranscript:\n" + youtube_transcript

        # Run summarization
        summary = summarizer(text, max_length=1000, min_length=300, do_sample=False)

        return summary[0]['summary_text']

    except Exception as e:
        raise e'''





'''
"""
This file contains a function to generate content from Hugging Face based on the transcript provided.
"""

## required imports
from dotenv import load_dotenv
import os
from openai import OpenAI   # Hugging Face Inference API uses OpenAI-compatible client

## loading the variables from .env file
load_dotenv()

## fetching HF key
hf_key = os.getenv("HF_TOKEN")

## initialize inference client
client = OpenAI(api_key=hf_key, base_url="https://api-inference.huggingface.co/v1")

prompt = """You are a helpful assistant that summarizes YouTube videos.

Summarize the following transcript in a **structured format**:
1. Start with a short 2 to 3 sentence introduction.
2. Provide 4 to 5 bullet points highlighting the key ideas.
3. End with a 1 to 2 sentence conclusion.
"""

# helper function to split transcript into chunks
def chunk_text(text, max_chunk=1000):
    words = text.split()
    chunks, current_chunk = [], []
    
    for word in words:
        if len(" ".join(current_chunk + [word])) <= max_chunk:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def hf_content_generation(youtube_transcript, prompt):
    try:
        # Step 1: Break transcript into chunks
        chunks = chunk_text(youtube_transcript)

        summaries = []
        for chunk in chunks:
            user_prompt = prompt + "\n\nTranscript:\n" + chunk

            response = client.chat.completions.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",  # conversational model
                messages=[
                    {"role": "system", "content": "You are a structured summarizer."},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=600,
                temperature=0.7,
            )
            summaries.append(response.choices[0].message.content)

        # Step 3: Combine chunk summaries into final structured summary
        final_summary = "\n\n".join(summaries)

        return final_summary

    except Exception as e:
        raise e'''
