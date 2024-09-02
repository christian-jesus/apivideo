# routes/video_api.py
from flask import Blueprint, jsonify, request, Response
from services.mongo_service import MongoService
from models.video import Video
from bson import ObjectId

video_api = Blueprint('video_api', __name__)

@video_api.route('/videos', methods=['GET'])
def get_videos():
    videos = MongoService().get_all_videos()
    videos_data = []
    for video in videos:
        video_data = {
            'id': str(video.id),
            'title': video.title,
            'description': video.description,
            'url': video.url if video.url else f'/videos/{str(video.id)}/content',
            'duration': video.duration
        }
        videos_data.append(video_data)
    return jsonify(videos_data)

@video_api.route('/videos', methods=['POST'])
def upload_video():
    data = request.form
    
    if 'file' in request.files:
        file = request.files['file']
        content = file.read()
        video = Video(data['title'], data['description'], content=content, duration=data.get('duration'))
        MongoService().insert_video(video)
    elif 'url' in data:
        url = data['url']
        video = Video(data['title'], data['description'], url=url, duration=data.get('duration'))
        MongoService().insert_video(video)
    else:
        return jsonify({'error': 'No video provided'}), 400

    return jsonify({'message': 'Video uploaded successfully'})

@video_api.route('/videos/<video_id>/content', methods=['GET'])
def get_video_content(video_id):
    video = MongoService().get_video_by_id(video_id)
    if video and video.content:
        return Response(video.content, mimetype='video/mp4')
    else:
        return jsonify({'error': 'Video not found or no content available'}), 404

@video_api.route('/videos/<video_id>', methods=['GET'])
def get_video(video_id):
    video = MongoService().get_video_by_id(video_id)
    if video:
        video_data = {
            'id': str(video.id),
            'title': video.title,
            'description': video.description,
            'url': video.url if video.url else f'/videos/{str(video.id)}/content',
            'duration': video.duration
        }
        return jsonify(video_data)
    else:
        return jsonify({'error': 'Video not found'}), 404

@video_api.route('/videos/<video_id>/watch', methods=['POST'])
def watch_video(video_id):
    time_watched = request.form['time_watched']
    MongoService().update_video_watch_time(video_id, time_watched)
    return jsonify({'message': 'Watch time updated'})
