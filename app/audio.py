from gtts import gTTS
# from pygame import mixer
import time
import tempfile
import os
from flask import url_for

def get_audio_file(name):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(text=f"{name}以完成點名", lang='zh-TW')
        filename = fp.name.split("\\")[-1]
        file = url_for("static", filename=f"temp/{filename}.mp3")
        tts.save(f"./app/static/temp/{filename}.mp3")

    return file
