from math import floor
from os import path
from yt_dlp import YoutubeDL


def download_youtube_video(url, output_dir='./temp', _format='best'):
    def hook(d):
        if d['status'] == 'finished':
            filename = ydl.prepare_filename(d)
            print(f"Загружен файл: {filename}")

    save_path_template = path.join(output_dir, '%(title)s.%(ext)s')
    ydl_opts = {
        'format': _format,
        'outtmpl': save_path_template,
        'progress_hooks': [hook],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        if 'entries' in info_dict:
            video = info_dict['entries'][0]
        else:
            video = info_dict
        filename = ydl.prepare_filename(video)

    return filename


def format_time(seconds):
    hours = floor(seconds / 3600)
    seconds %= 3600
    minutes = floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - floor(seconds)) * 1000)
    seconds = floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

    return formatted_time
