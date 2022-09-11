import ffmpeg
from pydantic import BaseModel


class VideoModel(BaseModel):
    path: str
    name: str
    framerate: float
    raw_probe: dict

def classVideo():
    def __init__(self):

