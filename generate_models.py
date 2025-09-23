import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# Exemple de corpus de CV
corpus = [
    "Experienced Python developer with strong skills in machine learning and data analysis.",
    "Data engineer with solid SQL and ETL pipeline experience.",
    "AI specialist working on NLP and deep learning models."
]

# Créer le vecteur TF-IDF
vectorizer = TfidfVectorizer()
vectorizer.fit(corpus)

# Créer une liste de mots-clés valides
valid_keywords = ["python", "machine", "learning", "data", "sql", "nlp", "deep"]

# Sauvegarder proprement dans le bon dossier
os.makedirs("models", exist_ok=True)
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")
joblib.dump(valid_keywords, "models/valid_keywords.pkl")

print("✅ Modèles .pkl générés avec Python 3.11.")
