# module4.py - Investment Analysis Module

import os
from pathlib import Path
from dotenv import load_dotenv
from agno.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from agno.knowledge.embedder.mistral import MistralEmbedder
from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.agent import Agent
from agno.team.team import Team
from agno.models.mistral import MistralChat
from agno.tools.calculator import CalculatorTools
from agno.tools.pandas import PandasTools

# Import des outils custom
try:
    from .tools import roi_calculator, risk_analysis, cash_flow_projection
except ImportError:
    from tools import roi_calculator, risk_analysis, cash_flow_projection

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()


# ----------------------------
# Knowledge Base Setup
# ----------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5432/investment"

markdown_reader = MarkdownReader(name="Investment Analysis Reader")

vector_db = PgVector(
    table_name="investment_docs",
    db_url=db_url,
    embedder=MistralEmbedder(api_key=os.getenv("MISTRAL_API_KEY"), dimensions=1024)
)

knowledge_base = Knowledge(
    name="Investment KB",
    vector_db=vector_db,
    max_results=5
)

# =============================
# Agent 1: ROI Calculator Agent
# =============================
ROICalculatorAgent = Agent(
    name="ROI Calculator Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[CalculatorTools(), roi_calculator],
    description="""
    Un agent IA chargé de calculer le retour sur investissement d'une propriété
    à partir du prix, revenus locatifs et dépenses.
    """,
    instructions="""
    Vous êtes ROICalculatorAgent. Calculez le ROI pour une propriété donnée.

    ## Agent Responsibilities
    1. Recevoir les données financières du bien.
    2. Calculer le ROI.
    3. Retourner des métriques claires et détaillées.

    ## Tool Usage Guidelines
    - CalculatorTools pour calculs financiers.
    - roi_calculator pour exécuter le calcul du ROI.

    ## Sortie attendue
    - roi_metrics
    """,
    markdown=True,
    knowledge=knowledge_base
)

# =============================
# Agent 2: Risk Analysis Agent
# =============================
RiskAnalysisAgent = Agent(
    name="Risk Analysis Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[CalculatorTools(), PandasTools(), risk_analysis],
    description="""
    Un agent IA chargé d'évaluer le risque d'investissement basé sur les tendances du marché et le ROI.
    """,
    instructions="""
    Vous êtes RiskAnalysisAgent. Évaluez le risque associé à l'investissement.

    ## Agent Responsibilities
    1. Recevoir ROI et tendances du marché.
    2. Calculer un score de risque normalisé.
    3. Fournir un rapport synthétique.

    ## Tool Usage Guidelines
    - CalculatorTools et PandasTools pour calcul et traitement des données.
    - risk_analysis pour produire le score de risque.

    ## Sortie attendue
    - risk_assessment
    """,
    markdown=True,
    knowledge=knowledge_base
)

# =============================
# Agent 3: Cash Flow Projection Agent
# =============================
CashFlowProjectionAgent = Agent(
    name="Cash Flow Projection Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[CalculatorTools(), PandasTools(), cash_flow_projection],
    description="""
    Un agent IA qui projette les flux de trésorerie futurs d'une propriété en tenant compte
    des revenus, dépenses et paiements hypothécaires.
    """,
    instructions="""
    Vous êtes CashFlowProjectionAgent. Produisez les projections de flux de trésorerie.

    ## Agent Responsibilities
    1. Recevoir données financières et hypothèque.
    2. Calculer les flux de trésorerie pour chaque année.
    3. Fournir un tableau clair des projections.

    ## Tool Usage Guidelines
    - CalculatorTools et PandasTools pour traitement et calcul.
    - cash_flow_projection pour produire les projections.

    ## Sortie attendue
    - cash_flow_projections
    """,
    markdown=True,
    knowledge=knowledge_base
)

# =============================
# Team: Investment Analysis Team (Module)
# =============================
InvestmentAnalysisTeam = Team(
    name="InvestmentAnalysis",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    members=[
        ROICalculatorAgent,
        RiskAnalysisAgent,
        CashFlowProjectionAgent,
    ],
    description="""
    Module complet pour analyser la rentabilité et le risque d'investissement immobilier,
    et projeter les flux de trésorerie futurs.
    """,
    instructions="""
    Coordination des agents:
    1) ROICalculatorAgent → calcul du ROI
    2) RiskAnalysisAgent → évaluation du risque
    3) CashFlowProjectionAgent → projections des flux de trésorerie
    """,
    markdown=True,
)

if __name__ == "__main__":
    print("Investment Analysis Module loaded ✅")
    ROICalculatorAgent.print_response(input="Calculate ROI for property price 2,000,000 MAD, rental 120,000 MAD, expenses 20,000 MAD")
    RiskAnalysisAgent.print_response(input="Assess risk using market trends {'volatility': 0.15} and ROI 0.05")
    CashFlowProjectionAgent.print_response(input="Project cash flow for 5 years with mortgage 15,000 MAD/year")
