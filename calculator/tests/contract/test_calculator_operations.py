"""
Contract test for Calculator.input_operation() method
계산기 연산자 입력 기능 계약 테스트
"""
import pytest
from decimal import Decimal


class TestCalculatorOperations:
    """Calculator.input_operation() 계약 테스트"""

    def test_add_operation(self):
        """더하기 연산자 입력 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        result = calc.input_operation(OperationType.ADD)
        assert result == "5"  # 디스플레이는 유지

    def test_subtract_operation(self):
        """빼기 연산자 입력 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('0')
        result = calc.input_operation(OperationType.SUBTRACT)
        assert result == "10"

    def test_multiply_operation(self):
        """곱하기 연산자 입력 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('7')
        result = calc.input_operation(OperationType.MULTIPLY)
        assert result == "7"

    def test_divide_operation(self):
        """나누기 연산자 입력 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('8')
        result = calc.input_operation(OperationType.DIVIDE)
        assert result == "8"

    def test_sqrt_unary_operation(self):
        """제곱근 단항 연산 즉시 실행 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('6')
        result = calc.input_operation(OperationType.SQRT)
        assert result == "4"  # √16 = 4

    def test_square_unary_operation(self):
        """제곱 단항 연산 즉시 실행 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        result = calc.input_operation(OperationType.SQUARE)
        assert result == "25"  # 5² = 25

    def test_reciprocal_unary_operation(self):
        """역수 단항 연산 즉시 실행 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('4')
        result = calc.input_operation(OperationType.RECIPROCAL)
        assert result == "0.25"  # 1/4 = 0.25

    def test_percent_operation(self):
        """백분율 연산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_digit('0')
        result = calc.input_operation(OperationType.PERCENT)
        assert result == "0.5"  # 50% = 0.5

    def test_negate_operation(self):
        """부호 변경 연산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        result = calc.input_operation(OperationType.NEGATE)
        assert result == "-5"

        # 다시 부호 변경
        result = calc.input_operation(OperationType.NEGATE)
        assert result == "5"

    def test_sin_operation_degrees(self):
        """sin 연산 테스트 (도 모드)"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType, AngleMode

        calc = Calculator()
        calc.set_angle_mode(AngleMode.DEGREES)
        calc.input_digit('3')
        calc.input_digit('0')
        result = calc.input_operation(OperationType.SIN)
        # sin(30°) = 0.5
        assert abs(float(result) - 0.5) < 1e-10

    def test_cos_operation_degrees(self):
        """cos 연산 테스트 (도 모드)"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType, AngleMode

        calc = Calculator()
        calc.set_angle_mode(AngleMode.DEGREES)
        calc.input_digit('6')
        calc.input_digit('0')
        result = calc.input_operation(OperationType.COS)
        # cos(60°) = 0.5
        assert abs(float(result) - 0.5) < 1e-10

    def test_tan_operation_degrees(self):
        """tan 연산 테스트 (도 모드)"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType, AngleMode

        calc = Calculator()
        calc.set_angle_mode(AngleMode.DEGREES)
        calc.input_digit('4')
        calc.input_digit('5')
        result = calc.input_operation(OperationType.TAN)
        # tan(45°) = 1
        assert abs(float(result) - 1.0) < 1e-10

    def test_log_operation(self):
        """log (log10) 연산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('0')
        calc.input_digit('0')
        result = calc.input_operation(OperationType.LOG)
        # log10(100) = 2
        assert abs(float(result) - 2.0) < 1e-10

    def test_ln_operation(self):
        """ln (자연로그) 연산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('1')
        result = calc.input_operation(OperationType.LN)
        # ln(1) = 0
        assert abs(float(result) - 0.0) < 1e-10

    def test_exp_operation(self):
        """eˣ 연산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('0')
        result = calc.input_operation(OperationType.EXP)
        # e⁰ = 1
        assert abs(float(result) - 1.0) < 1e-10

    def test_power10_operation(self):
        """10ˣ 연산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('3')
        result = calc.input_operation(OperationType.POWER10)
        # 10³ = 1000
        assert result == "1000"

    def test_factorial_operation(self):
        """팩토리얼 연산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        result = calc.input_operation(OperationType.FACTORIAL)
        # 5! = 120
        assert result == "120"

    def test_chained_operations(self):
        """연속 연산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_operation(OperationType.ADD)
        calc.input_digit('3')
        # 두 번째 연산자 입력 시 이전 연산 실행
        result = calc.input_operation(OperationType.MULTIPLY)
        assert result == "8"  # 5 + 3 = 8, 이제 8 × 대기
