"""
Contract test for Calculator.input_digit() method
계산기 숫자 입력 기능 계약 테스트
"""
import pytest
from decimal import Decimal


class TestCalculatorInputDigit:
    """Calculator.input_digit() 계약 테스트"""

    def test_input_single_digit(self):
        """단일 숫자 입력 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        result = calc.input_digit('5')
        assert result == "5"

    def test_input_multiple_digits(self):
        """여러 숫자 연속 입력 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('2')
        result = calc.input_digit('3')
        assert result == "123"

    def test_input_decimal_point(self):
        """소수점 입력 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('5')
        calc.input_digit('.')
        result = calc.input_digit('3')
        assert result == "5.3"

    def test_input_decimal_point_duplicate_ignored(self):
        """소수점 중복 입력 무시 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('5')
        calc.input_digit('.')
        calc.input_digit('3')
        calc.input_digit('.')  # 두 번째 소수점은 무시되어야 함
        result = calc.input_digit('4')
        assert result == "5.34"

    def test_input_leading_zero(self):
        """앞자리 0 처리 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        result = calc.input_digit('0')
        assert result == "0"

    def test_input_zero_then_digit(self):
        """0 다음 숫자 입력 시 0 대체 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('0')
        result = calc.input_digit('5')
        assert result == "5"  # 0이 5로 대체되어야 함

    def test_input_decimal_after_zero(self):
        """0 다음 소수점 입력 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('0')
        calc.input_digit('.')
        result = calc.input_digit('5')
        assert result == "0.5"

    def test_input_max_length_32_chars(self):
        """최대 32자 제한 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        # 32자 입력
        for i in range(32):
            calc.input_digit('9')

        result = calc.input_digit('9')  # 33번째 입력은 무시되어야 함
        assert len(result) == 32

    def test_input_invalid_character_ignored(self):
        """잘못된 문자 입력 무시 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('5')
        calc.input_digit('a')  # 문자는 무시되어야 함
        result = calc.input_digit('3')
        assert result == "53"

    def test_input_after_calculation(self):
        """계산 후 새 숫자 입력 시 초기화 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_operation(OperationType.ADD)
        calc.input_digit('3')
        calc.calculate()  # 결과: 8

        # 새 숫자 입력 시 이전 결과 대체
        result = calc.input_digit('9')
        assert result == "9"
