# =============================
# tools.py - Investment Analysis Module
# =============================
from agno.tools import tool
from typing import Dict, Any
from datetime import datetime


# =============================
# Tool 1: ROI Calculator (Agent 1)
# =============================
@tool(
    name="roi_calculator",
    description="Calcule le retour sur investissement (ROI) à partir du prix du bien, revenus locatifs et coûts",
    show_result=True,
)
def roi_calculator(
    property_price: float,
    rental_income: float,
    expenses: float
) -> Dict[str, Any]:
    try:
        roi = (rental_income - expenses) / property_price
    except ZeroDivisionError:
        roi = 0.0
    return {
        "property_price": property_price,
        "rental_income": rental_income,
        "expenses": expenses,
        "roi": round(roi, 4),
        "calculated_at": datetime.now().isoformat(),
    }


# =============================
# Tool 2: Risk Analysis (Agent 2)
# =============================
@tool(
    name="risk_analysis",
    description="Évalue le risque d'investissement basé sur tendances du marché et ROI",
    show_result=True,
)
def risk_analysis(
    market_trends: Dict[str, Any],
    roi_metrics: Dict[str, Any]
) -> Dict[str, Any]:
    roi = roi_metrics.get("roi", 0)
    volatility = market_trends.get("volatility", 0.1)
    risk_score = min(max(volatility * (1 - roi), 0), 1)
    return {
        "roi": roi,
        "market_volatility": volatility,
        "risk_score": round(risk_score, 4),
        "analyzed_at": datetime.now().isoformat(),
    }


# =============================
# Tool 3: Cash Flow Projection (Agent 3)
# =============================
@tool(
    name="cash_flow_projection",
    description="Projette les flux de trésorerie d'une propriété en tenant compte du financement et des revenus",
    show_result=True,
)
def cash_flow_projection(
    purchase_price: float,
    rental_income: float,
    expenses: float,
    mortgage_payment: float,
    years: int = 5
) -> Dict[str, Any]:
    projections = []
    for year in range(1, years + 1):
        net_cash_flow = rental_income - expenses - mortgage_payment
        projections.append({"year": year, "net_cash_flow": net_cash_flow})
    return {
        "purchase_price": purchase_price,
        "years": years,
        "projections": projections,
        "projected_at": datetime.now().isoformat(),
    }
