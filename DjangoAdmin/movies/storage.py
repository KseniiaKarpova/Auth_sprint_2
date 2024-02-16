import requests
from django.conf import settings
from django.core.files.storage import Storage
from django.core.files.uploadedfile import InMemoryUploadedFile


class CustomStorage(Storage):
    def _save(self, name, content: InMemoryUploadedFile):
        r = requests.post(
            f'http://{settings.FILE_API_HOST}:{settings.FILE_API_PORT}{settings.FILE_API_URL}',
            files={'file': (content.name, content, content.content_type)}
        )
        return r.json().get('short_name')

    def url(self, name):
        return f'http://{settings.FILE_API_HOST}:{settings.FILE_API_PORT}{settings.FILE_API_URL}\
        /download-stream/{name}/'

    def exists(self, name):
        return False
