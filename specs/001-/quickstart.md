# Quickstart: 만능 계산기 프로그램

**Date**: 2025-10-04
**목적**: 사용자 시나리오 기반 통합 테스트 가이드

## 개요

이 문서는 윈도우 계산기 클론의 주요 사용 시나리오를 검증하는 단계별 테스트 계획입니다. 각 시나리오는 기능 요구사항과 매핑되며, 구현 완료 후 수동 또는 자동화 테스트로 실행됩니다.

---

## 시나리오 1: 기본 사칙연산

**User Story**: 사용자가 두 숫자를 더하고 결과를 확인한다.

### 단계

1. **앱 실행**
   ```bash
   python src/app.py
   ```
   - **예상 결과**: 윈도우가 열리고 디스플레이에 "0" 표시

2. **숫자 입력**: `5` 버튼 클릭
   - **예상 결과**: 디스플레이에 "5" 표시

3. **연산자 입력**: `+` 버튼 클릭
   - **예상 결과**: 디스플레이는 "5" 유지, 내부적으로 + 연산 대기

4. **두 번째 숫자 입력**: `3` 버튼 클릭
   - **예상 결과**: 디스플레이에 "3" 표시

5. **계산 실행**: `=` 버튼 클릭
   - **예상 결과**: 디스플레이에 "8" 표시

6. **히스토리 확인** (선택사항)
   - **예상 결과**: 히스토리에 "5 + 3 = 8" 기록됨

### 검증 포인트

- ✅ FR-001: 기본 사칙연산 수행
- ✅ FR-003: 계산 결과 정확 표시
- ✅ FR-004: 즉시 결과 확인 가능

### 자동화 테스트

```python
def test_basic_addition():
    calc = Calculator()
    calc.input_digit('5')
    calc.input_operation(OperationType.ADD)
    calc.input_digit('3')
    result = calc.calculate()
    assert result == "8"
```

---

## 시나리오 2: 0으로 나누기 에러 처리

**User Story**: 사용자가 숫자를 0으로 나누려 할 때 명확한 에러 메시지를 받는다.

### 단계

1. **앱 실행 및 숫자 입력**: `1` `0` 버튼 클릭
   - **예상 결과**: 디스플레이에 "10" 표시

2. **나누기 연산**: `÷` 버튼 클릭
   - **예상 결과**: 디스플레이 "10" 유지

3. **0 입력**: `0` 버튼 클릭
   - **예상 결과**: 디스플레이에 "0" 표시

4. **계산 실행**: `=` 버튼 클릭
   - **예상 결과**: 디스플레이에 "0으로 나눌 수 없습니다" 에러 메시지 표시
   - **예상 결과**: 2초 후 디스플레이가 "10"으로 복원

### 검증 포인트

- ✅ FR-002: 0으로 나누기 시 명확한 오류 메시지
- ✅ FR-005: 잘못된 입력에 대한 적절한 피드백

### 자동화 테스트

```python
def test_division_by_zero():
    calc = Calculator()
    calc.input_digit('1')
    calc.input_digit('0')
    calc.input_operation(OperationType.DIVIDE)
    calc.input_digit('0')

    with pytest.raises(ZeroDivisionError, match="0으로 나눌 수 없습니다"):
        calc.calculate()
```

---

## 시나리오 3: 연속 계산

**User Story**: 사용자가 이전 결과를 활용하여 연속으로 계산을 수행한다.

### 단계

1. **첫 번째 계산**: `5` `+` `3` `=`
   - **예상 결과**: 디스플레이에 "8" 표시

2. **연산자 즉시 입력**: `×` 버튼 클릭
   - **예상 결과**: 이전 결과 "8"을 첫 번째 피연산자로 사용

3. **두 번째 피연산자**: `2` 버튼 클릭
   - **예상 결과**: 디스플레이에 "2" 표시

4. **계산 실행**: `=` 버튼 클릭
   - **예상 결과**: 디스플레이에 "16" 표시 (8 × 2)

### 검증 포인트

- ✅ Acceptance Scenario 2: 연속 계산 수행

### 자동화 테스트

