"""
FastAPI Enterprise Gateway for Inkloom Verity™ / VeriBrand AI™
Provides full REST and WebSocket endpoints for pre-flight checking,
brand vault management, multimodal CV analysis, CMS gate simulation, and telemetry.
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import json

from .models.schemas import (
    DocumentAuditRequest,
    DocumentAuditResponse,
    VisualAssetInput,
    VisualFinding,
    CreatorOverrideRequest,
    BrandRule,
    TemporalFact,
    CryptographicCertificate
)
from .core import (
    UnifiedBrandGovernanceEngine,
    CMSPublishingGateway,
    AmbiguityTelemetryEngine
)

app = FastAPI(
    title="Inkloom Verity™ Governance API",
    description="Intelligent Enterprise Brand-Governance & Pre-Publication Verification Platform",
    version="2.4.0"
)

# Enable CORS for local Vite and extension clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize singletons
engine = UnifiedBrandGovernanceEngine()
cms_gateway = CMSPublishingGateway(engine.ledger)
telemetry_engine = AmbiguityTelemetryEngine()


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "engine": "Inkloom Verity Unified Governance Engine",
        "version": "2.4.0",
        "active_rules_count": len(engine.vault.rules),
        "temporal_facts_count": len(engine.kg.facts),
        "zero_data_retention": True,
        "air_gapped_vpc": True
    }


@app.post("/api/audit", response_model=DocumentAuditResponse)
def audit_document(request: DocumentAuditRequest):
    """
    Main Pre-Publication Inspection Endpoint.
    Executes the 6 verification subsystems across text and multimodal assets.
    """
    return engine.audit_document(request)


@app.post("/api/audit/visual", response_model=List[VisualFinding])
def audit_visual_assets(assets: List[VisualAssetInput]):
    """
    Audits visual assets for CIELAB ΔE00, WCAG 2.1 contrast, logo safe space, and alt-text.
    """
    results = []
    for asset in assets:
        findings = engine.vision_auditor.audit_asset(asset)
        results.extend(findings)
    return results


@app.post("/api/mped/preview")
def preview_mped_diff(payload: Dict[str, Any]):
    """
    Computes Minimal Perturbation Edit Distance and word-level diff preview.
    """
    full_text = payload.get("full_text", "")
    span = payload.get("span", [0, 0])
    replacement = payload.get("replacement", "")

    return engine.rewriter.generate_span_diff(full_text, (span[0], span[1]), replacement)


@app.get("/api/brand-vault/rules", response_model=List[BrandRule])
def get_brand_rules():
    """
    Returns the codified Brand Constitution rules DAG.
    """
    return engine.vault.get_all_rules()


@app.get("/api/brand-vault/tokens")
def get_brand_tokens():
    """
    Returns official design tokens, color palette swatches, and target persona vector.
    """
    return {
        "palette": engine.vault.official_palette,
        "logo_constraints": engine.vault.logo_constraints,
        "target_persona": engine.vault.target_persona.model_dump(),
        "prohibited_lexicon": engine.vault.prohibited_lexicon,
        "trademark_registry": engine.vault.trademark_registry
    }


@app.get("/api/temporal-facts", response_model=List[TemporalFact])
def get_temporal_facts():
    """
    Returns all enterprise facts in the Temporal Knowledge Graph.
    """
    return engine.kg.get_all_facts()


@app.post("/api/temporal-facts")
def add_temporal_fact(fact: TemporalFact):
    """
    Adds a new verified fact with explicit temporal validity intervals.
    """
    engine.kg.add_fact(fact)
    return {"message": "Fact recorded successfully in Temporal SSOT", "fact_id": fact.id}


@app.post("/api/override")
def record_creator_override(override: CreatorOverrideRequest):
    """
    Records a creator's deliberate override and feeds the Ambiguity Telemetry engine.
    """
    telemetry_engine.record_override(override)
    return {
        "status": "recorded",
        "message": f"Override for {override.rule_id} recorded in governance telemetry ledger."
    }


@app.get("/api/telemetry")
def get_telemetry():
    """
    Returns aggregate ambiguity telemetry, friction points, and departmental heatmaps.
    """
    return telemetry_engine.analyze_ambiguity()


@app.post("/api/cms/publish")
def simulate_cms_publish(payload: Dict[str, Any]):
    """
    Pre-Publish CMS Gateway simulation (WordPress, Webflow, Contentful).
    Blocks publications lacking a valid Green Tier certificate token.
    """
    cms = payload.get("cms_platform", "wordpress")
    doc_id = payload.get("document_id", "doc-default")
    token = payload.get("token")
    return cms_gateway.intercept_publish_attempt(cms, doc_id, token)


@app.get("/api/audit/certificates", response_model=List[CryptographicCertificate])
def get_audit_certificates():
    """
    Returns immutable SHA-256 compliance certificates issued by the platform.
    """
    return engine.ledger.get_all_certificates()


@app.get("/api/papers")
def get_academic_papers():
    """
    Returns the comprehensive 20-paper academic deconstruction and synthesis matrix.
    """
    return [
        {
            "id": 1,
            "title": "FActScore",
            "citation": "Min et al., EMNLP 2023",
            "core_mechanism": "Decomposes text into atomic, independent propositions using dependency parsing; evaluates veracity individually.",
            "what_we_extract": "Fine-grained atomic claim decomposition eliminating compound sentence ambiguity.",
            "what_we_fix": "Replaces public static Wikipedia with private Temporal Enterprise Knowledge Graph (T-EKG).",
            "filename": "01_FActScore_2305.14251.pdf"
        },
        {
            "id": 2,
            "title": "Chain-of-Verification (CoVe)",
            "citation": "Dhuliawala et al., Meta AI, ACL 2024",
            "core_mechanism": "Four-stage pipeline: Draft -> Plan questions -> Execute decoupled queries -> Generate verified output.",
            "what_we_extract": "Decoupled verification questions planned independently without draft context bias.",
            "what_we_fix": "Constrains revisions to span-level replacements instead of wholesale rewriting that flattens author voice.",
            "filename": "02_Chain_of_Verification_2309.11495.pdf"
        },
        {
            "id": 3,
            "title": "SAFE",
            "citation": "Wei et al., Google DeepMind, 2024",
            "core_mechanism": "Search-Augmented Factuality Evaluator using multi-turn reasoning and web query formulation.",
            "what_we_extract": "Multi-step reasoning over extracted factual claims.",
            "what_we_fix": "Replaces public search engine queries (which leak trade secrets) with air-gapped internal hybrid vector/graph RAG.",
            "filename": "03_SAFE_Factuality_2403.18802.pdf"
        },
        {
            "id": 4,
            "title": "AVeriTeC",
            "citation": "Schlichtkrull et al., NeurIPS 2023",
            "core_mechanism": "Real-world claim verification pairing veracity verdicts with exact textual justification.",
            "what_we_extract": "Standardized multi-class labels (Supported, Refuted, Outdated, Conflicting) with mandatory citation spans.",
            "what_we_fix": "Links directly to official version-controlled corporate documentation instead of arbitrary web pages.",
            "filename": "04_AVeriTeC_2305.13117.pdf"
        },
        {
            "id": 5,
            "title": "FacTool",
            "citation": "Chern et al., 2023",
            "core_mechanism": "Tool-augmented framework deploying external Python calculators and code interpreters.",
            "what_we_extract": "Deterministic verification of numeric, percentage, and statistical assertions without LLM math hallucinations.",
            "what_we_fix": "Binds calculators directly to enterprise pricing schedules and SLA formula definitions.",
            "filename": "05_FacTool_2307.13528.pdf"
        },
        {
            "id": 6,
            "title": "RAGAS",
            "citation": "Es et al., 2023",
            "core_mechanism": "Automated evaluation metrics: Faithfulness, Answer Relevance, and Context Precision.",
            "what_we_extract": "Automated mathematical quality gate: rejects any claim with Faithfulness < 0.90.",
            "what_we_fix": "Connects post-hoc evaluation to automated minimal-perturbation span repair.",
            "filename": "06_RAGAS_2309.15217.pdf"
        },
        {
            "id": 7,
            "title": "Self-RAG",
            "citation": "Asai et al., ICLR 2024",
            "core_mechanism": "Selective retrieval via special reflection tokens ([Retrieve], [IsSup], [IsUse]).",
            "what_we_extract": "Eliminates redundant retrieval latency on creative prose; triggers heavy RAG only for empirical claims.",
            "what_we_fix": "Implements reflection gating via lightweight prompt/classifier heads without requiring base model fine-tuning.",
            "filename": "07_Self_RAG_2310.11511.pdf"
        },
        {
            "id": 8,
            "title": "Siren's Song",
            "citation": "Zhang et al., Computational Linguistics 2023",
            "core_mechanism": "Taxonomy classifying hallucinations into Input-conflicting, Context-conflicting, and Fact-conflicting.",
            "what_we_extract": "Root-cause classification allowing targeted triage routing for brand vs legal issues.",
            "what_we_fix": "Operationalizes the academic taxonomy into a real-time editorial triage routing engine.",
            "filename": "08_Sirens_Song_Hallucinations_2309.01219.pdf"
        },
        {
            "id": 9,
            "title": "Constitutional AI",
            "citation": "Bai et al., Anthropic 2022",
            "core_mechanism": "Steers model evaluation using a natural-language constitution of principles.",
            "what_we_extract": "Enables brand managers to codify plain-English guidelines into active system guardrails.",
            "what_we_fix": "Splits 100-page style guides into a hierarchical Directed Acyclic Graph (DAG) of micro-agents to stop attention dilution.",
            "filename": "09_Constitutional_AI_2212.08073.pdf"
        },
        {
            "id": 10,
            "title": "Self-Refine",
            "citation": "Madaan et al., NeurIPS 2023",
            "core_mechanism": "Iterative generation-feedback-refinement loop without supervised data.",
            "what_we_extract": "Progressive editorial polish across multiple guideline dimensions.",
            "what_we_fix": "Freezes already-compliant spans using token masking to prevent regression drift.",
            "filename": "10_Self_Refine_2303.17651.pdf"
        },
        {
            "id": 11,
            "title": "CRITIC",
            "citation": "Gou et al., ICLR 2024",
            "core_mechanism": "Interactive critiquing where models execute external tools to cross-examine their reasoning.",
            "what_we_extract": "Combines semantic LLM reasoning with microsecond deterministic Vale AST linters.",
            "what_we_fix": "Expands tool registry to include computer vision geometry and CIELAB colorimetry APIs.",
            "filename": "11_CRITIC_2305.11738.pdf"
        },
        {
            "id": 12,
            "title": "TIGERScore",
            "citation": "Jiang et al., EMNLP 2023",
            "core_mechanism": "Reference-free explainable metric pinpointing exact error tokens [s_start, s_end] with rationales.",
            "what_we_extract": "Span-level localization formatting findings into non-destructive in-line diffs.",
            "what_we_fix": "Calibrates the generic NLG error taxonomy specifically for enterprise brand, legal, and tone rules.",
            "filename": "12_TIGERScore_2304.05353.pdf"
        },
        {
            "id": 13,
            "title": "LayoutLMv3",
            "citation": "Huang et al., ACM MM 2022",
            "core_mechanism": "Multimodal pre-training jointly modeling 2D bounding boxes, text tokens, and image patches.",
            "what_we_extract": "Structural layout compliance in complex documents (slide decks, brochures, one-pagers).",
            "what_we_fix": "Pairs spatial layout with OpenCV deterministic geometry for exact logo clear-space buffer checks.",
            "filename": "13_LayoutLMv3_2204.08387.pdf"
        },
        {
            "id": 14,
            "title": "DocOwl 1.5",
            "citation": "Ye et al., 2024",
            "core_mechanism": "Vision-Language Model specialized in OCR, complex table parsing, and chart reading.",
            "what_we_extract": "Automated inspection of embedded infographics, financial tables, and data visualizations.",
            "what_we_fix": "Backs qualitative chart reading with deterministic calculation of axis scales and margins.",
            "filename": "14_DocOwl1.5_2403.12895.pdf"
        },
        {
            "id": 15,
            "title": "ScreenAI",
            "citation": "Google Research, 2024",
            "core_mechanism": "Vision-Language model specialized in UI elements, banners, visual hierarchy, and accessibility.",
            "what_we_extract": "Checks digital banners and social cards for visual hierarchy and alt-text completeness.",
            "what_we_fix": "Retargets attention weights specifically to marketing assets and advertising collateral.",
            "filename": "15_ScreenAI_2402.04615.pdf"
        },
        {
            "id": 16,
            "title": "Co-Writing with Opinionated LLMs",
            "citation": "Jakesch et al., ACM CHI 2023",
            "core_mechanism": "Empirical study showing how AI writing assistants subtly manipulate opinions and homogenize voice.",
            "what_we_extract": "Establishes the Anti-Overruling Mandate: AI must never silently rewrite; human retains ultimate agency.",
            "what_we_fix": "Constructs the creator override architecture and feedback telemetry loop.",
            "filename": "16_Co_Writing_Opinionated_LLM_2302.00560.pdf"
        },
        {
            "id": 17,
            "title": "Chain-of-Thought (CoT)",
            "citation": "Wei et al., NeurIPS 2022",
            "core_mechanism": "Elicits multi-step deductive reasoning before rendering a final judgment.",
            "what_we_extract": "Ensures complex brand and comparative advertising rules are reasoned through systematically.",
            "what_we_fix": "Restricts CoT to high-risk Amber and Red tier violations to prevent unnecessary review latency.",
            "filename": "17_Chain_of_Thought_2201.11903.pdf"
        },
        {
            "id": 18,
            "title": "Controllable Text Generation Survey",
            "citation": "Zhang et al., ACM CSUR",
            "core_mechanism": "Formalizes attribute-conditioned generation using latent persona vectors.",
            "what_we_extract": "Formulates brand voice as a 5D coordinate vector: Formality, Warmth, Authority, Technicality, Directness.",
            "what_we_fix": "Implements real-time style drift computation using calibrated cosine distance.",
            "filename": "18_Controllable_Text_Gen_Survey_2104.14816.pdf"
        },
        {
            "id": 19,
            "title": "Directional Stimulus Prompting",
            "citation": "Li et al., NeurIPS 2023",
            "core_mechanism": "Policy network generates guiding keywords/hints to steer black-box LLM output toward target style.",
            "what_we_extract": "Steers minimal-perturbation edits using specific brand keywords without altering sentence structure.",
            "what_we_fix": "Applies directional prompting to span-level intent-preserving repairs.",
            "filename": "19_Directional_Stimulus_Prompting_2302.11520.pdf"
        },
        {
            "id": 20,
            "title": "Judging the Judges",
            "citation": "Zheng et al., NeurIPS 2023",
            "core_mechanism": "Analyzes systematic biases in LLM evaluators (position bias, verbosity bias, self-enhancement).",
            "what_we_extract": "Swap-evaluation calibration to prevent over-flagging benign marketing metaphors.",
            "what_we_fix": "Converts MT-bench methodologies into automated runtime calibration filters.",
            "filename": "20_Judge_Alignment_2306.05685.pdf"
        }
    ]
