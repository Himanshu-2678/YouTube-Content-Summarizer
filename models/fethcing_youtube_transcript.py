
"""
In this file, we will transcript from the YouTube video for which we want to summarize the content.
"""

## importing the transcript api
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def fetching_transcript_details(youtube_video_url):
    try:

        parsed_url = urlparse(youtube_video_url)
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get("v")
        
        if not video_id:
            raise ValueError("Invalid YouTube URL or missing video ID")

        video_id = video_id[0] 

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


