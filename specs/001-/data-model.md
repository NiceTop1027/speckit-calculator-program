# Data Model: 만능 계산기 프로그램

**Date**: 2025-10-04
**Feature**: 윈도우 계산기 클론

## Overview

계산기 애플리케이션의 핵심 데이터 구조. 데이터베이스나 영구 저장소 없이 메모리 내에서만 동작하는 상태 관리.

## Core Entities

### 1. CalculatorState

계산기의 현재 상태를 나타내는 중앙 모델.

**Attributes**:
- `current_value: Decimal` - 디스플레이에 표시되는 현재 값
- `previous_value: Decimal | None` - 이전 계산 값 (연산 대기 중일 때)
- `operation: str | None` - 대기 중인 연산자 (+, -, *, /, 등)
- `memory: Decimal` - 메모리에 저장된 값
- `mode: CalculatorMode` - 현재 모드 (표준/공학용)
- `angle_mode: AngleMode` - 각도 단위 (도/라디안, 공학용 모드에서만)
- `is_new_calculation: bool` - 새 숫자 입력 시작 여부
- `display_text: str` - 화면에 표시될 텍스트 (포맷팅된 숫자)

**Validation Rules**:
- `current_value`는 항상 유효한 Decimal 값 (NaN 불허)
- `operation`은 유효한 연산자 목록에만 존재: {'+', '-', '*', '/', 'sqrt', 'square', 'reciprocal', 'percent', ...}
- `display_text` 최대 길이: 32자 (윈도우 계산기 제한)
- 오버플로우 시 `display_text = "오버플로"`

**State Transitions**:
```
초기 상태 → 숫자 입력 → 연산자 입력 → 숫자 입력 → = → 결과 표시 → 초기 상태
         ↓                                              ↑
         └──────────────────────────────────────────────┘
                   (연속 계산 가능)
```

### 2. CalculationHistory

세션 내 계산 히스토리 관리.

**Attributes**:
- `entries: List[HistoryEntry]` - 계산 기록 목록 (최대 100개)
- `max_size: int = 100` - 최대 보관 개수

**Methods**:
- `add_entry(expression: str, result: Decimal)` - 새 계산 추가
- `clear()` - 히스토리 전체 삭제
- `get_recent(n: int)` - 최근 n개 항목 조회

**Validation Rules**:
- `entries` 크기가 `max_size` 초과 시 가장 오래된 항목 자동 삭제 (FIFO)
- 중복 항목도 별도 엔트리로 저장 (타임스탬프 다름)

### 3. HistoryEntry

개별 계산 기록.

**Attributes**:
- `expression: str` - 계산 수식 (예: "5 + 3")
- `result: Decimal` - 계산 결과 (예: Decimal('8'))
- `timestamp: datetime` - 계산 수행 시각

**Example**:
```python
HistoryEntry(
    expression="√(16)",
    result=Decimal('4'),
    timestamp=datetime(2025, 10, 4, 14, 30, 0)
)
```

### 4. MemoryState

메모리 기능 상태.

**Attributes**:
- `stored_value: Decimal` - 메모리에 저장된 값 (초기값: 0)
- `is_empty: bool` - 메모리가 비어있는지 (True면 MR 버튼 비활성)

**Methods**:
- `clear()` - MC (Memory Clear)
- `recall()` - MR (Memory Recall)
- `add(value: Decimal)` - M+ (Memory Add)
- `subtract(value: Decimal)` - M- (Memory Subtract)
- `store(value: Decimal)` - MS (Memory Store)

**Validation Rules**:
- `stored_value`는 항상 유효한 Decimal
- 오버플로우 시 메모리 값 변경 없이 에러 표시

## Enumerations

### CalculatorMode

```python
class CalculatorMode(Enum):
    STANDARD = "표준"
    SCIENTIFIC = "공학용"
```

### AngleMode

```python
class AngleMode(Enum):
    DEGREES = "도"     # 360도 체계
    RADIANS = "라디안"  # 2π 라디안 체계
```

### OperationType

```python
class OperationType(Enum):
    # 기본 사칙연산
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"

    # 단항 연산
    SQUARE = "x²"
    SQRT = "√"
    RECIPROCAL = "1/x"
    PERCENT = "%"
    NEGATE = "+/-"

    # 공학용 삼각함수
    SIN = "sin"
    COS = "cos"
    TAN = "tan"
    ASIN = "sin⁻¹"
    ACOS = "cos⁻¹"
    ATAN = "tan⁻¹"

    # 공학용 기타
    LOG = "log"
    LN = "ln"
    EXP = "eˣ"
    POWER10 = "10ˣ"
    FACTORIAL = "n!"
```

## Relationships

```
CalculatorState (1) ───> (1) MemoryState
       │
       │ (1)
       │
       ▼
       (0..1) CalculationHistory
                    │
                    │ (1)
                    │
                    ▼
                    (0..100) HistoryEntry
```

**Explanation**:
- CalculatorState는 하나의 MemoryState를 소유
- CalculatorState는 선택적으로 CalculationHistory를 가짐 (히스토리 패널 활성화 시)
- CalculationHistory는 0~100개의 HistoryEntry를 포함

## Validation & Error Handling

### Overflow Detection

```python
MAX_DECIMAL = Decimal('9.9999999999999999999999999999999e+9999')
MIN_DECIMAL = Decimal('-9.9999999999999999999999999999999e+9999')

if result > MAX_DECIMAL or result < MIN_DECIMAL:
    raise OverflowError("계산 결과가 너무 큽니다")
```

### Division by Zero

```python
if operation == OperationType.DIVIDE and current_value == 0:
    raise ZeroDivisionError("0으로 나눌 수 없습니다")
```

### Invalid Operations

```python
# 음수의 제곱근
if operation == OperationType.SQRT and value < 0:
    raise ValueError("잘못된 입력입니다")

# 음수의 팩토리얼
if operation == OperationType.FACTORIAL and (value < 0 or value != int(value)):
    raise ValueError("잘못된 입력입니다")
```

## Persistence (None)

이 애플리케이션은 영구 저장소를 사용하지 않습니다. 모든 상태는 메모리에만 존재하며 애플리케이션 종료 시 삭제됩니다.

**Rationale**:
- 개인정보 보호 (계산 내역이 디스크에 남지 않음)
- 단순성 (파일 I/O, 직렬화 불필요)
- 윈도우 계산기 동작과 일치

## Sample State Example

```python
# 사용자가 "5 + 3 =" 계산 후 상태
state = CalculatorState(
    current_value=Decimal('8'),
    previous_value=None,
    operation=None,
    memory=Decimal('0'),
    mode=CalculatorMode.STANDARD,
    angle_mode=AngleMode.DEGREES,
    is_new_calculation=True,
    display_text="8"
)

# 히스토리
history.entries = [
    HistoryEntry(
        expression="5 + 3",
        result=Decimal('8'),
        timestamp=datetime.now()
    )
]

# 메모리 (비어있음)
memory_state.stored_value = Decimal('0')
memory_state.is_empty = True
```
