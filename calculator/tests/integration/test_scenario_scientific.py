"""
Integration test: Scenario 5 - Scientific Mode
통합 테스트: 시나리오 5 - 공학용 모드 삼각함수
"""
import math
from src.core.calculator import Calculator
from src.core.enums import OperationType, AngleMode, CalculatorMode


def test_scientific_trigonometry_scenario():
    """공학용 모드 삼각함수 시나리오 테스트"""
    calc = Calculator()
    calc.set_mode(CalculatorMode.SCIENTIFIC)

    # 도 모드에서 sin(30°) = 0.5
    calc.set_angle_mode(AngleMode.DEGREES)
    calc.input_digit('3')
    calc.input_digit('0')
    result = calc.input_operation(OperationType.SIN)
    assert abs(float(result) - 0.5) < 1e-10

    # 라디안 모드로 전환
    calc.set_angle_mode(AngleMode.RADIANS)

    # π 입력 (특수 상수)
    calc.input_constant('π')  # π ≈ 3.14159...

    # π ÷ 2
    calc.input_operation(OperationType.DIVIDE)
    calc.input_digit('2')
    calc.calculate()  # π/2

    # sin(π/2) = 1
    result = calc.input_operation(OperationType.SIN)
    assert abs(float(result) - 1.0) < 1e-10
