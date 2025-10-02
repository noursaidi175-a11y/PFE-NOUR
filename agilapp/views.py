from django.shortcuts import render
from django.http import JsonResponse
from .models import TurnoverModel
import pandas as pd

def form_predict_turnover(request):
    sexes = ['M', 'F']
    sens = ['1','2']
    geo = ['Nord', 'Sud', 'Est', 'Ouest']
    ufa = ['UFA1', 'UFA2', 'UFA3']
    college = ['Cadre', 'Non Cadre', 'Technicien']
    echelle = ['Echelle 1', 'Echelle 2', 'Echelle 3']
    fonction = ['Fonction A', 'Fonction B', 'Fonction C']
    emploi = ['CDI', 'CDD', 'Intérim']

    if request.method == 'POST':
        data = {
            'SEXE': request.POST['sexe'],
            'SENS': request.POST['sens'],
            'GEO_DSG': request.POST['geo'],
            'LIB_UFA': request.POST['ufa'],
            'COLLEGE': request.POST['college'],
            'ECHELLE': request.POST['echelle'],
            'FONCTION': request.POST['fonction'],
            'EMPLOI': request.POST['emploi'],
        }

        df = pd.DataFrame([data])
        model = TurnoverModel()
        prediction, probability = model.predict(df)

        context = {
            'prediction': 'Départ' if prediction == 1 else 'Reste',
            'probability': round(probability * 100, 2),
        }

        # Si c'est AJAX, on renvoie du JSON avec le HTML partiel
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render(request, 'result_content.html', context).content.decode('utf-8')
            return JsonResponse({'html': html})

        # Sinon, rendu normal (classique)
        return render(request, 'result.html', context)

    # GET => afficher formulaire
    return render(request, 'form.html', {
        'sexes': sexes,
        'sens': sens,
        'geo': geo,
        'ufa': ufa,
        'college': college,
        'echelle': echelle,
        'fonction': fonction,
        'emploi': emploi,
    })
