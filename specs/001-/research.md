# Research: 만능 계산기 프로그램

**Date**: 2025-10-04
**Feature**: 윈도우 계산기 클론 (한글 UI)

## Research Questions Resolved

### 1. GUI 프레임워크 선택: Tkinter vs PyQt6

**Decision**: Tkinter 선택

**Rationale**:
- Python 표준 라이브러리로 추가 설치 불필요
- 윈도우 계산기 수준의 간단한 UI에 충분한 기능
- 가볍고 빠른 실행 (메모리 < 50MB 제약 충족)
- 단일 실행 파일 생성 용이 (PyInstaller 호환성 우수)
- 한글 폰트 지원 문제 없음

**Alternatives Considered**:
- **PyQt6**: 더 풍부한 UI 컴포넌트, 현대적 디자인 가능하지만 의존성 크기 증가 (100MB+), 라이선스 고려 필요 (GPL/상용)
- **Kivy**: 터치 중심, 모바일 우선 설계로 데스크톱 계산기에 과도함
- **wxPython**: 네이티브 Look&Feel이지만 Tkinter보다 복잡하고 윈도우 계산기 복제에 과도

### 2. 계산 정밀도: Decimal vs Float

**Decision**: Python `decimal.Decimal` 사용

**Rationale**:
- 부동소수점 오류 방지 (0.1 + 0.2 = 0.30000000000000004 문제 해결)
- 윈도우 계산기의 정확한 계산 결과 재현
- 15자리 이상 정밀도 요구사항 충족
- 회계/재무 계산에서도 정확성 보장

**Alternatives Considered**:
- **float**: 빠르지만 부동소수점 오차 발생, 윈도우 계산기 정확도 미달
- **fractions.Fraction**: 유리수 정확 표현 가능하지만 UI 표시 복잡, 계산기 용도에 과도

### 3. 윈도우 계산기 기능 범위

**Decision**: 표준 모드 + 공학용 모드 구현

**Features to Implement**:

**표준 모드**:
- 기본 사칙연산: +, -, ×, ÷
- 백분율 (%)
- 제곱근 (√)
- 제곱 (x²)
- 역수 (1/x)
- 부호 변경 (+/-)
- 메모리 기능: MC, MR, M+, M-, MS (Memory Store)

**공학용 모드**:
- 삼각함수: sin, cos, tan (각도/라디안 모드)
- 역삼각함수: sin⁻¹, cos⁻¹, tan⁻¹
- 쌍곡선 함수: sinh, cosh, tanh
- 로그: log, ln
- 지수: eˣ, 10ˣ
- 팩토리얼 (n!)
- 괄호 계산
- 원주율 (π), 자연상수 (e)

**Not Implemented (Out of Scope)**:
- 프로그래머 모드 (진법 변환)
- 날짜 계산
- 통계 모드
- 그래프 계산기

**Rationale**: 표준+공학용 모드가 일반 사용자의 90% 사용 사례를 커버. 추가 모드는 복잡도 대비 가치 낮음.

### 4. 계산 히스토리 기능

**Decision**: 세션 메모리에만 히스토리 유지 (영구 저장 없음)

**Rationale**:
- 윈도우 계산기 기본 동작과 일치
- 파일 I/O 불필요로 복잡도 감소
- 개인정보 보호 (계산 내역이 디스크에 남지 않음)
- 메모리 제약 준수 (<50MB)

**Implementation**:
- 세션 내 최근 100개 계산 내역 유지
- UI에서 히스토리 패널로 조회 가능
- 앱 종료 시 자동 삭제

### 5. 한글 UI 구현 방법

**Decision**: 모든 버튼 레이블과 메뉴를 한글로 번역

**Korean Labels**:
- 메모리: MC (메모리 지우기), MR (메모리 불러오기), M+ (메모리에 더하기), M- (메모리에서 빼기), MS (메모리 저장)
- 연산자: 더하기, 빼기, 곱하기, 나누기
- 기능: 지우기 (C), 전체 지우기 (CE), 백스페이스 (←)
- 모드: 표준, 공학용

**Font Selection**:
- Windows: "맑은 고딕" (Malgun Gothic)
- macOS/Linux: "Apple SD Gothic Neo" / "Noto Sans KR" fallback

**Rationale**: 윈도우 계산기의 한글 버전과 동일한 사용자 경험 제공

### 6. 배포 방식

**Decision**: PyInstaller로 단일 실행 파일 생성

**Commands**:
```bash
pyinstaller --onefile --windowed --name "계산기" src/app.py
```

**Rationale**:
- 사용자가 Python 설치 불필요
- 더블클릭으로 즉시 실행 가능
- Windows .exe, macOS .app, Linux binary 생성 가능
- 윈도우 계산기와 유사한 배포 방식

**Alternatives Considered**:
- **pip install**: 개발자 전용, 일반 사용자에게 부적합
- **cx_Freeze**: PyInstaller보다 복잡하고 커뮤니티 지원 적음

### 7. 테스팅 전략

**Decision**: pytest + unittest.mock for GUI

**Test Coverage**:
- **Unit Tests**: 계산 로직, 연산자, 메모리 함수 (core/)
- **Integration Tests**: UI 이벤트 → 계산 → 디스플레이 업데이트 플로우

**Mocking Strategy**:
- Tkinter 위젯을 mock하여 GUI 없이 로직 테스트
- 실제 윈도우 생성 없이 버튼 클릭 시뮬레이션

**Rationale**:
- TDD 가능 (테스트 먼저 작성)
- CI/CD 환경에서 헤드리스 실행 가능
- 빠른 테스트 실행 (<1초)

## Best Practices Identified

### Python Decimal 사용법
```python
from decimal import Decimal, getcontext

# 정밀도 설정 (윈도우 계산기는 32자리)
getcontext().prec = 32

# 계산 예시
a = Decimal('0.1')
b = Decimal('0.2')
result = a + b  # Decimal('0.3') - 정확함
```

### Tkinter 한글 폰트 설정
```python
import tkinter.font as tkfont

# 시스템 폰트 확인
fonts = tkfont.families()

# 한글 폰트 우선순위 선택
font_list = ['맑은 고딕', 'Apple SD Gothic Neo', 'Noto Sans KR']
selected_font = next((f for f in font_list if f in fonts), 'TkDefaultFont')
```

### MVC 패턴 적용
- **Model**: `core/calculator.py` - 계산 상태와 로직
- **View**: `ui/main_window.py`, `ui/display.py` - UI 렌더링
- **Controller**: `ui/buttons.py` - 사용자 입력 처리

이로써 계산 로직과 UI가 분리되어 테스트와 유지보수 용이

## Dependencies

```
# requirements.txt
# Python 3.11+ 표준 라이브러리만 사용
# 추가 패키지 없음 (Tkinter는 포함됨)

# Development dependencies
pytest==7.4.3
pytest-cov==4.1.0
pyinstaller==6.3.0
```

## Technical Constraints Resolved

| Constraint | Resolution |
|------------|------------|
| <50MB 메모리 | Tkinter 사용, 히스토리 100개 제한 |
| <50ms UI 응답성 | Decimal 연산은 <1ms, UI 업데이트는 동기 처리 |
| 15자리 정밀도 | Decimal with prec=32 |
| 단일 실행 파일 | PyInstaller --onefile |
| 오프라인 동작 | 모든 기능 로컬, 네트워크 불필요 |
| 윈도우 계산기 동등 | 표준+공학용 모드 완전 구현 |

## Open Questions (None)

모든 기술적 불확실성이 해결되었으며 구현 준비 완료.
