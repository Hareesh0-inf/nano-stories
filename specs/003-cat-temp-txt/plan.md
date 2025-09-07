# Implementation Plan: Build a Web Application for Brand Storytelling

**Branch**: `003-cat-temp-txt` | **Date**: September 7, 2025 | **Spec**: /specs/003-cat-temp-txt/spec.md
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
4. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, or `GEMINI.md` for Gemini CLI).
6. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
8. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Build a web application for brand storytelling with four layers: character, product, background, fusion. Users create projects, provide details for each layer, get approvals, and generate three creative images. Backend uses Python FastAPI with Gemini API client and nano-banana model. Frontend uses pure vanilla JavaScript, HTML, CSS.

## Technical Context
**Language/Version**: Python 3.11 for backend, JavaScript ES6+ for frontend  
**Primary Dependencies**: FastAPI, google-genai >=1.32.0 for Gemini, vanilla JS  
**Storage**: SQLite for projects and data  
**Testing**: pytest for backend, manual for frontend  
**Target Platform**: Web browsers  
**Project Type**: Web application  
**Performance Goals**: Response time <2s for image generation  
**Constraints**: No authentication, open source  
**Scale/Scope**: Single user, small scale

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: [#] (max 3 - e.g., api, cli, tests)
- Using framework directly? (no wrapper classes)
- Single data model? (no DTOs unless serialization differs)
- Avoiding patterns? (no Repository/UoW without proven need)

**Architecture**:
- EVERY feature as library? (no direct app code)
- Libraries listed: [name + purpose for each]
- CLI per library: [commands with --help/--version/--format]
- Library docs: llms.txt format planned?

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN-Refactor cycle enforced? (test MUST fail first)
- Git commits show tests before implementation?
- Order: Contract→Integration→E2E→Unit strictly followed?
- Real dependencies used? (actual DBs, not mocks)
- Integration tests for: new libraries, contract changes, shared schemas?
- FORBIDDEN: Implementation before test, skipping RED phase

**Observability**:
- Structured logging included?
- Frontend logs → backend? (unified stream)
- Error context sufficient?

**Versioning**:
- Version number assigned? (MAJOR.MINOR.BUILD)
- BUILD increments on every change?
- Breaking changes handled? (parallel tests, migration plan)

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure]
```

**Structure Decision**: Option 2: Web application

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - Latest Gemini API documentation and usage
   - Nano-banana model specifics
   - FastAPI best practices for image generation
   - Vanilla JS for file upload and image display

2. **Generate and dispatch research agents**:
   ```
   Task: "Research latest Google AI Python SDK for Gemini API"
   Task: "Research nano-banana model integration"
   Task: "Research FastAPI for async image processing"
   Task: "Research vanilla JS for multipart form upload"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: Use google-generativeai 0.3.2
   - Rationale: Latest stable version
   - Alternatives considered: Older versions
   - Decision: Nano-banana model via Gemini API
   - Rationale: Specified in requirements
   - Alternatives considered: Other models
   - Decision: FastAPI 0.104.1
   - Rationale: Latest version
   - Alternatives considered: Flask
   - Decision: Vanilla JS with fetch and FormData
   - Rationale: No frameworks needed
   - Alternatives considered: jQuery

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Project: id, name, created_at
   - Character: id, project_id, details, personality, image_url
   - Product: id, project_id, image_file
   - Background: id, project_id, scene_details, lighting, image_url
   - Story: id, project_id, story_text
   - Image: id, project_id, prompt, image_url

2. **Generate API contracts** from functional requirements:
   - POST /projects - create project
   - POST /projects/{id}/character - generate character
   - POST /projects/{id}/product - upload product image
   - POST /projects/{id}/background - generate background
   - POST /projects/{id}/story - set story
   - POST /projects/{id}/generate - generate images
   - Output OpenAPI schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - Test each endpoint with mock data
   - Assert response schemas
   - Tests must fail initially

4. **Extract test scenarios** from user stories:
   - Full workflow integration test
   - Quickstart test = create project and generate

5. **Update agent file incrementally**:
   - Create .github/copilot-instructions.md
   - Add tech stack and guidelines

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, .github/copilot-instructions.md

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model creation task [P] 
- Each user story → integration test task
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation 
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 25-30 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*