import ffmpeg
from utils.colorPrint import *
from utils.speech_to_text import speech_to_text
from utils.srt2ass import srt2ass
from utils.transcribeGui import TranscribeGui
import tkinter as tk
import os

def burn_subtitles_to_video(input_video, subtitles_file, output_video):
    try:
        ffmpeg.input(input_video).output(
            output_video,
            vf=f"subtitles='{subtitles_file}'",
            preset="ultrafast"
        ).run()
        print(f"Subtitles burned successfully into {output_video}")
    except ffmpeg.Error as e:
        error(f"Error occurred while burning subtitles: {e}")
        exit()

def transcribe(app):
    input_file = app.input_file
    output_file = app.output_file
    font = app.font
    font_size = app.font_size
    color = app.color
    srt_file = 'captions.srt'
    speech_to_text(input_file, srt_file)
    ass_file = srt2ass(srt_file,font,font_size,color)
    burn_subtitles_to_video(input_file, ass_file, output_file)
    os.rename(ass_file)

if __name__ == '__main__':
    root = tk.Tk()
    app = TranscribeGui(root)
    app.root.mainloop()
    if app.valid:
        transcribe(app)
        success("TRANSCRIPTION SUCCESSFUL")