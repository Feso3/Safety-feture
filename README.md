# Safety-feture
Hidden Prompt Detector — Technical Specification

⸻

Objectives

Primary Goal

Create a local-first security scanner that detects prompt-injection signals, hidden instructions, and obfuscation patterns in content before it is consumed by LLMs or autonomous agents.

Core Use Case

Provide a preflight scanning tool that developers and AI builders can run on documents, webpages, or datasets prior to ingestion into AI workflows.

Design Principles
	•	Deterministic detection before AI-based analysis
	•	Evidence-driven security reporting
	•	Transparent scoring and explainability
	•	Modular architecture with extensible scanners
	•	Human-in-the-loop decision model

Non-Goals
	•	Not malware detection
	•	Not AI-content authorship detection
	•	Not runtime guardrails or enterprise API middleware
	•	Not automatic enforcement beyond optional policy mode

⸻

Features

CLI Interface
	•	hidprompt scan <path>
	•	Optional flags:
	•	--format json|md|both
	•	--out <directory>
	•	--policy <policy.yaml>
	•	--quiet
	•	--verbose

Supported Inputs (Phased)
	•	Phase 1:
	•	.txt
	•	.md
	•	Phase 2:
	•	.html
	•	.htm
	•	Phase 3:
	•	.pdf
	•	Phase 4:
	•	scan-url (HTTP fetch + HTML extraction)

Output Artifacts
	•	report.json — canonical machine-readable output
	•	report.md — human-readable security report

Detection Categories
	1.	prompt_injection_phrase
	2.	assistant_directive_language
	3.	hidden_text_html
	4.	unicode_obfuscation
	5.	encoded_blob
	6.	tool_call_bait (optional early)

Security Report Capabilities
	•	Risk score (0–100)
	•	Risk level (LOW/MEDIUM/HIGH)
	•	Severity classification per finding
	•	Evidence snippets with location metadata
	•	Rationale and remediation guidance
	•	Summary counts by severity

Policy Mode (Later Phase)
	•	YAML-based thresholds
	•	Exit codes:
	•	0 LOW
	•	2 MEDIUM
	•	3 HIGH

⸻

Logic

Processing Pipeline
	1.	Extraction
	•	Normalize content into plain text
	•	Preserve offsets, line numbers, page hints
	•	Capture annotations (hidden regions, encoding signals)
	2.	Scanning
	•	Each scanner runs independently
	•	Returns structured findings
	•	No scanner modifies content
	3.	Aggregation
	•	Merge findings
	•	Deduplicate overlapping detections
	•	Compute weighted risk score
	4.	Rendering
	•	Generate JSON report
	•	Generate Markdown report

⸻

Scanner Responsibilities

Injection Phrase Scanner
Detect explicit instructions targeting agents or assistants:
	•	Override patterns
	•	System prompt language
	•	Imperative directives

Unicode Obfuscation Scanner
Detect:
	•	bidirectional override characters
	•	zero-width characters
	•	homoglyph substitution risks

Encoded Blob Scanner
Detect:
	•	Base64-like blocks
	•	High entropy sequences
	•	Suspicious encoded regions

Hidden HTML Scanner (Phase 2)
Detect:
	•	display:none
	•	invisible spans
	•	off-screen positioning
	•	zero-size text

⸻

Risk Scoring Model
	•	Weighted aggregation of findings
	•	Severity tiers:
	•	HIGH: explicit override or hidden instruction
	•	MEDIUM: obfuscation or suspicious steering patterns
	•	LOW: weak contextual signals
	•	Transparent mapping from findings to score

⸻

Report Schema (JSON)

Top-Level Fields
	•	tool
	•	version
	•	scan_id
	•	timestamp
	•	target
	•	file_info
	•	size
	•	sha256
	•	mime
	•	summary
	•	risk_score
	•	risk_level
	•	counts by severity
	•	findings
	•	extraction

Finding Object
	•	id
	•	severity
	•	category
	•	confidence
	•	title
	•	evidence
	•	snippets
	•	offsets
	•	line numbers
	•	page numbers (if applicable)
	•	rationale
	•	recommendation
	•	tags

⸻

Constraints

Technical Constraints
	•	No LLM dependency in early phases
	•	Deterministic scanners only in MVP
	•	Local execution only
	•	Modular plugin-style scanner design
	•	Extraction layer separated from scanning logic

Performance Constraints
	•	Must handle large text files without memory exhaustion
	•	Streaming or chunk-based scanning allowed
	•	Avoid quadratic scanning algorithms

Security Constraints
	•	Scanner must not execute embedded code
	•	Treat all input as untrusted
	•	No outbound network calls in scan process (except explicit scan-url command)

UX Constraints
	•	Evidence must always include location context
	•	Reports must remain readable without external tooling
	•	Stable report schema across minor versions

⸻

File Structure

hidprompt/
│
├── cli.py
├── pipeline.py
├── schema.py
├── scoring.py
├── config.py
│
├── extractors/
│   ├── text_extractor.py
│   ├── html_extractor.py
│   └── pdf_extractor.py
│
├── scanners/
│   ├── injection_phrase_scanner.py
│   ├── unicode_obfuscation_scanner.py
│   ├── encoded_blob_scanner.py
│   └── hidden_html_scanner.py
│
├── renderers/
│   ├── json_renderer.py
│   └── markdown_renderer.py
│
├── utils/
│   ├── hashing.py
│   ├── offsets.py
│   └── normalization.py
│
├── tests/
│   ├── test_pipeline.py
│   ├── test_scanners.py
│   └── test_renderers.py
│
├── corpus/
│   ├── clean/
│   ├── malicious/
│   └── edge_cases/
│
├── docs/
│   └── SPEC.md
│
├── README.md
└── pyproject.toml
