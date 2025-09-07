# Tasks: Build a Web Application for Brand Storytelling

**Input**: Design documents from `/specs/003-cat-temp-txt/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below assume web app structure from plan.md

## Phase 3.1: Setup
- [ ] T001 Create backend/ and frontend/ directories per implementation plan
- [ ] T002 Initialize Python project in backend/ with FastAPI, google-genai>=1.32.0, SQLAlchemy dependencies
- [ ] T003 Initialize frontend project with vanilla JS, HTML, CSS
- [ ] T004 [P] Configure linting and formatting tools (black, flake8 for Python; eslint for JS)

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T005 [P] Contract test POST /projects in backend/tests/contract/test_projects_post.py
- [ ] T006 [P] Contract test POST /projects/{id}/character in backend/tests/contract/test_character_post.py
- [ ] T007 [P] Contract test POST /projects/{id}/product in backend/tests/contract/test_product_post.py
- [ ] T008 [P] Contract test POST /projects/{id}/background in backend/tests/contract/test_background_post.py
- [ ] T009 [P] Contract test POST /projects/{id}/story in backend/tests/contract/test_story_post.py
- [ ] T010 [P] Contract test POST /projects/{id}/generate in backend/tests/contract/test_generate_post.py
- [ ] T011 [P] Integration test full user flow in backend/tests/integration/test_full_flow.py
- [ ] T012 [P] Integration test character generation approval in backend/tests/integration/test_character_approval.py
- [ ] T013 [P] Integration test product upload in backend/tests/integration/test_product_upload.py
- [ ] T014 [P] Integration test background generation in backend/tests/integration/test_background_generation.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T015 [P] Project model in backend/src/models/project.py
- [ ] T016 [P] Character model in backend/src/models/character.py
- [ ] T017 [P] Product model in backend/src/models/product.py
- [ ] T018 [P] Background model in backend/src/models/background.py
- [ ] T019 [P] Story model in backend/src/models/story.py
- [ ] T020 [P] Image model in backend/src/models/image.py
- [ ] T021 GeminiService for image generation in backend/src/services/gemini_service.py
- [ ] T022 POST /projects endpoint in backend/src/api/projects.py
- [ ] T023 POST /projects/{id}/character endpoint in backend/src/api/character.py
- [ ] T024 POST /projects/{id}/product endpoint in backend/src/api/product.py
- [ ] T025 POST /projects/{id}/background endpoint in backend/src/api/background.py
- [ ] T026 POST /projects/{id}/story endpoint in backend/src/api/story.py
- [ ] T027 POST /projects/{id}/generate endpoint in backend/src/api/generate.py
- [ ] T028 Create project form in frontend/src/components/project-form.js
- [ ] T029 Character input form in frontend/src/components/character-form.js
- [ ] T030 Product upload form in frontend/src/components/product-form.js
- [ ] T031 Background input form in frontend/src/components/background-form.js
- [ ] T032 Story input form in frontend/src/components/story-form.js
- [ ] T033 Image display and selection in frontend/src/components/image-gallery.js
- [ ] T034 Main app logic in frontend/src/app.js
- [ ] T035 HTML structure in frontend/index.html
- [ ] T036 CSS styling in frontend/styles.css

## Phase 3.4: Integration
- [ ] T037 Connect models to SQLite DB in backend/src/database.py
- [ ] T038 Frontend API integration in frontend/src/api.js
- [ ] T039 Error handling and logging in backend/src/middleware.py
- [ ] T040 CORS configuration for frontend-backend communication

## Phase 3.5: Polish
- [ ] T041 [P] Unit tests for models in backend/tests/unit/test_models.py
- [ ] T042 [P] Unit tests for services in backend/tests/unit/test_services.py
- [ ] T043 Performance tests (<2s for image generation)
- [ ] T044 [P] Update API documentation in docs/api.md
- [ ] T045 Frontend accessibility improvements
- [ ] T046 Run quickstart.md validation

## Dependencies
- Tests (T005-T014) before implementation (T015-T036)
- Models (T015-T020) before services (T021) and endpoints (T022-T027)
- Backend implementation before frontend (T028-T036)
- T037 blocks T022-T027
- T038 blocks T028-T036
- Implementation before polish (T041-T046)

## Parallel Example
```
# Launch T005-T014 together:
Task: "Contract test POST /projects in backend/tests/contract/test_projects_post.py"
Task: "Contract test POST /projects/{id}/character in backend/tests/contract/test_character_post.py"
... (all contract and integration tests)
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All contracts have corresponding tests
- [ ] All entities have model tasks
- [ ] All tests come before implementation
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task
