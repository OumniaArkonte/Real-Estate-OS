# module3.py - Market Analysis Module

import os
import ast
from pathlib import Path
from dotenv import load_dotenv
from agno.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from agno.knowledge.embedder.mistral import MistralEmbedder
from agno.agent import Agent
from agno.team.team import Team
from agno.models.mistral import MistralChat
from agno.tools.pandas import PandasTools
from agno.tools.calculator import CalculatorTools
from agno.tools.file import FileTools

# Import des outils custom
try:
    from .tools import aggregate_market_data, analyze_trends, forecast_market, generate_visual_reports
except ImportError:
    from tools import aggregate_market_data, analyze_trends, forecast_market, generate_visual_reports

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()



# =============================
# Agent 1: Data Aggregator Agent
# =============================
DataAggregatorAgent = Agent(
    name="Data Aggregator Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[PandasTools(), FileTools(base_dir=Path(os.path.join(os.path.dirname(__file__), "documents3"))), aggregate_market_data],
    description="""
    Un agent IA centré sur la collecte et l'agrégation des données de marché
    depuis datasets historiques, listings publics et autres sources fiables.
    """,
    instructions="""
    Vous êtes DataAggregatorAgent.

    ## Agent Responsibilities
    1. Collecter des datasets de marché (prix, offres, ventes passées).
    2. Normaliser et dédupliquer les données.
    3. Produire une sortie prête pour l'analyse (aggregated_market_data).

    ## Tool Usage Guidelines
    - PandasTools pour la manipulation et nettoyage des données.
    - FileTools pour lire/écrire fichiers locaux.
    - aggregate_market_data pour l'agrégation des datasets.

    ## Sortie attendue
    - aggregated_market_data
    - entries_count
    - aggregated_at
    """,
    markdown=True,
    #knowledge=knowledge_base,
)

# =============================
# Agent 2: Trend Analysis Agent
# =============================
TrendAnalysisAgent = Agent(
    name="Trend Analysis Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[CalculatorTools(), analyze_trends],
    description="""
    Un agent IA qui analyse les tendances de prix et fluctuations sur le marché immobilier.
    """,
    instructions="""
    Vous êtes TrendAnalysisAgent.

    ## Agent Responsibilities
    1. Recevoir les données agrégées du marché.
    2. Calculer les indicateurs de tendance et de volatilité.
    3. Identifier les segments de marché avec forte variation.

    ## Tool Usage Guidelines
    - CalculatorTools pour calculs et statistiques.
    - analyze_trends pour produire les métriques de tendance.

    ## Sortie attendue
    - trend_indicators
    - price_fluctuation_metrics
    - analyzed_at
    """,
    markdown=True,
    #knowledge=knowledge_base,
)

# =============================
# Agent 3: Forecasting Agent
# =============================
ForecastingAgent = Agent(
    name="Forecasting Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[forecast_market],
    description="""
    Un agent IA qui prévoit l'évolution future des prix immobiliers
    en utilisant les indicateurs de tendance et données historiques.
    """,
    instructions="""
    Vous êtes ForecastingAgent.

    ## Agent Responsibilities
    1. Recevoir les indicateurs de tendance.
    2. Prévoir les prix pour les 6-12 prochains mois.
    3. Fournir une estimation claire pour chaque période.

    ## Tool Usage Guidelines
    - forecast_market pour produire les prévisions de prix.
    
    ## Sortie attendue
    - future_market_predictions
    - forecast_generated_at
    """,
    markdown=True,
    #knowledge=knowledge_base,
)

# =============================
# Agent 4: Visualization Agent
# =============================
VisualizationAgent = Agent(
    name="Visualization Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[generate_visual_reports, FileTools(base_dir=Path(os.path.join(os.path.dirname(__file__), "reports3")))],
    description="""
    Un agent IA qui génère des rapports visuels et graphiques basés sur les prévisions de marché.
    """,
    instructions="""
    Vous êtes VisualizationAgent.

    ## Agent Responsibilities
    1. Recevoir les prévisions de marché.
    2. Produire des résumés statistiques et graphiques.
    3. Sauvegarder les rapports localement.

    ## Tool Usage Guidelines
    - generate_visual_reports pour créer les summaries et graphiques.
    - FileTools pour gérer l'enregistrement des fichiers.

    ## Sortie attendue
    - visual_reports
    - generated_at
    - output_file
    """,
    markdown=True,
    #knowledge=knowledge_base,
)

# =============================
# Team: Market Analysis Team (Module)
# =============================
MarketAnalysisTeam = Team(
    name="MarketAnalysis",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    members=[DataAggregatorAgent, TrendAnalysisAgent, ForecastingAgent, VisualizationAgent],
    description="""
    Module complet d'analyse du marché immobilier:
    collecte, analyse, prévision et visualisation.
    """,
    instructions="""
    ## Workflow conseillé
    1) DataAggregatorAgent → collecte et agrégation des données
    2) TrendAnalysisAgent → analyse des tendances et fluctuations
    3) ForecastingAgent → prévision des prix futurs
    4) VisualizationAgent → génération des rapports visuels
    """,
    markdown=True,
    #knowledge=knowledge_base,
)


if __name__ == "__main__":
    print("Market Analysis Module loaded ✅")

    datasets_example = [
        {"location": "Casablanca", "price": 1800000, "date": "2025-01-01"},
        {"location": "Casablanca", "price": 1850000, "date": "2025-02-01"},
        {"location": "Casablanca", "price": 1780000, "date": "2025-03-01"},
    ]

    # Utiliser print_response pour obtenir le rendu style module1
    DataAggregatorAgent.print_response(input=datasets_example)
    TrendAnalysisAgent.print_response(input=datasets_example)  
    ForecastingAgent.print_response(input=datasets_example)    
    VisualizationAgent.print_response(input=datasets_example)  
