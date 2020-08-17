from flask import render_template, Response
from . import main


@main.route('/')
def index():
    return render_template('index.html')
    # return render_template('video.html')

    