# module1.py - Property Valuation Module

import os
from pathlib import Path
from dotenv import load_dotenv
from agno.agent import Agent
from agno.team.team import Team
from agno.models.mistral import MistralChat
from agno.tools.file import FileTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.pandas import PandasTools
from agno.tools.calculator import CalculatorTools

from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from agno.knowledge.embedder.mistral import MistralEmbedder

# Import des outils custom
try:
    from .tools import (
        avm_engine,
        web_property_scraper,
        document_property_parser,
        kb_ingest_indexer,
        valuation_model_runner,
    )
except ImportError:
    from tools import (
        avm_engine,
        web_property_scraper,
        document_property_parser,
        kb_ingest_indexer,
        valuation_model_runner,
    )

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

# ----------------------------
# Knowledge Base
# ----------------------------
"""
db_url = "postgresql+psycopg://ai:ai@localhost:5432/ai"

markdown_reader = MarkdownReader(name="Property Valuation Reader")

vector_db = PgVector(
    table_name="property_valuation_docs",
    db_url=db_url,
    embedder=MistralEmbedder(api_key=os.getenv("MISTRAL_API_KEY"), dimensions=1024)
)

knowledge_base = Knowledge(
    name="Property Valuation KB",
    vector_db=vector_db,
    max_results=5
)
"""
# =============================
# Agent 1: Data Collector Agent
# =============================
DataCollectorAgent = Agent(
    name="Data Collector Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(base_dir=Path(os.path.join(os.path.dirname(__file__), "documents1"))),
        GoogleSearchTools(),
        PandasTools(),
        avm_engine,
        web_property_scraper,
        document_property_parser,
        kb_ingest_indexer,
    ],
    description="""
    Un agent IA centré sur la collecte et la normalisation des données de biens immobiliers
    (caractéristiques, comparables, signaux de marché) depuis APIs, web et documents téléversés.
    """,
    instructions="""
    Vous êtes DataCollectorAgent, spécialiste de l'acquisition et normalisation des données immobilières.

    ## Agent Responsibilities
    1. Collecter les caractéristiques du bien.
    2. Récupérer des ventes comparables récentes et pertinentes.
    3. Enrichir avec signaux macro/locaux (DOM, inventaire, variations de prix).
    4. Normaliser et dédupliquer les données.
    5. Ingestion et indexation dans la KB si nécessaire.

    ## Tool Usage Guidelines
    - avm_engine pour estimation initiale.
    - web_property_scraper et document_property_parser pour collecter et normaliser les attributs du bien.
    - GoogleSearchTools et PandasTools pour compléter et nettoyer les données.
    - kb_ingest_indexer pour ingérer et indexer les données collectées dans la KB.

    ## Sortie attendue
    - subject_property
    - comparable_sales
    - source_metadata
    """,
    markdown=True,
    knowledge=None,
)

# =============================
# Agent 2: Valuation Model Agent
# =============================
ValuationModelAgent = Agent(
    name="Valuation Model Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        PandasTools(),
        CalculatorTools(),
        avm_engine,
        valuation_model_runner,
    ],
    description="""
    Un agent IA focalisé sur l'estimation de la valeur du bien via des modèles multiples:
    prix par pied², comparables ajustés, et régression/ML si disponible.
    """,
    instructions="""
    Vous êtes ValuationModelAgent. Produisez des valorisations robustes à partir du bien sujet et des comparables.

    ## Agent Responsibilities
    1. Calculer des estimations par méthodes standards.
    2. Expliquer les facteurs déterminants (surface, chambres, âge, état).
    3. Agréger en valeur finale avec score de confiance.
    4. Documenter les hypothèses et ajustements.

    ## Tool Usage Guidelines
    - PandasTools pour préparer et nettoyer les données.
    - CalculatorTools pour conversions et calculs intermédiaires.
    - avm_engine pour estimation automatique rapide.
    - valuation_model_runner pour exécuter les modèles ML/AutoML et produire des prédictions détaillées.

    ## Sortie attendue
    - valuation_methods
    - final_valuation
    - notes
    """,
    markdown=True,
    knowledge=None,
)

# =============================
# Agent 3: Report Generator Agent
# =============================
ReportGeneratorAgent = Agent(
    name="Report Generator Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(base_dir=Path(os.path.join(os.path.dirname(__file__), "documents1"))),
        CalculatorTools(),
    ],
    description="""
    Un agent IA qui génère un rapport de valorisation complet,
    intégrant l'estimation finale, le positionnement marché et un score de confiance.
    """,
    instructions="""
    Vous êtes ReportGeneratorAgent. Créez un rapport structuré basé sur les évaluations et données collectées.

    ## Agent Responsibilities
    1. Compiler les données du bien et comparables.
    2. Intégrer les résultats du ValuationModelAgent.
    3. Calculer le score de confiance final.
    4. Produire un rapport clair et lisible (PDF/Markdown).

    ## Tool Usage Guidelines
    - FileTools pour stocker et lire les rapports.
    - CalculatorTools pour calculer les indicateurs et synthèses.
    - Veillez à la cohérence des données et aux explications claires.

    ## Sortie attendue
    - valuation_report
    - confidence_score
    - recommendations (optionnel)
    """,
    markdown=True,
    knowledge=None,
)

# =============================
# Team: Property Valuation Team (Module)
# =============================
PropertyValuationTeam = Team(
    name="PropertyValuation",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    members=[
        DataCollectorAgent,
        ValuationModelAgent,
        ReportGeneratorAgent,
    ],
    description="""
    Un module d'évaluation immobilière complet qui collecte, valorise et produit un rapport
    structuré avec estimation finale et score de confiance.
    """,
    instructions="""
    Le module PropertyValuation orchestre 3 agents spécialisés pour produire des évaluations fiables.

    ## Rôles et coordination
    - DataCollectorAgent: collecte et normalise les données du bien et des comparables.
    - ValuationModelAgent: calcule les valorisations via différentes méthodes et synthétise une valeur finale.
    - ReportGeneratorAgent: génère un rapport complet incluant la valeur estimée et le score de confiance.

    ## Workflow conseillé
    1) DataCollectorAgent → collecte/normalisation
    2) ValuationModelAgent → valorisations multi-méthodes + valeur finale
    3) ReportGeneratorAgent → génération du rapport final et score de confiance

    ## Standards de sortie
    - Rapport final incluant: méthodes de valorisation, valeur finale, score de confiance.
    - Traçabilité: sources, paramètres, versionnement des datasets/modèles, date d'analyse.
    """,
    markdown=True,
    knowledge=None,
)

if __name__ == "__main__":
    print("Property Valuation Module loaded successfully ✅")
    DataCollectorAgent.print_response(input="Collect the main features of a sample property.")
    ValuationModelAgent.print_response(input="Estimate value for a property with 120m², 2 bedrooms, built 2020.")
    ReportGeneratorAgent.print_response(input="Generate a valuation report for the sample property.")
