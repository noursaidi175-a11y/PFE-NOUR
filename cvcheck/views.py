from django.shortcuts import render
from .models import CVRecommender
from PyPDF2 import PdfReader

def cv_upload_view(request):
    result = None
    keywords = []
    
    if request.method == 'POST' and request.FILES['cv']:
        uploaded_file = request.FILES['cv']
        reader = PdfReader(uploaded_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        
        model = CVRecommender()
        is_valid, keywords = model.is_valid_cv(text)
        result = "CV Valide ✅" if is_valid else "CV Non Valide ❌"

    return render(request, 'cv_form.html', {
        'result': result,
        'keywords': keywords
    })

