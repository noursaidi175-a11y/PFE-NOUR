from django.db import models
import joblib
import os
from django.conf import settings
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class CVRecommender:
    def __init__(self):
        base_path = os.path.join(settings.BASE_DIR, 'models')  # dossier models/ dans ton projet
        self.valid_keywords = joblib.load(os.path.join(base_path, 'valid_keywords.pkl'))
        self.vectorizer = joblib.load(os.path.join(base_path, 'tfidf_vectorizer.pkl'))

    def preprocess(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [t for t in tokens if t not in string.punctuation]
        stop_words = set(stopwords.words('english')).union(set(stopwords.words('french')))
        tokens = [t for t in tokens if t not in stop_words]
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(t) for t in tokens]
        return ' '.join(tokens)

    def extract_keywords(self, text, threshold=0.001):
        preprocessed = self.preprocess(text)
        tfidf_matrix = self.vectorizer.transform([preprocessed])
        tfidf_scores = tfidf_matrix.toarray().flatten()
        feature_names = self.vectorizer.get_feature_names_out()
        keyword_indices = [i for i, score in enumerate(tfidf_scores) if score > threshold]
        keywords = [feature_names[i] for i in keyword_indices]
        return keywords

    def is_valid_cv(self, text):
        keywords = self.extract_keywords(text)
        return any(kw in self.valid_keywords for kw in keywords), keywords

