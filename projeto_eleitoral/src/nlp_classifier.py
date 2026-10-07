"""Módulo de PLN para Classificação de Relatos (Coação, Compra de Votos, Discussão Comum)."""

from __future__ import annotations

from typing import List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def create_baseline_nlp_pipeline() -> Pipeline:
    """Cria pipeline TF-IDF + Logistic Regression para classificação de textos em português."""
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
        ("clf", LogisticRegression(random_state=42, max_iter=1000)),
    ])


def train_classifier(pipeline: Pipeline, texts: List[str], labels: List[str]) -> Pipeline:
    """Treina o classificador com textos e rótulos fornecidos."""
    pipeline.fit(texts, labels)
    return pipeline


def classify_texts(pipeline: Pipeline, texts: List[str]) -> List[Tuple[str, float]]:
    """Classifica novos textos retornando a categoria prevista e a probabilidade máxima."""
    predictions = pipeline.predict(texts)
    probabilities = pipeline.predict_proba(texts)
    max_probs = np.max(probabilities, axis=1)
    return list(zip(predictions, max_probs))
