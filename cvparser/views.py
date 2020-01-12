import os

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from pyresparser import ResumeParser

import nltk

nltk.data.path.append(settings.NLTK_DATA_PATH)


# Create your views here.
def home(request):
    msg = None
    skills = None
    allowed_file_type = ['application/pdf']
    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        file_path = None
        if resume_file:
            if resume_file.content_type in allowed_file_type:
                try:
                    fs = FileSystemStorage()
                    filename = fs.save(resume_file.name, resume_file)
                    file_path = os.path.join(fs.location, filename)

                    parsed_data = ResumeParser(file_path).get_extracted_data()
                except Exception as e:
                    msg = f"Error occurred while parsing the CV. Detail error msg: {str(e)}"
                else:
                    skills = parsed_data.get('skills')
                finally:
                    if file_path and os.path.isfile(file_path):
                        os.remove(file_path)
            else:
                msg = "Please provide pdf and docx document"
        else:
            msg = "Please upload your resume"
    return render(request, 'home.html', context={'msg': msg, 'skills': skills})
