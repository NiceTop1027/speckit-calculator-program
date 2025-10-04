"""
Contract test for Calculator clear methods
계산기 지우기 기능 계약 테스트
"""
import pytest


class TestCalculatorClear:
    """Calculator clear/backspace 메서드 계약 테스트"""

    def test_clear_current_input(self):
        """현재 입력 지우기 (C 버튼) 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('2')
        calc.input_digit('3')
        result = calc.clear()
        assert result == "0"

    def test_clear_keeps_operation(self):
        """C 버튼은 대기 중인 연산 유지 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_operation(OperationType.ADD)
        calc.input_digit('9')
        calc.input_digit('9')
        calc.clear()  # 99 지우기

        calc.input_digit('3')
        result = calc.calculate()
        assert result == "8"  # 5 + 3 = 8 (연산은 유지됨)

    def test_clear_all_resets_everything(self):
        """전체 지우기 (CE 버튼) 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_operation(OperationType.ADD)
        calc.input_digit('3')
        result = calc.clear_all()
        assert result == "0"

        # 연산도 지워져서 새로 시작
        calc.input_digit('7')
        result = calc.calculate()
        assert result == "7"  # 연산 없이 7만 표시

    def test_clear_all_keeps_memory(self):
        """CE 버튼은 메모리 유지 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('4')
        calc.input_digit('2')
        calc.memory_store()  # 메모리에 42 저장

        calc.input_digit('1')
        calc.input_digit('0')
        calc.clear_all()  # 전체 지우기

        result = calc.memory_recall()
        assert result == "42"  # 메모리는 유지됨

    def test_backspace_removes_last_digit(self):
        """백스페이스 (← 버튼) 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('2')
        calc.input_digit('3')
        result = calc.backspace()
        assert result == "12"

    def test_backspace_multiple_times(self):
        """연속 백스페이스 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('5')
        calc.input_digit('6')
        calc.input_digit('7')
        calc.backspace()
        result = calc.backspace()
        assert result == "5"

    def test_backspace_to_empty(self):
        """백스페이스로 전부 지우면 0 표시 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('5')
        calc.backspace()
        result = calc.get_display()
        assert result == "0"

    def test_backspace_on_zero_does_nothing(self):
        """0에서 백스페이스는 무시 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        result = calc.backspace()
        assert result == "0"

    def test_backspace_removes_decimal_point(self):
        """소수점 백스페이스 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('3')
        calc.input_digit('.')
        calc.input_digit('1')
        calc.input_digit('4')
        calc.backspace()  # 4 제거 → 3.1
        result = calc.backspace()  # 1 제거 → 3.
        assert result == "3."

        result = calc.backspace()  # . 제거 → 3
        assert result == "3"

    def test_backspace_after_calculation(self):
        """계산 결과에서 백스페이스 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_operation(OperationType.ADD)
        calc.input_digit('3')
        calc.calculate()  # 8

        result = calc.backspace()
        assert result == "0"  # 계산 결과는 백스페이스로 한 번에 지워짐

    def test_clear_after_error(self):
        """에러 후 clear 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('1')
        calc.input_operation(OperationType.DIVIDE)
        calc.input_digit('0')

        try:
            calc.calculate()  # 0으로 나누기 에러
        except ZeroDivisionError:
            pass

        result = calc.clear_all()
        assert result == "0"  # 에러 상태 초기화
