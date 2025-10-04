# UI Interface Contract

**Version**: 1.0.0
**Date**: 2025-10-04

## Overview

사용자 인터페이스 컴포넌트의 공개 인터페이스. UI는 Calculator Core와 독립적으로 동작하며, 이 계약을 통해 통신합니다.

## Interface: MainWindow

### Methods

#### `__init__(calculator: CalculatorProtocol) -> None`

메인 윈도우 초기화.

**Parameters**:
- `calculator: CalculatorProtocol` - 계산기 코어 인스턴스

**Postconditions**:
- Tkinter 윈도우 생성
- 디스플레이, 버튼 레이아웃 초기화
- 이벤트 핸들러 바인딩

---

#### `run() -> None`

애플리케이션 실행.

**Postconditions**:
- Tkinter 메인 루프 시작
- 사용자 입력 대기

---

#### `update_display(text: str) -> None`

디스플레이 업데이트.

**Parameters**:
- `text: str` - 표시할 텍스트 (숫자 또는 에러 메시지)

**Postconditions**:
- 디스플레이 위젯의 텍스트 업데이트
- 텍스트가 32자 초과 시 자동 스크롤

**Example**:
```python
window.update_display("123.45")
window.update_display("오버플로")
```

---

#### `switch_mode(mode: CalculatorMode) -> None`

UI 모드 전환.

**Parameters**:
- `mode: CalculatorMode` - 표준 또는 공학용

**Postconditions**:
- 표준 모드: 기본 버튼만 표시
- 공학용 모드: 삼각함수, 로그 등 추가 버튼 표시
- 윈도우 크기 자동 조정

**Example**:
```python
window.switch_mode(CalculatorMode.SCIENTIFIC)
# 윈도우가 확장되어 sin, cos, tan 등 버튼 표시
```

---

#### `show_error(message: str) -> None`

에러 메시지 표시.

**Parameters**:
- `message: str` - 에러 메시지 ("0으로 나눌 수 없습니다", "잘못된 입력입니다" 등)

**Postconditions**:
- 디스플레이에 에러 메시지 표시
- 2초 후 자동으로 현재 값 복원

**Example**:
```python
try:
    calc.input_operation(OperationType.DIVIDE, 0)
except ZeroDivisionError as e:
    window.show_error(str(e))
```

---

## Interface: DisplayWidget

디스플레이 영역 컴포넌트.

### Properties

#### `text: str`

현재 표시 중인 텍스트.

**Getter**:
```python
current_text = display.text
```

**Setter**:
```python
display.text = "42"
```

---

### Methods

#### `format_number(value: Decimal) -> str`

숫자를 디스플레이 형식으로 변환.

**Parameters**:
- `value: Decimal` - 표시할 숫자

**Returns**:
- `str` - 포맷팅된 문자열

**Formatting Rules**:
- 정수는 천 단위 구분 쉼표: "1,234"
- 소수는 불필요한 0 제거: "3.14" (not "3.140000")
- 과학적 표기법: 절댓값이 1e10 이상 또는 1e-10 이하일 때 (예: "1.23e+12")
- 최대 15자리 유효숫자

**Example**:
```python
display.format_number(Decimal('1234.5'))  # "1,234.5"
display.format_number(Decimal('0.00000001'))  # "1e-08"
```

---

## Interface: ButtonLayout

버튼 배치 관리.

### Methods

#### `create_standard_buttons() -> None`

표준 모드 버튼 생성.

**Postconditions**:
- 숫자 버튼 (0-9)
- 연산자 버튼 (+, -, ×, ÷)
- 기능 버튼 (C, CE, ←, =)
- 메모리 버튼 (MC, MR, M+, M-, MS)
- 단항 연산 (%, √, x², 1/x, +/-)

**Layout** (5x6 그리드):
```
MC    MR    M+    M-    MS
C     CE    ←     %     √
7     8     9     ÷     x²
4     5     6     ×     1/x
1     2     3     -     +/-
0     .     =     +
```

---

#### `create_scientific_buttons() -> None`

공학용 모드 추가 버튼 생성.

**Postconditions**:
- 삼각함수 (sin, cos, tan, asin, acos, atan)
- 로그 (log, ln)
- 지수 (eˣ, 10ˣ)
- 팩토리얼 (n!)
- 상수 (π, e)
- 괄호 ( (, ) )
- 각도/라디안 토글

**Layout** (확장 영역 추가):
```
[표준 버튼 영역]    [공학용 확장 영역]
                    π     e    sin   cos
                    tan   log  ln    eˣ
                    10ˣ   n!   (     )
                    도/라디안
```

---

#### `bind_button(button_id: str, handler: Callable) -> None`

버튼 이벤트 핸들러 바인딩.

**Parameters**:
- `button_id: str` - 버튼 식별자 ("btn_0", "btn_add", 등)
- `handler: Callable` - 클릭 이벤트 핸들러

