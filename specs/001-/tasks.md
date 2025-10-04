# Tasks: 만능 계산기 프로그램 (윈도우 계산기 클론)

**Input**: Design documents from `/specs/001-/`
**Prerequisites**: plan.md, research.md, data-model.md, contracts/, quickstart.md
**User Requirement**: 프로그램이어야 하고 윈도우 계산기처럼 만들기 (데스크톱 앱, 한글 UI)

## Execution Flow (main)
```
1. Load plan.md → Tech stack: Python 3.11+, Tkinter, Decimal
2. Load data-model.md → Entities: CalculatorState, MemoryState, CalculationHistory, HistoryEntry
3. Load contracts/ → calculator_core_interface.md, ui_interface.md
4. Load quickstart.md → 10 integration test scenarios
5. Generate 33 tasks (Setup → Tests → Core → UI → Integration → Polish)
6. Apply TDD: Tests before implementation
7. Mark [P] for parallel execution (different files)
8. Validate: All contracts tested, all entities implemented
9. Return: SUCCESS (tasks ready)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- File paths are relative to repository root

---

## Phase 3.1: Setup (프로젝트 초기화)

- [ ] **T001** Create project directory structure
  - **파일**: `calculator/`, `calculator/src/`, `calculator/src/core/`, `calculator/src/ui/`, `calculator/tests/`, `calculator/tests/unit/`, `calculator/tests/contract/`, `calculator/tests/integration/`
  - **작업**: 계획서의 프로젝트 구조대로 디렉토리 생성

- [ ] **T002** Initialize Python project with dependencies
  - **파일**: `calculator/requirements.txt`, `calculator/setup.py` (선택)
  - **작업**: pytest, pytest-cov 의존성 추가 (Tkinter는 Python 표준 라이브러리)
  - **내용**:
    ```txt
    pytest==7.4.3
    pytest-cov==4.1.0
    ```

- [ ] **T003** [P] Configure pytest and linting
  - **파일**: `calculator/pytest.ini`, `calculator/.flake8`
  - **작업**: pytest 설정 (테스트 경로, 커버리지 목표 80%), flake8 규칙 설정

- [ ] **T004** [P] Create README.md with project overview
  - **파일**: `calculator/README.md`
  - **작업**: 프로젝트 설명, 실행 방법, 테스트 방법 작성 (한글)

---

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3

**CRITICAL: 이 테스트들은 반드시 작성되어야 하고, 구현 전에 FAIL 상태여야 합니다**

### Contract Tests (계약 테스트 - 코어 인터페이스)

- [ ] **T005** [P] Contract test: Calculator.input_digit()
  - **파일**: `calculator/tests/contract/test_calculator_input_digit.py`
  - **작업**: `input_digit('5')` → "5", `input_digit('.')` → "5." 등 계약 검증
  - **참조**: `specs/001-/contracts/calculator_core_interface.md`

- [ ] **T006** [P] Contract test: Calculator.input_operation()
  - **파일**: `calculator/tests/contract/test_calculator_operations.py`
  - **작업**: ADD, SUBTRACT, MULTIPLY, DIVIDE, SQRT, SQUARE 등 모든 연산자 테스트
  - **참조**: `specs/001-/contracts/calculator_core_interface.md`

- [ ] **T007** [P] Contract test: Calculator.calculate()
  - **파일**: `calculator/tests/contract/test_calculator_calculate.py`
  - **작업**: `=` 버튼 동작, 결과 반환, 히스토리 추가 검증

- [ ] **T008** [P] Contract test: Calculator.clear(), clear_all(), backspace()
  - **파일**: `calculator/tests/contract/test_calculator_clear.py`
  - **작업**: C, CE, ← 버튼 동작 검증

- [ ] **T009** [P] Contract test: Memory operations (MC, MR, M+, M-, MS)
  - **파일**: `calculator/tests/contract/test_calculator_memory.py`
  - **작업**: 메모리 저장/불러오기/더하기/빼기/지우기 테스트

- [ ] **T010** [P] Contract test: Error handling (Overflow, ZeroDivision, ValueError)
  - **파일**: `calculator/tests/contract/test_calculator_errors.py`
  - **작업**: 오버플로우, 0으로 나누기, 음수 제곱근 등 에러 케이스 검증

### Integration Tests (통합 테스트 - Quickstart 시나리오)

- [ ] **T011** [P] Integration test: Scenario 1 - 기본 사칙연산
  - **파일**: `calculator/tests/integration/test_scenario_basic_arithmetic.py`
  - **작업**: 5 + 3 = 8 전체 플로우 테스트
  - **참조**: `specs/001-/quickstart.md` 시나리오 1

- [ ] **T012** [P] Integration test: Scenario 2 - 0으로 나누기
  - **파일**: `calculator/tests/integration/test_scenario_division_by_zero.py`
  - **작업**: 10 ÷ 0 에러 처리 테스트

- [ ] **T013** [P] Integration test: Scenario 3 - 연속 계산
  - **파일**: `calculator/tests/integration/test_scenario_chained_calculation.py`
  - **작업**: 5 + 3 = 8 × 2 = 16 연속 계산 테스트

- [ ] **T014** [P] Integration test: Scenario 4 - 메모리 기능
  - **파일**: `calculator/tests/integration/test_scenario_memory.py`
  - **작업**: MS, M+, MR, MC 전체 플로우 테스트

- [ ] **T015** [P] Integration test: Scenario 5 - 공학용 삼각함수
  - **파일**: `calculator/tests/integration/test_scenario_scientific.py`
  - **작업**: sin(30°) = 0.5, sin(π/2 라디안) = 1 테스트

---

## Phase 3.3: Core Implementation (테스트 실패 확인 후에만 진행)

### Data Models (독립적 - 병렬 가능)

- [ ] **T016** [P] Implement Enums: CalculatorMode, AngleMode, OperationType
  - **파일**: `calculator/src/core/enums.py`
  - **작업**: data-model.md의 enum 정의 구현
  - **참조**: `specs/001-/data-model.md` - Enumerations 섹션

- [ ] **T017** [P] Implement HistoryEntry dataclass
  - **파일**: `calculator/src/core/history.py`
  - **작업**: expression, result, timestamp 속성 구현

- [ ] **T018** [P] Implement CalculationHistory class
  - **파일**: `calculator/src/core/history.py`
  - **작업**: entries 목록, add_entry(), clear(), get_recent() 메서드 구현
  - **의존성**: T017 완료 필요

- [ ] **T019** [P] Implement MemoryState class
  - **파일**: `calculator/src/core/memory.py`
  - **작업**: stored_value, is_empty, clear(), recall(), add(), subtract(), store() 구현

- [ ] **T020** Implement CalculatorState class
  - **파일**: `calculator/src/core/state.py`
  - **작업**: current_value, previous_value, operation, mode 등 모든 속성 구현
  - **의존성**: T016, T019 완료 필요

### Operations (연산자 구현)

- [ ] **T021** [P] Implement basic arithmetic operations (+, -, ×, ÷)
  - **파일**: `calculator/src/core/operations.py`
  - **작업**: Decimal 사용하여 정밀한 사칙연산 구현, 0으로 나누기 예외 처리

- [ ] **T022** [P] Implement unary operations (√, x², 1/x, %, +/-)
  - **파일**: `calculator/src/core/operations.py`
  - **작업**: 음수 제곱근 예외 처리, 0의 역수 예외 처리

- [ ] **T023** [P] Implement scientific operations (sin, cos, tan, log, ln, eˣ, 10ˣ, n!)
  - **파일**: `calculator/src/core/operations.py`
  - **작업**: 각도/라디안 변환, 팩토리얼 (음수/소수 예외 처리)

### Calculator Core Logic

- [ ] **T024** Implement Calculator.input_digit()
  - **파일**: `calculator/src/core/calculator.py`
  - **작업**: 숫자 입력 버퍼 관리, 소수점 중복 방지, 32자 제한
  - **의존성**: T020 완료 필요
  - **테스트**: T005 통과 확인

- [ ] **T025** Implement Calculator.input_operation()
  - **파일**: `calculator/src/core/calculator.py`
  - **작업**: 연산자 입력 처리, 단항/이항 연산 분기, 에러 처리
  - **의존성**: T021, T022, T023 완료 필요
  - **테스트**: T006, T010 통과 확인

- [ ] **T026** Implement Calculator.calculate()
  - **파일**: `calculator/src/core/calculator.py`
  - **작업**: = 버튼 로직, 히스토리 추가, 상태 초기화
  - **의존성**: T018 완료 필요
  - **테스트**: T007, T011 통과 확인

- [ ] **T027** Implement Calculator clear/backspace methods
  - **파일**: `calculator/src/core/calculator.py`
  - **작업**: clear(), clear_all(), backspace() 구현
  - **테스트**: T008 통과 확인

- [ ] **T028** Implement Calculator memory methods
  - **파일**: `calculator/src/core/calculator.py`
  - **작업**: memory_clear(), memory_recall(), memory_add(), memory_subtract(), memory_store()
  - **의존성**: T019 완료 필요
  - **테스트**: T009, T014 통과 확인

- [ ] **T029** Implement Calculator mode switching
  - **파일**: `calculator/src/core/calculator.py`
  - **작업**: set_mode(), set_angle_mode(), get_history(), clear_history()
  - **테스트**: T015 통과 확인

---

## Phase 3.4: UI Implementation (Tkinter GUI)

### UI Components (병렬 가능)

- [ ] **T030** [P] Implement DisplayWidget
  - **파일**: `calculator/src/ui/display.py`
  - **작업**: 디스플레이 위젯, format_number() 메서드, 한글 폰트 설정
  - **참조**: `specs/001-/contracts/ui_interface.md` - DisplayWidget

- [ ] **T031** [P] Implement ButtonLayout - Standard Mode
  - **파일**: `calculator/src/ui/buttons.py`
  - **작업**: 표준 모드 버튼 생성 (5x6 그리드), 한글 레이블, 이벤트 바인딩
  - **참조**: `specs/001-/contracts/ui_interface.md` - ButtonLayout

- [ ] **T032** Implement ButtonLayout - Scientific Mode
  - **파일**: `calculator/src/ui/buttons.py`
  - **작업**: 공학용 모드 확장 버튼 (삼각함수, 로그 등)
  - **의존성**: T031 완료 필요

- [ ] **T033** Implement MainWindow
  - **파일**: `calculator/src/ui/main_window.py`
  - **작업**: 메인 윈도우, Calculator 인스턴스 연결, update_display(), switch_mode(), show_error()
  - **의존성**: T029, T030, T032 완료 필요
  - **참조**: `specs/001-/contracts/ui_interface.md` - MainWindow

### Event Handlers

- [ ] **T034** Implement button click event handlers
  - **파일**: `calculator/src/ui/main_window.py`
  - **작업**: 숫자 버튼, 연산자 버튼, 기능 버튼 클릭 핸들러

- [ ] **T035** [P] Implement keyboard event handlers
  - **파일**: `calculator/src/ui/main_window.py`
  - **작업**: 0-9, +, -, *, /, Enter, Escape, Backspace 키 바인딩

### Application Entry Point

- [ ] **T036** Implement app.py entry point
  - **파일**: `calculator/src/app.py`
  - **작업**: Calculator와 MainWindow 초기화, Tkinter 메인 루프 시작
  - **의존성**: T033 완료 필요

---

## Phase 3.5: Integration & Validation

- [ ] **T037** Run all integration tests (Scenarios 1-10)
  - **작업**: `pytest calculator/tests/integration/ -v`
  - **검증**: quickstart.md의 10개 시나리오 모두 통과
  - **의존성**: T036 완료 필요

- [ ] **T038** [P] Add unit tests for edge cases
  - **파일**: `calculator/tests/unit/test_edge_cases.py`
  - **작업**: 오버플로우, 언더플로우, 최대 입력 길이 등 경계값 테스트

- [ ] **T039** Performance test: UI responsiveness (<50ms)
  - **파일**: `calculator/tests/performance/test_ui_responsiveness.py`
  - **작업**: 버튼 클릭 후 디스플레이 업데이트 시간 측정
  - **목표**: <50ms

- [ ] **T040** Performance test: Memory usage (<50MB)
  - **작업**: 앱 실행 상태에서 메모리 사용량 측정
  - **목표**: <50MB

---

## Phase 3.6: Deployment

- [ ] **T041** Create PyInstaller spec file
  - **파일**: `calculator/calculator.spec`
  - **작업**: `--onefile --windowed --name "계산기"` 옵션 설정

- [ ] **T042** Build standalone executable
  - **작업**: `pyinstaller calculator.spec` 실행
  - **검증**: `dist/계산기.exe` (Windows) 또는 `dist/계산기` (macOS/Linux) 생성 확인

- [ ] **T043** Test executable on clean environment
  - **작업**: Python 미설치 환경에서 실행 파일 테스트
  - **검증**: 정상 실행, 한글 폰트 표시, 모든 기능 동작 확인

---

## Phase 3.7: Polish & Documentation

- [ ] **T044** [P] Add docstrings to all public methods
  - **파일**: `calculator/src/core/calculator.py`, `calculator/src/ui/main_window.py` 등
  - **작업**: 한글로 docstring 작성 (함수 설명, 매개변수, 반환값)

- [ ] **T045** [P] Update README.md with build instructions
  - **파일**: `calculator/README.md`
  - **작업**: 빌드 방법, 배포 방법 추가

- [ ] **T046** Run full test suite with coverage report
  - **작업**: `pytest calculator/tests/ --cov=calculator/src --cov-report=html`
  - **목표**: 80% 이상 커버리지

- [ ] **T047** Remove code duplication and refactor
  - **작업**: 중복 코드 제거, 매직 넘버 상수화, 함수 길이 최적화

---

## Dependencies (의존성 그래프)

```
Setup (T001-T004)
  ↓
