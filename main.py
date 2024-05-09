import argparse
import os
from math import ceil

from utils.audio import convert_webm_to_wav, transcribe
from utils.common import download_youtube_video, clear_temp_dir, move_to
from utils.text import generate_subtitle_file, translate_segments_to
from utils.video import add_subtitles_to_video, crop_video_horizontal_to_vertical, overlay_watermark, \
    get_video_duration, cut_video, print_part_on_video


def process_video(video_url, languages):
    # Download the video from YouTube
    file_path_webm = download_youtube_video(video_url)

    # Convert the video to WAV format
    file_path_wav = convert_webm_to_wav(file_path_webm)

    # Transcribe the audio to get language and segments
    video_language, segments = transcribe(file_path_wav)

    # Get the base filename and extension
    file_name, _ = os.path.splitext(os.path.basename(file_path_wav))

    # Crop the video horizontally to vertical orientation
    video_vertical = crop_video_horizontal_to_vertical(file_path_webm,
                                                       f'./temp/{file_name}.vertical.{video_language}.mp4')

    # Process each language
    for language in languages:
        if video_language != language:
            # Translate segments if the language differs
            translated_segments = translate_segments_to(segments, language)
            subtitle_file = generate_subtitle_file(input_video_name=file_name, language=language,
                                                   segments=translated_segments)
        else:
            # Use original segments if the language matches
            subtitle_file = generate_subtitle_file(input_video_name=file_name, language=language, segments=segments)

        # Add subtitles to the horizontal video
        video_vertical_with_subtitles = add_subtitles_to_video(video_vertical, subtitle_file,
                                                               f'./temp/{file_name}.subtitles.vertical.{language}.mp4')

        # Add subtitles to the full video
        video_with_subtitles = add_subtitles_to_video(file_path_webm, subtitle_file,
                                                      f'./temp/{file_name}.subtitles.full.{language}.mp4')

        video_vertical_with_watermark = overlay_watermark(video_vertical_with_subtitles,
                                                          f'./static/watermark.vertical.{language}.jpeg',
                                                          f'./temp/{file_name}.watermark.subtitles.vertical.{language}.mp4')
        video_with_watermark = overlay_watermark(video_with_subtitles, f'./static/watermark.full.{language}.jpeg',
                                                 f'./temp/{file_name}.watermark.subtitles.full.{language}.mp4',
                                                 '[1][0]scale2ref=oh*mdar:ih*0.2[logo][video];[video][logo]overlay')

        move_to(video_vertical_with_watermark,
                       f'./output/{file_name}.watermark.subtitles.vertical.{language}.mp4')
        move_to(video_with_watermark, f'./output/{file_name}.watermark.subtitles.full.{language}.mp4')

        seconds = get_video_duration(f'./output/{file_name}.watermark.subtitles.vertical.{language}.mp4')

        for i in range(ceil(seconds // 30 / 2)):
            index = str(i + 1)
            start = str(i * 60)
            end = str((i + 1) * 60)
            if language == 'ru':
                part = f'{index} часть'
            else:
                part = f'{index} part'
            cutted_video_path = cut_video(f'./output/{file_name}.watermark.subtitles.vertical.{language}.mp4', start,
                                          end,
                                          f'./output/{file_name}.{index}.watermark.subtitles.vertical.{language}.mp4')
            print_part_on_video(cutted_video_path, part,
                                f'./output/{file_name}.{index}.part.watermark.subtitles.vertical.{language}.mp4')
            os.remove(cutted_video_path)

    # Clean up temporary files
    clear_temp_dir()
    print('Processing complete.')


def main():
    parser = argparse.ArgumentParser(description='Process YouTube video with subtitles and watermark.')
    parser.add_argument('video_url', type=str, help='URL of the YouTube video')
    parser.add_argument('--languages', nargs='+', default=['ru'],
                        help='Languages for subtitles (default: ru, en)')
    args = parser.parse_args()

    # Validate arguments
    if args.video_url is None:
        raise ValueError('Video URL is required.')

    # Call the video processing function
    process_video(args.video_url, args.languages)


if __name__ == '__main__':
    main()
