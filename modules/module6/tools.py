# =============================
# tools6.py - Legal & Compliance Module
# =============================
from agno.tools import tool
from typing import Dict, Any, Optional
from datetime import datetime
import re

# =============================
# Tool 1: Document Parser Tool (Document Verification Agent)
# =============================
@tool(
    name="document_parser_tool",
    description="Analyse des documents légaux (titre, contrat) et extrait les informations clés",
    show_result=True,
)
def document_parser_tool(file_path: str, doc_type: Optional[str] = None) -> Dict[str, Any]:
    extracted: Dict[str, Any] = {
        "title": None,
        "contract_number": None,
        "parties": [],
        "dates": [],
        "clauses": [],
    }
    matched_lines = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return {"error": f"Impossible de lire le fichier: {str(e)}", "file_path": file_path}

    # Patterns simples pour extraction
    patterns = {
        "title": r"(Title|Property Title)\s*[:\-]?\s*(.+)",
        "contract_number": r"(Contract Number|No\.)\s*[:\-]?\s*(\w+)",
        "dates": r"(\d{2}/\d{2}/\d{4})",
        "parties": r"(Seller|Buyer|Party)\s*[:\-]?\s*(.+)",
        "clauses": r"(Clause\s*\d+:.+)",
    }

    for key, pat in patterns.items():
        matches = re.findall(pat, content, re.IGNORECASE)
        if matches:
            if key in ["dates"]:
                extracted[key] = matches
            elif key in ["parties", "clauses"]:
                extracted[key] = [m[1] if isinstance(m, tuple) else m for m in matches]
            else:
                extracted[key] = matches[0][1] if isinstance(matches[0], tuple) else matches[0]
            matched_lines.extend([m if isinstance(m, str) else " ".join(m) for m in matches])

    return {
        "file_path": file_path,
        "doc_type": doc_type,
        "extracted": extracted,
        "matched_examples": matched_lines[:5],
        "parsed_at": datetime.now().isoformat(),
    }

# =============================
# Tool 2: Compliance Checker Tool (Compliance Check Agent)
# =============================
@tool(
    name="compliance_checker_tool",
    description="Vérifie la conformité d'une propriété ou d'une transaction selon les règles légales",
    show_result=True,
)
def compliance_checker_tool(property_data: Dict[str, Any], transaction_data: Dict[str, Any]) -> Dict[str, Any]:
    # Exemple simplifié : vérification fictive
    compliance_issues = []
    if property_data.get("year_built", 0) < 1900:
        compliance_issues.append("Property older than 1900, check historical regulations.")
    if transaction_data.get("sale_price", 0) <= 0:
        compliance_issues.append("Sale price missing or invalid.")

    return {
    "property_id": property_data.get("property_id"),
    "transaction_id": transaction_data.get("transaction_id"),
    "compliance_issues": compliance_issues,
    "is_compliant": len(compliance_issues) == 0,
    "checked_at": datetime.now().isoformat(),
}


# =============================
# Tool 3: Contract NLP Tool (Contract Review Agent)
# =============================
@tool(
    name="contract_nlp_tool",
    description="Analyse le texte d'un contrat pour générer un résumé et identifier les risques",
    show_result=True,
)
def contract_nlp_tool(contract_text: str) -> Dict[str, Any]:
    # Exemple simplifié : résumé et détection de mots-clés de risque
    summary = contract_text[:200] + "..." if len(contract_text) > 200 else contract_text
    risk_keywords = ["penalty", "breach", "termination", "fine"]
    risk_flags = [kw for kw in risk_keywords if kw.lower() in contract_text.lower()]

    return {
        "summary": summary,
        "risk_flags": risk_flags,
        "analyzed_at": datetime.now().isoformat(),
    }
