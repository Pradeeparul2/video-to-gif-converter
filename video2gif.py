import os
import streamlit as st
from moviepy.editor import *


class VideoToGifConverter:
    def __init__(self):
        st.title("MP4 to GIF converter")
        self.cwd = os.getcwd()
        self.start_time = 0
        self.end_time = 0

    def _convert_gif(self, video):
        self.convert_gif = VideoFileClip(os.path.join(self.cwd, video))
        self.convert_gif.write_gif("mp4_to_gif.gif")
        st.success("Converted to Gif..")

    def upload_video(self):
        st.sidebar.subheader("Upload video")
        self.video_file = st.sidebar.file_uploader(
            "select video file to upload", type="mp4"
        )
        if self.video_file is not None:
            # save video as mp4
            with open(self.video_file.name, "wb") as video_file:
                video_file.write(self.video_file.getvalue())
            st.subheader("Original video")
            st.video(self.video_file.getvalue(), format="video/mp4", start_time=0)

    def trim_video(self):
        if self.video_file is not None:
            self.start_time = st.sidebar.number_input(
                "Stat time in seconds", min_value=0, step=1
            )
            self.end_time = st.sidebar.number_input(
                "End time in seconds", min_value=0, step=1
            )
            is_trim = st.sidebar.button("Trim video")
            if is_trim:
                # Trim and save video as mp4
                self.trimed_video = VideoFileClip(
                    os.path.join(self.cwd, self.video_file.name)
                ).subclip(self.start_time, self.end_time)
                self.trimed_video.write_videofile("Trimed " + self.video_file.name)
                st.success("Video Trimed.")

    def convert_to_gif(self):
        if self.video_file is not None:
            is_gif = st.sidebar.button("Convert to Gif")
            if is_gif:
                # video to gif conversion
                try:
                    self._convert_gif("Trimed " + self.video_file.name)
                except Exception as e:
                    self._convert_gif(self.video_file.name)
                st.success(
                    f'Gif file stored on - {os.path.join(self.cwd,"mp4_to_gif.gif")}'
                )

                # Remove video files
                try:
                    os.remove(os.path.join(self.cwd, "Trimed " + self.video_file.name))
                    os.remove(os.path.join(self.cwd, self.video_file.name))
                except Exception as e:
                    os.remove(os.path.join(self.cwd, self.video_file.name))


if __name__ == "__main__":
    editor = VideoToGifConverter()
    editor.upload_video()
    editor.trim_video()
    editor.convert_to_gif()
