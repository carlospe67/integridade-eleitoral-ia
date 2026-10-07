from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from report_generator import generate_technical_summary, generate_gemini_report


def test_generate_technical_summary() -> None:
    metrics = {"total_sections": 100, "flagged_sections": 5}
    report = generate_technical_summary(metrics)
    assert "100" in report
    assert "5" in report
    assert "Relatório Técnico" in report


def test_generate_gemini_report_fallback(monkeypatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    metrics = {"total_sections": 100, "flagged_sections": 5}
    report = generate_gemini_report(metrics, api_key="")
    assert "Relatório Técnico" in report
    assert "GEMINI_API_KEY" in report
