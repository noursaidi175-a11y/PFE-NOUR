import os
import pandas as pd
import joblib
import unicodedata
from django.shortcuts import render
from django.core.files.storage import default_storage


MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models')


kmeans = joblib.load(os.path.join(MODEL_DIR, 'kmeans_model.pkl'))
scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
imputer = joblib.load(os.path.join(MODEL_DIR, 'imputer.pkl'))
label_encoders = joblib.load(os.path.join(MODEL_DIR, 'label_encoders.pkl'))


def remove_accents(text):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', str(text)) if not unicodedata.combining(c)
    )

def clustering_view(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            
            file = request.FILES['file']
            file_path = default_storage.save(file.name, file)

           
            df = pd.read_csv(file_path, sep=';', encoding='utf-8')

            
            features = df[["ECHELON", "MVP_MNT", "MVP_NBR", "SEXE", "FONCTION", "EMPLOI", "COLLEGE"]].copy()

           
            cols_to_clean = ["SEXE", "FONCTION", "EMPLOI", "COLLEGE"]
            for col in cols_to_clean:
                features[col] = features[col].astype(str).str.strip().str.upper().apply(remove_accents)

          
            for col in cols_to_clean:
                encoder = label_encoders[col]
                features[col] = encoder.transform(features[col])

          
            features = features.applymap(lambda x: str(x).replace(',', '.') if isinstance(x, str) else x)

           
            for col in features.columns:
                features[col] = pd.to_numeric(features[col], errors='coerce')

         
            features_imputed = pd.DataFrame(imputer.transform(features), columns=features.columns)
            X_scaled = scaler.transform(features_imputed)

           
            clusters = kmeans.predict(X_scaled)
            df['Cluster'] = clusters

           
            return render(request, 'result.html', {
                'tables': df.to_html(classes='table table-bordered', index=False),
                'filename': file.name
            })

        except Exception as e:
            return render(request, 'upload.html', {'error': str(e)})

    return render(request, 'upload.html')
