
# Implementation Plan: 만능 계산기 프로그램

**Branch**: `001-` | **Date**: 2025-10-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from file system structure or context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code, or `AGENTS.md` for all other agents).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
윈도우 계산기와 동일한 기능을 가진 한글 UI 데스크톱 계산기 애플리케이션 개발. 기본 사칙연산, 공학용 계산, 메모리 기능 등을 포함하는 만능 계산기로, GUI 데스크톱 애플리케이션으로 구현됩니다.

## Technical Context
**User Requirement**: 웹이 아닌 데스크톱 앱(응용프로그램)으로 제작, 윈도우 계산기와 동일한 기능, 한글 UI

**Language/Version**: Python 3.11+ (크로스 플랫폼 GUI 지원)
**Primary Dependencies**: Tkinter (Python 표준 GUI 라이브러리) 또는 PyQt6 (고급 UI)
**Storage**: N/A (계산 히스토리는 세션 메모리에만 유지)
**Testing**: pytest (단위 테스트), pytest-qt (GUI 테스트)
**Target Platform**: Windows 10/11 (주 타겟), macOS/Linux 호환
**Project Type**: single (데스크톱 애플리케이션)
**Performance Goals**: UI 응답성 <50ms, 계산 정확도 15자리 이상
**Constraints**: 오프라인 동작, <50MB 메모리 사용, 단일 실행 파일 배포 가능
**Scale/Scope**: 단일 사용자, 윈도우 계산기 기능 세트 (표준/공학용 모드, 메모리 기능)

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Status**: Constitution template is not yet configured for this project.

**Initial Assessment**:
- ✅ Single desktop application (no unnecessary complexity)
- ✅ Self-contained project (no external service dependencies)
- ✅ Testable architecture (계산 로직과 UI 분리 가능)
- ✅ Simple scope (윈도우 계산기 복제)

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
calculator/
├── src/
│   ├── core/              # 계산 엔진 (비즈니스 로직)
│   │   ├── calculator.py  # 계산기 핵심 로직
│   │   ├── operations.py  # 연산자 구현
│   │   └── memory.py      # 메모리 기능 (M+, M-, MR, MC)
│   ├── ui/                # GUI 인터페이스
│   │   ├── main_window.py # 메인 윈도우
│   │   ├── buttons.py     # 버튼 레이아웃
│   │   └── display.py     # 디스플레이 위젯
│   └── app.py             # 애플리케이션 진입점

tests/
├── unit/
│   ├── test_calculator.py
│   ├── test_operations.py
│   └── test_memory.py
└── integration/
    └── test_ui_integration.py

requirements.txt           # Python 의존성
README.md                 # 프로젝트 설명서
```

**Structure Decision**: 단일 데스크톱 애플리케이션 구조 선택. 계산 로직(core)과 UI를 분리하여 테스트 가능성 확보. 윈도우 계산기의 표준/공학용 모드를 지원하기 위한 확장 가능한 구조.

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh claude`
     **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs:
  - **contracts/calculator_core_interface.md** → 계산기 코어 인터페이스 구현 및 테스트
  - **contracts/ui_interface.md** → UI 컴포넌트 구현 및 테스트
  - **data-model.md** → 데이터 모델 클래스 구현
  - **quickstart.md** → 통합 테스트 시나리오

**Task Categories**:
1. **Setup Tasks** (환경 구성):
   - Python 가상환경 생성
   - requirements.txt 작성
   - 프로젝트 디렉토리 구조 생성
   - pytest 설정

2. **Core Logic Tasks** (계산 엔진):
   - CalculatorState, MemoryState 데이터 클래스 [P]
   - CalculationHistory, HistoryEntry 구현 [P]
   - Enum 정의 (CalculatorMode, AngleMode, OperationType) [P]
   - Calculator 핵심 로직 (input_digit, calculate) [테스트 먼저]
   - 연산자 구현 (사칙연산, 단항 연산, 삼각함수)
   - 메모리 기능 구현
   - 에러 처리 (오버플로우, 0으로 나누기, 잘못된 입력)

3. **UI Tasks** (Tkinter GUI):
   - DisplayWidget 구현 [테스트 먼저]
   - ButtonLayout 구현 (표준 모드 버튼) [테스트 먼저]
   - ButtonLayout 확장 (공학용 모드 버튼)
   - MainWindow 통합
   - 이벤트 핸들러 바인딩
   - 한글 폰트 설정
   - 에러 메시지 표시 UI

4. **Integration Tasks**:
   - 시나리오 1-10 통합 테스트 (quickstart.md 기반)
   - 성능 테스트 (UI 응답성, 메모리)
   - 정밀도 테스트

5. **Deployment Tasks**:
   - PyInstaller 설정
   - 단일 실행 파일 빌드
   - 배포 테스트 (Python 미설치 환경)

**Ordering Strategy**:
- **TDD 순서**: 각 모듈에 대해 테스트 먼저 작성 → 구현 → 테스트 통과
- **의존성 순서**:
  1. Data models (CalculatorState, Enums) - 의존성 없음
  2. Core logic (Calculator) - 데이터 모델 의존
  3. UI components (Display, Buttons) - 코어 인터페이스 의존
  4. Integration (MainWindow) - 모든 컴포넌트 의존
- **병렬 표시 [P]**: 독립적인 파일 (예: 각 enum, 각 데이터 모델)

**Estimated Task Count**: 30-35개
- Setup: 4개
- Core: 12-15개
- UI: 8-10개
- Integration: 4-6개
- Deployment: 2개

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
  - ✅ research.md 생성 완료
  - ✅ 모든 기술 선택 완료 (Tkinter, Decimal, PyInstaller)
- [x] Phase 1: Design complete (/plan command)
  - ✅ data-model.md 생성 완료
  - ✅ contracts/calculator_core_interface.md 생성 완료
  - ✅ contracts/ui_interface.md 생성 완료
  - ✅ quickstart.md 생성 완료 (10개 시나리오)
  - ✅ CLAUDE.md 업데이트 완료
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
  - ✅ 5개 카테고리 정의 (Setup, Core, UI, Integration, Deployment)
  - ✅ 30-35개 작업 추정
  - ✅ TDD 순서 및 의존성 순서 계획
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
  - ✅ 단일 애플리케이션 (복잡도 낮음)
  - ✅ 외부 의존성 최소화 (Tkinter 표준 라이브러리)
- [x] Post-Design Constitution Check: PASS
  - ✅ MVC 패턴으로 관심사 분리 (Core/UI)
  - ✅ 테스트 가능한 아키텍처
- [x] All NEEDS CLARIFICATION resolved
  - ✅ UI 형태: 데스크톱 앱 (Tkinter)
  - ✅ 계산 범위: 표준 + 공학용 모드
  - ✅ 히스토리: 세션 메모리만
  - ✅ 정밀도: Decimal 32자리
  - ✅ 괄호: 공학용 모드에서 지원
  - ✅ 메모리 기능: MS, MR, M+, M-, MC
- [x] Complexity deviations documented
  - ✅ 복잡도 위반 없음 (단순한 단일 앱)

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*
