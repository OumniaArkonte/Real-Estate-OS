# =============================
# tools.py - Property Valuation Module
# =============================
from agno.tools import tool
from typing import Dict, Any, List, Optional
from datetime import datetime
import re


# =============================
# Tool 1: Web Property Scraper (Agent 1)
# =============================
@tool(
    name="web_property_scraper",
    description="Scrape multi-sources (requêtes web/listings) et normalise les champs principaux du bien et des comparables",
    show_result=True,
)
def web_property_scraper(
    query: str,
    location: str,
    max_results: int = 50,
    radius_km: float = 3.0,
) -> Dict[str, Any]:
    normalized_results: List[Dict[str, Any]] = []

    sample = [
        {
            "address": "123 Sample St, {}".format(location),
            "list_price": 460000,
            "sqft": 2200,
            "bedrooms": 3,
            "bathrooms": 2.5,
            "lot_size": 0.22,
            "year_built": 2012,
            "amenities": ["garage", "garden"],
            "source": "web",
            "date": datetime.now().strftime("%Y-%m-%d"),
        },
        {
            "address": "456 Example Ave, {}".format(location),
            "list_price": 485000,
            "sqft": 2400,
            "bedrooms": 4,
            "bathrooms": 3,
            "lot_size": 0.30,
            "year_built": 2015,
            "amenities": ["garage"],
            "source": "web",
            "date": datetime.now().strftime("%Y-%m-%d"),
        },
    ]

    for item in sample[: max_results]:
        ppsf = None
        if item.get("list_price") and item.get("sqft"):
            try:
                ppsf = round(item["list_price"] / item["sqft"], 2)
            except Exception:
                ppsf = None
        normalized_results.append({**item, "price_per_sqft": ppsf})

    return {
        "query": query,
        "location": location,
        "radius_km": radius_km,
        "results": normalized_results,
        "normalized": True,
        "collected_at": datetime.now().isoformat(),
    }


# =============================
# Tool 2: Document Property Parser (Agent 1)
# =============================
@tool(
    name="document_property_parser",
    description="Extrait des attributs structurés d'un bien depuis des documents texte (listing/inspection)",
    show_result=True,
)
def document_property_parser(
    file_path: str,
    doc_type: Optional[str] = None,
) -> Dict[str, Any]:
    extracted: Dict[str, Any] = {
        "address": None,
        "sqft": None,
        "bedrooms": None,
        "bathrooms": None,
        "lot_size": None,
        "year_built": None,
        "amenities": [],
    }
    matched_lines: List[str] = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return {"error": f"Lecture impossible: {str(e)}", "file_path": file_path, "doc_type": doc_type}

    patterns = {
        "address": r"address\s*[:\-]?\s*(.+)$",
        "sqft": r"(sqft|square\s*feet)\s*[:\-]?\s*(\d{3,6})",
        "bedrooms": r"bed(room)?s?\s*[:\-]?\s*(\d{1,2})",
        "bathrooms": r"bath(room)?s?\s*[:\-]?\s*(\d{1,2}(?:\.\d)?)",
        "lot_size": r"lot\s*size\s*[:\-]?\s*(\d{1,2}(?:\.\d{1,2})?)",
        "year_built": r"year\s*built\s*[:\-]?\s*(\d{4})",
    }

    for key, pat in patterns.items():
        m = re.search(pat, content, re.IGNORECASE | re.MULTILINE)
        if m:
            val = m.group(1) if key == "address" else m.group(2) if m.lastindex and m.lastindex >= 2 else m.group(1)
            matched_lines.append(m.group(0))
            try:
                if key in ["sqft"]:
                    extracted[key] = int(val)
                elif key in ["bedrooms"]:
                    extracted[key] = int(float(val))
                elif key in ["bathrooms", "lot_size"]:
                    extracted[key] = float(val)
                elif key in ["year_built"]:
                    extracted[key] = int(val)
                else:
                    extracted[key] = val.strip()
            except Exception:
                extracted[key] = val

    amenities_map = ["garage", "pool", "garden", "balcony", "fireplace"]
    for amenity in amenities_map:
        if re.search(rf"\b{amenity}\b", content, re.IGNORECASE):
            extracted["amenities"].append(amenity)

    return {
        "file_path": file_path,
        "doc_type": doc_type,
        "extracted": extracted,
        "matched_examples": matched_lines[:5],
        "parsed_at": datetime.now().isoformat(),
    }

# =============================
# Tool 0: AVM Engine (Agent 1 & 2)
# =============================


@tool(
    name="avm_engine",
    description="Automated Valuation Model: calcule une estimation initiale rapide d'une propriété",
    show_result=True,
)
def avm_engine(property_features: Dict[str, Any]) -> Dict[str, Any]:
    # Exemple simple : valeur simulée en fonction de la surface
    sqft = property_features.get("sqft", 1000)
    bedrooms = property_features.get("bedrooms", 2)
    bathrooms = property_features.get("bathrooms", 1)
    estimated_value = sqft * 200 + bedrooms * 10000 + bathrooms * 5000
    return {
        "estimated_value": estimated_value,
        "features_used": {
            "sqft": sqft,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms
        }
    }

# =============================
# Tool 3: Knowledge Base Ingest & Indexer (Agent 2)
# =============================
@tool(
    name="kb_ingest_indexer",
    description="Ingestion et indexation vecteur de documents/datasets de valorisation pour la base de connaissance",
    show_result=True,
)
def kb_ingest_indexer(
    paths: List[str],
    collection: str,
    recreate: bool = False,
) -> Dict[str, Any]:
    return {
        "collection": collection,
        "ingested_items": len(paths),
        "recreated": recreate,
        "indexed_at": datetime.now().isoformat(),
    }


# =============================
# Tool 4: Valuation Model Runner (Agent 3)
# =============================
@tool(
    name="valuation_model_runner",
    description="Exécute un modèle ML/AutoML de valorisation (features -> valeur + explications)",
    show_result=True,
)
def valuation_model_runner(
    model_name: str,
    features: Dict[str, Any],
    version: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "model_name": model_name,
        "features": features,
        "predicted_value": 250000,  # valeur simulée
        "confidence": 0.87,
        "version": version or "v1.0",
        "run_at": datetime.now().isoformat(),
        "explanations": {"ppsf_adjustment": 0, "comparables_delta": 0},
    }
