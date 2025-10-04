"""
Contract test for Calculator.calculate() method
계산기 = 버튼 기능 계약 테스트
"""
import pytest


class TestCalculatorCalculate:
    """Calculator.calculate() 계약 테스트"""

    def test_calculate_addition(self):
        """덧셈 계산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_operation(OperationType.ADD)
        calc.input_digit('3')
        result = calc.calculate()
        assert result == "8"

    def test_calculate_subtraction(self):
        """뺄셈 계산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('0')
        calc.input_operation(OperationType.SUBTRACT)
        calc.input_digit('3')
        result = calc.calculate()
        assert result == "7"

    def test_calculate_multiplication(self):
        """곱셈 계산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('6')
        calc.input_operation(OperationType.MULTIPLY)
        calc.input_digit('7')
        result = calc.calculate()
        assert result == "42"

    def test_calculate_division(self):
        """나눗셈 계산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('5')
        calc.input_operation(OperationType.DIVIDE)
        calc.input_digit('3')
        result = calc.calculate()
        assert result == "5"

    def test_calculate_decimal_result(self):
        """소수 결과 계산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('0')
        calc.input_operation(OperationType.DIVIDE)
        calc.input_digit('4')
        result = calc.calculate()
        assert result == "2.5"

    def test_calculate_adds_to_history(self):
        """계산 결과가 히스토리에 추가되는지 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_operation(OperationType.ADD)
        calc.input_digit('3')
        calc.calculate()

        history = calc.get_history()
        assert len(history) == 1
        assert history[0].expression == "5 + 3"
        assert str(history[0].result) == "8"

    def test_calculate_without_operation_returns_current(self):
        """연산자 없이 = 버튼 누르면 현재 값 반환 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('5')
        result = calc.calculate()
        assert result == "5"

    def test_calculate_resets_state(self):
        """계산 후 상태 초기화 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_operation(OperationType.ADD)
        calc.input_digit('3')
        calc.calculate()  # 8

        # 새 숫자 입력 시 이전 결과 대체
        calc.input_digit('9')
        result = calc.get_display()
        assert result == "9"

    def test_calculate_repeat_equals(self):
        """= 버튼 반복 누르기 테스트 (윈도우 계산기 동작)"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_operation(OperationType.ADD)
        calc.input_digit('3')
        calc.calculate()  # 8

        # = 다시 누르면 마지막 연산 반복 (8 + 3 = 11)
        result = calc.calculate()
        assert result == "11"

        # 한 번 더 (11 + 3 = 14)
        result = calc.calculate()
        assert result == "14"

    def test_calculate_chained(self):
        """연속 계산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_operation(OperationType.ADD)
        calc.input_digit('3')
        calc.calculate()  # 8

        calc.input_operation(OperationType.MULTIPLY)
        calc.input_digit('2')
        result = calc.calculate()
        assert result == "16"  # 8 × 2 = 16

    def test_calculate_precision(self):
        """Decimal 정밀도 테스트 (부동소수점 오차 없음)"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

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

    def test_calculate_large_numbers(self):
        """큰 숫자 계산 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        for _ in range(10):
            calc.input_digit('9')
        calc.input_operation(OperationType.MULTIPLY)
        calc.input_digit('2')
        result = calc.calculate()
        assert result == "19999999998"  # 9999999999 × 2
