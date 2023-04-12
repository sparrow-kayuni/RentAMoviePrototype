from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Customer, Rental, Video, Staff, Genre
from app.videos import videos_bp
from app.videos.forms import NewVideoForm, VideoForm, DeleteForm
from app.videos.errors import NotFoundException


@videos_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # view all movies
    available = {}
    errmsg = ''
    msg = ''
    
    videos = Video.query.filter(Video.video_title!='Deleted').all()

    if not videos:
        errmsg = 'There are currently no Videos'
        
    if errmsg:
        return render_template('videos/index.html', errmsg=errmsg)
    import datetime
    default_date = datetime.datetime.utcnow()\
            .replace(year=1000, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    for video in videos:
        rental = video.rentals.filter(Rental.date_returned==default_date).first()
        if rental:
            available[video] = False
        else:
            available[video] = True

    if request.args.get('msg'):
        msg = request.args.get('msg')

    return render_template('videos/index.html', videos=videos,\
                            available=available, msg=msg)


@videos_bp.route('/new', methods=['GET', 'POST'])
def new_video():
    msg = ''
    new_video_form = NewVideoForm()
    new_video_form.genre.choices = [(genre.genre_id, genre.genre_name) for genre in Genre.query.all()]
    
    if new_video_form.is_submitted():
        if not new_video_form.confirm_checkbox.data:
            return render_template('videos/new_video.html', new_video_form=new_video_form, msg=msg)
        
        if Video.query.filter(Video.video_title==new_video_form.video_title.data).first():
            msg = 'Video already Exists'
            return render_template('videos/new_video.html', new_video_form=new_video_form, msg=msg)
        
        genre = Genre.query.filter(Genre.genre_id==new_video_form.genre.data).first()
        
        video = Video(video_title=new_video_form.video_title.data, \
                      release_year=new_video_form.release_year.data, \
                        unit_price=new_video_form.unit_price.data, genre=genre)
        db.session.add(video)
        db.session.commit()
        msg = f'{video.video_title} is added successfully'
        return redirect(url_for('videos.index', msg=msg))
    
    return render_template('videos/new_video.html', new_video_form=new_video_form, msg=msg)


@videos_bp.route('/update/<int:video_id>', methods=['GET', 'POST'])
def update_video(video_id):
    msg = ''
    video = Video.query.filter(Video.video_id==video_id).first()
    video_form = VideoForm()
    video_form.genre.choices = [(genre.genre_id, genre.genre_name) for genre in Genre.query.all()]
    
    if request.method == 'GET':
        pass
        # video_form.genre.d = video.genre.genre_id

    if request.method == 'POST':
        if video_form.is_submitted():

            if not current_user.check_password(video_form.password.data):
                return render_template('videos/update_video.html', video_form=video_form, video=video)

            video.video_title = video_form.video_title.data
            video.release_year = video_form.release_year.data
            video.unit_price = video_form.unit_price.data
            video.genre = Genre.query.filter(Genre.genre_id==video_form.genre.data).first()

            db.session.add(video)
            db.session.commit()

            return redirect(url_for('videos.index'))

    return render_template('videos/update_video.html', video_form=video_form, video=video)


@videos_bp.route('/delete/<int:video_id>', methods=['GET', 'POST'])
def delete_video(video_id):
    delete_form = DeleteForm()
    video = Video.query.filter(Video.video_id==video_id).first()

    if request.method == 'POST':
        if not current_user.check_password(delete_form.password.data):
            return render_template('videos/delete_video.html', delete_form=delete_form, video=video) 

        video.video_title='Deleted'
        video.release_year=0
        for rental in video.rentals:
            rental.date_returned = None
            rental.date_due = None
        
        db.session.add(video)
        
        db.session.commit()
        return redirect(url_for('videos.index'))
    
    return render_template('videos/delete_video.html', delete_form=delete_form, video=video)