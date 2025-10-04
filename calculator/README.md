# 계산기 (윈도우 계산기 클론)

윈도우 계산기와 동일한 기능을 가진 한글 UI 데스크톱 계산기 애플리케이션입니다.

## 기능

### 표준 모드
- 기본 사칙연산 (+, -, ×, ÷)
- 백분율 (%)
- 제곱근 (√)
- 제곱 (x²)
- 역수 (1/x)
- 부호 변경 (+/-)
- 메모리 기능 (MC, MR, M+, M-, MS)

### 공학용 모드
- 삼각함수 (sin, cos, tan, asin, acos, atan)
- 쌍곡선 함수 (sinh, cosh, tanh)
- 로그 (log, ln)
- 지수 (eˣ, 10ˣ)
- 팩토리얼 (n!)
- 괄호 계산
- 상수 (π, e)
- 각도/라디안 모드 전환

## 기술 스택

- **언어**: Python 3.11+
- **GUI**: Tkinter (Python 표준 라이브러리)
- **정밀도**: Decimal (부동소수점 오차 없음)
- **테스트**: pytest, pytest-cov
- **배포**: PyInstaller (단일 실행 파일)

## 설치

### 의존성 설치

```bash
pip install -r requirements.txt
```

### 개발 환경 설정

```bash
# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

## 실행

```bash
python src/app.py
```

## 테스트

### 전체 테스트 실행

```bash
pytest
```

### 커버리지 리포트

```bash
pytest --cov=src --cov-report=html
```

### 특정 테스트만 실행

```bash
# 계약 테스트만
pytest tests/contract/

# 통합 테스트만
pytest tests/integration/

# 특정 파일
pytest tests/contract/test_calculator_input_digit.py
```

## 빌드

### 단일 실행 파일 생성

```bash
pyinstaller --onefile --windowed --name "계산기" src/app.py
```

실행 파일은 `dist/계산기.exe` (Windows) 또는 `dist/계산기` (macOS/Linux)에 생성됩니다.

### PyInstaller spec 파일 사용

```bash
pyinstaller calculator.spec
```

## 프로젝트 구조

```
calculator/
├── src/
│   ├── core/              # 계산 엔진 (비즈니스 로직)
│   │   ├── calculator.py  # 계산기 핵심 로직
│   │   ├── operations.py  # 연산자 구현
│   │   ├── memory.py      # 메모리 기능
│   │   ├── state.py       # 계산기 상태 관리
│   │   ├── history.py     # 계산 히스토리
│   │   └── enums.py       # 열거형 정의
│   ├── ui/                # GUI 인터페이스
│   │   ├── main_window.py # 메인 윈도우
│   │   ├── buttons.py     # 버튼 레이아웃
│   │   └── display.py     # 디스플레이 위젯
│   └── app.py             # 애플리케이션 진입점
├── tests/
│   ├── unit/              # 단위 테스트
│   ├── contract/          # 계약 테스트
│   ├── integration/       # 통합 테스트
│   └── performance/       # 성능 테스트
├── requirements.txt       # Python 의존성
├── pytest.ini             # pytest 설정
└── README.md              # 이 파일
```

## 성능 목표

- **UI 응답성**: 버튼 클릭 후 디스플레이 업데이트 <50ms
- **계산 정밀도**: 15자리 이상 (Decimal 32자리)
- **메모리 사용량**: <50MB
- **테스트 커버리지**: 80% 이상

## 개발 가이드

### TDD (Test-Driven Development)

이 프로젝트는 TDD 방식으로 개발됩니다:

1. 테스트를 먼저 작성
2. 테스트가 실패하는 것을 확인
3. 최소한의 코드로 테스트 통과
4. 리팩토링

### 코드 스타일

- **PEP 8** 준수
- 최대 줄 길이: 100자
- 모든 공개 메서드에 docstring 작성 (한글)

### 커밋 전략

- 각 작업(Task) 완료 후 개별 커밋
- 테스트 통과 확인 후 커밋
- 커밋 메시지 형식: `[T###] 작업 설명`

## 라이선스

MIT License

## 문의

프로젝트 관련 문의사항은 이슈로 등록해주세요.
