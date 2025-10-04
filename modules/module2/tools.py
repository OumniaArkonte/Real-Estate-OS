# =============================
# tools.py - Property Search & Recommendation Module
# =============================
from agno.tools import tool
from typing import Dict, Any, List, Optional
from datetime import datetime

# =============================
# Tool 1: Search Properties (SearchQueryAgent)
# =============================
@tool(
    name="search_properties",
    description="Recherche des biens immobiliers candidats à partir des critères utilisateur",
    show_result=True,
)
def search_properties(
    location: str,
    property_type: Optional[str] = "Appartement",
    max_price: Optional[float] = None,
    min_area: Optional[float] = None,
    max_results: int = 10
) -> Dict[str, Any]:
    # Exemple simulé : liste de biens fictifs
    sample_properties = [
        {"id": 1, "address": f"Appartement {location} - Bourgogne", "price": 1800000, "area": 120, "type": "Appartement"},
        {"id": 2, "address": f"Appartement {location} - Maarif", "price": 1147500, "area": 85, "type": "Appartement"},
        {"id": 3, "address": f"Studio {location} - Gauthier", "price": 800000, "area": 50, "type": "Studio"},
    ]
    filtered = [
        p for p in sample_properties
        if (max_price is None or p["price"] <= max_price)
        and (min_area is None or p["area"] >= min_area)
        and (property_type is None or p["type"] == property_type)
    ][:max_results]

    return {
        "location": location,
        "criteria": {"property_type": property_type, "max_price": max_price, "min_area": min_area},
        "results": filtered,
        "searched_at": datetime.now().isoformat(),
    }

# =============================
# Tool 2: Generate User Profile (UserPreferenceAgent)
# =============================
@tool(
    name="generate_user_profile",
    description="Génère un vecteur de profil utilisateur à partir de préférences explicites",
    show_result=True,
)
def generate_user_profile(
    preferences: Dict[str, Any],
    interactions: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    profile = {
        "budget": preferences.get("budget", 1000000),
        "preferred_type": preferences.get("type", "Appartement"),
        "preferred_location": preferences.get("location", "Casablanca"),
        "interactions": interactions or [],
        "generated_at": datetime.now().isoformat(),
    }
    return profile

# =============================
# Tool 3: Recommend Properties (RecommendationEngineAgent)
# =============================
@tool(
    name="recommend_properties",
    description="Recommande les propriétés les mieux adaptées au profil utilisateur",
    show_result=True,
)
def recommend_properties(
    candidate_properties: List[Dict[str, Any]],
    user_profile: Dict[str, Any],
    top_k: int = 3
) -> Dict[str, Any]:
    budget = user_profile.get("budget", float("inf"))
    preferred_type = user_profile.get("preferred_type")
    preferred_location = user_profile.get("preferred_location")

    filtered = [
        p for p in candidate_properties
        if p.get("price", float("inf")) <= budget
        and (preferred_type is None or p.get("type") == preferred_type)
        and (preferred_location is None or preferred_location in p.get("address", ""))
    ]
    sorted_props = sorted(filtered, key=lambda x: x.get("area", 0), reverse=True)[:top_k]

    return {
        "recommended": sorted_props,
        "user_profile": user_profile,
        "recommended_at": datetime.now().isoformat(),
    }