Tests (T005-T015) [모두 병렬 가능]
  ↓
Enums & Data Models (T016-T020) [T016, T017, T019는 병렬 가능]
  ↓
Operations (T021-T023) [병렬 가능]
  ↓
Calculator Core (T024-T029) [순차 실행 - 같은 파일]
  ↓
UI Components (T030-T032) [T030, T031은 병렬 가능]
  ↓
MainWindow & Handlers (T033-T036) [순차 실행]
  ↓
Integration & Performance (T037-T040)
  ↓
Deployment (T041-T043)
  ↓
Polish (T044-T047) [T044, T045는 병렬 가능]
```

### Blocking Dependencies

- **T020** (CalculatorState) blocks T024-T029
- **T021-T023** (Operations) block T025
- **T018** (History) blocks T026
- **T029** (Calculator complete) blocks T033
- **T033** (MainWindow) blocks T036
- **T036** (app.py) blocks T037

---

## Parallel Execution Examples

### 병렬 실행 그룹 1: Contract Tests (T005-T010)
```bash
# 6개 테스트 파일을 동시에 작성 가능 (서로 다른 파일)
pytest calculator/tests/contract/ -v -n 6
```

### 병렬 실행 그룹 2: Data Models (T016, T017, T019)
```bash
# 3개 모델을 동시에 구현 가능
calculator/src/core/enums.py
calculator/src/core/history.py (HistoryEntry만)
calculator/src/core/memory.py
```

### 병렬 실행 그룹 3: Operations (T021-T023)
```bash
# operations.py 내 독립 함수들 - 같은 파일이지만 함수 단위로는 병렬 가능
```

---

## Notes

- **[P] 작업**: 다른 파일을 수정하므로 병렬 실행 가능
- **순차 작업**: 같은 파일을 수정하므로 순서대로 실행
- **TDD 필수**: T005-T015 테스트가 실패하는 것을 확인한 후 T016부터 구현 시작
- **커밋 전략**: 각 작업 완료 후 개별 커밋 (테스트 통과 확인 후)
- **한글 지원**: 모든 UI 레이블, 에러 메시지, docstring을 한글로 작성

---

## Validation Checklist (최종 검증)
*모든 작업 완료 후 확인*

- [ ] 모든 contract tests 통과 (T005-T010)
- [ ] 모든 integration tests 통과 (T011-T015, T037)
- [ ] 모든 엔티티 구현 완료 (CalculatorState, MemoryState, History 등)
- [ ] 윈도우 계산기와 동일한 기능 동작 확인
- [ ] 한글 UI 정상 표시 (맑은 고딕 폰트)
- [ ] 성능 목표 달성 (UI <50ms, 메모리 <50MB)
- [ ] 단일 실행 파일 빌드 성공
- [ ] Python 미설치 환경에서 실행 확인
- [ ] 테스트 커버리지 80% 이상

---

**총 작업 수**: 47개
**예상 소요 시간**:
- Setup: 1시간
- Tests: 4-6시간
- Core: 8-10시간
- UI: 6-8시간
- Integration: 2-3시간
- Deployment: 1-2시간
- Polish: 2-3시간

**Total**: 24-33시간

---

*이 tasks.md는 `/implement` 명령어 또는 수동 구현을 위해 즉시 실행 가능합니다.*
