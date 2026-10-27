export interface VisualAssetInput {
  id?: string;
  filename: string;
  image_base64?: string;
  width?: number;
  height?: number;
  dominant_hexes?: string[];
  has_logo?: boolean;
  logo_bbox?: [number, number, number, number];
  has_alt_text?: boolean;
  alt_text?: string;
  text_overlay?: string;
  text_color_hex?: string;
  background_color_hex?: string;
}

export interface Finding {
  id: string;
  span: [number, number];
  flagged_text: string;
  category: 'FACT' | 'TONE' | 'VISUAL' | 'REGULATORY' | 'LEXICAL' | 'MATH';
  severity: 'BLOCKER' | 'WARNING' | 'SUGGESTION';
  title: string;
  explanation: string;
  cited_source: string;
  rule_id: string;
  suggested_edit: string;
  confidence: number;
  anomaly_type?: string;
  math_details?: {
    claimed: string;
    computed: string;
    formula: string;
    discrepancy: number;
  };
}

export interface VisualFinding {
  id: string;
  asset_id: string;
  check_type: 'COLOR_DELTA_E' | 'WCAG_CONTRAST' | 'LOGO_SAFE_ZONE' | 'LOGO_ASPECT_RATIO' | 'ALT_TEXT';
  severity: 'BLOCKER' | 'WARNING' | 'SUGGESTION';
  title: string;
  explanation: string;
  measured_value: number;
  threshold_value: number;
  passed: boolean;
  citation: string;
  suggestion: string;
  bounding_box?: [number, number, number, number];
}

export interface PersonaVector {
  formality: number;
  warmth: number;
  authority: number;
  technicality: number;
  directness: number;
}

export interface AuditSummary {
  total_findings: number;
  blockers: number;
  warnings: number;
  suggestions: number;
  compliance_score: number;
  tier: 'GREEN' | 'AMBER' | 'RED';
  publishing_status: 'AUTO_APPROVED' | 'BRAND_REVIEW_REQUIRED' | 'LEGAL_BLOCKED';
  cryptographic_token?: string;
}

export interface DocumentAuditResponse {
  document_id: string;
  title: string;
  timestamp: number;
  summary: AuditSummary;
  findings: Finding[];
  visual_findings: VisualFinding[];
  scrubbed_pii_count: number;
  persona_distance: number;
  measured_persona: PersonaVector;
  target_persona: PersonaVector;
}

export interface BrandRule {
  id: string;
  category: string;
  name: string;
  description: string;
  severity: string;
  source_document: string;
  section: string;
  page: number;
  rule_type: string;
  active: boolean;
}

export interface TemporalFact {
  id: string;
  entity: string;
  attribute: string;
  value: string;
  valid_from: string;
  valid_to: string;
  source_document: string;
  section: string;
  page: number;
  status: 'ACTIVE' | 'DEPRECATED' | 'UPCOMING';
}

export interface CryptographicCertificate {
  token: string;
  document_id: string;
  sha256_hash: string;
  timestamp: number;
  compliance_score: number;
  tier: string;
  status: string;
  issuer: string;
}

export interface AcademicPaper {
  id: number;
  title: string;
  citation: string;
  core_mechanism: string;
  what_we_extract: string;
  what_we_fix: string;
  filename: string;
}
