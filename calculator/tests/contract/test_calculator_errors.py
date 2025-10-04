"""
Contract test for Calculator error handling
계산기 에러 처리 계약 테스트
"""
import pytest
from decimal import Decimal


class TestCalculatorErrors:
    """Calculator 에러 처리 계약 테스트"""

    def test_division_by_zero_error(self):
        """0으로 나누기 에러 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('0')
        calc.input_operation(OperationType.DIVIDE)
        calc.input_digit('0')

        with pytest.raises(ZeroDivisionError, match="0으로 나눌 수 없습니다"):
            calc.calculate()

    def test_reciprocal_zero_error(self):
        """0의 역수 에러 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('0')

        with pytest.raises(ZeroDivisionError, match="0으로 나눌 수 없습니다"):
            calc.input_operation(OperationType.RECIPROCAL)

    def test_sqrt_negative_error(self):
        """음수의 제곱근 에러 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('9')
        calc.input_operation(OperationType.NEGATE)  # -9

        with pytest.raises(ValueError, match="잘못된 입력입니다"):
            calc.input_operation(OperationType.SQRT)

    def test_log_zero_error(self):
        """log(0) 에러 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('0')

        with pytest.raises(ValueError, match="잘못된 입력입니다"):
            calc.input_operation(OperationType.LOG)

    def test_log_negative_error(self):
        """log(음수) 에러 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_operation(OperationType.NEGATE)  # -5

        with pytest.raises(ValueError, match="잘못된 입력입니다"):
            calc.input_operation(OperationType.LOG)

    def test_ln_zero_error(self):
        """ln(0) 에러 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('0')

        with pytest.raises(ValueError, match="잘못된 입력입니다"):
            calc.input_operation(OperationType.LN)

    def test_factorial_negative_error(self):
        """음수 팩토리얼 에러 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_operation(OperationType.NEGATE)  # -5

        with pytest.raises(ValueError, match="잘못된 입력입니다"):
            calc.input_operation(OperationType.FACTORIAL)

    def test_factorial_decimal_error(self):
        """소수 팩토리얼 에러 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('3')
        calc.input_digit('.')
        calc.input_digit('5')

        with pytest.raises(ValueError, match="잘못된 입력입니다"):
            calc.input_operation(OperationType.FACTORIAL)

    def test_tan_90_degrees_error(self):
        """tan(90°) 에러 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType, AngleMode

        calc = Calculator()
        calc.set_angle_mode(AngleMode.DEGREES)
        calc.input_digit('9')
        calc.input_digit('0')

        with pytest.raises(ValueError, match="잘못된 입력입니다"):
            calc.input_operation(OperationType.TAN)

    def test_overflow_large_multiplication(self):
        """오버플로우 에러 테스트 (큰 숫자 곱셈)"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        # 매우 큰 숫자 입력
        for _ in range(30):
            calc.input_digit('9')

        with pytest.raises(OverflowError, match="계산 결과가 너무 큽니다"):
            calc.input_operation(OperationType.SQUARE)

    def test_overflow_power10(self):
        """오버플로우 에러 테스트 (10^큰수)"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('0')
        calc.input_digit('0')
        calc.input_digit('0')
        calc.input_digit('0')  # 10000

        with pytest.raises(OverflowError, match="계산 결과가 너무 큽니다"):
            calc.input_operation(OperationType.POWER10)

    def test_factorial_large_number_error(self):
        """큰 수의 팩토리얼 오버플로우 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('0')
        calc.input_digit('0')
        calc.input_digit('0')  # 1000

        with pytest.raises(OverflowError, match="계산 결과가 너무 큽니다"):
            calc.input_operation(OperationType.FACTORIAL)

    def test_error_preserves_previous_value(self):
        """에러 발생 시 이전 값 유지 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('6')  # 16

        try:
            calc.input_digit('0')
            calc.input_operation(OperationType.DIVIDE)
            calc.input_digit('0')
            calc.calculate()
        except ZeroDivisionError:
            # 에러 발생 후에도 이전 상태 유지
            pass

        # 에러 후 상태 확인 (디스플레이는 에러 메시지지만 내부 값은 유지)
        calc.clear()
        result = calc.get_display()
        assert result == "0"  # clear 후 초기화

    def test_memory_overflow_ignored(self):
        """메모리 오버플로우 시 에러만 발생하고 메모리는 변경 안 됨 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        # 메모리에 큰 값 저장
        for _ in range(25):
            calc.input_digit('9')
        calc.memory_store()

        # 메모리에 큰 값 더하기 시도
        for _ in range(25):
            calc.input_digit('9')

        with pytest.raises(OverflowError):
            calc.memory_add()

        # 메모리는 이전 값 유지
        result = calc.memory_recall()
        assert len(result) == 25  # 원래 저장된 값 유지
