"""Geração de relatório de crédito em PDF."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def generate_credit_pdf(output_path: str | Path, analysis: dict[str, Any]) -> str:
    """Gera parecer de crédito em PDF para a análise atual."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(str(output_path), pagesize=A4, rightMargin=36, leftMargin=36, topMargin=42, bottomMargin=42)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=colors.HexColor("#0F172A"), spaceAfter=12)
    subtitle_style = ParagraphStyle("SubtitleStyle", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12, textColor=colors.HexColor("#1F2937"), spaceAfter=10)
    normal_style = ParagraphStyle("NormalCustom", parent=styles["BodyText"], fontName="Helvetica", fontSize=9, leading=12)

    content: list[Any] = []
    content.append(Paragraph("Angola Corporate Credit Decision Engine", title_style))
    content.append(Paragraph(f"Parecer de crédito — {datetime.now().strftime('%d/%m/%Y %H:%M')}", subtitle_style))
    content.append(Paragraph("Aviso: protótipo de apoio à decisão, sem substituir o comité de crédito nem qualquer aprovação regulatória.", normal_style))
    content.append(Spacer(1, 12))

    company = analysis.get("company_name", "Empresa de demonstração")
    recommendation = analysis.get("recommendation", "Solicitar informação adicional")
    score = analysis.get("score", 0)
    content.append(Paragraph(f"Resumo executivo: {company} — recomendação: {recommendation} — score: {score}", normal_style))
    content.append(Spacer(1, 12))

    currency = str(analysis.get("currency", "AOA")).upper()
    data_rows = [
        ["Campo", "Valor"],
        ["Empresa", company],
        ["Sector", analysis.get("sector", "-")],
        ["Província", analysis.get("province", "-")],
        ["Montante solicitado", f"{analysis.get('requested_amount', 0):,.2f} {currency}"],
        ["DSCR", f"{analysis.get('dscr', 0):.2f}x"],
        ["Score", f"{score:.2f}"],
        ["Classe", analysis.get("risk_class", "-")],
    ]
    table = Table(data_rows, colWidths=[160, 300])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.8, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
    ]))
    content.append(table)
    content.append(Spacer(1, 18))

    content.append(Paragraph("Factores positivos", subtitle_style))
    for item in analysis.get("positive_factors", []):
        content.append(Paragraph(f"- {item}", normal_style))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Factores negativos", subtitle_style))
    for item in analysis.get("negative_factors", []):
        content.append(Paragraph(f"- {item}", normal_style))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Condições", subtitle_style))
    for item in analysis.get("conditions", []):
        content.append(Paragraph(f"- {item}", normal_style))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Limitações", subtitle_style))
    content.append(Paragraph("Este relatório é um protótipo de apoio à decisão, baseado em regras transparentes e dados fictícios, sem substituir o comité de crédito, a validação regulatória ou a metodologia interna da instituição.", normal_style))
    content.append(Spacer(1, 18))

    doc.build(content)
    return str(output_path)
