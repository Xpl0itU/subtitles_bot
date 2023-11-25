import ffmpeg
import subtitles
import multiprocessing


def generate_final_video(input_clip):
    return input_clip.filter(
        "subtitles",
        "output.srt",
        force_style=subtitles.get_subtitles_style(
            desired_style=2,
        ),
    )


input_clip = ffmpeg.input("input_clip.mp4")
input_clip.output(
    "temp-audio-subtitles.mp3",
    **{
        "b:a": "192k",
        "threads": multiprocessing.cpu_count(),
    },
).overwrite_output().run()
subtitles.transcribe_audio("temp-audio-subtitles.mp3", "output.srt")
ffmpeg.output(
    generate_final_video(input_clip),
    ffmpeg.input("temp-audio-subtitles.mp3"),
    "output.mp4",
    f="mp4",
    **{
        "c:v": "h264",
        "b:v": "20M",
        "b:a": "128k",
        "threads": multiprocessing.cpu_count(),
    },
).overwrite_output().run()
