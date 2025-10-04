# Calculator Core Interface Contract

**Version**: 1.0.0
**Date**: 2025-10-04

## Overview

계산기 핵심 로직의 공개 인터페이스. UI 레이어는 이 인터페이스를 통해서만 계산 로직과 통신합니다.

## Interface: Calculator

### Methods

#### `input_digit(digit: str) -> str`

숫자 버튼 입력 처리.

**Parameters**:
- `digit: str` - 입력된 숫자 ('0'-'9', '.')

**Returns**:
- `str` - 업데이트된 디스플레이 텍스트

**Preconditions**:
- `digit`는 '0'-'9' 또는 '.' 중 하나
- 소수점은 한 번만 입력 가능

**Postconditions**:
- 현재 입력 버퍼에 숫자 추가
- 디스플레이 텍스트 반환 (최대 32자)

**Errors**:
- None (잘못된 입력은 무시)

**Example**:
```python
calc = Calculator()
result = calc.input_digit('5')  # "5"
result = calc.input_digit('.')  # "5."
result = calc.input_digit('3')  # "5.3"
```

---

#### `input_operation(operation: OperationType) -> str`

연산자 버튼 입력 처리.

**Parameters**:
- `operation: OperationType` - 연산자 종류

**Returns**:
- `str` - 업데이트된 디스플레이 텍스트

**Preconditions**:
- `operation`은 유효한 OperationType enum 값

**Postconditions**:
- 이항 연산자 (+, -, *, /)의 경우 대기 상태로 전환
- 단항 연산자 (√, x², 1/x)의 경우 즉시 계산하여 결과 표시

**Errors**:
- `ValueError`: 잘못된 입력 (예: 음수의 제곱근)
- `ZeroDivisionError`: 0으로 나누기 또는 0의 역수
- `OverflowError`: 계산 결과가 표현 범위 초과

**Example**:
```python
calc.input_digit('5')
calc.input_operation(OperationType.ADD)
calc.input_digit('3')
calc.calculate()  # "8"

calc.input_digit('1')
calc.input_digit('6')
calc.input_operation(OperationType.SQRT)  # "4"
```

---

#### `calculate() -> str`

'=' 버튼 입력 처리 (계산 실행).

**Parameters**: None

**Returns**:
- `str` - 계산 결과 디스플레이 텍스트

**Preconditions**:
- 대기 중인 연산이 있어야 함

**Postconditions**:
- 대기 중인 연산 실행
- 결과를 current_value에 저장
- 히스토리에 계산 추가
- 연산 상태 초기화

**Errors**:
- `ValueError`: 잘못된 계산 상태
- `ZeroDivisionError`: 0으로 나누기
- `OverflowError`: 결과 오버플로우

**Example**:
```python
calc.input_digit('1')
calc.input_digit('0')
calc.input_operation(OperationType.DIVIDE)
calc.input_digit('2')
calc.calculate()  # "5"
```

---

#### `clear() -> str`

'C' 버튼 (현재 입력 지우기).

**Parameters**: None

**Returns**:
- `str` - "0" (초기 디스플레이)

**Postconditions**:
- 현재 입력만 지움
- 대기 중인 연산은 유지

**Example**:
```python
calc.input_digit('5')
calc.input_operation(OperationType.ADD)
calc.input_digit('9')
calc.input_digit('9')
calc.clear()  # "0" (but + operation is still waiting)
calc.input_digit('3')
calc.calculate()  # "8"
```

---

#### `clear_all() -> str`

'CE' 버튼 (전체 지우기).

**Parameters**: None

**Returns**:
- `str` - "0"

**Postconditions**:
- 모든 상태 초기화
- 대기 연산, 이전 값 모두 제거
- 메모리와 히스토리는 유지

**Example**:
```python
calc.input_digit('5')
calc.input_operation(OperationType.ADD)
calc.clear_all()  # "0" (operation cleared)
```

---

#### `backspace() -> str`

'←' 버튼 (마지막 자리 삭제).

**Parameters**: None

**Returns**:
- `str` - 업데이트된 디스플레이

**Postconditions**:
- 디스플레이 텍스트의 마지막 문자 제거
- 빈 문자열이 되면 "0"으로 설정

**Example**:
```python
calc.input_digit('1')
calc.input_digit('2')
calc.input_digit('3')
calc.backspace()  # "12"
calc.backspace()  # "1"
calc.backspace()  # "0"
```

---

### Memory Operations

#### `memory_clear() -> None`

