import os
import shutil
from math import floor

from yt_dlp import YoutubeDL


def move_to_output(file_path, output_path):
    shutil.move(file_path, output_path)


def clear_temp_dir():
    """Clears the temporary directory by deleting all files and subdirectories."""
    temp_folder = './temp'
    for filename in os.listdir(temp_folder):
        file_path = os.path.join(temp_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def download_youtube_video(url, output_dir='./temp', video_format='best'):
    """
    Downloads a YouTube video using yt-dlp library.

    Args:
        url (str): URL of the YouTube video.
        output_dir (str): Directory where the video will be saved.
        video_format (str): Video format to download (e.g., 'best', 'worst').

    Returns:
        str: File path of the downloaded video.
    """

    def progress_hook(d):
        """Callback function to track download progress."""
        if d['status'] == 'finished':
            filename = ydl.prepare_filename(d)
            print(f"Downloaded file: {filename}")

    # Define output template for saving the video
    save_path_template = os.path.join(output_dir, '%(title)s.%(ext)s')

    # Configure options for YoutubeDL
    ydl_opts = {
        'format': video_format,
        'outtmpl': save_path_template,
        'progress_hooks': [progress_hook],
    }

    # Download the video using YoutubeDL
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        if 'entries' in info_dict:
            video = info_dict['entries'][0]
        else:
            video = info_dict
        downloaded_filename = ydl.prepare_filename(video)

    return downloaded_filename


def format_time(seconds):
    """
    Converts a duration in seconds to a formatted time string (HH:MM:SS,mmm).

    Args:
        seconds (int): Duration in seconds.

    Returns:
        str: Formatted time string (e.g., '01:23:45,678').
    """
    hours = floor(seconds / 3600)
    seconds %= 3600
    minutes = floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - floor(seconds)) * 1000)
    seconds = floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    return formatted_time
