import subprocess
from os.path import splitext

from faster_whisper import WhisperModel


def convert_webm_to_wav(input_file):
    """
    Converts a WebM file to WAV format using ffmpeg.

    Args:
        input_file (str): Path to the input WebM file.

    Returns:
        str: Path to the output WAV file.
    """
    try:
        output_file = splitext(input_file)[0] + '.wav'

        # Command for ffmpeg conversion
        command = [
            'ffmpeg',
            '-i', input_file,  # Input WebM file
            '-y',  # Overwrite output file if exists
            '-vn',  # Disable video stream
            '-acodec', 'pcm_s16le',  # Use PCM (WAV) codec without loss
            output_file  # Output WAV file
        ]

        # Execute ffmpeg command
        subprocess.run(command, check=True)
        return output_file

    except subprocess.CalledProcessError as e:
        print(f"Error executing ffmpeg command: {e}")


def transcribe(file_path):
    """
    Transcribes audio from a WAV file using a WhisperModel.

    Args:
        file_path (str): Path to the input WAV file.

    Returns:
        tuple: A tuple containing the detected language (str) and a list of transcribed segments.
    """
    try:
        # Initialize WhisperModel with 'small' configuration
        model = WhisperModel("small")

        # Transcribe audio file
        segments, info = model.transcribe(file_path)

        # Extract language from info
        language = info[0]

        # Convert segments to a list
        segments = list(segments)

        return language, segments

    except Exception as e:
        print(f"Error during transcription: {e}")
        return None, []