메모리 지우기 (MC).

**Postconditions**:
- 메모리 값 = 0
- `is_empty = True`

---

#### `memory_recall() -> str`

메모리 불러오기 (MR).

**Returns**:
- `str` - 메모리에 저장된 값

**Preconditions**:
- `is_empty == False`

**Postconditions**:
- 메모리 값을 현재 디스플레이에 표시

---

#### `memory_add() -> None`

메모리에 더하기 (M+).

**Postconditions**:
- `memory += current_value`
- `is_empty = False`

**Errors**:
- `OverflowError`: 메모리 값 오버플로우

---

#### `memory_subtract() -> None`

메모리에서 빼기 (M-).

**Postconditions**:
- `memory -= current_value`
- `is_empty = False`

---

#### `memory_store() -> None`

메모리 저장 (MS).

**Postconditions**:
- `memory = current_value`
- `is_empty = False`

---

### Mode & Settings

#### `set_mode(mode: CalculatorMode) -> None`

계산기 모드 변경.

**Parameters**:
- `mode: CalculatorMode` - 표준 또는 공학용

**Postconditions**:
- 현재 모드 변경
- UI는 모드에 맞는 버튼 표시

---

#### `set_angle_mode(angle_mode: AngleMode) -> None`

각도 단위 변경 (공학용 모드에서만).

**Parameters**:
- `angle_mode: AngleMode` - 도 또는 라디안

**Preconditions**:
- `current_mode == CalculatorMode.SCIENTIFIC`

**Postconditions**:
- 삼각함수 계산 시 지정된 단위 사용

---

### History

#### `get_history() -> List[HistoryEntry]`

계산 히스토리 조회.

**Returns**:
- `List[HistoryEntry]` - 최근 계산 목록 (최대 100개)

**Example**:
```python
history = calc.get_history()
for entry in history:
    print(f"{entry.expression} = {entry.result}")
```

---

#### `clear_history() -> None`

히스토리 전체 삭제.

**Postconditions**:
- `history.entries = []`

---

## Error Handling Contract

모든 메서드는 다음 예외를 발생시킬 수 있습니다:

### `OverflowError`

**Message**: `"계산 결과가 너무 큽니다"`

**Trigger**: 결과가 ±9.99...e+9999 초과

**UI Response**: 디스플레이에 "오버플로" 표시, 상태 초기화

### `ZeroDivisionError`

**Message**: `"0으로 나눌 수 없습니다"`

**Trigger**:
- x ÷ 0
- 1/x where x = 0

**UI Response**: 디스플레이에 "0으로 나눌 수 없습니다" 표시, 상태 유지

### `ValueError`

**Message**: `"잘못된 입력입니다"`

**Trigger**:
- √x where x < 0
- n! where n < 0 또는 n이 정수가 아님
- log(x) where x ≤ 0
- tan(90°) 또는 tan(π/2)

**UI Response**: 디스플레이에 "잘못된 입력입니다" 표시, 상태 유지

## Type Signatures (Python)

```python
from typing import Protocol, List
from decimal import Decimal
from datetime import datetime

class CalculatorProtocol(Protocol):
    """계산기 핵심 인터페이스"""

    def input_digit(self, digit: str) -> str: ...
    def input_operation(self, operation: OperationType) -> str: ...
    def calculate(self) -> str: ...
    def clear(self) -> str: ...
    def clear_all(self) -> str: ...
    def backspace(self) -> str: ...

    # Memory
    def memory_clear(self) -> None: ...
    def memory_recall(self) -> str: ...
    def memory_add(self) -> None: ...
    def memory_subtract(self) -> None: ...
    def memory_store(self) -> None: ...

    # Mode
    def set_mode(self, mode: CalculatorMode) -> None: ...
    def set_angle_mode(self, angle_mode: AngleMode) -> None: ...

    # History
    def get_history(self) -> List[HistoryEntry]: ...
    def clear_history(self) -> None: ...
```

## Contract Tests

계약 테스트는 `tests/contract/test_calculator_contract.py`에 위치합니다. 모든 인터페이스 메서드의 사전조건, 사후조건, 예외 처리를 검증합니다.

**Test Coverage Required**:
- ✅ 각 메서드의 정상 동작
- ✅ 에러 조건 (오버플로우, 0으로 나누기, 잘못된 입력)
- ✅ 상태 전이 (숫자 입력 → 연산 → 계산 → 결과)
- ✅ 경계값 테스트 (최대/최소 Decimal 값)
