# module2.py - Property Search & Recommendation Module

import os
from pathlib import Path
from dotenv import load_dotenv

from agno.agent import Agent
from agno.team.team import Team
from agno.models.mistral import MistralChat
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.pandas import PandasTools

# Import des outils custom
try:
    from .tools import search_properties, generate_user_profile, recommend_properties
except ImportError:
    from tools import search_properties, generate_user_profile, recommend_properties

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()
# =============================
# Agent 1: Search Query Agent
# =============================
SearchQueryAgent = Agent(
    name="Search Query Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[GoogleSearchTools(), PandasTools(), search_properties],
    description="""
    Un agent IA chargé de rechercher et collecter les biens immobiliers correspondant aux critères
    spécifiés par l'utilisateur (localisation, budget, type de propriété).
    """,
    instructions="""
    Vous êtes SearchQueryAgent. Collectez les biens candidats à partir des critères de l'utilisateur.

    ## Agent Responsibilities
    1. Recevoir la requête utilisateur avec les critères (localisation, budget, type).
    2. Rechercher des biens pertinents via la base de données et sur le web.
    3. Normaliser et filtrer les résultats selon les critères.
    4. Fournir la liste des biens candidats.

    ## Tool Usage Guidelines
    - GoogleSearchTools pour rechercher les listings web.
    - PandasTools pour nettoyer et organiser les données.
    - search_properties pour interroger la base de données vectorisée.

    ## Sortie attendue
    - candidate_properties
    """,
    markdown=True,
    
)

# =============================
# Agent 2: User Preference Agent
# =============================
UserPreferenceAgent = Agent(
    name="User Preference Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[PandasTools(), generate_user_profile],
    description="""
    Un agent IA qui construit un profil utilisateur basé sur les préférences explicites et les
    interactions, afin de personnaliser les recommandations de biens.
    """,
    instructions="""
    Vous êtes UserPreferenceAgent. Créez un vecteur utilisateur à partir des préférences et interactions.

    ## Agent Responsibilities
    1. Collecter les préférences explicites et les données d'interaction utilisateur.
    2. Normaliser et vectoriser ces informations.
    3. Mettre à jour le profil utilisateur dans la base vectorisée.

    ## Tool Usage Guidelines
    - PandasTools pour traiter et analyser les données utilisateur.
    - generate_user_profile pour créer le vecteur utilisateur final.

    ## Sortie attendue
    - user_profile_vector
    """,
    markdown=True,
   
)

# =============================
# Agent 3: Recommendation Engine Agent
# =============================
RecommendationEngineAgent = Agent(
    name="Recommendation Engine Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[PandasTools(), recommend_properties],
    description="""
    Un agent IA chargé de produire les recommandations de biens immobiliers les plus adaptées
    au profil utilisateur, à partir des biens candidats et des préférences vectorisées.
    """,
    instructions="""
    Vous êtes RecommendationEngineAgent. Produisez la liste des propriétés recommandées
    en combinant les biens candidats et le profil utilisateur.

    ## Agent Responsibilities
    1. Recevoir les biens candidats et le vecteur utilisateur.
    2. Évaluer la pertinence de chaque bien par rapport au profil utilisateur.
    3. Générer une liste ordonnée de recommandations.

    ## Tool Usage Guidelines
    - PandasTools pour manipuler et traiter les données.
    - recommend_properties pour produire la liste finale des recommandations.

    ## Sortie attendue
    - recommended_properties
    """,
    markdown=True,
   
)

# =============================
# Team: Property Search & Recommendation
# =============================
PropertySearchTeam = Team(
    name="PropertySearch",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    members=[SearchQueryAgent, UserPreferenceAgent, RecommendationEngineAgent],
    description="Module complet pour la recherche et recommandation de biens immobiliers.",
    instructions="""
    Coordination des agents:
    1) SearchQueryAgent → collecte des biens candidats
    2) UserPreferenceAgent → création du profil utilisateur
    3) RecommendationEngineAgent → génération de recommandations
    """,
)

if __name__ == "__main__":
    print("Property Search & Recommendation Module loaded ✅")
    SearchQueryAgent.print_response(input="Search properties in Casablanca, type: Appartement, max price: 2,000,000")
    UserPreferenceAgent.print_response(
    input={"preferences": {"budget": 1500000, "type": "Appartement", "location": "Casablanca"}}
)

    RecommendationEngineAgent.print_response(input="Recommend properties based on candidate properties and user profile")
