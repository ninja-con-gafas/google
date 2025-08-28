"""
The module provides utilities to interact with YouTube.
"""

import yt_dlp

from googleapiclient import discovery, errors
from re import search
from socket import timeout
from youtube_transcript_api import TranscriptsDisabled, YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def download_audio_as_mp3(download_path: str, file_name: str, url: str) -> None:

    """
    Download the best available audio stream from a YouTube video and save it as a mp3 file.

    args:
        download_path (str): Path to download the mp3 file.
        file_name (str): Name of the mp3 file to save the audio stream.
        url (str): URL of the YouTube video to download.

    returns:
        None

    raises:
        yt_dlp.utils.DownloadError: If there is an error during the download process.
        yt_dlp.utils.ExtractorError: If there is an error extracting the video information.
    """

    try:
        print(f"Downloading audio stream for {file_name} from URL: {url}")
        ydl_opts = {
            "abort_on_error": True,
            "abort_on_unavailable_fragments": True,
            "format": "bestaudio/best",
            "outtmpl": f"{download_path}/.tmp/{file_name}.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "0",
                },
                {
                    'key': 'ExecAfterDownload',
                    'exec_cmd': f'mv "{download_path}/.tmp/{file_name}.%(ext)s" "{download_path}/{file_name}.%(ext)s"'
                }],
            "socket_timeout": 30,
            "verbose": True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except (AttributeError, TypeError, ValueError,
            yt_dlp.utils.DownloadError, yt_dlp.utils.ExtractorError) as exception:
        print(f"Error downloading {file_name}: {exception} for URL: {url}")

def download_video_as_mp4(download_path: str, file_name: str, url: str) -> None:

    """
    Download the best available video stream from a YouTube video and save it as a mp4 file.

    args:
        download_path (str): Path to download the mp4 file.
        file_name (str): Name of the mp4 file to save the video stream.
        url (str): URL of the YouTube video to download.

    returns:
        None

    raises:
        yt_dlp.utils.DownloadError: If there is an error during the download process.
        yt_dlp.utils.ExtractorError: If there is an error extracting the video information.
    """

    try:
        print(f"Downloading video stream for {file_name} from URL: {url}")
        ydl_opts = {
            "abort_on_error": True,
            "abort_on_unavailable_fragments": True,
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": f"{download_path}/.tmp/{file_name}.%(ext)s",
            "postprocessors": [
                {
                    'key': 'ExecAfterDownload',
                    'exec_cmd': f'mv "{download_path}/.tmp/{file_name}.%(ext)s" "{download_path}/{file_name}.%(ext)s"'
                }],
            "socket_timeout": 30,
            "verbose": True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except (AttributeError, TypeError, ValueError,
            yt_dlp.utils.DownloadError, yt_dlp.utils.ExtractorError) as exception:
        print(f"Error downloading {file_name}: {exception} for URL: {url}")

def get_video_id(url: str) -> str:

    """
    Extracts the video ID from a YouTube URL using regular expression.

    args:
        url (str): The YouTube URL string from which the video ID should be extracted.

    returns:
        str: The extracted video ID.

    raises:
        AttributeError: If the pattern is not found in the input string.
    """

    pattern = r'(?:youtube(?:-nocookie)?\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=|live/)|youtu\.be/)([^"&?/ ]{11})'
    return search(pattern=pattern, string=url).group(1)

def get_video_transcript_en(video_id: str) -> str:

    """
    Retrieves the English transcript of a YouTube video and returns it in plain text format.

    args:
        video_id (str): The unique identifier for the YouTube video.

    returns:
        str: A plain text formatted string containing the transcript of the video.
    """

    try:
        return TextFormatter().format_transcript(YouTubeTranscriptApi.get_transcript(video_id))
    except TranscriptsDisabled:
        return f"Transcripts are disabled for video ID {video_id}"
        
def get_video_url(developer_key: str, service_name: str, query: str, version: str) -> str:

    """
    Get the YouTube video URL corresponding to the query.

    args:
        developer_key (str): YouTube Data API developer key.
        service_name (str): Name of the YouTube API service.
        query (str): The search query string (title and artist of the song).
        version (str): Version of the YouTube API.

    returns:
        str: URL of the YouTube video or an empty string if no video is found.

    raises:
        errors.HttpError: If the YouTube API request fails.
        timeout: If the request times out.
    """

    print(f"Getting video ID for {query}")
    try:
        video_id: str = discovery.build(developerKey=developer_key,
                                        num_retries=5,
                                        serviceName=service_name,
                                        version=version).search() \
            .list(maxResults=1,
                  part="id",
                  q=f"{query}",
                  type="video",
                  videoDefinition="high",
                  videoDuration="any") \
            .execute().get("items", [{}])[0].get("id", {}).get("videoId")

        if video_id:
            print(f"{video_id} is the video ID of {query}")
            return f"https://youtu.be/{video_id}"
        else:
            print(f"No video found for {query}")
            return ""
    except (errors.HttpError, timeout) as exception:
        print(f"Error fetching video for {query}: {exception}")
        return ""
