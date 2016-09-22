import six

from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class Example(models.Model):
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)

    title = models.CharField(max_length=255)
    input_file = models.FileField(max_length=255, upload_to='example', storage=fs)


class Example2(models.Model):
    title = models.CharField(max_length=255)


@six.python_2_unicode_compatible
class ExampleFile(models.Model):
    fs = FileSystemStorage(location=settings.MEDIA_ROOT)

    example = models.ForeignKey(Example2, related_name='files')
    input_file = models.FileField(max_length=255, upload_to='example', storage=fs)

    def __str__(self):
        return six.text_type(self.input_file)
