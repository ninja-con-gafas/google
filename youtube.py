"""
The module provides utilities to interact with YouTube.
"""

import yt_dlp

from ffmpeg import Error, input, probe
from re import search
from requests import get, post, Response
from requests.exceptions import HTTPError, ConnectionError, Timeout
from typing import Dict, List
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

def get_video_duration(video_file_path: str) -> float:

    """
    Retrieves the duration of a video file.

    args:
        video_file_path (str): The file path of the video whose duration is to be retrieved.

    returns:
        float: The duration of the video in seconds.

    raises:
        KeyError: If the duration information is not found in the video file's metadata.
        ValueError: If the metadata does not contain a valid duration value.
    """

    print(f"Getting video duration of {video_file_path}")
    return float(probe(filename=video_file_path, v='error', select_streams='v:0', show_entries='stream=duration')
                 .get("format")
                 .get("duration"))

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

    print(f"Extracting Video ID from URL: {url}")
    pattern = r'(?:youtube(?:-nocookie)?\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)?)/|.*[?&]v=|live/)|youtu\.be/)([^"&?/ ]{11})'
    return search(pattern=pattern, string=url).group(1)

def get_video_metadata(video_id: str) -> Dict:

    """
    Retrieves metadata for a YouTube video using its video ID.

    args:
        video_id (str): The unique identifier of the YouTube video.

    returns:
        Dict: A dictionary containing the video's metadata or None if an error occurs during the request.

    raises:
        ConnectionError: Raised if there is a network connectivity issue.
        HTTPError: Raised if the HTTP response status is an error.
        Timeout: Raised if the request to the server times out.
    """

    print(f"Getting video metadata for the YouTube video ID: {video_id}")
    url = "https://www.youtube.com/oembed"
    params = {
        "format": "json",
        "url": f"https://www.youtube.com/watch?v={video_id}"
    }

    try:
        response = get(url, params=params)
        response.raise_for_status()
    except (ConnectionError, HTTPError, Timeout) as exception:
        print(f"An error occurred: {exception}")
        return {}
    else:
        return response.json()

def get_video_transcript_en(video_id: str) -> str:

    """
    Retrieves the English transcript of a YouTube video and returns it in plain text format.

    args:
        video_id (str): The unique identifier for the YouTube video.

    returns:
        str: A plain text formatted string containing the transcript of the video.
    """

    try:
        print(f"Fetching English transcript for the video ID: {video_id}")
        return TextFormatter().format_transcript(YouTubeTranscriptApi.get_transcript(video_id))
    except TranscriptsDisabled:
        return f"Transcripts are disabled for video ID {video_id}"

def is_video_corrupted(video_file_path: str) -> bool:

    """
    Checks whether a video file is corrupted by attempting to process it with FFmpeg.

    args:
        video_file_path (str): The file path of the video to be checked for corruption.

    Returns:
        bool: Returns `True` if the video file is likely corrupted, `False` otherwise.

    Raises:
        Error: If an error occurs while processing the file, indicating potential corruption.
    """

    try:
        input(video_file_path).output("null", f="null").run()
        return False
    except Error:
        return True

def search_youtube(query: str) -> List[str]:

    """
    Get the list of YouTube video URLs for a search query.

    args:
        query (str): The search query.

    returns:
        List[str]: The list of URLs result of the search query.

    raises:
        ConnectionError: Raised if there is a network connectivity issue.
        HTTPError: Raised if the HTTP response status is an error.
        Timeout: Raised if the request to the server times out.
    """

    print(f"Getting the list of video URLs for the search query: {query}")
    url = 'https://www.youtube.com/youtubei/v1/search'
    params = {
        'prettyPrint': 'false'
    }
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }
    json_data = {
        'context': {
            'client': {
                'hl': 'en-IN',
                'gl': 'IN',
                'clientName': 'WEB',
                'clientVersion': '2.20241107.01.00',
                'originalUrl': 'https://www.youtube.com/results',
                'platform': 'DESKTOP',
            },
        },
        'query': query,
    }

    try:
        response: Response = post(url, params=params, headers=headers, json=json_data)
        response.raise_for_status()
    except (ConnectionError, HTTPError, Timeout) as exception:
        print(f"An error occurred: {exception}")
    else:
        video_ids: List[str] = []

        def __search_dictionary(dictionary: Dict, key: str):
            if key in dictionary:
                return dictionary.get(key)
            for value in dictionary.values():
                if isinstance(value, dict):
                    item = __search_dictionary(value, key)
                    if item is not None:
                        return item

        search_results: Dict = (response.json()
                .get("contents")
                .get("twoColumnSearchResultsRenderer")
                .get("primaryContents")
                .get("sectionListRenderer")
                .get("contents")[0]
                .get("itemSectionRenderer")
                .get("contents"))

        for result in search_results :
            video_ids.append(__search_dictionary(dictionary=result, key="videoId"))

        return [f"https://youtu.be/{video_id}" for video_id in video_ids if video_id is not None]