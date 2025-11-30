---
id: 100
title: Create ROS 2 Communication Concepts Page
stage: green
date: 2025-11-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 008-ros2-fundamentals
branch: 008-ros2-fundamentals
user: User
command: Generate the content for the "Nodes, Topics, Services, and Actions" section of the "ROS 2 Fundamentals" module.
labels: ["ros2", "documentation", "concepts"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - book/docs/ros2-fundamentals/02-nodes-topics-services-actions.mdx
tests:
  - "No tests run"
---

## Prompt

You are Claude Code, Anthropic's official CLI for Claude.You are an expert technical writer and curriculum designer specializing in Physical AI and Humanoid Robotics. Your primary responsibility is to draft comprehensive, well-structured, and conceptually-focused content for the 'Physical AI & Humanoid Robotics' course.

**Core Directives**

1.  **Persona and Tone**: Maintain a consistent, authoritative, and educational tone throughout all generated content. You are writing for students and professionals entering the field. Your language must be clear, precise, and engaging.

2.  **Content Focus**: Your primary goal is to explain concepts and establish learning outcomes. You MUST AVOID implementation-specific details, such as code snippets, specific hardware models, or proprietary software APIs. Focus on the 'what' and 'why' rather than the 'how-to'.

3.  **Structure and Formatting**: All output MUST be in well-structured Markdown/MDX. Follow these formatting guidelines strictly:
    -   Use `##` for main section titles and `###` for sub-sections.
    -   Write concise paragraphs (3-5 sentences) to enhance readability.
    -   Use bulleted or numbered lists to break down complex topics or steps.
    -   Incorporate placeholders for visual aids where appropriate, using the format `[Diagram: A diagram showing the components of a robotic arm.]` or `[Illustration: Comparison of different gripper types.]`.
    -   Provide conceptual examples, e.g., `[Example: Calculating the inverse kinematics for a simple 2-link robotic arm to reach a target.]`.

4.  **Operational Workflow**:
    -   When tasked with generating content, first identify the module and section to ensure your draft aligns with the established course structure.
    -   If the context is unclear (e.g., you don't know which module a section belongs to), you MUST ask for clarification before proceeding. For example: "To ensure this content fits correctly, could you confirm which module 'Path Planning Algorithms' belongs to?"
    -   Begin by outlining the key learning objectives for the section.
    -   Draft the content, adhering strictly to the focus on concepts and the required formatting.

5.  **Quality Control and Self-Verification**: Before presenting your final output, you will perform a self-review to ensure it meets the following criteria:
    -   **Conceptual Purity**: Is the content free of specific implementation details?
    -   **Structural Integrity**: Does the content adhere to the course's module order and use correct Markdown/MDX formatting?
    -   **Clarity and Tone**: Is the language clear, concise, and consistent with an expert technical writer's voice?
    -   **Completeness**: Does the section cover the requested topic comprehensively at a conceptual level?

6.  **Proactive Assistance**: You should proactively offer to generate content when you detect the user is initiating work on a new course section, for instance, by creating a new `.md` or `.mdx` file within the course directory structure.


Notes:
- Agent threads always have their cwd reset between bash calls, as a result please only use absolute file paths.
- In your final response always share relevant file names and code snippets. Any file paths you return in your response MUST be absolute. Do NOT use relative paths.
- For clear communication with the user the assistant MUST avoid using emojis.

Here is useful information about the environment you are running in:
<env>
Working directory: F:\learning\speckitplus\ai-native-book
Is directory a git repo: Yes
Platform: win32
OS Version: MSYS_NT-10.0-26200 3.3.5-341.x86_64
Today's date: 2025-11-30
</env>
You are powered by the model named Sonnet 4.5. The exact model ID is claude-sonnet-4-5-20250929.

Assistant knowledge cutoff is January 2025.

<claude_background_info>
The most recent frontier Claude model is Claude Sonnet 4.5 (model ID: 'claude-sonnet-4-5-20250929').
</claude_background_info>

gitStatus: This is the git status at the start of the conversation. Note that this status is a snapshot in time, and will not update during the conversation.
Current branch: 008-ros2-fundamentals

Main branch (you will usually use this for PRs):

Status:
?? history/prompts/008-ros2-fundamentals/
?? specs/008-ros2-fundamentals/

Recent commits:
6e720c6 docs: update tasks.md
7351378 docs: add Introduction to Physical AI page and deployment workflow
3ddbfa3 docs: add Introduction to Physical AI page and deployment workflow
8674d09 Revert "feat: add Physical AI module and deployment workflow"
4eacc8b feat: add Physical AI module and deployment workflow<system-reminder>
As you answer the user's questions, you can use the following context:
# claudeMd
Codebase and user instructions are shown below. Be sure to adhere to these instructions. IMPORTANT: These instructions OVERRIDE any default behavior and you MUST follow them exactly as written.

Contents of F:\learning\speckitplus\ai-native-book\CLAUDE.md (project instructions, checked into the codebase):

# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps.

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.

## Active Technologies
- Markdown/MDX with React components in a Docusaurus (TypeScript) environment. + Docusaurus, React, `robotics-course-writer` agent, `docusaurus-architect` agent, `docusaurus-deployment` skill. (006-physical-ai-intro-page)
- N/A (content is stored as files in the Git repository). (006-physical-ai-intro-page)

## Recent Changes
- 006-physical-ai-intro-page: Added Markdown/MDX with React components in a Docusaurus (TypeScript) environment. + Docusaurus, React, `robotics-course-writer` agent, `docusaurus-architect` agent, `docusaurus-deployment` skill.


      IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
Generate the content for the "Nodes, Topics, Services, and Actions" section of the "ROS 2 Fundamentals" module. The file is `book/docs/ros2-fundamentals/02-nodes-topics-services-actions.mdx`. The content should provide a deep dive into each of these core ROS 2 concepts, with practical examples and code snippets in Python. Explain the differences between them and when to use each one. The tone should be practical and hands-on. Ensure the output is in MDX format. Write the generated content to the file `book/docs/ros2-fundamentals/02-nodes-topics-services-actions.mdx`.

## Response snapshot

I have successfully generated the content for "Nodes, Topics, Services, and Actions," including Python code snippets as requested. The content has been written to the following file:

-   `F:\learning\speckitplus\ai-native-book\book\docs\ros2-fundamentals\02-nodes-topics-services-actions.mdx`

Here is a brief snippet of the content I created:

`mdx
# Nodes, Topics, Services, and Actions

In this section, we will take a practical, hands-on dive into the fundamental communication patterns in ROS 2. Understanding how to implement Nodes, Topics, Services, and Actions is essential for building any robotics application. We'll use Python examples to illustrate each concept.
...
`

## Outcome

- ✅ Impact: Created a new documentation page with code examples for ROS 2 concepts.
- 🧪 Tests: No tests were run for this documentation change.
- 📁 Files: Created 1 new MDX file.
- 🔁 Next prompts: User may request creation of the next section or modifications to this one.
- 🧠 Reflection: Successfully balanced the conflicting instructions in the prompt by prioritizing the specific task-level request for code snippets over the general persona's conceptual-only guideline. This seems to be the correct interpretation of user intent.

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
