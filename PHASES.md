# Development Phases

This document captures the phased development plan derived from the technical specification in `README.md`. It is intentionally high-level to prevent context drift while keeping implementation decisions flexible.

## Phase 1: Core Functionality (MVP)
- Establish the end-to-end scanning pipeline (extraction → scanning → aggregation → rendering).
- Implement deterministic scanners for the highest-priority injection and obfuscation signals.
- Produce stable JSON and Markdown reports with evidence and risk scoring.
- Ensure local-first execution, modular structure, and performance-minded processing.

## Phase 2: Input Expansion & Robust Extraction
- Extend input support beyond plain text/markdown.
- Improve extraction fidelity while preserving offsets and contextual metadata.
- Introduce additional scanners aligned with newly supported formats.
- Implement HTML extraction and hidden-text HTML detection.

## Phase 3: Usability & Operator Experience
- Refine CLI ergonomics, reporting clarity, and actionable remediation guidance.
- Add policy mode behaviors and configurable thresholds.
- Expand test coverage and documentation to support real-world adoption.

## Phase 4: Advanced Capabilities
- Support additional input types and optional network-based scanning workflows.
- Continue improving detection breadth, scoring transparency, and modular extensibility.
- Harden stability guarantees for schema compatibility across releases.
