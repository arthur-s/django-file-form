from django.conf import settings


# Must the client be logged in for an upload or delete?
MUST_LOGIN = getattr(settings, 'FILE_FORM_MUST_LOGIN', False)

STORAGE = getattr(settings, 'FILE_FORM_STORAGE', settings.DEFAULT_FILE_STORAGE)
STORAGE_KWARGS = getattr(settings, 'FILE_FORM_STORAGE_KWARGS', {'location': settings.MEDIA_ROOT})