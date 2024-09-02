# app.py
from flask import Flask, jsonify, request, Response, render_template, redirect, url_for
from services.mongo_service import MongoService
from models.video import Video
from bson import ObjectId

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_videos', methods=['GET'])
def get_videos():
    videos = MongoService().get_all_videos()
    # Convertir ObjectId a string antes de pasar a la plantilla
    for video in videos:
        video['_id'] = str(video['_id'])
    return render_template('videos.html', videos=videos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        duration = request.form.get('duration')

        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            content = file.read()
            video = Video(title, description, content=content, duration=duration)
            MongoService().insert_video(video.to_dict())
        elif 'url' in request.form and request.form['url']:
            url = request.form['url']
            video = Video(title, description, url=url, duration=duration)
            MongoService().insert_video(video.to_dict())
        else:
            return jsonify({'error': 'No video provided'}), 400

        return redirect(url_for('get_videos'))
    return render_template('upload.html')

@app.route('/videos/<video_id>/content', methods=['GET'])
def get_video_content(video_id):
    video = MongoService().get_video_by_id(video_id)
    if video and 'content' in video:
        return Response(video['content'], mimetype='video/mp4')
    else:
        return jsonify({'error': 'Video not found or no content available'}), 404

@app.route('/videos/<video_id>', methods=['GET'])
def get_video(video_id):
    video = MongoService().get_video_by_id(video_id)
    if video:
        video_data = {
            'id': str(video['_id']),
            'title': video['title'],
            'description': video['description'],
            'url': video['url'] if 'url' in video else f'/videos/{str(video["_id"])}/content',
            'duration': video['duration']
        }
        return jsonify(video_data)
    else:
        return jsonify({'error': 'Video not found'}), 404

@app.route('/videos/<video_id>/watch', methods=['POST'])
def watch_video(video_id):
    time_watched = request.form['time_watched']
    MongoService().update_video_watch_time(video_id, time_watched)
    return jsonify({'message': 'Watch time updated'})

if __name__ == '__main__':
    app.run(debug=True)
