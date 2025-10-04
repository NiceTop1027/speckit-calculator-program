"""
Contract test for Calculator memory operations
계산기 메모리 기능 계약 테스트
"""
import pytest


class TestCalculatorMemory:
    """Calculator 메모리 기능 계약 테스트"""

    def test_memory_store(self):
        """메모리 저장 (MS 버튼) 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('4')
        calc.input_digit('2')
        calc.memory_store()

        result = calc.memory_recall()
        assert result == "42"

    def test_memory_recall_empty(self):
        """빈 메모리 불러오기 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        # 초기 메모리는 비어있음
        assert calc.memory_state.is_empty is True

    def test_memory_add(self):
        """메모리에 더하기 (M+ 버튼) 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('0')
        calc.memory_store()  # M = 10

        calc.input_digit('5')
        calc.memory_add()  # M = 10 + 5 = 15

        result = calc.memory_recall()
        assert result == "15"

    def test_memory_subtract(self):
        """메모리에서 빼기 (M- 버튼) 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('2')
        calc.input_digit('0')
        calc.memory_store()  # M = 20

        calc.input_digit('7')
        calc.memory_subtract()  # M = 20 - 7 = 13

        result = calc.memory_recall()
        assert result == "13"

    def test_memory_clear(self):
        """메모리 지우기 (MC 버튼) 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('9')
        calc.input_digit('9')
        calc.memory_store()  # M = 99

        calc.memory_clear()  # M = 0, is_empty = True
        assert calc.memory_state.is_empty is True

    def test_memory_operations_sequence(self):
        """메모리 연산 시퀀스 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('0')
        calc.memory_store()  # M = 10

        calc.input_digit('5')
        calc.memory_add()  # M = 15

        calc.input_digit('3')
        calc.memory_subtract()  # M = 12

        result = calc.memory_recall()
        assert result == "12"

    def test_memory_recall_sets_display(self):
        """MR 버튼으로 메모리 값 디스플레이에 표시 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('7')
        calc.input_digit('7')
        calc.memory_store()

        calc.clear_all()  # 디스플레이 0

        result = calc.memory_recall()
        assert result == "77"  # 디스플레이에 77 표시

    def test_memory_with_calculations(self):
        """계산과 메모리 함께 사용 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_operation(OperationType.ADD)
        calc.input_digit('3')
        calc.calculate()  # 8
        calc.memory_store()  # M = 8

        calc.input_digit('2')
        calc.input_operation(OperationType.MULTIPLY)
        calc.memory_recall()  # 8 불러오기
        result = calc.calculate()  # 2 × 8 = 16
        assert result == "16"

    def test_memory_add_zero(self):
        """메모리에 0 더하기 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('5')
        calc.memory_store()  # M = 5

        calc.input_digit('0')
        calc.memory_add()  # M = 5 + 0 = 5

        result = calc.memory_recall()
        assert result == "5"

    def test_memory_negative_value(self):
        """음수 메모리 저장 테스트"""
        from src.core.calculator import Calculator
        from src.core.enums import OperationType

        calc = Calculator()
        calc.input_digit('5')
        calc.input_operation(OperationType.NEGATE)  # -5
        calc.memory_store()

        result = calc.memory_recall()
        assert result == "-5"

    def test_memory_decimal_value(self):
        """소수 메모리 저장 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('3')
        calc.input_digit('.')
        calc.input_digit('1')
        calc.input_digit('4')
        calc.memory_store()  # M = 3.14

        result = calc.memory_recall()
        assert result == "3.14"

    def test_memory_replace_with_ms(self):
        """MS로 메모리 값 대체 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('1')
        calc.input_digit('0')
        calc.memory_store()  # M = 10

        calc.input_digit('2')
        calc.input_digit('0')
        calc.memory_store()  # M = 20 (10 대체)

        result = calc.memory_recall()
        assert result == "20"

    def test_memory_survives_clear_all(self):
        """CE 후에도 메모리 유지 테스트"""
        from src.core.calculator import Calculator

        calc = Calculator()
        calc.input_digit('5')
        calc.input_digit('5')
        calc.memory_store()  # M = 55

        calc.clear_all()

        result = calc.memory_recall()
        assert result == "55"  # 메모리는 유지됨
