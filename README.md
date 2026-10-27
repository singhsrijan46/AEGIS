# Inkloom Verity™ / VeriBrand AI™

> **Intelligent Enterprise Brand-Governance & Pre-Publication Verification Platform**  
> *Resolving the Content Velocity vs. Brand Integrity Crisis Across Distributed Teams and Generative AI Agents.*

---

## 1. Executive Summary

As enterprise organizations scale, content production is decentralized across hundreds of employees, regional business units, freelance agencies, and autonomous Generative AI tools (ChatGPT, Claude, Midjourney). Static brand books (80+ page PDFs stored in shared drives) fail to prevent off-brand messaging, outdated SLAs, unsupported metrics, non-compliant visual treatments, and deceptive marketing claims before publication.

**Inkloom Verity™** is an enterprise-grade pre-publication brand governance and verification platform that operates directly within native authoring environments and CMS publishing gateways. Rather than acting as a punitive binary blocker, Verity functions as an **explainable, intent-preserving editorial pair-assistant**. It surfaces exact guideline violations, provides transparent citations with source links, and suggests one-click, non-destructive revisions that preserve the creator's voice and rhetorical intent while ensuring absolute factual, visual, and regulatory compliance.

---

## 2. System Architecture & The 5-Step Stepwise Pipeline

```
STEPWISE ARCHITECTURE PIPELINE
[Step 1: Grounding & SSOT] ──► [Step 2: Claim & Linter Engines] ──► [Step 3: Multimodal CV & WCAG]
• PDF Brand Vault Parser       • Vale AST Deterministic Linter     • OpenCV CIELAB ΔE < 2.0
• Temporal KG (Neo4j)          • E-AFV Atomic Fact Extraction      • WCAG 2.1 AA/AAA Contrast
• Dense Vector Store (Qdrant)  • Decoupled CoVe Question Planner   • LayoutLMv3 Logo Safe-Zones
• Air-Gapped VPC & PII Scrub   • Two-Stage Self-RAG & RAGAS Gate   • Alt-Text & Spatial Auditor
                                                                             │
┌────────────────────────────────────────────────────────────────────────────┘
▼
[Step 4: Intent-Preserving UI] ──► [Step 5: Governance & CMS Gates]
• TIGERScore Span Localizer        • Tiered Approval Routing (Green/Amber/Red)
• Levenshtein-Constrained MPED     • Pre-Publish Blocking CMS Webhooks
• TipTap In-line Diff Viewer       • Slack & Teams Single-Click Sign-Off Bots
• Google Docs & Figma Plugins      • Cryptographic SHA-256 Compliance Ledger
                                   • HDBSCAN Guideline Ambiguity Heatmaps
```

### The 6 Core Verification Subsystems
1. **Subsystem 1: Brand Constitution & Persona Vectorization**
   - Rules DAG compilation stopping LLM attention dilution.
   - 5D persona coordinates: Formality, Warmth, Authority, Technicality, Directness.
   - Calibrated cosine style distance: $\mathcal{D}_{\text{voice}}(x, \mathbf{c}_{\text{brand}}) = 1 - \frac{\mathbf{v}_x \cdot \mathbf{c}_{\text{brand}}}{\|\mathbf{v}_x\| \|\mathbf{c}_{\text{brand}}\|}$.

