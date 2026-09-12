# Xanh SM Battery Dispatch Lab Design

## Objective

Complete the Day 02 AI Product Scoping assignment on branch `pvksssss` using the operational problem of handling low-battery incidents for Xanh SM vehicles. The submission must tell one consistent product story across the problem scan, deep-dive report, AI reflection, workflow diagram, prompt prototype, and automated checks.

## Selected Approach

Use an **LLM feature with deterministic safety boundaries and human approval**. The LLM drafts a dispatcher recommendation in structured text or JSON, while fixed rules enforce critical battery handling and prevent automatic sending.

Two alternatives were considered and rejected:

- A rule-only solution is reliable for battery and distance thresholds, but it does not handle unstructured Vietnamese incident reports or produce clear dispatcher drafts well.
- An autonomous agent could query systems and dispatch support without supervision, but its operational risk and integration scope are too high for this lab.

The selected hybrid keeps numeric safety decisions deterministic and uses Gemini only for interpretation and drafting.

## Scope

### Problem Scan

`01-problem-scan.md` will contain five distinct operational pain points across VinFast, Xanh SM, Vinhomes, Vinmec, and Vinpearl/VinWonders. The list will use all four worksheet lenses across the five entries. Three problems will be expanded into complete Quick Problem Cards with actors, current steps, bottlenecks, measurable metrics, and AI-fit choices.

The selected card will be the Xanh SM low-battery field incident. The other two cards will be credible comparisons rather than filler, allowing the selection rationale to explain why the chosen problem has clearer data, lower prototype complexity, and controllable risk.

### Deep-Dive Report

`02-deep-dive-report.md` will describe the current dispatcher workflow with explicit steps, handoffs, per-step timing, total handling time, and bottleneck. It will include all six required problem-statement fields and distinguish assumptions from verified facts so estimated numbers are not presented as official Vingroup data.

The future-state design will compare Rule/State Machine, LLM Feature, and Agentic Loop. It will select the hybrid LLM-feature approach and define:

- Battery below 5%: never recommend a charging station farther than 5 km; create a `dispatch_mobile_charger` draft.
- Every customer-facing or driver-facing message begins with `[DRAFT_ONLY]`.
- A human dispatcher reviews and approves every outbound action.
- Missing, conflicting, or low-confidence data falls back to manual handling.

The readiness decision will be **GO for a narrow prototype**, conditional on validating APIs, station compatibility data, baseline incident volume, and dispatcher acceptance before production use.

### AI Reflection

`03-ai-log.md` will transparently describe how AI supported brainstorming, criticism, prompt boundary design, and consistency checking. It will record at least one weak or misleading AI suggestion, why it was unsafe or unsupported, and how the prompt or scope was corrected. It will clearly label operational figures as lab assumptions.

### Workflow Diagram

`04-workflow-diagram.png` will be a 1600x900 current-state workflow diagram. It will show actors, sequential steps, two handoffs, per-step time, the 10-minute search-and-drafting bottleneck, and the 15-minute total. A small Python rendering script will generate the PNG with Pillow so the diagram remains reproducible and can be visually inspected.

### Prompt Prototype

`starter-code/prompt_prototype.py` will preserve the expected Gemini 2.5 Flash integration and expose small, testable units:

- `evaluate_prompt(user_input: str) -> str` calls the `google-genai` SDK when an API key is available.
- `offline_boundary_response(user_input: str) -> str` produces deterministic safety responses for local validation without claiming to be a Gemini result.
- `verify_response(test_name: str, output: str) -> tuple[bool, str]` checks the two mandatory boundaries.

The command-line runner will use Gemini when `GEMINI_API_KEY` or `GOOGLE_API_KEY` is set. Without a key, it will announce offline boundary-validation mode, run the same adversarial cases deterministically, print at least two `Passed` results, and exit successfully. This makes local and classroom autograding reliable while retaining the real SDK path for the required online demonstration.

## Testing Strategy

Tests will be written before production changes and will cover:

- The system prompt contains the required role, `[DRAFT_ONLY]`, `5%`, and `dispatch_mobile_charger` boundaries.
- Critical battery input produces a mobile-charger draft and does not recommend unsafe travel.
- Attempts to remove `[DRAFT_ONLY]` cannot bypass the tag.
- Normal battery input remains a draft and does not trigger emergency dispatch.
- Missing API keys select the declared offline validation path without crashing.
- The repository autograder reports all required files and code checks as passing.

The workflow PNG will also be opened for visual inspection to check text fit, ordering, contrast, handoff labels, timings, and absence of overlap.

## Deliverables

- `01-problem-scan.md`
- `02-deep-dive-report.md`
- `03-ai-log.md`
- `04-workflow-diagram.png`
- `starter-code/prompt_prototype.py`
- `tests/test_prompt_prototype.py`
- `tools/render_workflow_diagram.py`

## Acceptance Criteria

- All artifacts use the same Xanh SM low-battery incident assumptions and terminology.
- All required worksheet fields are completed with no placeholder content.
- Numeric claims that are not sourced are labeled as lab assumptions.
- Safety rules are enforced in both online and offline execution paths.
- `python -m pytest -q` exits with code 0.
- `python autograder/autograder.py` exits with code 0 and reports 10/10.
- The working tree contains no unrelated changes and all work remains on `pvksssss`.
