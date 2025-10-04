# module5.py - Mortgage & Financing Module

import os
from pathlib import Path
from dotenv import load_dotenv

from agno.agent import Agent
from agno.team.team import Team
from agno.models.mistral import MistralChat
from agno.tools.file import FileTools
from agno.tools.pandas import PandasTools
from agno.tools.calculator import CalculatorTools

from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.knowledge.embedder.mistral import MistralEmbedder

# Import des outils custom
try:
    from .tools import (
        loan_option_engine,
        eligibility_checker_engine,
        payment_simulator_engine,
    )
except ImportError:
    from tools import (
        loan_option_engine,
        eligibility_checker_engine,
        payment_simulator_engine,
    )

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

# ----------------------------
# Knowledge Base
# ----------------------------
db_uri = os.path.join(os.path.dirname(__file__), "mortgage_finance_index")

markdown_reader = MarkdownReader(name="Mortgage & Financing Reader")

vector_db = LanceDb(
    uri=db_uri,
    table_name="mortgage_financing_docs",
    embedder=MistralEmbedder(api_key=os.getenv("MISTRAL_API_KEY"), dimensions=1024),
)

knowledge_base = Knowledge(
    name="Mortgage & Financing KB",
    vector_db=vector_db,
    max_results=5,
)

# =============================
# Agent 1: Loan Options Agent
# =============================
LoanOptionsAgent = Agent(
    name="Loan Options Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(base_dir=Path(os.path.join(os.path.dirname(__file__), "documents2"))),
        PandasTools(),
        CalculatorTools(),
        loan_option_engine,
    ],
    description="""
    Un agent IA qui propose des options de prêt (durée, taux, mensualité)
    en fonction du prix du bien, des revenus et du profil utilisateur.
    """,
    instructions="""
    Vous êtes LoanOptionsAgent.

    ## Agent Responsibilities
    1. Prendre en entrée prix du bien, revenu et score de crédit.
    2. Générer plusieurs options de prêt (durée, taux, mensualité).
    3. Fournir un résumé clair des options.

    ## Tool Usage Guidelines
    - CalculatorTools pour calculer mensualités.
    - PandasTools pour organiser les données.
    - FileTools pour stocker ou lire documents de prêt.
    - loan_option_engine pour générer les options de prêt.

    ## Sortie attendue
    - loan_options
    """,
    markdown=True,
    knowledge=knowledge_base,
)

# =============================
# Agent 2: Eligibility Checker Agent
# =============================
EligibilityCheckerAgent = Agent(
    name="Eligibility Checker Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        CalculatorTools(),
        PandasTools(),
        eligibility_checker_engine,
    ],
    description="""
    Un agent IA qui évalue l'éligibilité d’un utilisateur à un prêt
    selon ses revenus, dettes et score de crédit.
    """,
    instructions="""
    Vous êtes EligibilityCheckerAgent.

    ## Agent Responsibilities
    1. Vérifier le ratio dette/revenu (DTI).
    2. Évaluer la compatibilité avec des seuils bancaires.
    3. Produire un statut clair d’éligibilité.

    ## Tool Usage Guidelines
    - CalculatorTools pour ratios financiers.
    - PandasTools pour structurer les données.
    - eligibility_checker_engine pour l'évaluation de l'éligibilité.

    ## Sortie attendue
    - eligibility_status
    """,
    markdown=True,
    knowledge=knowledge_base,
)

# =============================
# Agent 3: Payment Simulator Agent
# =============================
PaymentSimulatorAgent = Agent(
    name="Payment Simulator Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        CalculatorTools(),
        PandasTools(),
        FileTools(base_dir=Path(os.path.join(os.path.dirname(__file__), "documents5"))),
        payment_simulator_engine,
    ],
    description="""
    Un agent IA qui simule le calendrier des paiements et vérifie l'abordabilité.
    """,
    instructions="""
    Vous êtes PaymentSimulatorAgent.

    ## Agent Responsibilities
    1. Simuler un échéancier de paiements pour un prêt donné.
    2. Vérifier l'abordabilité en fonction du revenu utilisateur.
    3. Produire un rapport clair avec paiements annuels.

    ## Tool Usage Guidelines
    - CalculatorTools pour mensualités et échéancier.
    - PandasTools pour organisation des données.
    - FileTools pour stocker les rapports.
    - payment_simulator_engine pour générer le calendrier et le rapport.

    ## Sortie attendue
    - payment_schedule
    - affordability_report
    """,
    markdown=True,
    knowledge=knowledge_base,
)

# =============================
# Team: Mortgage & Financing Team
# =============================
MortgageFinancingTeam = Team(
    name="MortgageFinancing",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    members=[
        LoanOptionsAgent,
        EligibilityCheckerAgent,
        PaymentSimulatorAgent,
    ],
    description="""
    Un module de simulation hypothécaire et financement.
    Il génère des options de prêt, vérifie l'éligibilité et produit des simulations de paiements.
    """,
    instructions="""
    Le module MortgageFinancing orchestre 3 agents spécialisés.

    ## Rôles et coordination
    - LoanOptionsAgent: propose des options de prêt.
    - EligibilityCheckerAgent: vérifie l'éligibilité de l'utilisateur.
    - PaymentSimulatorAgent: produit des échéanciers et rapports d'abordabilité.

    ## Workflow conseillé
    1) LoanOptionsAgent → options de prêt
    2) EligibilityCheckerAgent → statut éligibilité
    3) PaymentSimulatorAgent → calendrier + rapport

    ## Standards de sortie
    - Liste d'options de prêt avec mensualités.
    - Statut d'éligibilité avec justification.
    - Rapport d'échéancier clair.
    """,
    markdown=True,
    knowledge=knowledge_base,
)

if __name__ == "__main__":
    print("Mortgage & Financing Module loaded successfully ✅")
    LoanOptionsAgent.print_response(input="Loan options for property price 1,000,000 MAD, income 30,000 MAD, credit score 700.")
    EligibilityCheckerAgent.print_response(input="Check eligibility for monthly debt 5,000 MAD, income 25,000 MAD.")
    PaymentSimulatorAgent.print_response(input="Simulate payments for loan 1,000,000 MAD at 5% over 20 years, income 25,000 MAD.")
