"""
계산 연산자 구현
Calculator operations implementation
"""
import math
from decimal import Decimal, getcontext
from .enums import OperationType, AngleMode

# Decimal 정밀도 설정 (윈도우 계산기: 32자리)
getcontext().prec = 32

# 오버플로우 한계값
MAX_DECIMAL = Decimal('9.9999999999999999999999999999999e+9999')
MIN_DECIMAL = Decimal('-9.9999999999999999999999999999999e+9999')


def check_overflow(value: Decimal) -> Decimal:
    """오버플로우 검사"""
    if value > MAX_DECIMAL or value < MIN_DECIMAL:
        raise OverflowError("계산 결과가 너무 큽니다")
    return value


def add(a: Decimal, b: Decimal) -> Decimal:
    """덧셈"""
    return check_overflow(a + b)


def subtract(a: Decimal, b: Decimal) -> Decimal:
    """뺄셈"""
    return check_overflow(a - b)


def multiply(a: Decimal, b: Decimal) -> Decimal:
    """곱셈"""
    return check_overflow(a * b)


def divide(a: Decimal, b: Decimal) -> Decimal:
    """나눗셈"""
    if b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다")
    return check_overflow(a / b)


def square(a: Decimal) -> Decimal:
    """제곱"""
    return check_overflow(a * a)


def sqrt(a: Decimal) -> Decimal:
    """제곱근"""
    if a < 0:
        raise ValueError("잘못된 입력입니다")
    return check_overflow(Decimal(str(math.sqrt(float(a)))))


def reciprocal(a: Decimal) -> Decimal:
    """역수"""
    if a == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다")
    return check_overflow(Decimal('1') / a)


def percent(a: Decimal) -> Decimal:
    """백분율"""
    return check_overflow(a / Decimal('100'))


def negate(a: Decimal) -> Decimal:
    """부호 변경"""
    return -a


def sin_deg(a: Decimal, angle_mode: AngleMode) -> Decimal:
    """사인 (각도/라디안)"""
    angle = float(a)
    if angle_mode == AngleMode.DEGREES:
        angle = math.radians(angle)
    result = math.sin(angle)
    return Decimal(str(result))


def cos_deg(a: Decimal, angle_mode: AngleMode) -> Decimal:
    """코사인 (각도/라디안)"""
    angle = float(a)
    if angle_mode == AngleMode.DEGREES:
        angle = math.radians(angle)
    result = math.cos(angle)
    return Decimal(str(result))


def tan_deg(a: Decimal, angle_mode: AngleMode) -> Decimal:
    """탄젠트 (각도/라디안)"""
    angle = float(a)
    if angle_mode == AngleMode.DEGREES:
        angle = math.radians(angle)
        # tan(90°), tan(270°) 등 예외 처리
        if abs(angle - math.pi / 2) < 1e-10 or abs(angle - 3 * math.pi / 2) < 1e-10:
            raise ValueError("잘못된 입력입니다")
    else:
        # tan(π/2) 예외 처리
        if abs(angle - math.pi / 2) < 1e-10:
            raise ValueError("잘못된 입력입니다")
    result = math.tan(angle)
    return Decimal(str(result))


def asin_deg(a: Decimal, angle_mode: AngleMode) -> Decimal:
    """아크사인"""
    if a < -1 or a > 1:
        raise ValueError("잘못된 입력입니다")
    result = math.asin(float(a))
    if angle_mode == AngleMode.DEGREES:
        result = math.degrees(result)
    return Decimal(str(result))


def acos_deg(a: Decimal, angle_mode: AngleMode) -> Decimal:
    """아크코사인"""
    if a < -1 or a > 1:
        raise ValueError("잘못된 입력입니다")
    result = math.acos(float(a))
    if angle_mode == AngleMode.DEGREES:
        result = math.degrees(result)
    return Decimal(str(result))


def atan_deg(a: Decimal, angle_mode: AngleMode) -> Decimal:
    """아크탄젠트"""
    result = math.atan(float(a))
    if angle_mode == AngleMode.DEGREES:
        result = math.degrees(result)
    return Decimal(str(result))


def sinh_func(a: Decimal) -> Decimal:
    """쌍곡선 사인"""
    result = math.sinh(float(a))
    return check_overflow(Decimal(str(result)))


def cosh_func(a: Decimal) -> Decimal:
    """쌍곡선 코사인"""
    result = math.cosh(float(a))
    return check_overflow(Decimal(str(result)))


def tanh_func(a: Decimal) -> Decimal:
    """쌍곡선 탄젠트"""
    result = math.tanh(float(a))
    return Decimal(str(result))


def log10_func(a: Decimal) -> Decimal:
    """상용로그 (log10)"""
    if a <= 0:
        raise ValueError("잘못된 입력입니다")
    result = math.log10(float(a))
    return Decimal(str(result))


def ln_func(a: Decimal) -> Decimal:
    """자연로그 (ln)"""
    if a <= 0:
        raise ValueError("잘못된 입력입니다")
    result = math.log(float(a))
    return Decimal(str(result))


def exp_func(a: Decimal) -> Decimal:
    """eˣ"""
    try:
        result = math.exp(float(a))
        return check_overflow(Decimal(str(result)))
    except OverflowError:
        raise OverflowError("계산 결과가 너무 큽니다")


def power10_func(a: Decimal) -> Decimal:
    """10ˣ"""
    try:
        result = 10 ** float(a)
        return check_overflow(Decimal(str(result)))
    except OverflowError:
        raise OverflowError("계산 결과가 너무 큽니다")


def factorial_func(a: Decimal) -> Decimal:
    """팩토리얼"""
    # 음수나 소수는 불가
    if a < 0 or a != int(a):
        raise ValueError("잘못된 입력입니다")

    n = int(a)
    # 너무 큰 수는 오버플로우
    if n > 170:  # 170! 근처에서 float 오버플로우
        raise OverflowError("계산 결과가 너무 큽니다")

    result = math.factorial(n)
    return check_overflow(Decimal(str(result)))


# 상수
PI = Decimal(str(math.pi))
E = Decimal(str(math.e))
