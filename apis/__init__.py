from flask import Blueprint

video_api = Blueprint('video_api', __name__)
auth_api = Blueprint('auth_api', __name__)
upload_api = Blueprint('upload_api', __name__)

from .video_api import *
from .auth_api import *
from .upload_api import *