from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Reports
import numpy as np
from .forms import FileUploadForm
import google.generativeai as genai
import time
import re
from sentence_transformers import SentenceTransformer
from django.conf import settings
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.docstore.document import Document

from include.DocumentStoreRetriveEmbed import DocumentStore

from include.AzureOcrHelper import AzureOcrHelper

AzureOcrObj = AzureOcrHelper()

document_store = DocumentStore()

@login_required
def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Create user-specific directory if it doesn't exist
            user_dir = os.path.join(settings.MEDIA_ROOT, str(request.user.id))
            os.makedirs(user_dir, exist_ok=True)

            uploaded_file = request.FILES['file']
            file_upload = form.save(commit=False)
            file_upload.user = request.user
            file_upload.save()

            # Save the file temporarily
            temp_path = os.path.join(settings.MEDIA_ROOT, 'temp', uploaded_file.name)
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            with open(temp_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            extracted_text = AzureOcrObj.azure_ocr(temp_path)
            os.remove(temp_path)

            metadata = {
                "filename": uploaded_file.name,
                "report_type": "medical",
                "upload_date": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            document_store.store_document(request.user.id, uploaded_file.name, extracted_text, metadata)
            document_store.persist_all()
            file_upload.extracted_text = extracted_text
            file_upload.summary = ''
            file_upload.save()

        return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'file_upload.html', {'form': form})

@login_required
def file_edit(request, file_id):
    file = get_object_or_404(Reports, id=file_id, user=request.user)
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES, instance=file)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = FileUploadForm(instance=file)
    return render(request, 'file_edit.html', {'form': form, 'file': file})

@login_required
def file_list(request):
    files = Reports.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'file_list.html', {'files': files})