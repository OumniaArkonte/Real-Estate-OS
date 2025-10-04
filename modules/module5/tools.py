# =============================
# tools5.py - Mortgage & Financing Module
# =============================
from agno.tools import tool
from typing import Dict, Any, List, Optional
from datetime import datetime

# =============================
# Tool 1: Loan Option Engine (Agent 1)
# =============================
@tool(
    name="loan_option_engine",
    description="Génère plusieurs options de prêt en fonction du prix du bien, du revenu et du score de crédit",
    show_result=True,
)
def loan_option_engine(
    property_price: float,
    income: float,
    credit_score: int,
    max_options: int = 3,
) -> Dict[str, Any]:
    options: List[Dict[str, Any]] = []
    base_rates = [5.0, 5.5, 6.0]  # taux annuels simulés
    durations = [15, 20, 25]      # durée en années
    for i in range(min(max_options, len(base_rates))):
        rate = base_rates[i]
        years = durations[i]
        monthly_payment = round(property_price * (rate / 100) / 12, 2)
        options.append({
            "duration_years": years,
            "interest_rate": rate,
            "monthly_payment": monthly_payment,
        })
    return {
        "property_price": property_price,
        "income": income,
        "credit_score": credit_score,
        "loan_options": options,
        "generated_at": datetime.now().isoformat(),
    }

# =============================
# Tool 2: Eligibility Checker Engine (Agent 2)
# =============================
@tool(
    name="eligibility_checker_engine",
    description="Vérifie l'éligibilité d'un utilisateur à un prêt selon revenu, dettes et score de crédit",
    show_result=True,
)
def eligibility_checker_engine(
    monthly_debt: float,
    income: float,
    credit_score: int,
    max_dti: float = 0.4,
) -> Dict[str, Any]:
    dti_ratio = monthly_debt / income if income else 0
    eligible = dti_ratio <= max_dti and credit_score >= 650
    return {
        "monthly_debt": monthly_debt,
        "income": income,
        "credit_score": credit_score,
        "dti_ratio": round(dti_ratio, 2),
        "eligible": eligible,
        "checked_at": datetime.now().isoformat(),
    }

# =============================
# Tool 3: Payment Simulator Engine (Agent 3)
# =============================
@tool(
    name="payment_simulator_engine",
    description="Simule le calendrier des paiements pour un prêt donné et vérifie l'abordabilité",
    show_result=True,
)
def payment_simulator_engine(
    loan_amount: float,
    annual_rate: float,
    term_years: int,
    income: float,
) -> Dict[str, Any]:
    monthly_rate = annual_rate / 12 / 100
    num_payments = term_years * 12
    try:
        monthly_payment = round(
            loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1),
            2
        )
    except ZeroDivisionError:
        monthly_payment = loan_amount / num_payments
    affordability = monthly_payment / income <= 0.3
    schedule = [{"month": i + 1, "payment": monthly_payment} for i in range(num_payments)]
    return {
        "loan_amount": loan_amount,
        "annual_rate": annual_rate,
        "term_years": term_years,
        "monthly_payment": monthly_payment,
        "affordable": affordability,
        "payment_schedule": schedule[:12],  # retourne les 12 premiers mois par exemple
        "simulated_at": datetime.now().isoformat(),
    }