```python
def test_chained_calculation():
    calc = Calculator()
    calc.input_digit('5')
    calc.input_operation(OperationType.ADD)
    calc.input_digit('3')
    calc.calculate()  # 8

    calc.input_operation(OperationType.MULTIPLY)
    calc.input_digit('2')
    result = calc.calculate()
    assert result == "16"
```

---

## 시나리오 4: 메모리 기능

**User Story**: 사용자가 계산 결과를 메모리에 저장하고 나중에 불러온다.

### 단계

1. **계산**: `2` `5` `=`
   - **예상 결과**: 디스플레이에 "25" 표시

2. **메모리 저장**: `MS` 버튼 클릭
   - **예상 결과**: 메모리에 25 저장, MR 버튼 활성화

3. **새 계산**: `1` `0` `0` 입력
   - **예상 결과**: 디스플레이에 "100" 표시

4. **메모리 더하기**: `M+` 버튼 클릭
   - **예상 결과**: 메모리 = 25 + 100 = 125

5. **전체 지우기**: `CE` 버튼 클릭
   - **예상 결과**: 디스플레이 "0", 메모리는 유지

6. **메모리 불러오기**: `MR` 버튼 클릭
   - **예상 결과**: 디스플레이에 "125" 표시

7. **메모리 지우기**: `MC` 버튼 클릭
   - **예상 결과**: 메모리 = 0, MR 버튼 비활성화

### 검증 포인트

- ✅ FR-010: 메모리 기능 (MS, MR, M+, M-, MC)

### 자동화 테스트

```python
def test_memory_operations():
    calc = Calculator()
    calc.input_digit('2')
    calc.input_digit('5')
    calc.memory_store()

    calc.clear_all()
    calc.input_digit('1')
    calc.input_digit('0')
    calc.input_digit('0')
    calc.memory_add()

    calc.clear_all()
    result = calc.memory_recall()
    assert result == "125"

    calc.memory_clear()
    assert calc.memory_state.is_empty is True
```

---

## 시나리오 5: 공학용 모드 - 삼각함수

**User Story**: 사용자가 공학용 모드로 전환하여 삼각함수를 계산한다.

### 단계

1. **모드 전환**: 메뉴에서 "공학용" 선택
   - **예상 결과**: 윈도우가 확장되고 삼각함수 버튼 표시

2. **각도 확인**: 각도 모드가 "도"로 설정되어 있는지 확인
   - **예상 결과**: 각도/라디안 토글이 "도" 표시

3. **입력**: `3` `0` 버튼 클릭
   - **예상 결과**: 디스플레이에 "30" 표시

4. **sin 계산**: `sin` 버튼 클릭
   - **예상 결과**: 디스플레이에 "0.5" 표시 (sin(30°) = 0.5)

5. **라디안 모드 전환**: 각도/라디안 토글 클릭
   - **예상 결과**: 모드가 "라디안"으로 변경

6. **π 입력**: `π` 버튼 클릭
   - **예상 결과**: 디스플레이에 "3.141592653589793" 표시

7. **2로 나누기**: `÷` `2` `=`
   - **예상 결과**: 디스플레이에 "1.5707963267948966" 표시 (π/2)

8. **sin 계산**: `sin` 버튼 클릭
   - **예상 결과**: 디스플레이에 "1" 표시 (sin(π/2) = 1)

### 검증 포인트

- ✅ FR-006: 공학용 함수 (삼각함수, 로그, 지수)
- ✅ 각도/라디안 모드 전환

### 자동화 테스트

```python
import math

def test_trigonometric_functions():
    calc = Calculator()
    calc.set_mode(CalculatorMode.SCIENTIFIC)
    calc.set_angle_mode(AngleMode.DEGREES)

    calc.input_digit('3')
    calc.input_digit('0')
    result = calc.input_operation(OperationType.SIN)

    # sin(30°) = 0.5
    assert abs(float(result) - 0.5) < 1e-10
```

---

## 시나리오 6: 제곱근과 음수 입력 에러

**User Story**: 사용자가 음수의 제곱근을 시도할 때 에러 메시지를 받는다.

### 단계

1. **음수 입력**: `9` 버튼 클릭, `+/-` 버튼 클릭
   - **예상 결과**: 디스플레이에 "-9" 표시

