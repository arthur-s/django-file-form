import json

from django.core.serializers.json import DjangoJSONEncoder

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed

from django_file_form.ajaxuploader.backends.local import LocalUploadBackend
from django_file_form.ajaxuploader.signals import file_uploaded

from django.conf import settings

class AjaxFileUploader(object):
    def __init__(self, backend=None, **kwargs):
        if backend is None:
            backend = LocalUploadBackend
        self.get_backend = lambda: backend(**kwargs)

    def __call__(self, request, *args, **kwargs):
        return self._ajax_upload(request, *args, **kwargs)

    def _ajax_upload(self, request, *args, **kwargs):
        if request.method == "POST":
            upload = request.FILES.get('qqfile', None)
            if not upload:
                return HttpResponseBadRequest("AJAX request not valid")

            # get chunks
            chunk_index = int(request.POST.get('qqpartindex'))
            total_chunks = int(request.POST.get('qqtotalparts'))


            filename = upload.name

            file_id = request.POST['qquuid']

            backend = self.get_backend()

            # custom filename handler
            filename = (backend.update_filename(request, filename, *args, **kwargs)
                        or filename)

            backend.setup(filename, *args, **kwargs)
            success = backend.upload_chunk(upload, *args, **kwargs)

            # callback - edited
            extra_context = None
            if total_chunks == chunk_index +1:
                extra_context = backend.upload_complete(request, filename, file_id, *args, **kwargs)
                # file_uploaded.send(sender=self.__class__, backend=backend, request=request)

            # let Ajax Upload know whether we saved it or not
            if settings.DEBUG:
                ret_json = {'success': success, 'filename': filename}
            else:
                ret_json = {'success': success}
            
            if extra_context is not None:
                if settings.DEBUG:
                    ret_json.update(extra_context)

            # although "application/json" is the correct content type, IE throws a fit
            return HttpResponse(json.dumps(ret_json, cls=DjangoJSONEncoder), content_type='text/html; charset=utf-8')
        else:
            response = HttpResponseNotAllowed(['POST'])
            response.write("ERROR: Only POST allowed")
            return response
