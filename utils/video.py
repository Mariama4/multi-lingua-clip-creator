import math
import subprocess
from os import path
import cv2 as cv


def get_video_duration(video_path):
    cap = cv.VideoCapture(video_path)
    fps = cap.get(cv.CAP_PROP_FPS)  # OpenCV v2.x used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    duration = math.ceil(frame_count / fps)
    return duration


def cut_video(video_path, cut_from, cut_to, part, output_path):
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', video_path,
        '-y',
        '-vf',
        f"drawtext=text='{part}':fontsize=18:fontcolor=black:box=1:boxcolor=white@1:x=(w-text_w)/2:y=(h-text_h)/2:enable='lt(t,5)'",
        '-ss', cut_from,
        '-to', cut_to,
        '-c:a', 'copy',
        output_path,
    ]
    subprocess.run(ffmpeg_cmd, check=True)
    return output_path


def overlay_watermark(video_path, watermark_path, output_path, filter_complex='[0:v][1:v]overlay=0:300'):
    """
    Overlay a watermark onto a video using FFmpeg.

    Args:
        video_path (str): Path to the input video file.
        watermark_path (str): Path to the watermark image file.
        output_path (str): Path to save the output video file.

    Returns:
        str: Path to the output video file with the watermark overlay.
    """
    try:
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', watermark_path,
            '-y',  # Overwrite output file if exists
            '-filter_complex', f'{filter_complex}',
            '-c:a', 'copy',  # Copy audio stream without re-encoding
            output_path,
        ]
        subprocess.run(ffmpeg_cmd, check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error executing FFmpeg command for overlaying watermark: {e}")
        return None


def crop_video_horizontal_to_vertical(video_path, output_path):
    """
    Crop a video horizontally to vertical orientation using FFmpeg.

    Args:
        video_path (str): Path to the input video file.
        output_path (str): Path to save the output cropped video file.

    Returns:
        str: Path to the output cropped video file.
    """
    try:
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-y',  # Overwrite output file if exists
            '-filter_complex',
            '[0:v]boxblur=40,scale=1080x1920,setsar=1[bg];[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=y=(H-h)/2',
            '-c:a', 'copy',  # Copy audio stream without re-encoding
            output_path,
        ]
        subprocess.run(ffmpeg_cmd, check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error executing FFmpeg command for cropping video: {e}")
        return None


def add_subtitles_to_video(video_path, subtitles_path, output_path):
    """
    Add subtitles to a video using FFmpeg.

    Args:
        video_path (str): Path to the input video file.
        subtitles_path (str): Path to the subtitles file (SRT format).
        output_path (str): Path to save the output video file with subtitles.

    Returns:
        str: Path to the output video file with subtitles.
    """
    try:
        # Check if input video and subtitles files exist
        if not path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        if not path.exists(subtitles_path):
            raise FileNotFoundError(f"Subtitles file not found: {subtitles_path}")

        ffmpeg_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-y',  # Overwrite output file if exists
            '-vf',
            f"subtitles={subtitles_path}:force_style='FontName=Arial,FontSize=12,PrimaryColour=&Hffffff&,Bold=1,MarginV=+40'",
            '-c:a', 'copy',  # Copy audio stream without re-encoding
            output_path,
        ]
        subprocess.run(ffmpeg_cmd, check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Error executing FFmpeg command for adding subtitles: {e}")
        return None
