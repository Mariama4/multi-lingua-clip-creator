import subprocess
from os.path import splitext

from faster_whisper import WhisperModel


def convert_webm_to_wav(input_file):
    try:
        output_file = splitext(input_file)[0] + '.wav'
        # Команда ffmpeg для конвертации
        command = [
            'ffmpeg',
            '-i', input_file,  # Входной файл WebM
            '-y',   # Перезаписать файл
            '-vn',  # Отключить видео
            '-acodec', 'pcm_s16le',  # Использовать без потерь PCM (WAV)
            output_file  # Выходной файл WAV
        ]

        # Выполнить команду ffmpeg
        subprocess.run(command, check=True)
        return output_file

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды ffmpeg: {e}")


def transcribe(file_path):
    model = WhisperModel("small")

    segments, info = model.transcribe(file_path)

    language = info[0]

    segments = list(segments)
    # for segment in segments:
    #     print("[%.2fs -> %.2fs] %s" %
    #           (segment.start, segment.end, segment.text))
    return language, segments