2. **Subsystem 2: Adaptive Gating & Anomaly Triage**
   - Reflection classifier predicting `PASS`, `CHECK_STYLE`, `CHECK_FACT`, `CHECK_VISUAL`.
   - Tri-faceted anomaly classification (Siren's Song): `Input-Conflicting`, `Context-Conflicting`, `Fact-Conflicting`.

3. **Subsystem 3: Air-Gapped Enterprise-Atomic Claim Verification (E-AFV)**
   - FActScore proposition decomposition: $\mathcal{A}(S) = \{a_1, a_2, \dots, a_k\}$.
   - Decoupled CoVe non-confirmatory question planning.
   - Deterministic FacTool Python calculator for statistical and percentage change assertions.
   - Temporal Single Source of Truth (SSOT) preventing anachronistic hallucinations of expired pricing or SLAs.
   - RAGAS Faithfulness quality gate ($F \ge 0.85/0.90$).

4. **Subsystem 4: Multimodal Spatial, Layout & Accessibility Guardrails**
   - Deterministic CIELAB $\Delta E_{00}$ colorimetric distance against official corporate palette ($\Delta E_{00} < 2.0$).
   - Mathematical WCAG 2.1 Contrast Ratio ($CR = \frac{L_1 + 0.05}{L_2 + 0.05}$) enforcing 4.5:1 for body copy.
   - Logo exclusion zone buffer ($M \ge 0.5 \times H_{\text{logo}}$) and aspect-ratio distortion check.
   - ScreenAI alt-text auditor ensuring accessible descriptive text.

5. **Subsystem 5: Interactive Deterministic Prose Linter**
   - Microsecond Vale AST linters for prohibited terms (e.g. *cheap* $\to$ *cost-effective*, *ninja* $\to$ *domain expert*).
   - Mandatory trademark placements on first mention (e.g., *Inkloom Verity™*).

6. **Subsystem 6: Intent-Preserving Revision & Human-in-the-Loop UI**
   - Minimal Perturbation Edit Distance (MPED):
     $$\hat{S}^* = \arg\min_{\hat{S} \in \mathcal{S}_{\text{compliant}}} \left( \mathcal{D}_{\text{Levenshtein}}(S, \hat{S}) + \lambda \cdot (1 - \cos(\mathbf{e}_S, \mathbf{e}_{\hat{S}})) \right)$$
   - Anti-Overruling Mandate: The human creator retains ultimate editorial discretion. Overrides are recorded with justification reasons into telemetry.

---

## 3. Academic Research Review & 20-Paper Synthesis Matrix

All 20 foundational research papers are downloaded and archived locally in [`research_papers/`](file:///d:/AEGIS/research_papers/):

| # | Paper & Citation | Extracted Capability (Unique Pro) | Enterprise Vulnerability Resolved |
|---|---|---|---|
| 1 | **FActScore** (Min et al., EMNLP 2023) | Fine-grained atomic proposition decomposition. | Replaced static Wikipedia with private Temporal Knowledge Graph. |
| 2 | **CoVe** (Dhuliawala et al., Meta AI, ACL 2024) | Decoupled verification question planning. | Constrained output to span-level diffs to preserve author's tone. |
| 3 | **SAFE** (Wei et al., Google DeepMind, 2024) | Multi-step agentic query formulation. | Replaced public search with air-gapped internal hybrid vector/graph RAG. |
| 4 | **AVeriTeC** (Schlichtkrull et al., NeurIPS 2023) | Multi-class labels with mandatory citation spans. | Bound evidence directly to official version-controlled corporate registers. |
| 5 | **FacTool** (Chern et al., 2023) | Tool-augmented deterministic calculations. | Integrated Python math sandbox for conversion deltas and SLA formulas. |
| 6 | **RAGAS** (Es et al., 2023) | Quantitative evaluation metrics (Faithfulness $\ge 0.90$). | Connected post-hoc evaluation to automated minimal-perturbation span repair. |
| 7 | **Self-RAG** (Asai et al., ICLR 2024) | Selective retrieval reflection tokens. | Implemented reflection gating to bypass RAG on purely transitional prose. |
| 8 | **Siren's Song** (Zhang et al., 2023) | Root-cause taxonomy of hallucinations. | Operationalized taxonomy into real-time triage routing queues. |
| 9 | **Constitutional AI** (Bai et al., Anthropic 2022) | Natural-language rule steering. | Decomposed 100-page style guides into a micro-agent DAG. |
| 10 | **Self-Refine** (Madaan et al., NeurIPS 2023) | Iterative generation-feedback-refinement. | Added token masking to freeze already-compliant text spans. |
| 11 | **CRITIC** (Gou et al., ICLR 2024) | Tool-interactive cross-examination. | Bound LLM reasoning to microsecond deterministic Vale AST linters. |
| 12 | **TIGERScore** (Jiang et al., EMNLP 2023) | Reference-free explainable error localization. | Calibrated NLG error metrics for enterprise brand, legal, and tone taxonomies. |
| 13 | **LayoutLMv3** (Huang et al., ACM MM 2022) | Multimodal 2D spatial document modeling. | Paired spatial layout with deterministic OpenCV geometry algorithms. |
| 14 | **DocOwl 1.5** (Ye et al., 2024) | OCR, table parsing, and infographic auditing. | Backed qualitative inference with deterministic axis and ratio checks. |
| 15 | **ScreenAI** (Google Research, 2024) | UI and visually-situated layout understanding. | Retargeted attention to marketing assets, social cards, and digital ad banners. |
| 16 | **Co-Writing CHI** (Jakesch et al., ACM CHI 2023) | Anti-Overruling Mandate: human retains ultimate agency. | Built creator override channel with justification logs feeding telemetry. |
| 17 | **Chain-of-Thought** (Wei et al., NeurIPS 2022) | Multi-step deductive reasoning. | Restricted CoT to high-risk Amber and Red tier legal violations. |
| 18 | **Controllable Text Gen** (Zhang et al., ACM CSUR) | Attribute-conditioned generation via latent persona vectors. | Parameterized brand voice as a 5D coordinate vector with cosine distance. |
| 19 | **Directional Stimulus** (Li et al., NeurIPS 2023) | Policy network generating keyword hints. | Applied directional prompting to span-level intent-preserving repairs. |
| 20 | **Judge Alignment** (Zheng et al., NeurIPS 2023) | Systematic bias analysis in LLM evaluators. | Applied position-swap calibration to prevent over-flagging benign metaphors. |

---

## 4. Repository Structure

```
d:\AEGIS
├── backend/
│   ├── app/
│   │   ├── main.py                      # FastAPI gateway & WebSocket hub
│   │   ├── models/schemas.py            # Pydantic models (Finding, Rule, Fact, Cert)
│   │   ├── core/
│   │   │   ├── engine.py                # UnifiedBrandGovernanceEngine orchestrator
│   │   │   ├── presidio_privacy.py      # Air-gapped PII & sensitive info sanitizer
│   │   │   ├── brand_vault.py           # Brand Constitution DAG & Design Tokens
│   │   │   ├── temporal_kg.py           # Temporal Knowledge Graph (SSOT)
│   │   │   ├── hybrid_retriever.py      # Air-Gapped Dense + BM25 Hybrid Retriever
│   │   │   ├── vale_linter.py           # Deterministic AST prose & trademark linter
│   │   │   ├── fact_decomposer.py       # E-AFV Atomic Proposition Decomposer
│   │   │   ├── cove_planner.py          # Decoupled CoVe Question Planner
│   │   │   ├── fact_calculator.py       # FacTool Python Math & Statistics Validator
│   │   │   ├── ragas_evaluator.py       # RAGAS Faithfulness Quality Gate
│   │   │   ├── persona_vector.py        # 5D Persona Vector Scorer
│   │   │   ├── vision_wcag.py           # OpenCV CIELAB ΔE00 & WCAG 2.1 Contrast
│   │   │   ├── mped_rewriter.py         # Minimal Perturbation Edit Distance Rewriter
│   │   │   ├── triage_router.py         # Green/Amber/Red Tier Risk Triage
│   │   │   ├── cms_gateways.py          # CMS Pre-Publish Webhooks & Slack Bots
│   │   │   ├── audit_ledger.py          # Immutable SHA-256 Compliance Ledger
│   │   │   └── ambiguity_telemetry.py   # HDBSCAN Override Ambiguity Heatmaps
│   │   └── tests/                       # Complete pytest unit & integration suite
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.tsx               # Top navigation & live status
│   │   │   ├── PreFlightEditor.tsx      # In-line diff review studio & sidecar
│   │   │   ├── VisualAssetInspector.tsx # Multimodal CV canvas & WCAG inspector
│   │   │   ├── BrandVaultManager.tsx    # Brand Constitution DAG & Temporal SSOT
│   │   │   ├── GovernanceTelemetry.tsx  # Department heatmaps & SHA-256 ledger
│   │   │   ├── CMSGateSimulator.tsx     # WordPress/Webflow pre-publish filter
│   │   │   ├── ResearchCorpusExplorer.tsx # 20-Paper academic synthesis matrix
│   │   │   └── OverrideModal.tsx        # Creator override justification modal
│   │   ├── styles/
│   │   │   ├── index.css                # Obsidian dark design system & tokens
│   │   │   └── components.css           # Specialized cards, meters, terminals
│   │   ├── api/client.ts                # Backend API client with offline fallback
│   │   └── data/                        # Presets & academic corpus data
├── research_papers/                     # 20 full-text academic research PDFs
├── run_server.py                        # Backend launcher script
└── README.md                            # Comprehensive platform documentation
```

---

## 5. Verification & Testing

### Running the Test Suite
The automated test suite verifies all mathematical formulations, deterministic linters, and publishing gates:
```bash
python -m pytest backend/app/tests
```
**Test Results:**
- `test_brand_vault.py`: Rules compilation, official palette fidelity, Presidio PII sanitization **(PASSED)**
- `test_claim_verification.py`: E-AFV decomposition, FacTool math discrepancies, RAGAS quality gate **(PASSED)**
- `test_vision_wcag.py`: CIELAB $\Delta E_{00}$ color distance, WCAG 2.1 contrast formula, logo safe-zones **(PASSED)**
- `test_end_to_end.py`: End-to-end audit, Red Tier blocking, Green Tier SHA-256 certificate issuance, and CMS publish gate **(PASSED)**

### Running the Services Locally

#### 1. Start Backend Server
```bash
python run_server.py
# Running on http://127.0.0.1:8000
# OpenAPI Docs: http://127.0.0.1:8000/docs
```

#### 2. Start Frontend Studio
```bash
cd frontend
npm run dev
# Running on http://localhost:5173/
```
