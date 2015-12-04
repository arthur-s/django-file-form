from django.conf import settings


# Must the client be logged in for an upload or delete?
MUST_LOGIN = getattr(settings, 'FILE_FORM_MUST_LOGIN', False)

STORAGE = getattr(settings, 'FILE_FORM_STORAGE', 'django.core.files.storage.FileSystemStorage')
STORAGE_KWARGS = getattr(settings, 'FILE_FORM_STORAGE_KWARGS', {'location': settings.MEDIA_ROOT})

HOSTNAME = getattr(settings, 'FILE_FORM_HOSTNAME', '')
