from app import db
from app.models import Customer, Rental, Video, Staff
from app.videos.errors import NotFoundException

class VideosController:
    
    def __init__(self):
        pass

    def get_videos(self):
        videos = Video.query.order_by(Video.video_id).all()

        if not videos:
            raise NotFoundException
        
        self.videos = videos

        return videos