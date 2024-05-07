from os.path import join
from googletrans import Translator
from dataclasses import dataclass
from typing import List
from utils.common import format_time


def generate_subtitle_file(input_video_name, language, segments, output_dir='./temp'):
    subtitle_file = join(output_dir, f"{input_video_name}.{language}.srt")
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)
        text += f"{str(index + 1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment.text} \n"
        text += "\n"

    f = open(subtitle_file, "w")
    f.write(text)
    f.close()

    return subtitle_file


def translate_segments_to(segments, language):
    @dataclass
    class TranslatedSegment:
        start: float
        end: float
        text: str

    translated_segments = []
    translator = Translator()
    for index, segment in enumerate(segments):
        translated_text = translator.translate(segment.text, dest=language).text
        translated_segment = TranslatedSegment(start=segment.start, end=segment.end, text=translated_text)
        translated_segments.append(translated_segment)

    return translated_segments
