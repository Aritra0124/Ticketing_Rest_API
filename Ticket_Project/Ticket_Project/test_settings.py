INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'ticket_app',
]
ROOT_URLCONF = 'Ticket_Project.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}