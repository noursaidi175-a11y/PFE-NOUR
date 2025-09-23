from django.db import models
import joblib
import os
from django.conf import settings

class TurnoverModel:
    def __init__(self):
        base_path = os.path.join(settings.BASE_DIR, 'models')  # chemin vers dossier models/
        model_path = os.path.join(base_path, 'turnover_model.pkl')
        self.model = joblib.load(model_path)

    def predict(self, data):
        prediction = self.model.predict(data)[0]
        probability = self.model.predict_proba(data)[0][1]
        return prediction, probability

        