2. **제곱근 시도**: `√` 버튼 클릭
   - **예상 결과**: 디스플레이에 "잘못된 입력입니다" 에러 메시지
   - **예상 결과**: 2초 후 "-9"로 복원

### 검증 포인트

- ✅ Edge Case: 음수의 제곱근 처리
- ✅ FR-005: 잘못된 입력에 대한 피드백

### 자동화 테스트

```python
def test_sqrt_negative_number():
    calc = Calculator()
    calc.input_digit('9')
    calc.input_operation(OperationType.NEGATE)  # -9

    with pytest.raises(ValueError, match="잘못된 입력입니다"):
        calc.input_operation(OperationType.SQRT)
```

---

## 시나리오 7: 오버플로우 처리

**User Story**: 사용자가 매우 큰 숫자를 계산하여 오버플로우가 발생한다.

### 단계

1. **큰 숫자 입력**: `9` 버튼을 30번 클릭
   - **예상 결과**: 디스플레이에 "999999999999999999999999999999" 표시

2. **제곱 계산**: `x²` 버튼 클릭
   - **예상 결과**: 디스플레이에 "오버플로" 에러 메시지
   - **예상 결과**: 상태 초기화 (디스플레이 "0")

### 검증 포인트

- ✅ Edge Case: 오버플로우 처리
- ✅ FR-005: 에러 피드백

### 자동화 테스트

```python
def test_overflow():
    calc = Calculator()
    large_number = "9" * 30
    for digit in large_number:
        calc.input_digit(digit)

    with pytest.raises(OverflowError, match="계산 결과가 너무 큽니다"):
        calc.input_operation(OperationType.SQUARE)
```

---

## 시나리오 8: 백스페이스 기능

**User Story**: 사용자가 잘못 입력한 숫자를 백스페이스로 수정한다.

### 단계

1. **숫자 입력**: `1` `2` `3` `4` 버튼 클릭
   - **예상 결과**: 디스플레이에 "1234" 표시

2. **실수 발견**: 마지막 두 자리가 잘못됨

3. **백스페이스**: `←` 버튼을 2번 클릭
   - **예상 결과**: 디스플레이에 "12" 표시

4. **수정 입력**: `5` 버튼 클릭
   - **예상 결과**: 디스플레이에 "125" 표시

### 검증 포인트

- ✅ Backspace 기능

### 자동화 테스트

```python
def test_backspace():
    calc = Calculator()
    calc.input_digit('1')
    calc.input_digit('2')
    calc.input_digit('3')
    calc.input_digit('4')

    calc.backspace()
    calc.backspace()
    result = calc.get_display()
    assert result == "12"
```

---

## 시나리오 9: 괄호 계산 (공학용 모드)

**User Story**: 사용자가 복잡한 수식을 괄호로 그룹핑하여 계산한다.

### 단계

1. **모드**: 공학용 모드

2. **입력**: `(` `5` `+` `3` `)` `×` `2` `=`
   - **예상 결과**: (5 + 3) × 2 = 16

### 검증 포인트

- ✅ FR-009: 괄호 사용, 연산자 우선순위

### 자동화 테스트

```python
def test_parentheses_calculation():
    calc = Calculator()
    calc.set_mode(CalculatorMode.SCIENTIFIC)

    # (5 + 3) × 2
    calc.input_operation(OperationType.LEFT_PAREN)
    calc.input_digit('5')
    calc.input_operation(OperationType.ADD)
    calc.input_digit('3')
    calc.input_operation(OperationType.RIGHT_PAREN)
    calc.input_operation(OperationType.MULTIPLY)
    calc.input_digit('2')
    result = calc.calculate()

    assert result == "16"
```

---

## 시나리오 10: 히스토리 조회 및 삭제

**User Story**: 사용자가 여러 계산을 수행한 후 히스토리를 확인하고 삭제한다.

### 단계

1. **여러 계산 수행**:
   - `2` `+` `2` `=` → "4"
   - `5` `×` `3` `=` → "15"
   - `1` `0` `÷` `2` `=` → "5"