**Example**:
```python
def on_add_click():
    calc.input_operation(OperationType.ADD)
    window.update_display(calc.get_display())

layout.bind_button("btn_add", on_add_click)
```

---

## Event Handlers Contract

UI는 다음 이벤트를 처리합니다:

### Button Click Events

**Signature**: `() -> None`

**Flow**:
1. 사용자가 버튼 클릭
2. UI가 해당 핸들러 호출
3. 핸들러가 Calculator Core 메서드 호출
4. Core가 결과 문자열 반환
5. UI가 `update_display(result)` 호출

**Example**:
```python
def handle_digit_click(digit: str):
    try:
        result = calc.input_digit(digit)
        window.update_display(result)
    except Exception as e:
        window.show_error(str(e))
```

### Keyboard Events

**지원 키**:
- 숫자: `0-9`
- 연산자: `+`, `-`, `*`, `/`
- 기능: `Enter` (=), `Escape` (C), `Backspace` (←)
- 소수점: `.`

**Signature**: `(event: KeyEvent) -> None`

**Example**:
```python
def handle_key_press(event):
    key = event.char
    if key.isdigit():
        handle_digit_click(key)
    elif key == '+':
        handle_operation_click(OperationType.ADD)
    # ...
```

---

## UI State Management

### Window State

**Properties**:
- `width: int` - 윈도우 너비 (표준: 400px, 공학용: 600px)
- `height: int` - 윈도우 높이 (표준: 500px, 공학용: 600px)
- `resizable: bool = False` - 크기 조정 불가
- `title: str = "계산기"` - 윈도우 제목

### Display State

**Properties**:
- `font: str = "맑은 고딕"` - 한글 폰트
- `font_size: int` - 디스플레이: 24pt, 버튼: 12pt
- `text_align: str = "right"` - 오른쪽 정렬 (숫자 표시 관례)
- `max_length: int = 32` - 최대 표시 문자 수

### Button State

**Properties**:
- `enabled: bool` - 활성/비활성 상태
- `highlighted: bool` - 강조 표시 (연산자 대기 중)

**State Rules**:
- MR 버튼: `memory.is_empty == True`일 때 비활성
- 각도/라디안 토글: 공학용 모드에서만 활성
- 공학용 버튼: 표준 모드에서 숨김

---

## Styling Contract

### Color Scheme (윈도우 계산기 참고)

**배경**:
- 윈도우: `#F0F0F0` (연한 회색)
- 디스플레이: `#FFFFFF` (흰색)

**버튼**:
- 숫자 버튼: `#FAFAFA` (밝은 회색)
- 연산자 버튼: `#E0E0E0` (회색)
- 기능 버튼 (C, CE): `#D0D0D0` (진한 회색)
- = 버튼: `#0078D4` (파란색, 강조)

**텍스트**:
- 숫자: `#000000` (검정)
- 에러: `#C42B1C` (빨강)

### Font Sizes

- 디스플레이: 24pt
- 버튼 레이블: 12pt
- 메뉴: 10pt

---

## Accessibility

### Keyboard Navigation

- `Tab`: 버튼 간 이동
- `Enter`: 선택된 버튼 클릭
- 숫자 키패드 지원

### Screen Reader Support

- 모든 버튼에 aria-label 설정 (한글 레이블)
- 디스플레이 값 변경 시 읽어주기

---

## Type Signatures (Python)

```python
from typing import Protocol, Callable
from tkinter import Tk, Frame, Label, Button

class MainWindowProtocol(Protocol):
    """메인 윈도우 인터페이스"""

    def __init__(self, calculator: CalculatorProtocol) -> None: ...
    def run(self) -> None: ...
    def update_display(self, text: str) -> None: ...
    def switch_mode(self, mode: CalculatorMode) -> None: ...
    def show_error(self, message: str) -> None: ...

class DisplayWidgetProtocol(Protocol):
    """디스플레이 위젯 인터페이스"""

    @property
    def text(self) -> str: ...

    @text.setter
    def text(self, value: str) -> None: ...

    def format_number(self, value: Decimal) -> str: ...

class ButtonLayoutProtocol(Protocol):
    """버튼 레이아웃 인터페이스"""

    def create_standard_buttons(self) -> None: ...
    def create_scientific_buttons(self) -> None: ...
    def bind_button(self, button_id: str, handler: Callable[[], None]) -> None: ...
```

---

## Contract Tests

UI 계약 테스트는 `tests/contract/test_ui_contract.py`에 위치합니다.

**Test Strategy**:
- Mock `CalculatorProtocol` 사용
- 버튼 클릭 시뮬레이션
- 디스플레이 업데이트 검증
- 키보드 이벤트 테스트

**Example Test**:
```python
def test_digit_button_updates_display():
    calc_mock = Mock(spec=CalculatorProtocol)
    calc_mock.input_digit.return_value = "5"

    window = MainWindow(calc_mock)
    window.handle_digit_click("5")

    calc_mock.input_digit.assert_called_once_with("5")
    assert window.display.text == "5"
```
