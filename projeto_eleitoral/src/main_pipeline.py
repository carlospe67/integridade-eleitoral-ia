"""Pipeline principal integrando todos os módulos do projeto eleitoral."""

from __future__ import annotations

import argparse
from pathlib import Path

from synthetic_pipeline import generate_synthetic_data, detect_anomalies
from spatial_features import calculate_spatial_indicators, compute_lisa
from nlp_classifier import create_baseline_nlp_pipeline, train_classifier, classify_texts
from report_generator import generate_gemini_report


def run_pipeline(output_dir: Path) -> None:
    print("1. Gerando dados / carregando amostra...")
    data = generate_synthetic_data(n_sections=200)

    print("2. Calculando indicadores e LISA...")
    spatial_data = calculate_spatial_indicators(data)
    analyzed_spatial = compute_lisa(spatial_data, feature_col="share_candidate", k=5)

    print("3. Executando detecção de anomalias (Isolation Forest)...")
    detected = detect_anomalies(analyzed_spatial, contamination=0.05)

    print("4. Executando classificador PLN de relatos...")
    train_texts = [
        "homens armados impediram eleitores",
        "distribuiram dinheiro e cestas",
        "debate sobre propostas de governo",
    ]
    train_labels = ["coercao", "compra_de_votos", "discussao_politica"]
    nlp_pipe = create_baseline_nlp_pipeline()
    train_classifier(nlp_pipe, train_texts, train_labels)

    sample_reports = [
        "denuncia de homens armados na secao",
        "candidato pagou pix para votos",
    ]
    classifications = classify_texts(nlp_pipe, sample_reports)
    print(f"  Classificações de teste: {classifications}")

    print("5. Gerando relatório técnico...")
    metrics = {
        "total_sections": len(detected),
        "flagged_sections": int((detected["anomaly_label"] == -1).sum()),
        "patterns_detected": detected["synthetic_pattern"].unique().tolist(),
        "top_anomalies": detected,
    }
    report_content = generate_gemini_report(metrics)

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "complete_analysis.csv"
    report_path = output_dir / "technical_report.md"

    detected.to_csv(csv_path, index=False)
    report_path.write_text(report_content, encoding="utf-8")

    print(f"\nPipeline concluído com sucesso!")
    print(f"  - Dados salvos em: {csv_path}")
    print(f"  - Relatório salvo em: {report_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    project_root = Path(__file__).resolve().parents[1]
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=project_root / "outputs",
    )
    args = parser.parse_args()
    run_pipeline(args.output_dir)


if __name__ == "__main__":
    main()
