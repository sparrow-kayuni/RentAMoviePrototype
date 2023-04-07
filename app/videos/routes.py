from flask import render_template, request
from app.videos import videos_bp


@videos_bp.route('/', methods=['GET', 'POST'])
def index():
    # view all movies
    return render_template('videos/index.html')