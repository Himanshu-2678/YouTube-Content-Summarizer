
"""
In this file, we will transcript from the YouTube video for which we want to summarize the content.
"""

## importing the transcript api
from youtube_transcript_api import YouTubeTranscriptApi

def fetching_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[-1]

        # create an instance and call fetch(video_id)
        transcript_api = YouTubeTranscriptApi()
        fetched = transcript_api.fetch(video_id)

        """
        The transcript is now a FetchedTranscript object containing snippet objects.
        We'll join their .text attributes together into a single string.
        """
        
        script = ""
        for snippet in fetched:
            script += " " + snippet.text

        return script

    except Exception as e:
        raise e


