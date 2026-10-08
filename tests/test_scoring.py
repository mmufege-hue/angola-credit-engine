from scoring import classify_score, calculate_score, evaluate_blocking_rules


def test_classification_by_score():
    assert classify_score(85) == "A"
    assert classify_score(72) == "B"
    assert classify_score(60) == "C"
    assert classify_score(44) == "D"
    assert classify_score(25) == "E"


def test_score_calculation_range():
    score = calculate_score({
        "dscr": 1.6,
        "current_ratio": 1.8,
        "debt_to_ebitda": 1.5,
        "payment_history": 95,
        "top_customer_concentration": 15,
        "guarantee_coverage": 0.9,
        "management_quality": 80,
        "information_quality": 85,
        "compliance_status": "bom",
        "documents_complete": True,
    })
    assert 0 <= score <= 100


def test_blocking_rules():
    validation = evaluate_blocking_rules({"documents_complete": False, "compliance_status": "risco", "guarantee_encumbrance": "incerto", "dscr": 0.9})
    assert validation["block_decision"] is True


def test_credit_application_uses_correct_term_field():
    from models import CreditApplication
    from sample_data import load_demo_companies

    application = CreditApplication.from_dict(load_demo_companies()[0])
    assert application.requested_term_months == 24


def test_blocked_application_cannot_be_presented_as_approved():
    from analysis_engine import analyse_credit
    from sample_data import load_demo_companies
    company = load_demo_companies()[1].copy()
    result = analyse_credit(company)
    assert result["blocking"]["block_decision"] is True
    assert result["recommendation"]["recommendation"] == "Decisão bloqueada"
