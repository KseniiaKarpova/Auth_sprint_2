import os

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('PG_ENGINE'),
        'NAME': os.environ.get('CINEMA_POSTGRES_NAME'),
        'USER': os.environ.get('CINEMA_POSTGRES_USER'),
        'PASSWORD': os.environ.get('CINEMA_POSTGRES_PASSWORD'),
        'HOST': os.environ.get('CINEMA_POSTGRES_HOST'),
        'PORT': os.environ.get('CINEMA_POSTGRES_PORT'),
        'OPTIONS': {
            # Нужно явно указать схемы, с которыми будет работать приложение.
            'options': '-c search_path=public,content'
        }
    }
}
