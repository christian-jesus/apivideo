# services/mongo_service.py
from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoService:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['apptok']
        self.videos_collection = self.db['prueba']

    def get_all_videos(self):
        return list(self.videos_collection.find())

    def insert_video(self, video):
        self.videos_collection.insert_one(video)

    def get_video_by_id(self, video_id):
        return self.videos_collection.find_one({"_id": ObjectId(video_id)})

    def update_video_watch_time(self, video_id, time_watched):
        self.videos_collection.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {"time_watched": time_watched}}
        )
