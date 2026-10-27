import { AcademicPaper } from '../types';

export const RESEARCH_PAPERS: AcademicPaper[] = [
  {
    id: 1,
    title: "FActScore: Fine-grained Atomic Evaluation of Factual Precision",
    citation: "Min et al., EMNLP 2023",
    core_mechanism: "Decomposes long-form text into atomic, independent propositions using dependency parsing; evaluates veracity individually against Wikipedia.",
    what_we_extract: "Eliminates compound sentence ambiguity. Computes a quantitative factuality score: S = (1/N) ∑ I(a_i ∈ K).",
    what_we_fix: "Assumes static Wikipedia. We substitute Wikipedia with a private Temporal Enterprise Knowledge Graph (T-EKG).",
    filename: "01_FActScore_2305.14251.pdf"
  },
  {
    id: 2,
    title: "Chain-of-Verification (CoVe) Reduces Hallucination in LLMs",
    citation: "Dhuliawala et al., Meta AI, ACL 2024",
    core_mechanism: "Four-stage pipeline: Draft -> Plan verification questions -> Execute questions independently -> Generate verified output.",
    what_we_extract: "Prevents circular hallucination by answering verification queries decoupled from draft context.",
    what_we_fix: "Tends to rewrite text wholesale, destroying author voice. We constrain output to span-level replacements only.",
    filename: "02_Chain_of_Verification_2309.11495.pdf"
  },
  {
    id: 3,
    title: "Long-form Factuality in Large Language Models (SAFE)",
    citation: "Wei et al., Google DeepMind, 2024",
    core_mechanism: "Agentic multi-turn query formulation, search execution, and step-by-step reasoning over retrieved snippets.",
    what_we_extract: "Dynamic query formulation handles complex, multi-hop factual claims.",
    what_we_fix: "Queries public Google Search, leaking trade secrets. We replace search with an Air-Gapped Hybrid Vector/Graph RAG.",
    filename: "03_SAFE_Factuality_2403.18802.pdf"
  },
  {
    id: 4,
    title: "AVeriTeC: Real-world Claim Verification with Web Evidence",
    citation: "Schlichtkrull et al., NeurIPS 2023",
    core_mechanism: "Benchmark and model pairing veracity verdicts with exact textual justification.",
    what_we_extract: "Standardizes multi-class labels (Supported, Refuted, Outdated, Conflicting) with mandatory citation spans.",
    what_we_fix: "Relies on unstructured web pages. We link directly to official corporate version-controlled documentation.",
    filename: "04_AVeriTeC_2305.13117.pdf"
  },
  {
    id: 5,
    title: "FacTool: Factuality Detection in Generative AI",
    citation: "Chern et al., 2023",
    core_mechanism: "Tool-augmented framework deploying specialized external checkers (code interpreters, Python calculators, search APIs).",
    what_we_extract: "Verifies numeric, statistical, and algorithmic assertions deterministically without relying on LLM math.",
    what_we_fix: "Disconnected tool calls. We bind tools directly to enterprise financial and product data warehouses.",
    filename: "05_FacTool_2307.13528.pdf"
  },
  {
    id: 6,
    title: "RAGAS: Automated Evaluation of Retrieval Augmented Generation",
    citation: "Es et al., 2023",
    core_mechanism: "Framework defining quantitative evaluation metrics: Faithfulness, Answer Relevance, and Context Precision.",
    what_we_extract: "Provides an automated mathematical quality gate: rejects any claim with Faithfulness < 0.90.",
    what_we_fix: "Evaluates retrieval post-hoc without suggesting fixes. We connect it to automated span repair.",
    filename: "06_RAGAS_2309.15217.pdf"
  },
  {
    id: 7,
    title: "Self-RAG: Learning to Retrieve, Generate, and Critique",
    citation: "Asai et al., ICLR 2024",
    core_mechanism: "Selective retrieval via special reflection tokens ([Retrieve], [IsSup], [IsUse]) to retrieve knowledge only when needed.",
    what_we_extract: "Eliminates unnecessary retrieval latency and database overhead on creative or transitional prose.",
    what_we_fix: "Requires base model fine-tuning. We implement reflection tokens via lightweight prompt-directed classification heads.",
    filename: "07_Self_RAG_2310.11511.pdf"
  },
  {
    id: 8,
    title: "Siren's Song in the AI Ocean: A Survey on Hallucination",
    citation: "Zhang et al., Computational Linguistics 2023",
    core_mechanism: "Taxonomy classifying hallucinations into Input-conflicting, Context-conflicting, and Fact-conflicting.",
    what_we_extract: "Structured root-cause classification allows triaging flags into targeted remediation workflows.",
    what_we_fix: "Purely diagnostic survey. We operationalize the taxonomy into a real-time triage routing engine.",
    filename: "08_Sirens_Song_Hallucinations_2309.01219.pdf"
  },
  {
    id: 9,
    title: "Constitutional AI: Harmlessness from AI Feedback",
    citation: "Bai et al., Anthropic 2022",
    core_mechanism: "Steers LLM evaluation and critique using a natural-language set of behavioral principles ('Constitution').",
    what_we_extract: "Allows brand directors to write plain-English guidelines that compile into active system prompts without code changes.",
    what_we_fix: "Rule cramming causes attention dilution. We split rules into a hierarchical Directed Acyclic Graph (DAG) of micro-agents.",
    filename: "09_Constitutional_AI_2212.08073.pdf"
  },
  {
    id: 10,
    title: "Self-Refine: Iterative Refinement with Self-Feedback",
    citation: "Madaan et al., NeurIPS 2023",
    core_mechanism: "Iterative generation-feedback-refinement loop (x0 -> f1 -> x1 ...) without external supervised data.",
    what_we_extract: "Produces progressive editorial polish across multiple guideline dimensions.",
    what_we_fix: "Prone to regression drift. We freeze already-compliant spans using token masking.",
    filename: "10_Self_Refine_2303.17651.pdf"
  },
  {
    id: 11,
    title: "CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing",
    citation: "Gou et al., ICLR 2024",
    core_mechanism: "Interactive critiquing where the LLM executes deterministic tools to cross-examine its own reasoning.",
    what_we_extract: "Bridges the gap between semantic LLM reasoning and deterministic regex/dictionary linters (Vale, AST parsers).",
    what_we_fix: "Lacks brand layout awareness. We expand the tool ecosystem to include computer vision geometry APIs.",
    filename: "11_CRITIC_2305.11738.pdf"
  },
  {
    id: 12,
    title: "TIGERScore: Towards Building an Explainable Metric for Text Generation",
    citation: "Jiang et al., EMNLP 2023",
    core_mechanism: "Reference-free explainable metric that pinpoints exact error tokens [s_start, s_end], error type, and rationales.",
    what_we_extract: "Formats findings into an in-line, localized user interface with actionable explanations.",
    what_we_fix: "Trained on generic NLG errors. We calibrate it specifically for enterprise brand, legal, and tone taxonomies.",
    filename: "12_TIGERScore_2304.05353.pdf"
  },
  {
    id: 13,
    title: "LayoutLMv3: Pre-training for Document AI with Multimodal Masking",
    citation: "Huang et al., ACM MM 2022",
    core_mechanism: "Multimodal pre-training jointly modeling 2D bounding boxes, textual tokens, and image patches.",
    what_we_extract: "Evaluates structural layout compliance in complex documents (slide decks, PDF brochures, one-pagers).",
    what_we_fix: "Cannot verify exact colorimetry or pixel padding. We pair it with OpenCV deterministic geometry algorithms.",
    filename: "13_LayoutLMv3_2204.08387.pdf"
  },
  {
    id: 14,
    title: "DocOwl 1.5: An Open-Source Vision-Language Model for Document Understanding",
    citation: "Ye et al., 2024",
    core_mechanism: "Open-source Vision-Language Model specialized in OCR, complex table parsing, and chart reading.",
    what_we_extract: "Automatically inspects embedded infographics, financial tables, and data visualizations in collateral.",
    what_we_fix: "Qualitative visual inference only. We back it with deterministic calculation of table margins and ratios.",
    filename: "14_DocOwl1.5_2403.12895.pdf"
  },
  {
    id: 15,
    title: "ScreenAI: A Vision-Language Model for UI and Visually-Situated Language",
    citation: "Google Research, 2024",
    core_mechanism: "Vision-Language model specialized in UI elements, buttons, banners, layout hierarchy, and visual accessibility.",
    what_we_extract: "Checks digital banners, social cards, and web graphics for visual hierarchy and alt-text completeness.",
    what_we_fix: "Focused on mobile screens. We retarget its attention weights to social media assets and advertising banners.",
    filename: "15_ScreenAI_2402.04615.pdf"
  },
  {
    id: 16,
    title: "Co-Writing with Opinionated Language Models Affects Users' Views",
    citation: "Jakesch et al., ACM CHI 2023",
    core_mechanism: "Empirical study demonstrating how AI writing assistants subtly manipulate human opinions and homogenize voice.",
    what_we_extract: "Establishes the 'Anti-Overruling Mandate': AI must never silently rewrite; human retains ultimate editorial agency.",
    what_we_fix: "Identifies the psychological hazard but provides no system. We build the human-in-the-loop override architecture.",
    filename: "16_Co_Writing_Opinionated_LLM_2302.00560.pdf"
  },
  {
    id: 17,
    title: "Chain-of-Thought Prompting Elicits Reasoning in LLMs",
    citation: "Wei et al., NeurIPS 2022",
    core_mechanism: "Elicits multi-step deductive reasoning via step-by-step intermediate thoughts before rendering a judgment.",
    what_we_extract: "Ensures complex brand policies (e.g., comparative advertising guidelines) are reasoned through systematically.",
    what_we_fix: "Verbose and slow. We restrict CoT to amber and red tier violations requiring complex legal interpretation.",
    filename: "17_Chain_of_Thought_2201.11903.pdf"
  },
  {
    id: 18,
    title: "Controllable Text Generation with Language Models: A Review",
    citation: "Zhang et al., ACM CSUR",
    core_mechanism: "Formalizes attribute-conditioned generation P(Y | X, c) using latent persona vectors c.",
    what_we_extract: "Formulates brand voice as a vector across 5 axes: Formality, Warmth, Authority, Technicality, and Directness.",
    what_we_fix: "Theoretical review. We implement vector projection using dense semantic style embeddings.",
    filename: "18_Controllable_Text_Gen_Survey_2104.14816.pdf"
  },
  {
    id: 19,
    title: "Guiding Large Language Models via Directional Stimulus Prompting",
    citation: "Li et al., NeurIPS 2023",
    core_mechanism: "Small directional policy network generates guiding keywords/hints to steer black-box LLM output toward target style.",
    what_we_extract: "Guides the rewording engine using specific brand keywords without overwriting the author's sentence structure.",
    what_we_fix: "Explored only for summarization. We apply it to span-level intent-preserving brand repairs.",
    filename: "19_Directional_Stimulus_Prompting_2302.11520.pdf"
  },
  {
    id: 20,
    title: "Judging the Judges: Evaluating Alignment and Robustness of LLM-as-a-Judge",
    citation: "Zheng et al., NeurIPS 2023",
    core_mechanism: "Analyzes systematic biases in LLM evaluators (position bias, verbosity bias, self-enhancement bias).",
    what_we_extract: "Implements position-swap and reference calibration to prevent over-flagging benign marketing metaphors.",
    what_we_fix: "Diagnostic benchmark. We convert MT-bench methodologies into automated runtime calibration filters.",
    filename: "20_Judge_Alignment_2306.05685.pdf"
  }
];
