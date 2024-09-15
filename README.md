# transcriber
Python script that transcribes audio of a video file into the video using whisper and ffmpeg

This script transcribes the audio of a video and burns the generated subtitles into the video using Whisper and FFmpeg.

It first runs a GUI environment using tkinter asking for input and output details along with font, font-size and color.

The input video file's audio is read and a subtitle file is genereated (temp.srt) using whisper
the .srt (SubRip Subtitle file) file is converted to .ass (SubStation Alpha Subtitles file) file which is used to burn the subtitles into the video with font and color.