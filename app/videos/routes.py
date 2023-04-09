from flask import render_template, request
from flask_login import login_required, current_user
from app.videos import videos_bp
from app.videos.controllers import VideosController
from app.videos.errors import NotFoundException


@videos_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # view all movies
    controller = VideosController()

    try:
        videos = controller.get_videos()
    except NotFoundException():
        videos = []

    return render_template('videos/index.html', videos=videos)