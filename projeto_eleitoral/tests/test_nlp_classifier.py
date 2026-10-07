from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from nlp_classifier import (
    create_baseline_nlp_pipeline,
    train_classifier,
    classify_texts,
)


def test_nlp_classifier_pipeline() -> None:
    train_texts = [
        "homens armados impediram a entrada dos eleitores na zona",
        "distribuiram dinheiro e cestas basicas em troca de votos na rua",
        "o debate de ontem teve propostas interessantes sobre educacao",
        "ameacaram fechar o comercio se nao votassem no candidato",
        "prometeram emprego e grana em troca do titulo de eleitor",
        "reuniao politica na praça com candidatos a vereador",
    ]
    train_labels = [
        "coercao",
        "compra_de_votos",
        "discussao_politica",
        "coercao",
        "compra_de_votos",
        "discussao_politica",
    ]

    pipeline = create_baseline_nlp_pipeline()
    trained = train_classifier(pipeline, train_texts, train_labels)

    test_texts = [
        "bandidos armados mandaram votar no 10",
        "pagaram pix de 50 reais para votarem",
        "qual sua opiniao sobre o plano de governo",
    ]
    results = classify_texts(trained, test_texts)

    assert len(results) == 3
    assert results[0][0] in {"coercao", "compra_de_votos", "discussao_politica"}
    assert 0.0 <= results[0][1] <= 1.0
