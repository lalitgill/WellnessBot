from django.shortcuts import render
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import os
import uuid
from django.conf import settings
from reportocr.selectors import *

class UploadImages(views.APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        data = request.data
        userid = request.user.id
        image_file = request.FILES['image']
        NewFileName = str(uuid.uuid4())
        file_size = image_file.size
        mime_type = image_file.content_type

        original_filename = image_file.name
        file_extension = os.path.splitext(original_filename)[1]


        file_path = os.path.join(settings.MEDIA_ROOT, NewFileName)
        with open(file_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        DataResponse = {}
        DataResponse['responseCode'] = 200
        DataResponse['responseData'] = 'Image uploaded successfully.'
        return Response(DataResponse)