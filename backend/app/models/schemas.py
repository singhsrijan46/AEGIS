"""
Pydantic schemas and data models for Inkloom Verity / VeriBrand AI.
"""

from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field
import time
import uuid


class SpanIndices(BaseModel):
    start: int
    end: int
    text: str


class Finding(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    span: Tuple[int, int]  # (start_char, end_char)
    flagged_text: str
    category: str  # 'FACT', 'TONE', 'VISUAL', 'REGULATORY', 'LEXICAL', 'MATH'
    severity: str  # 'BLOCKER', 'WARNING', 'SUGGESTION'
    title: str
    explanation: str  # Chain-of-Thought rationale
    cited_source: str  # Document, Section & Page
    rule_id: str
    suggested_edit: str  # Minimal Perturbation drop-in replacement
    confidence: float = 1.0  # 0.0 - 1.0 (RAGAS Faithfulness / Model confidence)
    anomaly_type: Optional[str] = None  # Siren's Song: 'Input-Conflicting', 'Context-Conflicting', 'Fact-Conflicting'
    math_details: Optional[Dict[str, Any]] = None


class PersonaVector(BaseModel):
    formality: float = 0.6     # [-1, 1]
    warmth: float = 0.4        # [-1, 1]
    authority: float = 0.8     # [-1, 1]
    technicality: float = 0.5  # [-1, 1]
    directness: float = 0.7    # [-1, 1]


class BrandRule(BaseModel):
    id: str
    category: str
    name: str
    description: str
    severity: str
    source_document: str
    section: str
    page: int
    rule_type: str  # 'regex', 'vector', 'kg_fact', 'wcag', 'logo_box'
    pattern: Optional[str] = None
    replacement: Optional[str] = None
    active: bool = True


class TemporalFact(BaseModel):
    id: str
    entity: str
    attribute: str
    value: str
    valid_from: str  # ISO date string e.g. "2024-01-01"
    valid_to: str    # ISO date string e.g. "2026-12-31" or "PRESENT"
    source_document: str
    section: str
    page: int
    status: str = "ACTIVE"  # ACTIVE, DEPRECATED, UPCOMING


class VisualAssetInput(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    filename: str
    image_base64: Optional[str] = None
    width: int = 1200
    height: int = 630
    dominant_hexes: List[str] = Field(default_factory=list)
    has_logo: bool = True
    logo_bbox: Optional[List[int]] = None  # [x, y, w, h]
    has_alt_text: bool = False
    alt_text: str = ""
    text_overlay: Optional[str] = None
    text_color_hex: Optional[str] = None
    background_color_hex: Optional[str] = None


class VisualFinding(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    asset_id: str
    check_type: str  # 'COLOR_DELTA_E', 'WCAG_CONTRAST', 'LOGO_SAFE_ZONE', 'ALT_TEXT'
    severity: str    # 'BLOCKER', 'WARNING', 'SUGGESTION'
    title: str
    explanation: str
    measured_value: float
    threshold_value: float
    passed: bool
    citation: str
    suggestion: str
    bounding_box: Optional[List[int]] = None  # [x, y, w, h]


class DocumentAuditRequest(BaseModel):
    document_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = "Untitled Draft"
    author: str = "Anonymous"
    department: str = "Content Marketing"  # Marketing, Sales, PR, Agency, AI
    text: str
    images: List[VisualAssetInput] = Field(default_factory=list)
    bypass_cache: bool = False


class AuditSummary(BaseModel):
    total_findings: int
    blockers: int
    warnings: int
    suggestions: int
    compliance_score: float  # 0.0 - 100.0
    tier: str  # 'GREEN' (>=90), 'AMBER' (70-89), 'RED' (<70)
    publishing_status: str  # 'AUTO_APPROVED', 'BRAND_REVIEW_REQUIRED', 'LEGAL_BLOCKED'
    cryptographic_token: Optional[str] = None


class DocumentAuditResponse(BaseModel):
    document_id: str
    title: str
    timestamp: float = Field(default_factory=time.time)
    summary: AuditSummary
    findings: List[Finding]
    visual_findings: List[VisualFinding]
    scrubbed_pii_count: int = 0
    persona_distance: float = 0.0
    measured_persona: PersonaVector
    target_persona: PersonaVector


class CreatorOverrideRequest(BaseModel):
    finding_id: str
    document_id: str
    rule_id: str
    reason_code: str  # 'STYLISTIC_CHOICE', 'CLIENT_EXCEPTION', 'METAPHOR', 'OUTDATED_RULE'
    justification_note: str
    author: str


class CryptographicCertificate(BaseModel):
    token: str
    document_id: str
    sha256_hash: str
    timestamp: float
    compliance_score: float
    tier: str
    status: str
    issuer: str = "Inkloom Verity Governance Engine v2.4"
