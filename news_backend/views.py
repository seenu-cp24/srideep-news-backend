from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def test_s3(request):
    try:
        default_storage.save("media_test.txt", ContentFile("S3 upload successful"))
        return HttpResponse("S3 upload OK")
    except Exception as e:
        return HttpResponse(f"S3 ERROR: {e}")
