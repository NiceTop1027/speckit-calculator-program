"""
계산기 Enum 정의
Calculator enumerations for modes and operations
"""
from enum import Enum


class CalculatorMode(Enum):
    """계산기 모드"""
    STANDARD = "표준"
    SCIENTIFIC = "공학용"


class AngleMode(Enum):
    """각도 단위 (공학용 모드)"""
    DEGREES = "도"
    RADIANS = "라디안"


class OperationType(Enum):
    """연산자 종류"""
    # 기본 사칙연산
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "×"
    DIVIDE = "÷"

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

    # 쌍곡선 함수
    SINH = "sinh"
    COSH = "cosh"
    TANH = "tanh"

    # 공학용 기타
    LOG = "log"
    LN = "ln"
    EXP = "eˣ"
    POWER10 = "10ˣ"
    FACTORIAL = "n!"

    # 괄호
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