2. **히스토리 패널 열기**: "보기" 메뉴 → "기록"
   - **예상 결과**: 히스토리 패널에 다음 항목 표시:
     ```
     10 ÷ 2 = 5
     5 × 3 = 15
     2 + 2 = 4
     ```

3. **히스토리 항목 클릭**: "5 × 3 = 15" 클릭
   - **예상 결과**: 디스플레이에 "15" 표시

4. **히스토리 삭제**: "기록 지우기" 버튼 클릭
   - **예상 결과**: 히스토리 패널이 비어있음

### 검증 포인트

- ✅ FR-007: 계산 히스토리 (세션 내 임시 저장)
- ✅ Acceptance Scenario 3: 히스토리 조회

### 자동화 테스트

```python
def test_calculation_history():
    calc = Calculator()

    # 계산 1
    calc.input_digit('2')
    calc.input_operation(OperationType.ADD)
    calc.input_digit('2')
    calc.calculate()

    # 계산 2
    calc.input_digit('5')
    calc.input_operation(OperationType.MULTIPLY)
    calc.input_digit('3')
    calc.calculate()

    history = calc.get_history()
    assert len(history) == 2
    assert history[0].expression == "2 + 2"
    assert history[0].result == Decimal('4')
    assert history[1].expression == "5 × 3"
    assert history[1].result == Decimal('15')

    calc.clear_history()
    assert len(calc.get_history()) == 0
```

---

## 성능 검증

### UI 응답성 테스트

**목표**: 버튼 클릭 후 디스플레이 업데이트까지 <50ms

**측정 방법**:
```python
import time

def test_ui_responsiveness():
    calc = Calculator()
    window = MainWindow(calc)

    start = time.perf_counter()
    window.handle_digit_click('5')
    end = time.perf_counter()

    elapsed_ms = (end - start) * 1000
    assert elapsed_ms < 50, f"UI response time {elapsed_ms}ms exceeds 50ms"
```

### 계산 정밀도 테스트

**목표**: 15자리 이상 유효숫자

**테스트**:
```python
def test_precision():
    calc = Calculator()
    calc.input_digit('0')
    calc.input_digit('.')
    calc.input_digit('1')
    calc.input_operation(OperationType.ADD)
    calc.input_digit('0')
    calc.input_digit('.')
    calc.input_digit('2')
    result = calc.calculate()

    # 부동소수점 오차 없이 정확히 0.3
    assert result == "0.3"
```

### 메모리 사용량 테스트

**목표**: <50MB

**측정 방법**:
```bash
# Windows
tasklist /fi "imagename eq 계산기.exe" /fo csv

# Linux/macOS
ps aux | grep calculator
```

---

## 실행 체크리스트

구현 완료 후 다음 체크리스트를 수행하여 모든 시나리오가 정상 동작하는지 확인:

- [ ] 시나리오 1: 기본 사칙연산
- [ ] 시나리오 2: 0으로 나누기 에러
- [ ] 시나리오 3: 연속 계산
- [ ] 시나리오 4: 메모리 기능
- [ ] 시나리오 5: 공학용 삼각함수
- [ ] 시나리오 6: 음수 제곱근 에러
- [ ] 시나리오 7: 오버플로우 처리
- [ ] 시나리오 8: 백스페이스
- [ ] 시나리오 9: 괄호 계산
- [ ] 시나리오 10: 히스토리 기능
- [ ] 성능: UI 응답성 <50ms
- [ ] 성능: 메모리 <50MB
- [ ] 정밀도: Decimal 15자리 이상

---

## 배포 테스트

### 단일 실행 파일 생성

```bash
pyinstaller --onefile --windowed --name "계산기" src/app.py
```

### 배포 파일 검증

1. **실행**: `dist/계산기.exe` 더블클릭
2. **크기 확인**: 실행 파일 크기 < 20MB
3. **의존성 확인**: Python 미설치 환경에서 실행 가능
4. **한글 폰트**: "맑은 고딕" 정상 표시

---

## 회귀 테스트

모든 자동화 테스트를 실행하여 회귀 없음을 확인:

```bash
pytest tests/ --cov=src --cov-report=html
```

**목표 커버리지**: 80% 이상
