from os import path

from utils.audio import convert_webm_to_wav, transcribe
from utils.common import download_youtube_video
from utils.text import generate_subtitle_file, translate_segments_to
from utils.video import add_subtitles_to_video, crop_video_horizontal_to_vertical, overlay_watermark


def main():
    languages = ['ru', 'en']
    file_path_webm = download_youtube_video(
        'https://www.youtube.com/watch?v=n-V4XyL0TCg&ab_channel=%D0%92%D0%B0%D0%BB%D1%8C%D0%BC%D0%B8%D0%BA%D0%B8%D0%B4%D0%B0%D1%81')
    file_path_wav = convert_webm_to_wav(file_path_webm)
    video_language, segments = transcribe(file_path_wav)
    file = path.basename(file_path_wav)
    file_name, file_extension = path.splitext(file)
    video_horizontal = crop_video_horizontal_to_vertical(file_path_webm, f'./temp/horizontal.{video_language}.mp4')
    for language in languages:
        if video_language != language:
            segments = translate_segments_to(segments, language)
        subtitle_file = generate_subtitle_file(
            input_video_name=file_name,
            language=language,
            segments=segments
        )
        video_with_subtitle = add_subtitles_to_video(video_horizontal, subtitle_file, f'./temp/subtitles.{language}.mp4')
        video_with_watermark = overlay_watermark(video_with_subtitle, './static/watermark.jpeg', f'./output/{file_name}.{language}.mp4')


if __name__ == '__main__':
    main()
