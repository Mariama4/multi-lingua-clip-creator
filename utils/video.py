import subprocess
from os import path


def overlay_watermark(video_path, watermark_path, output_path):
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', video_path,
        '-y',
        '-i', watermark_path,
        '-nostdin',
        '-filter_complex', '[0:v][1:v]overlay=0:300',
        '-c:a', 'copy',  # Копировать аудио без перекодирования
        '-threads', '0',
        #'-c:v', 'h264_videotoolbox',  # Кодировать видео с помощью libx264
        '-preset', 'fast',  # Использовать быстрое кодирование
        #'-crf', '23',  # Качество видео (меньше значение - лучше качество, больше - меньше размер файла)
        output_path,
    ]
    subprocess.run(ffmpeg_cmd, check=True)
    return output_path


def crop_video_horizontal_to_vertical(video_path, output_path):
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', video_path,
        '-y',
        '-nostdin',
        '-filter_complex',
        '[0:v]boxblur=40,scale=1080x1920,setsar=1[bg];[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=y=(H-h)/2',
        '-c:a', 'copy',  # Копировать аудио без перекодирования
        '-threads', '0',
        #'-c:v', 'h264_videotoolbox',  # Кодировать видео с помощью libx264
        '-preset', 'fast',  # Использовать быстрое кодирование
        #'-crf', '23',  # Качество видео (меньше значение - лучше качество, больше - меньше размер файла)
        output_path,
    ]
    subprocess.run(ffmpeg_cmd, check=True)
    return output_path


def add_subtitles_to_video(video_path, subtitles_path, output_path):
    try:
        # Проверка существования исходного видео и файла субтитров
        if not path.exists(video_path):
            raise FileNotFoundError(f"Файл видео не найден: {video_path}")
        if not path.exists(subtitles_path):
            raise FileNotFoundError(f"Файл субтитров не найден: {subtitles_path}")

        # Опции для ffmpeg
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-y',
            '-nostdin',
            '-vf', f"subtitles={subtitles_path}:force_style='FontName=Arial,FontSize=12,PrimaryColour=&Hffffff&,Bold=1,MarginV=+40'",  # Путь к файлу субтитров
            '-c:a', 'copy',  # Копировать аудио без перекодирования
            '-threads', '0',
            #'-c:v', 'h264_videotoolbox',  # Кодировать видео с помощью libx264
            '-preset', 'fast',  # Использовать быстрое кодирование
            #'-crf', '23',  # Качество видео (меньше значение - лучше качество, больше - меньше размер файла)
            output_path,
        ]

        # Выполнение команды ffmpeg
        subprocess.run(ffmpeg_cmd, check=True)
        return output_path

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды ffmpeg: {e}")
        return None
