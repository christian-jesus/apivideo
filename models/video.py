# models/video.py
class Video:
    def __init__(self, title, description, content=None, url=None, duration=None):
        self.title = title
        self.description = description
        self.content = content
        self.url = url
        self.duration = duration

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "url": self.url,
            "duration": self.duration
        }
