# module6.py - Legal & Compliance Module

import os
from pathlib import Path
from dotenv import load_dotenv

from agno.agent import Agent
from agno.team.team import Team
from agno.models.mistral import MistralChat
from agno.tools.file import FileTools

from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from agno.knowledge.embedder.mistral import MistralEmbedder

# Import des outils custom
try:
    from .tools import (
        document_parser_tool,
        compliance_checker_tool,
        contract_nlp_tool,
    )
except ImportError:
    from tools import (
        document_parser_tool,
        compliance_checker_tool,
        contract_nlp_tool,
    )

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()

# ----------------------------
# Knowledge Base
# ----------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5432/legal"

markdown_reader = MarkdownReader(name="Legal & Compliance Reader")

vector_db = PgVector(
    table_name="legal_docs",
    db_url=db_url,
    embedder=MistralEmbedder(api_key=os.getenv("MISTRAL_API_KEY"), dimensions=1024)
)

legal_kb = Knowledge(
    name="Legal KB",
    vector_db=vector_db,
    max_results=5
)

# =============================
# Agent 1: Document Verification Agent
# =============================
DocumentVerificationAgent = Agent(
    name="Document Verification Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        FileTools(base_dir=Path(os.path.join(os.path.dirname(__file__), "documents6"))),
        document_parser_tool,
    ],
    description="Agent IA pour vérifier la validité et conformité des documents légaux.",
    instructions="Vérifie les titres et contrats et retourne document_status.",
    markdown=True,
    knowledge=legal_kb,
)

# =============================
# Agent 2: Compliance Check Agent
# =============================
ComplianceCheckAgent = Agent(
    name="Compliance Check Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        compliance_checker_tool,
    ],
    description="Agent IA qui évalue la conformité des biens et transactions avec la réglementation.",
    instructions="Analyse property_data et transaction_data et retourne compliance_report.",
    markdown=True,
    knowledge=legal_kb,
)

# =============================
# Agent 3: Contract Review Agent
# =============================
ContractReviewAgent = Agent(
    name="Contract Review Agent",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    tools=[
        contract_nlp_tool,
    ],
    description="Agent IA qui analyse les contrats et identifie les risques potentiels.",
    instructions="Analyse le texte du contrat et retourne contract_summary et risk_flags.",
    markdown=True,
    knowledge=legal_kb,
)

# =============================
# Team: Legal & Compliance Team
# =============================
LegalComplianceTeam = Team(
    name="LegalCompliance",
    model=MistralChat(id="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY")),
    members=[
        DocumentVerificationAgent,
        ComplianceCheckAgent,
        ContractReviewAgent,
    ],
    description="Module complet de vérification légale et conformité des transactions immobilières.",
    instructions="""
    Le module LegalCompliance orchestre 3 agents spécialisés:

    1) DocumentVerificationAgent → vérifie documents légaux
    2) ComplianceCheckAgent → produit compliance_report
    3) ContractReviewAgent → résume contrats et identifie risques
    """,
    markdown=True,
    knowledge=legal_kb,
)

if __name__ == "__main__":
    print("Legal & Compliance Module loaded successfully ✅")
    DocumentVerificationAgent.print_response(input="Verify sample legal title document.")
    ComplianceCheckAgent.print_response(input="Check compliance for sample property and transaction data.")
    sample_contract = """
    This contract establishes that the Buyer agrees to purchase the property from the Seller.
    Clause 1: Payment terms.
    Clause 2: Penalty for breach.
    Clause 3: Termination conditions.
    """
    ContractReviewAgent.print_response(input=sample_contract)

